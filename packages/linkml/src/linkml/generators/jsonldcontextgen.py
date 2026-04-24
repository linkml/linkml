"""
Generate JSON-LD contexts
"""

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import click
from jsonasobj2 import JsonObj, as_json
from rdflib import SKOS, XSD, Namespace

from linkml._version import __version__
from linkml.utils.deprecation import deprecated_fields
from linkml.utils.generator import Generator, shared_arguments, well_known_prefix_map
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

URI_RANGES = (SHEX.nonliteral, SHEX.bnode, SHEX.iri)

ENUM_CONTEXT = {
    "text": "skos:notation",
    "description": "skos:prefLabel",
    "meaning": "@id",
}


@deprecated_fields({"emit_metadata": "metadata"})
@dataclass
class ContextGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["context", "json"]
    visit_all_class_slots = False
    uses_schemaloader = True
    requires_metamodel = True
    file_extension = "context.jsonld"

    # ObjectVars
    emit_prefixes: set[str] = field(default_factory=lambda: set())
    default_ns: str = None
    context_body: dict = field(default_factory=lambda: dict())
    slot_class_maps: dict = field(default_factory=lambda: dict())
    metadata: bool = False
    model: bool | None = True
    base: str | Namespace | None = None
    output: str | None = None
    prefixes: bool | None = True
    flatprefixes: bool | None = False
    fix_multivalue_containers: bool | None = False
    exclude_imports: bool = False
    """If True, elements from imported schemas won't be included in the generated context"""
    exclude_external_imports: bool = False
    """If True, elements from URL-based external vocabulary imports are excluded.

    Local file imports and linkml standard imports are kept.  This is useful
    when extending an external ontology (e.g. W3C Verifiable Credentials)
    whose terms are ``@protected`` in their own JSON-LD context — redefining
    them locally would violate JSON-LD 1.1 §4.1.11.

    This flag is effective regardless of the ``mergeimports`` setting:
    even with ``mergeimports=False``, external vocabulary elements can
    leak into the context via the schema map.
    """
    _local_classes: set | None = field(default=None, repr=False)
    _local_slots: set | None = field(default=None, repr=False)
    _external_classes: set | None = field(default=None, repr=False)
    _external_slots: set | None = field(default=None, repr=False)

    # Framing (opt-in via CLI flag)
    emit_frame: bool = False
    embed_context_in_frame: bool = False
    frame_body: dict = field(default_factory=lambda: dict())
    frame_root: str | None = None

    def __post_init__(self) -> None:
        # Must be set before super().__post_init__() because the parent triggers
        # the visitor pattern (visit_schema), which accesses _prefix_remap.
        self._prefix_remap: dict[str, str] = {}
        super().__post_init__()
        if self.namespaces is None:
            raise TypeError("Schema text must be supplied to context generator.  Preparsed schema will not work")
        if self.exclude_imports or self.exclude_external_imports:
            if self.schemaview:
                sv = self.schemaview
            else:
                source = self.schema.source_file or self.schema
                if isinstance(source, str) and self.base_dir and not Path(source).is_absolute():
                    source = str(Path(self.base_dir) / source)
                sv = SchemaView(source, importmap=self.importmap, base_dir=self.base_dir)
            if self.exclude_imports:
                self._local_classes = set(sv.all_classes(imports=False).keys())
                self._local_slots = set(sv.all_slots(imports=False).keys())
            if self.exclude_external_imports:
                self._external_classes, self._external_slots = self._collect_external_elements(sv)

    @staticmethod
    def _collect_external_elements(sv: SchemaView) -> tuple[set[str], set[str]]:
        """Identify classes and slots from URL-based external vocabulary imports.

        Walks the SchemaView ``schema_map`` (populated by ``imports_closure``)
        and collects element names from schemas whose import key starts with
        ``http://`` or ``https://``.  Local file imports and ``linkml:``
        standard imports are left untouched.
        """
        sv.imports_closure()
        external_classes: set[str] = set()
        external_slots: set[str] = set()
        for schema_key, schema_def in sv.schema_map.items():
            if schema_key == sv.schema.name:
                continue
            if schema_key.startswith("http://") or schema_key.startswith("https://"):
                external_classes.update(schema_def.classes.keys())
                external_slots.update(schema_def.slots.keys())
        return external_classes, external_slots

    def add_prefix(self, ncname: str) -> None:
        """Add a prefix, applying well-known prefix normalisation when enabled."""
        super().add_prefix(self._prefix_remap.get(ncname, ncname))

    def visit_schema(self, base: str | Namespace | None = None, output: str | None = None, **_):
        # Add any explicitly declared prefixes.
        # Direct .add() is safe here: the normalisation block below explicitly
        # rewrites emit_prefixes entries for any renamed prefixes (Cases 1-3).
        for prefix in self.schema.prefixes.values():
            self.emit_prefixes.add(prefix.prefix_prefix)

        # Add any prefixes explicitly declared
        for pfx in self.schema.emit_prefixes:
            self.add_prefix(pfx)

        # Normalise well-known prefix names when --normalize-prefixes is set.
        # If the schema declares a non-standard alias for a namespace that has
        # a well-known standard name (e.g. ``sdo`` for
        # ``https://schema.org/``), replace the alias with the standard name
        # so that generated JSON-LD contexts use the conventional prefix.
        #
        # Three cases are handled:
        # 1. Standard prefix is not yet bound → just rebind from old to new.
        # 2. Standard prefix is bound to a *different* URI:
        #    a. User-declared (in schema.prefixes) → collision, skip with warning.
        #    b. Runtime default (e.g. linkml-runtime's ``schema: http://…``)
        #       → remove stale binding, then rebind.
        # 3. Standard prefix is already bound to the *same* URI (duplicate)
        #    → just drop the non-standard alias.
        #
        # A remap dict is stored for ``_build_element_id`` because
        # ``prefix_suffix()`` splits CURIEs on ``:`` without looking up the
        # namespace dict.
        self._prefix_remap.clear()
        if self.normalize_prefixes:
            wk = well_known_prefix_map()
            for old_pfx in list(self.namespaces):
                url = str(self.namespaces[old_pfx])
                std_pfx = wk.get(url)
                if not std_pfx or std_pfx == old_pfx:
                    continue
                if std_pfx in self.namespaces:
                    if str(self.namespaces[std_pfx]) != url:
                        # Case 2: std_pfx is bound to a different URI.
                        # If the user explicitly declared std_pfx in the schema,
                        # it is intentional — skip to avoid data loss.
                        if std_pfx in self.schema.prefixes:
                            self.logger.warning(
                                "Prefix collision: cannot rename '%s' to '%s' because '%s' is "
                                "already declared for <%s>; skipping normalisation for <%s>",
                                old_pfx,
                                std_pfx,
                                std_pfx,
                                str(self.namespaces[std_pfx]),
                                url,
                            )
                            continue
                        # Not user-declared (e.g. linkml-runtime default) — safe to remove
                        self.emit_prefixes.discard(std_pfx)
                        del self.namespaces[std_pfx]
                    else:
                        # Case 3: standard prefix already bound to same URI
                        # — just drop the non-standard alias
                        del self.namespaces[old_pfx]
                        if old_pfx in self.emit_prefixes:
                            self.emit_prefixes.discard(old_pfx)
                            self.emit_prefixes.add(std_pfx)
                        self._prefix_remap[old_pfx] = std_pfx
                        continue
                # Case 1 (or Case 2 after stale removal): bind standard name
                self.namespaces[std_pfx] = self.namespaces[old_pfx]
                del self.namespaces[old_pfx]
                if old_pfx in self.emit_prefixes:
                    self.emit_prefixes.discard(old_pfx)
                    self.emit_prefixes.add(std_pfx)
                self._prefix_remap[old_pfx] = std_pfx

        # Add the default prefix
        if self.schema.default_prefix:
            dflt = self.namespaces.prefix_for(self.schema.default_prefix)
            if dflt:
                self.default_ns = dflt
            if self.default_ns:
                default_uri = self.namespaces[self.default_ns]
                # Direct .add() is safe: default_ns is already resolved from
                # the (possibly normalised) namespace bindings above.
                self.emit_prefixes.add(self.default_ns)
            else:
                default_uri = self.schema.default_prefix
                if self.schema.name:
                    self.namespaces[self.schema.name] = default_uri
                    self.emit_prefixes.add(self.schema.name)
            self.context_body["@vocab"] = default_uri

    def end_schema(
        self,
        base: str | Namespace | None = None,
        output: str | None = None,
        prefixes: bool | None = None,
        flatprefixes: bool | None = None,
        model: bool | None = None,
        **_,
    ) -> str:
        if base is None:
            base = self.base
        if output is None:
            output = self.output
        if prefixes is None:
            prefixes = self.prefixes
        if flatprefixes is None:
            flatprefixes = self.flatprefixes
        if model is None:
            model = self.model

        context = JsonObj()
        if self.metadata:
            comments = JsonObj()
            comments.description = "Auto generated by LinkML jsonld context generator"
            comments.generation_date = self.schema.generation_date
            comments.source = self.schema.source_file
            context.comments = comments
        context_content = {"xsd": "http://www.w3.org/2001/XMLSchema#"}
        if base:
            base = str(base)
            if "://" not in base:
                self.context_body["@base"] = os.path.relpath(base, os.path.dirname(self.schema.source_file))
            else:
                self.context_body["@base"] = base
        if prefixes:
            for prefix in sorted(self.emit_prefixes):
                url = str(self.namespaces[prefix])
                # Derived from line # ~5223 in pyld/lib/jsonld.py
                if bool(re.match(r".*[:/\?#\[\]@]$", url)) or flatprefixes:
                    context_content[prefix] = url
                else:
                    prefix_obj = JsonObj()
                    prefix_obj["@id"] = url
                    prefix_obj["@prefix"] = True
                    context_content[prefix] = prefix_obj
        if model:
            for k, v in self.context_body.items():
                context_content[k] = v
            for k, v in self.slot_class_maps.items():
                context_content[k] = v
        context["@context"] = context_content
        if output and not self.embed_context_in_frame:
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(as_json(context))

        if self.emit_frame and self.frame_body and output:
            root_name = None
            for cname, c in self.schema.classes.items():
                if getattr(c, "tree_root", False):
                    root_name = cname
                    break
            if root_name is None and self.schema.classes:
                root_name = next(iter(self.schema.classes))

            if self.embed_context_in_frame:
                frame = {
                    "@context": context["@context"],
                    "@omitGraph": True,
                }
            else:
                frame = {
                    "@context": Path(output).name,
                    "@omitGraph": True,
                }
            if root_name:
                root_cls = self.schema.classes[root_name]
                frame["@type"] = root_cls.class_uri or root_cls.name

            for prop, rule in self.frame_body.items():
                frame[prop] = rule

            frame_path = Path(output).with_suffix(".frame.jsonld")
            with open(frame_path, "w", encoding="UTF-8") as f:
                json.dump(frame, f, indent=2, ensure_ascii=False)

        return str(as_json(context)) + "\n"

    def visit_class(self, cls: ClassDefinition) -> bool:
        if self.exclude_imports and cls.name not in self._local_classes:
            return False
        if self.exclude_external_imports and cls.name in self._external_classes:
            return False

        class_def = {}
        cn = camelcase(cls.name)
        self.add_mappings(cls)

        self._build_element_id(class_def, cls.class_uri)
        if class_def:
            self.slot_class_maps[cn] = class_def

        # prefer explicit tree_root for frame @type
        if getattr(cls, "tree_root", False):
            self.frame_root = cls.name

        # We don't bother to visit class slots - just all slots
        return True

    def _literal_coercion_for_ranges(self, ranges: list[str]) -> tuple[bool, str | None]:
        """Return an unambiguous JSON-LD coercion for LinkML type ranges.

        The returned tuple is ``(resolved, coercion)``:

        - ``resolved`` is ``True`` only when all LinkML type branches collapse
          to the same JSON-LD coercion.
        - ``coercion`` is the JSON-LD ``@type`` value, or ``None`` when the
          resolved result is "no coercion" (for example ``xsd:string``).

        This allows callers to distinguish between "resolved to no coercion"
        and "could not resolve safely because the branches disagree".
        """
        coercions: set[str | None] = set()
        for range_name in ranges:
            if range_name not in self.schema.types:
                continue

            range_type = self.schema.types[range_name]
            range_uri = self.namespaces.uri_for(range_type.uri)
            if range_uri == XSD.string:
                coercions.add(None)
            elif range_uri in URI_RANGES:
                coercions.add("@id")
            else:
                coercions.add(range_type.uri)

        if not coercions:
            return False, None
        if len(coercions) == 1:
            return True, next(iter(coercions))
        return False, None

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if self.exclude_imports and slot.name not in self._local_slots:
            return
        if self.exclude_external_imports and slot.name in self._external_slots:
            return

        if slot.identifier:
            slot_def = "@id"
        else:
            slot_def = {}
            if not slot.usage_slot_name:
                any_of_ranges = [any_of_el.range for any_of_el in slot.any_of]
                has_class_range = slot.range in self.schema.classes or any(
                    rng in self.schema.classes for rng in any_of_ranges
                )
                has_literal_range = any(rng in self.schema.types for rng in any_of_ranges)

                if has_class_range and has_literal_range:
                    # Mixed any_of: prefer literal coercion when unambiguous.
                    resolved, literal_coercion = self._literal_coercion_for_ranges(any_of_ranges)
                    if resolved and literal_coercion is not None:
                        slot_def["@type"] = literal_coercion
                elif has_class_range:
                    slot_def["@type"] = "@id"
                elif slot.range in self.schema.enums:
                    slot_def["@context"] = ENUM_CONTEXT
                    # Add the necessary prefixes to the namespace
                    skos = self.namespaces.prefix_for(SKOS)
                    if not skos:
                        self.namespaces["skos"] = SKOS
                        skos = "skos"
                    self.emit_prefixes.add(skos)
                else:
                    range_type = self.schema.types[slot.range]
                    if self.namespaces.uri_for(range_type.uri) == XSD.string:
                        pass
                    elif self.namespaces.uri_for(range_type.uri) in URI_RANGES:
                        slot_def["@type"] = "@id"
                    else:
                        slot_def["@type"] = range_type.uri

                if self.fix_multivalue_containers and slot.multivalued:
                    if slot.inlined and not slot.inlined_as_list:
                        slot_def["@container"] = "@index"
                    else:
                        slot_def["@container"] = "@set"

                self._build_element_id(slot_def, slot.slot_uri)
                self.add_mappings(slot)
        if slot_def:
            key = underscore(aliased_slot_name)
            self.context_body[key] = slot_def

            # collect @embed only for object-valued slots (range is a class)
            if slot.range in self.schema.classes and slot.inlined is not None:
                self.frame_body[key] = {"@embed": "@always" if bool(slot.inlined) else "@never"}

    def _build_element_id(self, definition: Any, uri: str) -> None:
        """
        Defines the elements @id attribute according to the default namespace prefix of the schema.

        The @id namespace prefix is added only if it doesn't correspond to the default schema namespace prefix
        whether it is in URI format or as an alias.

        @param definition: the element (class or slot) definition
        @param uri: the uri of the element (class or slot)
        @return: None
        """
        uri_prefix, uri_suffix = self.namespaces.prefix_suffix(uri)
        # Apply well-known prefix normalisation (e.g. sdo → schema).
        # prefix_suffix() splits CURIEs on ':' without checking the
        # namespace dict, so it may return a stale alias.
        if uri_prefix and uri_prefix in self._prefix_remap:
            uri_prefix = self._prefix_remap[uri_prefix]
        is_default_namespace = uri_prefix == self.context_body["@vocab"] or uri_prefix == self.namespaces.prefix_for(
            self.context_body["@vocab"]
        )

        if not uri_prefix and not uri_suffix:
            definition["@id"] = uri
        elif not uri_prefix or is_default_namespace:
            definition["@id"] = uri_suffix
        else:
            definition["@id"] = (uri_prefix + ":" + uri_suffix) if uri_prefix else uri

        if uri_prefix and not is_default_namespace:
            self.add_prefix(uri_prefix)

    def serialize(
        self,
        base: str | Namespace | None = None,
        output: str | None = None,
        prefixes: bool | None = None,
        flatprefixes: bool | None = None,
        model: bool | None = None,
        **kwargs,
    ) -> str:
        return super().serialize(
            base=base, output=output, prefixes=prefixes, flatprefixes=flatprefixes, model=model, **kwargs
        )


