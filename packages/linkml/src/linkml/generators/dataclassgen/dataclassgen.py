"""
SchemaView/template-based generator for YAMLRoot dataclasses.

Successor architecture for the visitor-based pythongen (see issue #923 and
PLAN_PYDANTIC_METAMODEL_MIGRATION.md): the same TemplateModel rendering
pipeline as pydanticgen, emitting the dataclass/YAMLRoot shape. The parity
gate against pythongen is semantic - generated modules must compile and load
data equivalently - not byte-identical.
"""

import keyword
import os
from dataclasses import dataclass, field
from datetime import datetime

import click

from linkml._version import __version__
from linkml.generators.python.python_ifabsent_processor import PythonIfAbsentProcessor
from linkml.generators.dataclassgen.template import (
    DataclassClass,
    DataclassModule,
    EnumClass,
    NameClass,
    SlotEntry,
    TypeClass,
)
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition, TypeDefinition
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore

#: declared type base -> (annotation, coercion constructor); non-builtin bases
#: come from linkml_runtime.utils.metamodelcore and annotate as Union[str, Base]
_BUILTIN_BASES = {"str": "str", "int": "int", "float": "float"}
_BOOL_BASE = "Bool"


def _python_safe(name: str) -> str:
    name = underscore(name)
    if keyword.iskeyword(name):
        name = name + "_"
    return name


