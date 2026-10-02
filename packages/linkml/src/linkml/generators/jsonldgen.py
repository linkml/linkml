"""Generate JSONld from a LinkML schema."""

import os
from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import click
from jsonasobj2 import as_dict, as_json, items, loads

from linkml import METAMODEL_CONTEXT_URI
from linkml._version import __version__
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.utils.deprecation import deprecated_fields
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.mergeutils import slot_usage_name
from linkml.utils.rawloader import DATETIME_FORMAT
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    ElementName,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    SlotDefinitionName,
    SubsetDefinition,
    SubsetDefinitionName,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.formatutils import camelcase, mangled_attribute_name, underscore
from linkml_runtime.utils.yamlutils import YAMLRoot


@deprecated_fields({"emit_metadata": "metadata"})
@dataclass
class JSONLDGenerator(Generator):
    """
    Generates JSON-LD from a Schema

    Status: incompletely implemented

    Note: this is distinct from
    :class:`~linkml.generators.jsonldcontextgen.ContextGenerator`, which generates a JSON-LD context
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = [
        "jsonld",
        "json",
    ]  # jsonld includes @type and @context.  json is pure JSON
    uses_schemaloader = False
    requires_metamodel = True
    file_extension = "jsonld"

    # ObjectVars
    original_schema: SchemaDefinition = None
    """See https://github.com/linkml/linkml/issues/871"""

    context: Sequence[str] | None = field(default_factory=list)
    """Path to a JSONLD context file"""

    metamodel_context: str = None
    """Override for metamodel context URI/path. When None, uses METAMODEL_CONTEXT_URI."""

    def __post_init__(self) -> None:
        if self.uses_schemaloader:
            raise ValueError(
                f"{type(self).__name__} is a SchemaView-only generator and does not support the "
                "SchemaLoader path; 'uses_schemaloader' must remain False."
            )
        self.original_schema = deepcopy(self.schema)
        super().__post_init__()
        # super().__post_init__() takes the SchemaView path (uses_schemaloader is False)
        # and always assigns self.schemaview, so it is guaranteed non-None from here on.
        # Trigger imports_closure so that inject_metadata runs and populates
        # from_schema on all elements (SchemaView only does this lazily).
        self.schemaview.imports_closure()
        self._materialize_schema()

    def _materialize_schema(self) -> None:
        """Populate the flat ``self.schema.{types,slots,classes,subsets,enums}`` dicts
        that the base :class:`~linkml.utils.generator.Generator` visitor iterates over.

        Elements are materialized natively through :class:`SchemaView`:

        * types/subsets/enums are taken via their induced form so inherited metaslots
          (e.g. ``typeof`` chains for types) are resolved;
        * every class contributes its induced slots (``class_induced_slots``), yielding
          fully-resolved, class-mangled :class:`SlotDefinition` objects with ``owner``,
          ``domain_of``, ``inlined``, ``required`` and ``from_schema`` already set;
        * top-level (schema) slots are added via their induced form so that slots not
          attached to any class are still serialized.

        Unlike the previous SchemaLoader-parity port, this keeps the SchemaView-native
        output (including ``from_schema`` / ``domain_of`` provenance) rather than
        reconstructing SchemaLoader's byte-for-byte result.
        """
        sv = self.schemaview
        induced_types = {tn: sv.induced_type(tn) for tn in sv.all_types()}
        induced_enums = {en: sv.induced_enum(en) for en in sv.all_enums()}
        subsets = dict(sv.all_subsets())

        # Materialize slots. For every class, induce each of its (inherited + own) slots
        # into a fully-resolved SlotDefinition. Slots that a class overrides (via an
        # ``attributes`` entry or a ``slot_usage``) get a class-mangled name so the
        # override does not collide with the base slot; plain inherited slots keep their
        # base name. ``induced_slot`` sets ``owner``, ``domain_of``, ``inlined``,
        # ``required``, ``alias``, ``range`` and ``from_schema``.
        #
        # NOTE: all reads from ``sv`` happen BEFORE the schema is mutated below, because
        # ``self.schema`` IS ``sv.schema``; mutating classes/slots mid-induction would
        # corrupt SchemaView's own resolution (e.g. ``all_slots`` iterating attributes).
        materialized: dict[SlotDefinitionName, SlotDefinition] = {}
        class_resolved_slots: dict[ClassDefinitionName, list[SlotDefinitionName]] = {}
        # Maps each materialized slot name -> the base schema-slot name whose
        # ``definition_uri`` it inherits. Attribute-only slots have no schema-level base
        # (SchemaLoader assigned them no ``definition_uri``) and are omitted.
        self._slot_base_name: dict[SlotDefinitionName, SlotDefinitionName] = {}
        for class_name in sv.all_classes():
            cls = sv.get_class(class_name)
            resolved_slot_names: list[SlotDefinitionName] = []
            for slot_name in sv.class_slots(class_name):
                is_attribute = slot_name in cls.attributes
                is_usage = slot_name in cls.slot_usage
                if is_attribute:
                    # Attributes are class-local: induce in the class context and give each
                    # a unique mangled name so same-named attributes across classes do not
                    # collide, and (when no explicit slot_uri is declared) disambiguate the
                    # slot_uri via that mangled name. See
                    # https://github.com/linkml/linkml/issues/388.
                    # deepcopy: induced_slot() shallow-copies the source slot, so mutable
                    # fields (e.g. ``mappings``) are shared with the class ``attributes``.
                    induced = deepcopy(sv.induced_slot(slot_name, class_name))
                    induced.name = mangled_attribute_name(class_name, slot_name)
                    if induced.slot_uri is None:
                        induced.slot_uri = self._slot_uri_for(induced, use_name=True)
                    materialized[induced.name] = induced
                    resolved_slot_names.append(induced.name)
                elif is_usage:
                    # slot_usage overrides are class-specific: induce in the class context,
                    # give a class-mangled name so the override does not clobber the base
                    # slot definition, and record the base slot for definition_uri.
                    induced = deepcopy(sv.induced_slot(slot_name, class_name))
                    induced.name = slot_usage_name(slot_name, cls)
                    self._slot_base_name[induced.name] = slot_name
                    materialized[induced.name] = induced
                    resolved_slot_names.append(induced.name)
                else:
                    # Plain (possibly inherited) slot: a single canonical top-level slot is
                    # shared by every class that lists it. Induce ONCE, without class
                    # context, so ``owner`` is not pinned to whichever inheriting class was
                    # processed last (induced_slot sets owner to the induction context).
                    if slot_name not in materialized:
                        induced = deepcopy(sv.induced_slot(slot_name))
                        # owner is the most-derived class that lists the slot, i.e. the last
                        # entry of ``domain_of`` (meta.yaml: "the class if it appears in the
                        # slots list"). domain_of is populated by induced_slot.
                        if induced.domain_of:
                            induced.owner = ClassDefinitionName(induced.domain_of[-1])
                        self._slot_base_name[slot_name] = slot_name
                        materialized[slot_name] = induced
                    resolved_slot_names.append(slot_name)
            class_resolved_slots[class_name] = resolved_slot_names
        for slot_name in sv.all_slots(attributes=False):
            if slot_name not in materialized:
                induced = deepcopy(sv.induced_slot(slot_name))
                if induced.domain_of:
                    induced.owner = ClassDefinitionName(induced.domain_of[-1])
                materialized[slot_name] = induced
                self._slot_base_name[slot_name] = slot_name

        # Infer ``inlined``/``inlined_as_list`` for class-ranged slots. SchemaView's
        # ``induced_slot`` only propagates a declared value; it does not infer. LinkML
        # semantics require a class range with no identifier slot to be inlined, so
        # replicate that here to keep the serialized slot description accurate.
        for slot in materialized.values():
            self._infer_inlined(slot)

        # All SchemaView reads are done; now populate the flat visitor collections.
        self.schema.types.update(induced_types)
        self.schema.subsets.update(subsets)
        self.schema.enums.update(induced_enums)
        self.schema.classes.update(sv.all_classes())
        for class_name, resolved_slot_names in class_resolved_slots.items():
            cls = self.schema.classes[class_name]
            # Point the class at its resolved (possibly mangled) slot names. The class's
            # own ``attributes`` are preserved for provenance even though each has also
            # been promoted to a top-level (mangled) slot.
            cls.slots = resolved_slot_names
        # ``induced_slot`` sets ``owner`` to a plain class-name string; wrap it as a
        # ``ClassDefinitionName`` so the visitor camelcases it like ``domain_of`` entries.
        for slot in materialized.values():
            if slot.owner is not None:
                slot.owner = ClassDefinitionName(slot.owner)
        self.schema.slots.update(materialized)
        # Induced/copied elements carry initialized-empty container metaslots; drop them so
        # they do not serialize as spurious empty blank nodes.
        for collection in (
            self.schema.types,
            self.schema.slots,
            self.schema.enums,
            self.schema.subsets,
        ):
            for element in collection.values():
                self._strip_empty_containers(element)
        # Drop redundant ``alias`` on slots whose alias is merely the normalized name;
        # keep it only where it carries information (e.g. mangled attribute/usage slots,
        # whose alias is the base slot name). This matches the historical output.
        for slot in self.schema.slots.values():
            if slot.alias and slot.alias == underscore(slot.name):
                slot.__dict__.pop("alias", None)
        self._merge_imported_schema_metadata()
        self._assign_imported_from()
        self._stamp_load_metadata()

    def _infer_inlined(self, slot: SlotDefinition) -> None:
        """Materialize ``inlined``/``inlined_as_list`` for a class-ranged slot.

        The inference itself lives in :meth:`SchemaView.is_inlined` (a class range with no
        identifier slot must be inlined, since it cannot be referenced by URI). SchemaView
        exposes it as a query but does not write it back onto the slot; this method applies
        that result to the materialized slot so the serialized description is accurate.
        Never clobbers an explicitly declared value.
        """
        range_name = str(slot.range) if slot.range else None
        if range_name is None or range_name not in self.schema.classes:
            return
        if not self.schemaview.is_inlined(slot):
            return
        if slot.inlined is None:
            slot.inlined = True
        if slot.inlined and slot.inlined_as_list is None and slot.multivalued:
            slot.inlined_as_list = True

    def _stamp_load_metadata(self) -> None:
        """Stamp load-time metadata (``generation_date``, ``source_file_date``,
        ``source_file_size``) on the schema when ``metadata`` is enabled.

        SchemaLoader derives these in ``rawloader.load_raw_schema``; the SchemaView path
        loads via ``yaml_loader`` directly and skips that step, so they must be stamped
        here to preserve provenance. Honors the generator's ``metadata`` flag, matching
        the ``--metadata/--no-metadata`` contract.
        """
        if not self.metadata:
            return
        self.schema.generation_date = datetime.now().strftime(DATETIME_FORMAT)
        source_file = self.original_schema if isinstance(self.original_schema, str) else None
        if source_file and "://" not in source_file and os.path.exists(source_file):
            stat = os.stat(source_file)
            self.schema.source_file_size = stat.st_size
            self.schema.source_file_date = datetime.fromtimestamp(stat.st_mtime).strftime(DATETIME_FORMAT)

    @staticmethod
    def _strip_empty_containers(element: YAMLRoot) -> None:
        """Drop empty inline dictionaries (``alt_descriptions``, ``annotations``,
        ``extensions``, ``local_names``) from an element.

        SchemaView's ``induced_slot`` copies these container metaslots as initialized-empty
        ``JsonObj`` instances. ``as_json`` serializes any set field, so these empty
        containers would appear as spurious empty blank nodes in the RDF serialization.
        Removing them from ``__dict__`` keeps the output free of that noise, matching the
        behaviour of slots that never had the container populated.
        """
        for field_name in ("alt_descriptions", "annotations", "extensions", "local_names"):
            value = getattr(element, field_name, None)
            if value is not None and not as_dict(value):
                element.__dict__.pop(field_name, None)

    def _merge_imported_schema_metadata(self) -> None:
        """Merge schema-level metadata contributed by imported schemas.

        Mirrors the historical merge semantics: the importing schema inherits ``license``
        from an imported schema when it declares none, and accumulates ``emit_prefixes``.
        SchemaView keeps imported schemas separate, so this must be replicated explicitly.
        """
        for s in self.schemaview.all_schema():
            if self.schema.license is None and s.license:
                self.schema.license = s.license
            for pfx in s.emit_prefixes:
                if pfx not in self.schema.emit_prefixes:
                    self.schema.emit_prefixes.append(pfx)

    def _assign_imported_from(self) -> None:
        """Set ``imported_from`` on elements sourced from an imported schema.

        SchemaView records provenance as ``from_schema`` (the source schema *id* URI).
        Downstream RDF/JSON-LD consumers expect the ``imported_from`` CURIE (e.g.
        ``linkml:types``). Map each element's ``from_schema`` id back to the import
        key under which its schema was loaded and record it as ``imported_from``.
        """
        sv = self.schemaview
        main_id = str(self.schema.id)
        # Map source-schema id URI -> the import key it was loaded under (e.g.
        # "https://w3id.org/linkml/types" -> "linkml:types").
        id_to_import_key = {
            str(imp_schema.id): imp_key
            for imp_key, imp_schema in sv.schema_map.items()
            if str(imp_schema.id) != main_id
        }
        for collection in (
            self.schema.types,
            self.schema.slots,
            self.schema.classes,
            self.schema.subsets,
            self.schema.enums,
        ):
            for element in collection.values():
                if element.imported_from is not None:
                    continue
                from_schema = str(element.from_schema) if element.from_schema else None
                if from_schema and from_schema != main_id and from_schema in id_to_import_key:
                    element.imported_from = id_to_import_key[from_schema]

    def _slot_uri_for(self, slot: SlotDefinition, use_name: bool = False) -> str:
        """Compute the slot_uri for a slot with no declared slot_uri.

        Uses ``alias`` when present, otherwise ``name``, with :func:`underscore` casing.
        The namespace comes from the slot's source schema default prefix.

        :param use_name: force use of ``slot.name`` (ignoring ``alias``). Attribute-derived
            slots share a base ``alias`` across classes but carry a unique mangled ``name``;
            the mangled name is required to disambiguate their slot_uri
            (https://github.com/linkml/linkml/issues/388).
        """
        if use_name:
            alias_or_name = underscore(slot.name)
        else:
            alias_or_name = underscore(slot.alias if slot.alias else slot.name)
        src_schema_id = slot.from_schema or self.schema.id
        src_schema = next(
            (s for s in self.schemaview.all_schema() if str(s.id) == str(src_schema_id)),
            self.schemaview.schema,
        )
        if src_schema.default_prefix and src_schema.default_prefix in src_schema.prefixes:
            ns = src_schema.prefixes[src_schema.default_prefix].prefix_reference
        else:
            ns = str(src_schema.id) + "/"
        return f"{ns}{alias_or_name}"

    def _add_type(self, node: YAMLRoot) -> dict:
        if self.format == "jsonld":
            typ = node.__class__.__name__
            node = node.__dict__
            node["@type"] = typ
        return node

    def _visit(self, node: Any) -> Any | None:
        if isinstance(node, YAMLRoot | dict):
            if isinstance(node, YAMLRoot):
                self._strip_empty_containers(node)
                node = self._add_type(node)
            for k, v in list(items(node)):
                if v:
                    new_v = self._visit(v)
                    if new_v is not None:
                        node[k] = new_v
        elif isinstance(node, list):
            for i in range(0, len(node)):
                new_v = self._visit(node[i])
                if new_v is not None:
                    node[i] = new_v
        elif isinstance(node, set):
            for v in list(node):
                new_v = self._visit(v)
                if new_v is not None:
                    node.remove(v)
                    node.add(new_v)
        elif isinstance(node, ClassDefinitionName):
            return ClassDefinitionName(camelcase(node))
        elif isinstance(node, SlotDefinitionName):
            return SlotDefinitionName(underscore(node))
        elif isinstance(node, TypeDefinitionName):
            return TypeDefinitionName(underscore(node))
        elif isinstance(node, SubsetDefinitionName):
            return SubsetDefinitionName(underscore(node))
        elif isinstance(node, ElementName):
            return (
                ClassDefinitionName(camelcase(node))
                if node in self.schema.classes
                else (
                    SlotDefinitionName(underscore(node))
                    if node in self.schema.slots
                    else (
                        SubsetDefinitionName(camelcase(node))
                        if node in self.schema.subsets
                        else TypeDefinitionName(underscore(node))
                        if node in self.schema.types
                        else None
                    )
                )
            )
        return None

    def adjust_slot(self, slot: SlotDefinition) -> None:
        if slot.range in self.schema.classes:
            slot.range = ClassDefinitionName(camelcase(slot.range))
        elif slot.range in self.schema.slots:
            slot.range = SlotDefinitionName(underscore(slot.range))
        elif slot.range in self.schema.types:
            slot.range = TypeDefinitionName(underscore(slot.range))
        # Insert the declared slot_uri into mappings before overwriting it, then
        # synthesise slot_uri from the source-schema default prefix + alias/name when it
        # is unset (mirrors the historical JSON-LD serialization contract).
        if slot.slot_uri is not None:
            slot.mappings.insert(0, slot.slot_uri)
        else:
            slot.slot_uri = self._slot_uri_for(slot)
        slot.slot_uri = self.schemaview.namespaces().uri_for(slot.slot_uri)
        for f in [
            "mappings",
            "exact_mappings",
            "broad_mappings",
            "close_mappings",
            "narrow_mappings",
            "related_mappings",
        ]:
            setattr(slot, f, [self.schemaview.namespaces().uri_for(v) for v in getattr(slot, f)])

    def visit_class(self, cls: ClassDefinition) -> bool:
        cls.definition_uri = self.schemaview.get_uri(cls.name, native=True, expand=True)
        # SchemaLoader synthesises class_uri when missing (schemaloader.py:291-302) then
        # inserts it into exact_mappings (schemaloader.py:289-290 and 302).
        # get_uri(native=False) already implements this: it returns the declared class_uri
        # when set, otherwise constructs {default_prefix}:{camelcase(name)} — exactly
        # what SchemaLoader's uri_or_curie_for does.
        cls.exact_mappings.insert(0, cls.class_uri or self.schemaview.get_uri(cls.name, native=False))
        self._visit(cls)
        if hasattr(cls, "class_uri"):
            delattr(cls, "class_uri")
        # Slot usage is a construction artifact
        # TODO: Figure out why this is here.  It isn't good form to alter a schema that may be used by other things
        cls.slot_usage = {}
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        # ``slot`` may be a materialized, class-mangled induced slot (e.g. ``Person__name``
        # or an attribute-derived ``c1__a``) whose mangled name is not itself a schema
        # element. ``_slot_base_name`` records the base slot name to resolve the
        # ``definition_uri`` against; attribute-only slots have no base and are skipped.
        base_name = self._slot_base_name.get(slot.name)
        if base_name is not None:
            slot.definition_uri = self.schemaview.get_uri(base_name, native=True, expand=True)
        self._visit(slot)
        self.adjust_slot(slot)

    def visit_type(self, typ: TypeDefinition) -> None:
        typ.definition_uri = self.schemaview.get_uri(typ.name, native=True, expand=True)
        self._visit(typ)
        typ.uri = self.schemaview.namespaces().uri_for(typ.uri)

    def visit_subset(self, ss: SubsetDefinition) -> None:
        ss.definition_uri = self.schemaview.get_uri(ss.name, native=True, expand=True)
        self._visit(ss)

    def visit_enum(self, enum: EnumDefinition) -> None:
        enum.definition_uri = self.schemaview.get_uri(enum.name, native=True, expand=True)

    def end_schema(
        self, context: str | list[str] | tuple[str, ...] = [], context_kwargs: dict | None = None, **_
    ) -> str:
        default_context_kwargs = {"model": False}
        if context_kwargs is None:
            context_kwargs = default_context_kwargs
        else:
            context_kwargs = {**default_context_kwargs, **context_kwargs}

        self._add_type(self.schema)
        base_prefix = self.default_prefix()

        # `context` can be a `str`, a `list[str]` or a `tuple[str]`
        # since the context might need to get extended, `context_list` must be `list[str]`
        context_list: list[str] = []
        # TODO: fix this, see https://github.com/linkml/linkml/issues/871
        # JSON LD adjusts context reference using '@base'.  If context is supplied and not a URI, generate an
        # absolute URI for it
        if not context and self.format == "jsonld":
            # TODO: Once we get pyld running w/ relative contexts, we need to figure out how to generate and add
            #       the relative (?) context reference below
            # model_context = self.schema.source_file.replace('.yaml', '.prefixes.context.jsonld')
            # context = [METAMODEL_CONTEXT_URI, f'file://./{model_context}']
            # TODO: The _visit function above alters the schema in situ
            # force some context_kwargs
            context_kwargs["metadata"] = False
            # Forward importmap/base_dir so the spawned ContextGenerator can
            # re-resolve any URI-style imports in ``self.original_schema``
            # through the same ``--importmap`` the caller supplied.
            context_kwargs.setdefault("importmap", self.importmap)
            context_kwargs.setdefault("base_dir", self.base_dir)
            add_prefixes = ContextGenerator(self.original_schema, **context_kwargs).serialize()
            add_prefixes_json = loads(add_prefixes)
            metamodel_ctx = self.metamodel_context or METAMODEL_CONTEXT_URI
            context_list = [metamodel_ctx, add_prefixes_json["@context"]]
        elif isinstance(context, str):  # Some of the older code doesn't do multiple contexts
            context_list = [context]
        elif isinstance(context, tuple):
            context_list = list(context)
        else:
            context_list = context

        # Add context entries for all imported schemas, replicating the self.loaded approach.
        # SchemaLoader populated self.loaded in breadth-first order: direct imports of the
        # main schema first (in listed order), then their transitive dependencies.
        # Local schema references are kept relative; linkml: ones are expanded to full URL.
        visited: set[str] = {self.schemaview.schema.name}
        queue: list[str] = list(self.schemaview.schema.imports)
        while queue:
            imp = queue.pop(0)
            if imp in visited:
                continue
            visited.add(imp)
            imp_schema = self.schemaview.schema_map.get(imp)
            if imp_schema is None:
                continue
            if imp.startswith("linkml:") or "://" in imp:
                ref = str(imp_schema.id)
            else:
                ref = imp
            context_list.append(ref + ".context.jsonld")
            for sub_imp in imp_schema.imports:
                if sub_imp not in visited:
                    queue.append(sub_imp)

        # Absolute local filesystem paths must be pre-expressed as file:// URIs.
        # ``Path.as_uri`` handles both POSIX (``/x`` -> ``file:///x``) and bare
        # Windows drive paths (``D:\x`` -> ``file:///D:/x``); URLs (anything
        # with a ``://``) and relative refs are left untouched.
        for ci in range(0, len(context_list)):
            entry = context_list[ci]
            if isinstance(entry, str) and "://" not in entry and os.path.isabs(entry):
                context_list[ci] = Path(entry).as_uri()

        if self.format == "jsonld":
            self.schema["@context"] = context_list[0] if len(context_list) == 1 and not base_prefix else context_list
            if base_prefix:
                self.schema["@context"].append({"@base": base_prefix})
        # json_obj["@id"] = self.schema.id
        # SchemaLoader strips source_file to basename (schemaloader.py:705).
        # Do this here (after all imports are resolved) rather than in __post_init__,
        # so that SchemaView can still locate imported schemas via source_file during
        # the serialization pipeline.
        if isinstance(self.schema, dict) and "source_file" in self.schema:
            sf = self.schema["source_file"]
            if sf and "://" not in str(sf):
                self.schema["source_file"] = os.path.basename(str(sf))
        elif hasattr(self.schema, "source_file") and self.schema.source_file:
            if "://" not in self.schema.source_file:
                self.schema.source_file = os.path.basename(self.schema.source_file)
        out = str(as_json(self.schema, indent="  ")) + "\n"
        self.schema = self.original_schema
        return out

    def serialize(self, context: Sequence[str] | None = None, context_kwargs: dict | None = None, **kwargs) -> str:
        """
        Serialize the model to JSON-LD

        Args:
            context (str, list[str], None): If ``None``, use context from schema,
                otherwise replace context with this.
            context_kwargs (dict, None): Keyword arguments forwarded to the JSON-LD Context generator
        """
        return super().serialize(context=context, context_kwargs=context_kwargs, **kwargs)


# Option "context" can be specified multiple times.
@shared_arguments(JSONLDGenerator)
@click.command(name="jsonld")
@click.option(
    "--context",
    multiple=True,
    type=click.STRING,
    help=f"JSONLD context file (default: {METAMODEL_CONTEXT_URI} and <model>.prefixes.context.jsonld)",
)
@click.option(
    "--context-kwargs",
    "-k",
    type=(str, bool),
    multiple=True,
    help="kwargs passed to the JSONLD Context generator when instantiated. "
    "Since the context is embedded within the JSON-LD document, "
    "only the boolean instance attributes are formally supported, "
    'e.g. "output" and "base" are not applicable. '
    "The `emit_metadata` value is forced to be False.\n\n"
    "multiple kwargs like `-k {key} {value}` can be passed",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, context_kwargs: list[tuple[str, bool]], context: tuple[str], **kwargs):
    """Generate JSONLD file from LinkML schema.

    Status: incomplete
    """
    if context_kwargs:
        context_kwargs = dict(context_kwargs)
    else:
        context_kwargs = {}

    print(JSONLDGenerator(yamlfile, **kwargs).serialize(context=context, context_kwargs=context_kwargs, **kwargs))


if __name__ == "__main__":
    cli()