@shared_arguments(ContextGenerator)
@click.command(name="jsonld-context")
@click.option("--base", help="Base URI for model")
@click.option(
    "--prefixes/--no-prefixes",
    default=True,
    show_default=True,
    help="Emit context for prefixes (default=--prefixes)",
)
@click.option(
    "--model/--no-model",
    default=True,
    show_default=True,
    help="Emit context for model elements (default=--model)",
)
@click.option(
    "--flatprefixes/--no-flatprefixes",
    default=False,
    show_default=True,
    help="Emit non-JSON-LD compliant prefixes as an object (deprecated: use gen-prefix-map instead).",
)
@click.option(
    "--emit-frame/--no-emit-frame",
    default=False,
    show_default=True,
    help="Also emit a <schema>.frame.jsonld file with @embed rules for framing",
)
@click.option(
    "--embed-context-in-frame/--no-embed-context-in-frame",
    default=False,
    show_default=True,
    help="Emit a <schema>.frame.jsonld file with @context embedded directly (single file)",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file name",
)
@click.option(
    "--fix-multivalue-containers/--no-fix-multivalue-containers",
    default=False,
    show_default=True,
    help="For multivalued attributes declare a fix container type ('@set' for lists, '@index' for dictionaries).",
)
@click.option(
    "--exclude-imports/--include-imports",
    default=False,
    show_default=True,
    help="Use --exclude-imports to exclude imported elements from the generated JSON-LD context. This is useful when "
    "extending an ontology whose terms already have context definitions in their own JSON-LD context file.",
)
@click.option(
    "--exclude-external-imports/--no-exclude-external-imports",
    default=False,
    show_default=True,
    help="Exclude elements from URL-based external vocabulary imports while keeping local file imports. "
    "Useful when extending ontologies (e.g. W3C VC v2) whose terms are @protected in their own JSON-LD context.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, emit_frame, embed_context_in_frame, output, **args):
    """Generate jsonld @context definition from LinkML model"""
    if (emit_frame or embed_context_in_frame) and not output:
        raise click.UsageError("--emit-frame/--embed-context-in-frame requires --output")
    gen = ContextGenerator(yamlfile, **args)
    if embed_context_in_frame:
        gen.emit_frame = True
        gen.embed_context_in_frame = True
    else:
        gen.emit_frame = emit_frame
    print(gen.serialize(output=output, **args))


if __name__ == "__main__":
    cli()