@dataclass
class DataclassGenerator(Generator):
    """Generate YAMLRoot dataclasses from a schema via SchemaView and jinja templates."""

    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["python"]
    uses_schemaloader = False

    # populated during build
    _emitted_classes: set = field(default_factory=set)

    # -- naming ---------------------------------------------------------------

    def _class_py_name(self, class_name: str) -> str:
        return camelcase(class_name)

    def _name_class(self, cls: ClassDefinition) -> str | None:
        """Name of the class-reference type (e.g. PersonId) for a keyed/identified class."""
        id_slot = self.schemaview.get_identifier_slot(cls.name, use_key=True)
        if id_slot is None:
            return None
        alias = id_slot.alias if id_slot.alias else id_slot.name
        return camelcase(cls.name) + camelcase(alias)

    def _slot_alias(self, slot: SlotDefinition) -> str:
        return _python_safe(slot.alias if slot.alias else slot.name)

    def _is_any_class(self, class_name: str) -> bool:
        cls = self.schemaview.get_class(class_name)
        return cls is not None and str(cls.class_uri) == "linkml:Any"

    def _quoted(self, class_py_name: str) -> str:
        """Quote forward references to classes not yet emitted."""
        if class_py_name in self._emitted_classes:
            return class_py_name
        return f'"{class_py_name}"'

    # -- ranges ---------------------------------------------------------------

    def _type_info(self, type_name: str | None) -> tuple[str, str]:
        """(annotation, coercion constructor) for a type range."""
        if type_name is None:
            type_name = self.schema.default_range or "string"
        if type_name not in self.schemaview.all_types():
            return "str", "str"
        induced = self.schemaview.induced_type(type_name)
        base = induced.base or "str"
        if base in _BUILTIN_BASES:
            return _BUILTIN_BASES[base], _BUILTIN_BASES[base]
        if base == _BOOL_BASE:
            return "Union[bool, Bool]", "Bool"
        return f"Union[str, {base}]", base

    def _class_order(self) -> list[ClassDefinition]:
        """Classes in declaration order, parents hoisted before children."""
        ordered: list[ClassDefinition] = []
        seen: set[str] = set()

        def visit(cls: ClassDefinition) -> None:
            if cls.name in seen:
                return
            seen.add(cls.name)
            if cls.is_a:
                visit(self.schemaview.get_class(cls.is_a))
            for mixin in cls.mixins:
                visit(self.schemaview.get_class(mixin))
            ordered.append(cls)

        for cls in self.schemaview.all_classes().values():
            visit(cls)
        return ordered

    # -- per-slot field + post_init generation --------------------------------

    def _field_for_slot(self, cls: ClassDefinition, slot: SlotDefinition) -> tuple[str, list[str]]:
        """Return (field line, post_init lines) for one induced slot."""
        sv = self.schemaview
        alias = self._slot_alias(slot)
        self_ref = f"self.{alias}"
        required = bool(slot.required or slot.identifier or slot.key)
        post: list[str] = []

        if slot.identifier or slot.key:
            name_cls = self._name_class(cls)
            annotation = f"Union[str, {name_cls}]"
            post.append(f"if self._is_empty({self_ref}):")
            post.append(f'    self.MissingRequiredField("{alias}")')
            post.append(f"if not isinstance({self_ref}, {name_cls}):")
            post.append(f"    {self_ref} = {name_cls}({self_ref})")
            return f"{alias}: {annotation} = None", post

        if required:
            post.append(f"if self._is_empty({self_ref}):")
            post.append(f'    self.MissingRequiredField("{alias}")')

        guard = "" if required else f"{self_ref} is not None and "

        if slot.range in sv.all_classes():
            range_cls = sv.get_class(slot.range)
            range_py = self._class_py_name(slot.range)
            range_ref = self._quoted(range_py)
            id_slot = sv.get_identifier_slot(slot.range, use_key=True)
            inlined = sv.is_inlined(slot)

            if self._is_any_class(slot.range):
                # linkml:Any classes alias typing.Any - no coercion possible
                annotation = f"Union[dict, {range_py}]"
                if slot.multivalued:
                    annotation = f"Optional[Union[{annotation}, list[{annotation}]]]"
                    return f"{alias}: {annotation} = empty_list()", post
                if not required:
                    annotation = f"Optional[{annotation}]"
                return f"{alias}: {annotation} = None", post

            if not slot.multivalued:
                if inlined or id_slot is None:
                    annotation = f"Union[dict, {range_ref}]"
                    post.append(f"if {guard}not isinstance({self_ref}, {range_py}):")
                    post.append(f"    {self_ref} = {range_py}(**as_dict({self_ref}))")
                else:
                    name_cls = self._name_class(range_cls)
                    annotation = f"Union[str, {name_cls}]"
                    post.append(f"if {guard}not isinstance({self_ref}, {name_cls}):")
                    post.append(f"    {self_ref} = {name_cls}({self_ref})")
                default = "None"
                if not required:
                    annotation = f"Optional[{annotation}]"
                return f"{alias}: {annotation} = {default}", post

            # multivalued
            if inlined or id_slot is None:
                if id_slot is not None:
                    key_alias = _python_safe(id_slot.alias if id_slot.alias else id_slot.name)
                    name_cls = self._name_class(range_cls)
                    annotation = (
                        f"Optional[Union[dict[Union[str, {name_cls}], Union[dict, {range_ref}]], "
                        f"list[Union[dict, {range_ref}]]]]"
                    )
                    normalizer = "_normalize_inlined_as_list" if slot.inlined_as_list else "_normalize_inlined_as_dict"
                    post = [
                        f'self.{normalizer}(slot_name="{alias}", slot_type={range_py}, '
                        f'key_name="{key_alias}", keyed=True)'
                    ]
                    default = "empty_dict()"
                else:
                    first_required = next((s for s in sv.class_induced_slots(slot.range) if s.required), None)
                    key_alias = (
                        _python_safe(first_required.alias if first_required.alias else first_required.name)
                        if first_required
                        else self._slot_alias(sv.class_induced_slots(slot.range)[0])
                    )
                    annotation = f"Optional[Union[Union[dict, {range_ref}], list[Union[dict, {range_ref}]]]]"
                    post = [
                        f'self._normalize_inlined_as_list(slot_name="{alias}", slot_type={range_py}, '
                        f'key_name="{key_alias}", keyed=False)'
                    ]
                    default = "empty_list()"
                return f"{alias}: {annotation} = {default}", post

            # multivalued reference list
            name_cls = self._name_class(range_cls)
            annotation = f"Optional[Union[Union[str, {name_cls}], list[Union[str, {name_cls}]]]]"
            post.append(f"if not isinstance({self_ref}, list):")
            post.append(f"    {self_ref} = [{self_ref}] if {self_ref} is not None else []")
            post.append(f"{self_ref} = [v if isinstance(v, {name_cls}) else {name_cls}(v) for v in {self_ref}]")
            return f"{alias}: {annotation} = empty_list()", post

        if slot.range in sv.all_enums():
            enum_py = camelcase(slot.range)
            enum_ref = f'"{enum_py}"'
            if not slot.multivalued:
                annotation = f"Union[str, {enum_ref}]"
                post.append(f"if {guard}not isinstance({self_ref}, {enum_py}):")
                post.append(f"    {self_ref} = {enum_py}({self_ref})")
                if not required:
                    annotation = f"Optional[{annotation}]"
                return f"{alias}: {annotation} = None", post
            annotation = f"Optional[Union[Union[str, {enum_ref}], list[Union[str, {enum_ref}]]]]"
            post.append(f"if not isinstance({self_ref}, list):")
            post.append(f"    {self_ref} = [{self_ref}] if {self_ref} is not None else []")
            post.append(f"{self_ref} = [v if isinstance(v, {enum_py}) else {enum_py}(v) for v in {self_ref}]")
            return f"{alias}: {annotation} = empty_list()", post

        # type (or absent) range
        annotation, ctor = self._type_info(slot.range)
        isinstance_target = ctor if ctor not in ("str", "int", "float") else annotation
        if not slot.multivalued:
            post.append(f"if {guard}not isinstance({self_ref}, {isinstance_target}):")
            post.append(f"    {self_ref} = {ctor}({self_ref})")
            full = annotation if required else f"Optional[{annotation}]"
            return f"{alias}: {full} = None", post
        post.append(f"if not isinstance({self_ref}, list):")
        post.append(f"    {self_ref} = [{self_ref}] if {self_ref} is not None else []")
        post.append(
            f"{self_ref} = [v if isinstance(v, {isinstance_target}) else {ctor}(v) for v in {self_ref}]"
        )
        return f"{alias}: Optional[Union[{annotation}, list[{annotation}]]] = empty_list()", post

    # -- per-element builders --------------------------------------------------

    def _build_class(self, cls: ClassDefinition) -> DataclassClass:
        sv = self.schemaview
        induced = {s.name: s for s in sv.class_induced_slots(cls.name)}
        # slots declaring `domain: <this class>` are implicitly attached -
        # SchemaLoader materialized this; SchemaView does not
        for top_slot in sv.all_slots().values():
            if top_slot.domain == cls.name and top_slot.name not in induced:
                induced[top_slot.name] = sv.induced_slot(top_slot.name, cls.name)
        id_slot = sv.get_identifier_slot(cls.name, use_key=True)

        # "own" = not provided by the is_a parent via python inheritance (so
        # mixin-derived slots are declared here, as pythongen does), or
        # redefined via slot_usage; inherited required slots are re-declared
        # (dataclass field ordering) but their post_init runs in the parent
        parent_names = set(sv.class_slots(cls.is_a)) if cls.is_a else set()
        ordered: list[tuple[SlotDefinition, bool]] = []  # (slot, emit_post_init)
        if id_slot is not None:
            ordered.append((induced[id_slot.name], True))
        own = [
            s
            for n, s in induced.items()
            if (n not in parent_names or n in cls.slot_usage) and (id_slot is None or n != id_slot.name)
        ]
        inherited = [
            s
            for n, s in induced.items()
            if n in parent_names and n not in cls.slot_usage and (id_slot is None or n != id_slot.name)
        ]
        ordered += [(s, False) for s in inherited if s.required]
        ordered += [(s, True) for s in own if s.required and not s.ifabsent]
        ordered += [(s, True) for s in own if s.required and s.ifabsent]
        ordered += [(s, True) for s in own if not s.required]

        attributes: list[str] = []
        post_lines: list[str] = []
        for slot, emit_post in ordered:
            field_line, post = self._field_for_slot(cls, slot)
            if slot.ifabsent is not None:
                ifabsent_text = self.ifabsent_processor.process_slot(slot, cls)
                if ifabsent_text is not None:
                    field_line = field_line.rsplit(" = ", 1)[0] + f" = {ifabsent_text}"
            attributes.append(field_line)
            if emit_post and post:
                if post_lines:
                    post_lines.append("")
                post_lines.extend(post)

        class_uri = cls.class_uri if cls.class_uri else sv.get_uri(cls)
        expanded = sv.get_uri(cls, expand=True)
        model_uri = sv.get_uri(cls, expand=True, native=True)
        curie = f'"{class_uri}"' if ":" in str(class_uri) and "://" not in str(class_uri) else "None"

        base = self._class_py_name(cls.is_a) if cls.is_a else "YAMLRoot"
        inherited_names = sorted(self._slot_alias(s) for s in induced.values() if s.inherited)

        built = DataclassClass(
            name=self._class_py_name(cls.name),
            base=base,
            description=cls.description,
            inherited_slots=", ".join(f'"{n}"' for n in inherited_names),
            class_class_uri=f'URIRef("{expanded}")',
            class_class_curie=curie,
            class_name_value=cls.name,
            class_model_uri=f'URIRef("{model_uri}")',
            attributes=attributes,
            post_init_lines=post_lines,
        )
        self._emitted_classes.add(built.name)
        return built

    def _build_name_classes(self) -> list[NameClass]:
        sv = self.schemaview
        out: list[NameClass] = []
        for cls in self._class_order():
            id_slot = sv.get_identifier_slot(cls.name, use_key=True)
            if id_slot is None:
                continue
            base = None
            if cls.is_a:
                parent_id = sv.get_identifier_slot(cls.is_a, use_key=True)
                if parent_id is not None and parent_id.name == id_slot.name:
                    base = self._name_class(sv.get_class(cls.is_a))
            if base is None:
                annotation, ctor = self._type_info(id_slot.range)
                base = {"str": "extended_str", "int": "extended_int", "float": "extended_float"}.get(ctor, ctor)
            out.append(NameClass(name=self._name_class(cls), base=base))
        return out

    def _build_types(self) -> list[TypeClass]:
        sv = self.schemaview
        out: list[TypeClass] = []
        for typ in sv.all_types().values():
            if typ.typeof:
                base = camelcase(typ.typeof)
            else:
                base = typ.base or "str"
                base = {"Bool": "Bool", "str": "str", "int": "int", "float": "float"}.get(base, base)
            type_uri = typ.uri if typ.uri else sv.get_uri(typ)
            prefix, _, local = str(type_uri).partition(":")
            uri_expr = f'{self._ns_var(prefix)}["{local}"]' if local and "://" not in str(type_uri) else f'URIRef("{type_uri}")'
            out.append(
                TypeClass(
                    name=camelcase(typ.name),
                    base=base,
                    type_class_uri=uri_expr,
                    type_class_curie=f'"{type_uri}"' if "://" not in str(type_uri) else "None",
                    type_name_value=typ.name,
                    type_model_uri=f'URIRef("{sv.get_uri(typ, expand=True, native=True)}")',
                )
            )
        return out

    def _meaning_expr(self, meaning: str) -> str:
        """Render a permissible value meaning as a CurieNamespace member, as pythongen does."""
        prefix, _, local = str(meaning).partition(":")
        if local and "://" not in str(meaning) and prefix in self._ns_prefixes:
            return f'{self._ns_var(prefix)}["{local}"]'
        return f'"{meaning}"'

    def _build_enums(self) -> list[EnumClass]:
        out: list[EnumClass] = []
        for enum in self.schemaview.all_enums().values():
            pvs: list[str] = []
            addvals: list[str] = []
            for text, pv in (enum.permissible_values or {}).items():
                args = [f'text="{text}"']
                if pv.description:
                    args.append(f'description="""{pv.description}"""')
                if pv.meaning:
                    args.append(f"meaning={self._meaning_expr(pv.meaning)}")
                if not str(text).isidentifier() or keyword.iskeyword(str(text)):
                    addvals.append(f'setattr(cls, "{text}", PermissibleValue({", ".join(args)}))')
                else:
                    pvs.append(f"{text} = PermissibleValue({', '.join(args)})")
            out.append(
                EnumClass(
                    name=camelcase(enum.name),
                    description=enum.description,
                    permissible_values=pvs,
                    addvals=addvals,
                )
            )
        return out

    def _ns_var(self, prefix: str) -> str:
        var = prefix.upper().replace("-", "_").replace(".", "_")
        return var if var else "DEFAULT_"

    def _build_namespaces(self) -> tuple[list[str], str]:
        sv = self.schemaview
        lines: list[str] = []
        seen: set[str] = set()
        for schema in sv.schema_map.values():
            for prefix in schema.prefixes.values():
                if prefix.prefix_prefix in seen:
                    continue
                seen.add(prefix.prefix_prefix)
                lines.append(
                    f"{self._ns_var(prefix.prefix_prefix)} = "
                    f"CurieNamespace('{prefix.prefix_prefix}', '{prefix.prefix_reference}')"
                )
        default_prefix = self.schema.default_prefix
        if default_prefix and default_prefix in seen and "://" not in default_prefix:
            default_expr = f"CurieNamespace('', str({self._ns_var(default_prefix)}))"
        else:
            default_expr = f"CurieNamespace('', '{sfx(str(self.schema.id))}')"
        return lines, default_expr

    def _build_slot_entries(self) -> list[SlotEntry]:
        sv = self.schemaview
        out: list[SlotEntry] = []
        for slot in sv.all_slots().values():
            alias = self._slot_alias(slot)
            annotation, _ = self._type_info(slot.range if slot.range in sv.all_types() else None)
            if slot.identifier or slot.key:
                range_expr = "URIRef"
            elif slot.range in sv.all_classes() or slot.range in sv.all_enums():
                range_expr = f"Optional[str]"
            else:
                range_expr = annotation if slot.required else f"Optional[{annotation}]"
            out.append(
                SlotEntry(
                    pyname=alias,
                    uri=f"DEFAULT_.{alias}",
                    slot_name=slot.name,
                    curie=f"DEFAULT_.curie('{alias}')",
                    model_uri=f"DEFAULT_.{alias}",
                    domain="None",
                    range=range_expr,
                )
            )
        return out

    # -- entry point -----------------------------------------------------------

    def render(self) -> DataclassModule:
        sv = self.schemaview
        if self.mergeimports:
            sv.merge_imports()
        self._emitted_classes = set()
        self.ifabsent_processor = PythonIfAbsentProcessor(sv)
        namespaces, default_ns = self._build_namespaces()
        self._ns_prefixes = {line.split(" = ")[1].split("'")[1] for line in namespaces}
        types = self._build_types()
        name_classes = self._build_name_classes()
        classes: list = []
        for cls in self._class_order():
            if self._is_any_class(cls.name):
                name = self._class_py_name(cls.name)
                self._emitted_classes.add(name)
                classes.append(f"{name} = Any")
            else:
                classes.append(self._build_class(cls))
        return DataclassModule(
            source_file=os.path.basename(str(self.schema.source_file)) if self.schema.source_file else self.schema.name,
            generator_version=self.generatorversion,
            generation_date=datetime.now().isoformat() if self.metadata else None,
            schema_name=self.schema.name,
            schema_id=str(self.schema.id),
            schema_description=(self.schema.description or "").replace("\n", "\n#   "),
            schema_license=self.schema.license or "",
            metamodel_version=self.schema.metamodel_version or "",
            version=f'"{self.schema.version}"' if self.schema.version else "None",
            namespaces=namespaces,
            default_namespace=default_ns,
            types=types,
            name_classes=name_classes,
            classes=classes,
            enums=self._build_enums(),
            slot_entries=self._build_slot_entries(),
        )

    def serialize(self, **kwargs) -> str:
        return self.render().render()


@shared_arguments(DataclassGenerator)
@click.command(name="python-dataclasses")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate YAMLRoot dataclasses from a LinkML schema (template-based pythongen successor)"""
    print(DataclassGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
