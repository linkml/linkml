import keyword
import logging
import os
import re
from copy import copy
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Callable, Dict, Iterator, List, Optional, Set, Tuple, Union

import click
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import linkml_files
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    DefinitionName,
    Element,
    EnumDefinition,
    PermissibleValue,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
)
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import be, camelcase, sfx, split_col, underscore, wrapped_annotation
from linkml_runtime.utils.metamodelcore import builtinnames
from rdflib import URIRef

import linkml
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.ifabsent_functions import ifabsent_postinit_declaration, ifabsent_value_declaration


@dataclass
class PythonGenerator(Generator):
    """
    Generates Python dataclasses from a LinkML model

    See `Python Generator Docs <https://linkml.io/linkml/generators/python.html>`_
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["py"]
    file_extension = "py"
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

    def __post_init__(self) -> None:
        if isinstance(self.schema, Path):
            self.schema = str(self.schema)
        self.sourcefile = self.schema
        self.schemaview = SchemaView(self.schema, base_dir=self.base_dir)
        super().__post_init__()
        if self.format is None:
            self.format = self.valid_formats[0]
        if self.schema.default_prefix == "linkml" and not self.genmeta:
            logging.error("Generating metamodel without --genmeta is highly inadvisable!")
        if not self.schema.source_file and isinstance(self.sourcefile, str) and "\n" not in self.sourcefile:
            self.schema.source_file = os.path.basename(self.sourcefile)

    def compile_module(self, **kwargs) -> ModuleType:
        """
        Compiles generated python code to a module
        :return:
        """
        pycode = self.serialize(**kwargs)
        try:
            return compile_python(pycode)
        except NameError as e:
            logging.error(f"Code:\n{pycode}")
            logging.error(f"Error compiling generated python code: {e}")
            raise e

    def visit_schema(self, **kwargs) -> None:
        # Add explicitly declared prefixes
        self.emit_prefixes.update([p.prefix_prefix for p in self.schema.prefixes.values()])

        # Add all emit statements
        self.emit_prefixes.update(self.schema.emit_prefixes)

        # Add the default prefix
        if self.schema.default_prefix:
            self.emit_prefixes.add(self.namespaces.prefix_for(self.schema.default_prefix))

    def visit_class(self, cls: ClassDefinition) -> bool:
        if not cls.imported_from:
            cls_prefix = self.namespaces.prefix_for(cls.class_uri)
            if cls_prefix:
                self.emit_prefixes.add(cls_prefix)
            self.add_mappings(cls)
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if not slot.imported_from:
            slot_prefix = self.namespaces.prefix_for(slot.slot_uri)
            if slot_prefix:
                self.emit_prefixes.add(slot_prefix)
            self.add_mappings(slot)

    def visit_type(self, typ: TypeDefinition) -> None:
        if not typ.imported_from:
            type_prefix = self.namespaces.prefix_for(typ.uri)
            if type_prefix:
                self.emit_prefixes.add(type_prefix)

    def gen_schema(self) -> str:
        # The metamodel uses Enumerations to define itself, so don't import if we are generating the metamodel
        enumimports = (
            ""
            if self.genmeta
            else "from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions\n"
        )
        handlerimport = "from linkml_runtime.utils.enumerations import EnumDefinitionImpl"
        split_description = ""
        if self.schema.description:
            split_description = "\n#   ".join(d for d in self.schema.description.split("\n") if d is not None)
        head = (
            f"""# Auto generated from {self.schema.source_file} by {self.generatorname} version: {self.generatorversion}
# Generation date: {self.schema.generation_date}
# Schema: {self.schema.name}
#"""
            if self.emit_metadata and self.schema.generation_date
            else ""
        )

        return f"""{head}
# id: {self.schema.id}
# description: {split_description}
# license: {be(self.schema.license)}

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
{enumimports}
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
{handlerimport}
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
{self.gen_imports()}

metamodel_version = "{self.schema.metamodel_version}"
version = {'"' + self.schema.version + '"' if self.schema.version else None}

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
{self.gen_namespaces()}


# Types
{self.gen_typedefs()}
# Class references
{self.gen_references()}

{self.gen_classdefs()}

# Enumerations
{self.gen_enumerations()}

# Slots
{self.gen_slotdefs()}"""

    def end_schema(self, **_) -> str:
        return re.sub(r" +\n", "\n", self.gen_schema().replace("\t", "    ")).strip(" ")

    def gen_imports(self) -> str:
        list_ents = [f"from {k} import {', '.join(v)}" for k, v in self.gen_import_list().items()]
        return "\n".join(list_ents)

    def gen_import_list(self) -> Dict[str, List[str]]:
        """
        Generate a list of types to import

        :return: source file followed by elements to import
        """

        class ImportList:
            def __init__(self, schema_location: str):
                self.schema_location = schema_location
                self.v: Dict[str, Set[str]] = {}

            def add_element(self, e: Element) -> None:
                if e.imported_from:
                    self.add_entry(e.imported_from, camelcase(e.name))

            def add_entry(innerself, path: Union[str, URIRef], name: str) -> None:
                path = str(self.namespaces.uri_for(path) if ":" in path else path)
                if path.startswith(linkml_files.LINKML_NAMESPACE):
                    model_base = "." if self.genmeta else "linkml_runtime.linkml_model."
                    innerself.v.setdefault(model_base + path[len(linkml_files.LINKML_NAMESPACE) :], set()).add(name)
                elif path == linkml.BIOLINK_MODEL_URI:
                    innerself.v.setdefault(linkml.BIOLINK_MODEL_PYTHON_LOC, set()).add(name)
                elif "://" in path:
                    raise ValueError(f"Cannot map {path} into a python import statement")
                elif "/" in path:
                    innerself.v.setdefault(path.replace("./", ".").replace("/", "."), set()).add(name)
                elif "." in path:
                    innerself.v.setdefault(path, set()).add(name)
                else:
                    innerself.v.setdefault(". " + path, set()).add(name)

            def values(self) -> Dict[str, List[str]]:
                return {k: sorted(self.v[k]) for k in sorted(self.v.keys())}

        def add_type_ref(typ: TypeDefinition) -> None:
            if not typ.typeof and typ.base and typ.base not in builtinnames:
                if "." in typ.base:
                    rval.add_entry(*typ.base.rsplit("."))
                else:
                    rval.add_entry("linkml_runtime.utils.metamodelcore", typ.base)
            if typ.typeof:
                add_type_ref(self.schema.types[typ.typeof])
            rval.add_element(typ)

        def add_enum_ref(e: EnumDefinition) -> None:
            rval.add_element(e)

        def add_slot_range(slot: SlotDefinition) -> None:
            if slot.range:
                if slot.range in self.schema.types:
                    add_type_ref(self.schema.types[slot.range])
                elif slot.range in self.schema.enums:
                    add_enum_ref(self.schema.enums[slot.range])
                else:
                    cls = self.schema.classes[slot.range]
                    if cls.imported_from:
                        if self.class_identifier(cls):
                            identifier_range = self.class_identifier_path(cls, False)[-1]
                            if identifier_range in self.schema.types:
                                add_type_ref(TypeDefinition(identifier_range))
                            else:
                                rval.add_entry(cls.imported_from, identifier_range)
                        if slot.inlined:
                            rval.add_element(cls)

        rval = ImportList(self.schema_location)
        for typ in self.schema.types.values():
            if not typ.imported_from:
                add_type_ref(typ)
        for slot in self.schema.slots.values():
            if not slot.imported_from:
                if slot.is_a:
                    parent = self.schema.slots[slot.is_a]
                    if (parent.key or parent.identifier) and parent.imported_from:
                        rval.add_element(self.schema.slots[slot.is_a])
                if slot.domain:
                    domain = self.schema.classes[slot.domain]
                    if domain.imported_from:
                        rval.add_element(self.schema.classes[slot.domain])
                add_slot_range(slot)

        for cls in self.schema.classes.values():
            if not cls.imported_from:
                if cls.is_a:
                    parent = self.schema.classes[cls.is_a]
                    if parent.imported_from:
                        rval.add_element(self.schema.classes[cls.is_a])
                        if self.class_identifier(parent):
                            rval.add_entry(
                                parent.imported_from,
                                self.class_identifier_path(parent, False)[-1],
                            )
                for slotname in cls.slots:
                    add_slot_range(self.schema.slots[slotname])

        return rval.values()

    def gen_namespaces(self) -> str:
        dflt_prefix = self._default_curie_or_uri()
        dflt = f"CurieNamespace('', '{sfx(dflt_prefix)}')" if ":/" in dflt_prefix else dflt_prefix.upper()
        curienamespace_defs = [
            {
                "variable": f"{pfx.upper().replace('.', '_').replace('-', '_')}",
                "value": f"CurieNamespace('{pfx.replace('.', '_')}', '{self.namespaces[pfx]}')",
            }
            for pfx in sorted(self.emit_prefixes)
            if pfx in self.namespaces
        ]
        curienamespace_declarations = "\n".join(
            [f"{ns['variable']} = {ns['value']}" for ns in curienamespace_defs] + [f"DEFAULT_ = {dflt}"]
        )

        ",".join([x["variable"] for x in curienamespace_defs])
        # catalog_declaration = f"\nnamespace_catalog = CurieNamespaceCatalog.create({curienamespace_vars})\n"
        catalog_declaration = ""

        return curienamespace_declarations + catalog_declaration

    def gen_references(self) -> str:
        """Generate python type declarations for all identifiers (primary keys)"""
        rval = []
        for cls in self._sort_classes(self.schema.classes.values()):
            if not cls.imported_from:
                pkeys = self.primary_keys_for(cls)
                if pkeys:
                    for pk in pkeys:
                        classname = camelcase(cls.name) + camelcase(self.aliased_slot_name(pk))
                        # If we've got a parent slot and the range of the parent is the range of the child, the
                        # child slot is a subclass of the parent.  Otherwise, the child range has been overridden,
                        # so the inheritance chain has been broken
                        parent_pk = self.class_identifier(cls.is_a) if cls.is_a else None
                        parent_pk_slot = self.schema.slots[parent_pk] if parent_pk else None
                        pk_slot = self.schema.slots[pk]
                        if parent_pk_slot and (parent_pk_slot.name == pk or pk_slot.range == parent_pk_slot.range):
                            parents = self.class_identifier_path(cls.is_a, False)
                        else:
                            parents = self.slot_range_path(pk_slot)
                        parent_cls = (
                            "extended_" + parents[-1] if parents[-1] in ["str", "float", "int"] else parents[-1]
                        )
                        rval.append(f"class {classname}({parent_cls}):\n\tpass")
                        break  # We only do the first primary key
        return "\n\n\n".join(rval)

    def gen_typedefs(self) -> str:
        """Generate python type declarations for all defined types"""
        rval = []
        defs_to_generate = [x for x in self.schema.types.values() if not x.imported_from]
        emitted_types = []
        # all imported_from types are already considered generated
        emitted_types.extend([x.name for x in self.schema.types.values() if x.imported_from])
        for typ in [x for x in defs_to_generate if not x.typeof]:
            self._gen_typedef(typ, typ.base.rsplit(".")[-1], rval, emitted_types)

        while True:
            defs_to_generate_typeof = [x for x in defs_to_generate if x.typeof and x.name not in emitted_types]
            if len(defs_to_generate_typeof) == 0:
                break
            defs_can_generate = [x for x in defs_to_generate_typeof if x.typeof in emitted_types]
            if len(defs_can_generate) == 0:
                raise ValueError(
                    "Cannot generate type definition for "
                    f"{[f'{x.name} of {x.typeof}' for x in defs_to_generate_typeof]}. "
                    "Forgot a link in the type hierarchy chain?"
                )
            for typ in defs_can_generate:
                self._gen_typedef(typ, camelcase(typ.typeof), rval, emitted_types)

        return "\n".join(rval)

    def _gen_typedef(self, typ, superclass, rval, emitted_types):
        typname = camelcase(typ.name)
        desc = ""
        if typ.description:
            description = typ.description.replace('"""', "---")
            desc = f'\n\t""" {description} """'
        rval.append(f"class {typname}({superclass}):{desc}\n\t{self.gen_type_meta(typ)}\n\n")
        emitted_types.append(typ.name)

    def gen_classdefs(self) -> str:
        """Create class definitions for all non-mixin classes in the model
        Note that apply_to classes are transformed to mixins
        """
        clist = self._sort_classes(self.schema.classes.values())
        return "\n".join([self.gen_classdef(v) for v in clist if not v.imported_from])

    def gen_classdef(self, cls: ClassDefinition) -> str:
        """Generate python definition for class cls"""

        parentref = f'({self.formatted_element_name(cls.is_a, True) if cls.is_a else "YAMLRoot"})'
        slotdefs = self.gen_class_variables(cls)
        postinits = self.gen_postinits(cls)
        constructor = self.gen_constructor(cls)

        wrapped_description = (
            f'\n\t"""\n\t{wrapped_annotation(be(cls.description))}\n\t"""' if be(cls.description) else ""
        )

        if self.is_class_unconstrained(cls):
            return f"\n{self.class_or_type_name(cls.name)} = Any"

        cd_str = (
            ("\n@dataclass" if slotdefs else "")
            + f"\nclass {self.class_or_type_name(cls.name)}{parentref}:{wrapped_description}"
            + f"{self.gen_inherited_slots(cls)}"
            + f"{self.gen_class_meta(cls)}"
            + (f"\n\t{slotdefs}" if slotdefs else "")
            + (f"\n{postinits}" if postinits else "")
            + (f"\n{constructor}" if constructor else "")
        )

        return cd_str

    def gen_inherited_slots(self, cls: ClassDefinition) -> str:
        if not self.gen_classvars:
            return ""
        inherited_slots = []
        for slotname in cls.slots:
            slot = self.schema.slots[slotname]
            if slot.inherited:
                inherited_slots.append(slot.alias if slot.alias else slotname)
        inherited_slots_str = ", ".join([f'"{underscore(s)}"' for s in inherited_slots])
        return f"\n\t_inherited_slots: ClassVar[List[str]] = [{inherited_slots_str}]\n"

    def gen_class_meta(self, cls: ClassDefinition) -> str:
        if not self.gen_classvars:
            return ""
        class_class_uri = self.namespaces.uri_for(cls.class_uri)
        if class_class_uri:
            cls_python_uri = self.namespaces.curie_for(class_class_uri, default_ok=False, pythonform=True)
            class_class_curie = self.namespaces.curie_for(class_class_uri, default_ok=False, pythonform=False)
        else:
            cls_python_uri = None
            class_class_curie = None
        if class_class_curie:
            class_class_curie = f'"{class_class_curie}"'
        class_class_uri = cls_python_uri if cls_python_uri else f'URIRef("{class_class_uri}")'
        class_model_uri = self.namespaces.uri_or_curie_for(
            self.schema.default_prefix or "DEFAULT_", camelcase(cls.name)
        )
        if ":/" in class_model_uri:
            class_model_uri = f'URIRef("{class_model_uri}")'
        else:
            ns, ln = class_model_uri.split(":", 1)
            class_model_uri = f"{ns.upper()}.{ln}"

        vars = [
            f"class_class_uri: ClassVar[URIRef] = {class_class_uri}",
            f"class_class_curie: ClassVar[str] = {class_class_curie}",
            f'class_name: ClassVar[str] = "{cls.name}"',
            f"class_model_uri: ClassVar[URIRef] = {class_model_uri}",
        ]
        return "\n\t" + "\n\t".join(vars) + "\n"

    def gen_type_meta(self, typ: TypeDefinition) -> str:
        type_class_uri = self.namespaces.uri_for(typ.uri)
        if type_class_uri:
            type_python_uri = self.namespaces.curie_for(type_class_uri, default_ok=False, pythonform=True)
            type_class_curie = self.namespaces.curie_for(type_class_uri, default_ok=False, pythonform=False)
        else:
            type_python_uri = None
            type_class_curie = None
        if type_class_curie:
            type_class_curie = f'"{type_class_curie}"'
        type_class_uri = type_python_uri if type_python_uri else f'URIRef("{type_class_uri}")'
        type_model_uri = self.namespaces.uri_or_curie_for(self.schema.default_prefix, camelcase(typ.name))
        if ":/" in type_model_uri:
            type_model_uri = f'URIRef("{type_model_uri}")'
        else:
            ns, ln = type_model_uri.split(":", 1)
            ln_suffix = f".{ln}" if ln.isidentifier() else f'["{ln}"]'
            type_model_uri = f"{ns.upper()}{ln_suffix}"
        type_meta = [
            f"type_class_uri = {type_class_uri}",
            f"type_class_curie = {type_class_curie}",
            f'type_name = "{typ.name}"',
            f"type_model_uri = {type_model_uri}",
        ]
        return "\n\t".join(type_meta)

    def gen_class_variables(self, cls: ClassDefinition) -> str:
        """
        Generate the variable declarations for a dataclass.

        :param cls: class containing variables to be rendered in inheritance hierarchy
        :return: variable declarations for target class and its ancestors
        """
        initializers = []

        is_root = not cls.is_a
        domain_slots = self.domain_slots(cls)

        # Root keys and identifiers go first.  Note that even if a key or identifier is overridden it still
        # appears at the top of the list, as we need to keep the position
        slot_variables = self._slot_iter(
            cls,
            lambda slot: (slot.identifier or slot.key) and not slot.ifabsent,
            first_hit_only=True,
        )
        initializers += [self.gen_class_variable(cls, slot, not is_root) for slot in slot_variables]

        # Required slots
        slot_variables = self._slot_iter(
            cls,
            lambda slot: slot.required and not slot.identifier and not slot.key and not slot.ifabsent,
        )
        initializers += [self.gen_class_variable(cls, slot, not is_root) for slot in slot_variables]

        # Required or key slots with default values
        slot_variables = self._slot_iter(cls, lambda slot: slot.ifabsent and slot.required)
        initializers += [self.gen_class_variable(cls, slot, False) for slot in slot_variables]

        # Followed by everything else

        slot_variables = self._slot_iter(cls, lambda slot: not slot.required and slot in domain_slots)
        initializers += [self.gen_class_variable(cls, slot, False) for slot in slot_variables]

        return "\n\t".join(initializers)

    def gen_class_variable(self, cls: ClassDefinition, slot: SlotDefinition, can_be_positional: bool) -> str:
        """
        Generate a class variable declaration for the supplied slot.  Note: the can_be_positional attribute works,
        but it makes tag/value lists unduly complex, as you can't load them with tag=..., value=... -- you HAVE
        to load positionally. We currently ignore this parameter, meaning that we have a tag/value option for
        any LinkML element

        :param cls: Owning class
        :param slot: slot definition
        :param can_be_positional: True means that positional parameters are allowed.
        :return: Initializer string
        """
        can_be_positional = False  # Force everything to be tag values
        slotname = self.slot_name(slot.name)
        slot_range, default_val = self.range_cardinality(slot, cls, can_be_positional)
        ifabsent_text = (
            ifabsent_value_declaration(slot.ifabsent, self, cls, slot) if slot.ifabsent is not None else None
        )
        if ifabsent_text is not None:
            default = f"= {ifabsent_text}"
        else:
            default = f"= {default_val}" if default_val else ""
        return f"""{slotname}: {slot_range} {default}"""

    def range_cardinality(
        self,
        slot: SlotDefinition,
        cls: Optional[ClassDefinition],
        positional_allowed: bool,
    ) -> Tuple[str, Optional[str]]:
        """
        Return the range type including initializers, etc.
        Generate a class variable declaration for the supplied slot.  Note: the positional_allowed attribute works,
        but it makes tag/value lists unduly complex, as you can't load them with tag=..., value=... -- you HAVE
        to load positionally. We currently ignore this parameter, meaning that we have a tag/value option for
        any LinkML element

        :param slot: slot to generate type for
        :param cls: containing class -- used to render key slots correctly.  If absent, slot is an add-in
        :param positional_allowed: True Means that we are in the positional space and defaults are not supplied
        :return: python property name and initializer (if any)
        """
        positional_allowed = False  # Force everything to be tag values

        range_type, parent_type, _ = self.class_reference_type(slot, cls)
        pkey = self.class_identifier(slot.range)
        # Special case, inlined, identified range
        if pkey and slot.inlined and slot.multivalued:
            base_key = self.gen_class_reference(self.class_identifier_path(slot.range, False))
            num_elements = len(self.schema.classes[slot.range].slots)
            dflt = None if slot.required and positional_allowed else "empty_dict()"
            if num_elements == 1:
                if slot.required:
                    return (
                        f"Union[List[{base_key}], Dict[{base_key}, {range_type}]]",
                        dflt,
                    )
                else:
                    return (
                        f"Optional[Union[List[{base_key}], Dict[{base_key}, {range_type}]]]",
                        dflt,
                    )
            else:
                if slot.required:
                    return (
                        f"Union[Dict[{base_key}, {range_type}], List[{range_type}]]",
                        dflt,
                    )
                else:
                    return (
                        f"Optional[Union[Dict[{base_key}, {range_type}], List[{range_type}]]]",
                        dflt,
                    )

        # All other cases
        if slot.multivalued:
            if slot.required:
                return f"Union[{range_type}, List[{range_type}]]", (None if positional_allowed else "None")
            else:
                return (
                    f"Optional[Union[{range_type}, List[{range_type}]]]",
                    "empty_list()",
                )
        elif slot.required:
            return range_type, (None if positional_allowed else "None")
        else:
            return f"Optional[{range_type}]", "None"

    def class_reference_type(self, slot: SlotDefinition, cls: Optional[ClassDefinition]) -> Tuple[str, str, str]:
        """
        Return the type of slot referencing a class

        :param slot: slot to be typed
        :param cls: owning class.  Used for generating key references
        :return: Python class reference type, most proximal type, most proximal type name
        """
        rangelist = (
            self.class_identifier_path(cls, False) if slot.key or slot.identifier else self.slot_range_path(slot)
        )
        prox_type = self.slot_range_path(slot)[-1].rsplit(".")[-1]
        prox_type_name = rangelist[-1]

        # Quote forward references - note that enums always gen at the end
        if slot.range in self.schema.enums or (
            cls and slot.inlined and slot.range in self.schema.classes and self.forward_reference(slot.range, cls.name)
        ):
            rangelist[-1] = f'"{rangelist[-1]}"'
        return str(self.gen_class_reference(rangelist)), prox_type, prox_type_name

    @staticmethod
    def gen_class_reference(rangelist: List[str]) -> str:
        """
        Return a basic or a union type depending on the number of elements in range list

        :param rangelist: List of types from distal to proximal
        :return:
        """
        base = rangelist[0].rsplit(".")[-1]
        return f"Union[{base}, {rangelist[-1]}]" if len(rangelist) > 1 else base

    def gen_postinits(self, cls: ClassDefinition) -> str:
        """Generate all the typing and existence checks post initialize"""
        post_inits_pre_super = []
        for slot in self.domain_slots(cls):
            if slot.ifabsent:
                dflt = ifabsent_postinit_declaration(slot.ifabsent, self, cls, slot)

                if dflt and dflt != "None":
                    post_inits_pre_super.append(f"if self.{self.slot_name(slot.name)} is None:")
                    post_inits_pre_super.append(f"\tself.{self.slot_name(slot.name)} = {dflt}")

        post_inits = []
        if not (cls.mixin or cls.abstract):
            pkeys = self.primary_keys_for(cls)
            for pkey in pkeys:
                slot = self.schema.slots[pkey]
                # TODO: Remove the bypass whenever we get default_range fixed
                if not slot.ifabsent or True:
                    post_inits.append(self.gen_postinit(cls, slot))
        else:
            pkeys = []
        for slot in self.domain_slots(cls):
            if slot.required:
                # TODO: Remove the bypass whenever we get default_range fixed
                if slot.name not in pkeys and (not slot.ifabsent or True):
                    post_inits.append(self.gen_postinit(cls, slot))
        for slot in self.domain_slots(cls):
            if not slot.required:
                # TODO: Remove the bypass whenever we get default_range fixed
                if slot.name not in pkeys and (not slot.ifabsent or True):
                    post_inits.append(self.gen_postinit(cls, slot))
        post_inits_designators = []

        domain_slot_names = [s.name for s in self.domain_slots(cls)]
        for slot in self.schemaview.class_induced_slots(cls.name):
            # This is for all type designators that were defined at a parent class
            # We need to treat them specially: the initialisation should come
            # AFTER the call to super() because we want to override the super behaviour
            if slot.name not in domain_slot_names and slot.designates_type:
                post_inits_designators.append(self.gen_postinit(cls, slot))

        post_inits_pre_super_line = "\n\t\t".join([p for p in post_inits_pre_super if p]) + (
            "\n\t\t" if post_inits_pre_super else ""
        )
        post_inits_post_super_line = "\n\t\t".join(post_inits_designators)
        post_inits_line = "\n\t\t".join([p for p in post_inits if p])
        return (
            (
                f"""
    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        {post_inits_pre_super_line}{post_inits_line}
        super().__post_init__(**kwargs)
        {post_inits_post_super_line}"""
            )
            if post_inits_line or post_inits_pre_super_line or post_inits_post_super_line
            else ""
        )

    # sort classes such that if C is a child of P then C appears after P in the list
    @staticmethod
    def _sort_classes(clist: List[ClassDefinition]) -> List[ClassDefinition]:
        clist = list(clist)
        slist = []  # sorted
        while len(clist) > 0:
            for i in range(len(clist)):
                candidate = clist[i]
                can_add = False
                if candidate.is_a is None:
                    can_add = True
                else:
                    if candidate.is_a in [p.name for p in slist]:
                        can_add = True
                if can_add:
                    slist = slist + [candidate]
                    del clist[i]
                    break
            if not can_add:
                raise (f"could not find suitable element in {clist} that does not ref {slist}")
        return slist

    def is_key_value_class(self, range_name: DefinitionName) -> bool:
        """
        Return True if range_name references a class with exactly one key and one value

        :param range_name: class definition (name)
        :return: True if meets the special case
        """
        rng = self.schema.classes.get(range_name)
        if rng:
            pkeys = self.primary_keys_for(rng)
            if pkeys:
                return len(rng.slots) - len(pkeys) == 1
        return False

    def _roll_up_type(self, typ_name: str) -> str:
        if typ_name in self.schemaview.all_types():
            t = self.schemaview.get_type(typ_name)
            if t.typeof:
                return self._roll_up_type(t.typeof)
        return typ_name

    def gen_constructor(self, cls: ClassDefinition) -> Optional[str]:
        """
        Generate python constructor for class

        :param cls: class to generate constructor for
        :return: python constructor
        """
        rlines: List[str] = []
        designators = [x for x in self.domain_slots(cls) if x.designates_type]
        if len(designators) > 0:
            descendants = self.schemaview.class_descendants(cls.name)
            if len(descendants) > 1:
                slot = designators[0]
                aliased_slot_name = self.slot_name(slot.name)
                slot_range = self._roll_up_type(slot.range)

                rlines.append("def __new__(cls, *args, **kwargs):")
                td_val_expression = "kwargs[type_designator]"
                if slot_range == "string":
                    lookup_by_props = ["class_name"]
                elif slot_range == "uri":
                    lookup_by_props = ["class_class_uri", "class_model_uri"]
                    td_val_expression = (
                        f"URIRef({td_val_expression}) if "
                        f"isinstance({td_val_expression}, str) else {td_val_expression}"
                    )
                elif slot_range == "uriorcurie":
                    lookup_by_props = ["class_class_curie", "class_class_uri", "class_model_uri"]
                else:
                    raise ValueError(f"Unsupported type designator range: {slot.range}")
                rlines.append(
                    f"""
        type_designator = "{aliased_slot_name}"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = {td_val_expression}
            target_cls = cls._class_for("{lookup_by_props[0]}", type_designator_value)
"""
                )
                for prop in lookup_by_props[1:]:
                    rlines.append(
                        f"""
            if target_cls is None:
                target_cls = cls._class_for("{prop}", type_designator_value)
"""
                    )
                rlines.append(
                    f"""
            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {{cls.__name__}} "
                                 f"has no subclass with {lookup_by_props}='{{kwargs[type_designator]}}'")
            return super().__new__(target_cls,*args,**kwargs)
"""
                )

        if rlines and copy(rlines[-1]).strip() != "":
            rlines.append("")
        return ("\n\t" if len(rlines) > 0 else "") + "\n\t".join(rlines)

    def gen_postinit(self, cls: ClassDefinition, slot: SlotDefinition) -> Optional[str]:
        """Generate python post init rules for slot in class"""
        rlines: List[str] = []

        if slot.range in self.schema.classes:
            if self.is_class_unconstrained(self.schema.classes[slot.range]):
                return ""

        if slot.range in self.schema.enums:
            # Open enum
            if not self.schema.enums[slot.range].permissible_values:
                return ""

        aliased_slot_name = self.slot_name(slot.name)  # Mangled name by which the slot is known in python
        _, _, base_type_name = self.class_reference_type(slot, cls)

        # Generate existence check for required slots.  Note that inherited classes have to do post init checks because
        # You can't have required elements after optional elements in the parent class
        if slot.required:
            rlines.append(f"if self._is_empty(self.{aliased_slot_name}):")
            rlines.append(f'\tself.MissingRequiredField("{aliased_slot_name}")')

        # Generate the type co-ercion for the various types.
        # NOTE: if you set this to true, we will cast all types.   This may be what we really want
        if not slot.multivalued:
            if slot.designates_type:
                pass
            elif slot.required:
                rlines.append(f"if not isinstance(self.{aliased_slot_name}, {base_type_name}):")
            else:
                rlines.append(
                    f"if self.{aliased_slot_name} is not None and "
                    f"not isinstance(self.{aliased_slot_name}, {base_type_name}):"
                )
            if slot.designates_type:
                slot_range = self._roll_up_type(slot.range)
                if slot_range == "string":
                    td_value_classvar = "class_name"
                elif slot_range == "uri":
                    td_value_classvar = "class_model_uri"
                elif slot_range == "uriorcurie":
                    td_value_classvar = "class_class_curie"
                else:
                    raise ValueError(f"Unsupported type designator range: {slot_range}")
                rlines.append(f"self.{aliased_slot_name} = str(self.{td_value_classvar})")
            elif (
                # A really weird case -- a class that has no properties
                slot.range in self.schema.classes
                and not self.schema.classes[slot.range].slots
            ):
                rlines.append(f"\tself.{aliased_slot_name} = {base_type_name}()")
            else:
                if (
                    (self.class_identifier(slot.range) and not slot.inlined)
                    or slot.range in self.schema.types
                    or slot.range in self.schema.enums
                ):
                    rlines.append(f"\tself.{aliased_slot_name} = {base_type_name}(self.{aliased_slot_name})")
                else:
                    rlines.append(f"\tself.{aliased_slot_name} = {base_type_name}(**as_dict(self.{aliased_slot_name}))")
        elif slot.inlined:
            slot_range_cls = self.schema.classes[slot.range]
            identifier = self.class_identifier(slot_range_cls)
            # If we don't have an identifier, and we are expecting to be inlined first class elements
            # (inlined_as_list is not True), we will use the first required field as the key.
            #  Note that this may not always work, but the workaround is straight forward -- set inlined_as_list to
            #  True
            if not identifier and not slot.inlined_as_list:
                for range_slot_name in slot_range_cls.slots:
                    range_slot = self.schema.slots[range_slot_name]
                    if range_slot.required:
                        identifier = range_slot.name
                        break
                keyed = False
            else:
                # Place for future expansion
                keyed = True
            if identifier:
                if not slot.inlined_as_list:
                    rlines.append(
                        f'self._normalize_inlined_as_dict(slot_name="{aliased_slot_name}", '
                        f"slot_type={base_type_name}, "
                        f'key_name="{self.aliased_slot_name(identifier)}", '
                        f"keyed={keyed})"
                    )
                else:
                    rlines.append(
                        f'self._normalize_inlined_as_list(slot_name="{aliased_slot_name}", '
                        f"slot_type={base_type_name}, "
                        f'key_name="{self.aliased_slot_name(identifier)}", '
                        f"keyed={keyed})"
                    )
            else:
                # Multivalued, inlined and no identifier
                # TODO: JsonObj([...]) will not be treated correctly here.
                sn = f"self.{aliased_slot_name}"
                rlines.append(f"if not isinstance({sn}, list):")
                rlines.append(f"\t{sn} = [{sn}] if {sn} is not None else []")
                rlines.append(
                    f"{sn} = [v if isinstance(v, {base_type_name}) else {base_type_name}(**as_dict(v)) for v in {sn}]"
                )
        else:
            # Multivalued and not inlined
            # TODO: JsonObj([...]) will fail here as well
            sn = f"self.{aliased_slot_name}"
            rlines.append(f"if not isinstance({sn}, list):")
            rlines.append(f"\t{sn} = [{sn}] if {sn} is not None else []")
            rlines.append(f"{sn} = [v if isinstance(v, {base_type_name}) " f"else {base_type_name}(v) for v in {sn}]")
        while rlines and copy(rlines[-1]).strip() == "":
            rlines.pop()
        rlines.append("")
        return "\n\t\t".join(rlines)

    def _slot_iter(
        self,
        cls: ClassDefinition,
        test: Callable[[SlotDefinition], bool],
        first_hit_only: bool = False,
    ) -> Iterator[SlotDefinition]:
        """Return the representation for the set of own slots in cls that pass test

        :param cls: Class containing a set of slots
        :param test: Slot test function
        :param first_hit_only: True means stop on first match.  False means generate all
        :return: Set of slots that match
        """
        for slot in self.all_slots(cls):
            if test(slot):
                yield slot
                if first_hit_only:
                    break

    def primary_keys_for(self, cls: ClassDefinition) -> List[SlotDefinitionName]:
        """Return the primary key for cls.

        Note: At the moment we return at most one entry.  At some point, keys will be expanded to support
              composite keys.

        @param cls: class to get keys for
        @return: List of primary keys or identifiers
        """
        return [
            slot_name
            for slot_name in cls.slots
            if self.schema.slots[slot_name].key or self.schema.slots[slot_name].identifier
        ]

    def key_name_for(self, class_name: ClassDefinitionName) -> Optional[str]:
        for slot_name in self.primary_keys_for(self.schema.classes[class_name]):
            return self.formatted_element_name(class_name, True) + camelcase(slot_name)
        return None

    def range_type_name(self, slot: SlotDefinition) -> str:
        """Generate the type name for the slot"""
        cidpath = self.slot_range_path(slot)
        if len(cidpath) < 2:
            return cidpath[0]
        else:
            return f"Union[{cidpath[0]}, {cidpath[-1]}]"

    def forward_reference(self, slot_range: str, owning_class: str) -> bool:
        """Determine whether slot_range is a forward reference"""
        # logging.info(f"CHECKING: {slot_range} {owning_class}")
        if (slot_range in self.schema.classes and self.schema.classes[slot_range].imported_from) or (
            slot_range in self.schema.enums and self.schema.enums[slot_range].imported_from
        ):
            logging.info(
                f"FALSE: FORWARD: {slot_range} {owning_class} // IMP={self.schema.classes[slot_range].imported_from}"
            )
            return False
        if slot_range in self.schema.enums:
            return True
        clist = [x.name for x in self._sort_classes(self.schema.classes.values())]
        for cname in clist:
            if cname == owning_class:
                logging.info(f"TRUE: OCCURS SAME: {cname} == {slot_range} owning: {owning_class}")
                return True  # Occurs on or after
            elif cname == slot_range:
                logging.info(f"FALSE: OCCURS BEFORE: {cname} == {slot_range} owning: {owning_class}")
                return False  # Occurs before
        return True

    def python_uri_for(self, uriorcurie: Union[str, URIRef]) -> Tuple[str, Optional[str]]:
        """Return the python form of uriorcurie
        :param uriorcurie:
        :return: URI and CURIE form
        """
        ns, ln = self.namespaces.prefix_suffix(uriorcurie)
        if ns == "":
            ns = "DEFAULT_"
        if ns is None:
            return '"str(uriorcurie)"', None
        return (
            ns.upper() + (f".{ln}" if ln.isidentifier() else f"['{ln}']"),
            ns.upper() + f".curie('{ln}')",
        )

    def gen_slotdefs(self) -> str:
        if self.gen_slots:
            return "class slots:\n\tpass\n\n" + "\n\n".join(
                [self.gen_slot(slot) for slot in self.schema.slots.values() if not slot.imported_from]
            )
        else:
            return ""

    def gen_slot(self, slot: SlotDefinition) -> str:
        python_slot_name = underscore(slot.name)
        slot_uri, slot_curie = self.python_uri_for(slot.slot_uri)
        slot_model_uri, slot_model_curie = self.python_uri_for(
            self.namespaces.uri_or_curie_for(self.schema.default_prefix, python_slot_name)
        )
        domain = camelcase(slot.domain) if slot.domain and not self.schema.classes[slot.domain].mixin else "None"
        # Going to omit the range on keys where the domain isn't specified (for now)
        if slot.domain is None and (slot.key or slot.identifier):
            rnge = "URIRef"
        else:
            rnge, _ = self.range_cardinality(slot, self.schema.classes[slot.domain] if slot.domain else None, True)
        if slot.mappings:
            map_texts = [
                self.namespaces.curie_for(self.namespaces.uri_for(m), default_ok=True, pythonform=True)
                for m in slot.mappings
                if m != slot.slot_uri
            ]
        else:
            map_texts = []
        if map_texts:
            mappings = ", mappings = [" + ", ".join(map_texts) + "]"
        else:
            mappings = ""
        pattern = f",\n                   pattern=re.compile(r'{slot.pattern}')" if slot.pattern else ""
        return f"""slots.{python_slot_name} = Slot(uri={slot_uri}, name="{slot.name}", curie={slot_curie},
                   model_uri={slot_model_uri}, domain={domain}, range={rnge}{mappings}{pattern})"""

    def gen_enumerations(self) -> str:
        return "\n\n".join([self.gen_enum(enum) for enum in self.schema.enums.values() if not enum.imported_from])

    def gen_enum(self, enum: EnumDefinition) -> str:
        """
        Generate an enum class
        @param enum: EnumDefinition object to be converted into code
        @return: python code string
        """
        enum_name = camelcase(enum.name)
        return f"""
class {enum_name}(EnumDefinitionImpl):
    {self.gen_enum_comment(enum)}
    {self.gen_enum_description(enum, enum_name)}
""".strip()

    @staticmethod
    def gen_enum_comment(enum: EnumDefinition) -> str:
        if not be(enum.description):
            return ""
        desc_text = enum.description.replace('"""', "---")
        return f'"""\n\t{wrapped_annotation(be(desc_text))}\n\t"""'

    def gen_enum_description(self, enum: EnumDefinition, enum_name: str) -> str:
        return f"""
    {self.gen_pvs(enum)}

    {self.gen_enum_definition(enum, enum_name)}
    {self.gen_pvs_as_setattrs(enum)}
""".strip()

    def gen_enum_definition(self, enum: EnumDefinition, enum_name: str) -> str:
        enum_desc = self.process_multiline_string(enum.description, "\t\tdescription=") if enum.description else None
        desc = f"{enum_desc},\n" if enum.description else ""
        enum_code_set = (
            self.namespaces.curie_for(self.namespaces.uri_for(enum.code_set), default_ok=False, pythonform=True)
            if enum.code_set
            else None
        )
        cs = f"\t\tcode_set={enum_code_set},\n" if enum_code_set else ""
        tag = f'\t\tcode_set_tag="{enum.code_set_tag}",\n' if enum.code_set_tag else ""
        ver = f'\t\tcode_set_version="{enum.code_set_version}",\n' if enum.code_set_version else ""
        vf = f"\t\tpv_formula=PvFormulaOptions.{enum.pv_formula.code.text},\n" if enum.pv_formula else ""

        return f"""_defn = EnumDefinition(\n\t\tname="{enum_name}",\n{desc}{cs}{tag}{ver}{vf}\t)"""

    def gen_pvs(self, enum: EnumDefinition) -> str:
        """
        Generate the python compliant permissible value initializers as a set of class variables
        @param enum: EnumDefinition object to be converted into class variables
        @return: string containing the enum declaration
        """
        init_list = []
        for pv in enum.permissible_values.values():
            if str.isidentifier(pv.text) and not keyword.iskeyword(pv.text):
                init_list.append(f"{pv.text} = " + self.gen_pv_constructor(pv, 4))

        return "\n\t".join(init_list).strip()

    def gen_pvs_as_setattrs(self, enum: EnumDefinition) -> str:
        """
        Generate the non-python compliant permissible value initializers as a set of setattr instructions
        in the form

        @classmethod
        def _addvals(cls):
            setattr(cls, "NAME",
                PermissibleValue(
                    text="NAME",
                    description="description here"))

        @param enum: EnumDefinition object to be converted into code
        @return: string containing the enum declaration
        """
        if any(not str.isidentifier(pv.text) or keyword.iskeyword(pv.text) for pv in enum.permissible_values.values()):
            init_list = []
            for pv in enum.permissible_values.values():
                if not str.isidentifier(pv.text) or keyword.iskeyword(pv.text):
                    # first line is "        setattr("
                    indent = 12
                    indent_str = indent * " "
                    pv_text = pv.text.replace('"', '\\"').replace(r"\n", r"\\n")
                    pv_parts = self.gen_pv_constructor(pv, indent)
                    init_list.append(f'        setattr(cls, "{pv_text}",\n{indent_str}{pv_parts})')

            add_vals_text = "\n".join(init_list).rstrip()

            return f"""
    @classmethod
    def _addvals(cls):
{add_vals_text}
"""

        return ""

    def gen_pv_constructor(self, pv: PermissibleValue, indent: int) -> str:
        """
        Generate a permissible value constructor in the form

        PermissibleValue(text="NAME_ONLY")
        PermissibleValue(
            text="CODE",
            description="...",
            meaning="...")

        @param pv: Value to be constructed
        @param indent: number of additional spaces to add on successive lines
        @return: Permissible value constructor
        """
        constructor = "PermissibleValue"
        pv_text = pv.text.replace('"', '\\"')

        if not pv.description and not pv.meaning:
            return f'{constructor}(text="{pv_text}")'

        indent_str = (4 + indent) * " "
        pv_attrs = [f'{indent_str}text="{pv_text}"']
        if pv.description:
            pv_attrs.append(f'{self.process_multiline_string(pv.description, f"{indent_str}description=")}')
        if pv.meaning:
            pv_meaning = self.namespaces.curie_for(
                self.namespaces.uri_for(pv.meaning), default_ok=False, pythonform=True
            )
            pv_attrs.append(f"{indent_str}meaning={pv_meaning}")

        return "PermissibleValue(\n" + ",\n".join(pv_attrs) + ")"

    @staticmethod
    def process_multiline_string(input: str, prefix_string: str) -> str:
        """
        Process a (potentially multi-line) string, preserving existing formatting

        @param input: input string to be formatted
        @param prefix_string: the text to prefix the first line of the output
        @return: formatted string
        """
        string = input.rstrip().replace('"', '\\"')
        if len(prefix_string + string) < split_col and input.find("\n") == -1:
            return f'{prefix_string}"{string}"'

        return f'{prefix_string}"""{string}"""'

    def _default_curie_or_uri(self) -> str:
        dflt = self.schema.default_prefix if self.schema.default_prefix else sfx(self.schema.id)
        if ":/" in dflt:
            prefix = self.namespaces.prefix_for(self.schema.default_prefix)
            if prefix:
                dflt = prefix
        return dflt


@shared_arguments(PythonGenerator)
@click.command()
@click.option("--head/--no-head", default=True, show_default=True, help="Emit metadata heading")
@click.option(
    "--genmeta/--no-genmeta",
    default=False,
    show_default=True,
    help="Generating metamodel. Only use this for generating meta.py",
)
@click.option(
    "--classvars/--no-classvars",
    default=True,
    show_default=True,
    help="Generate CLASSVAR info",
)
@click.option(
    "--slots/--no-slots",
    default=True,
    show_default=True,
    help="Generate Slot information",
)
@click.option(
    "--validate/--no-validate",
    default=False,
    show_default=True,
    help="Validate generated code by compiling it",
)
@click.version_option(__version__, "-V", "--version")
def cli(
    yamlfile,
    head=True,
    genmeta=False,
    classvars=True,
    slots=True,
    validate=False,
    **args,
):
    """Generate python classes to represent a LinkML model"""
    gen = PythonGenerator(
        yamlfile,
        emit_metadata=head,
        genmeta=genmeta,
        gen_classvars=classvars,
        gen_slots=slots,
        **args,
    )
    if validate:
        mod = gen.compile_module()
        logging.info(f"Module {mod} compiled successfully")
    print(gen.serialize(emit_metadata=head, **args))


if __name__ == "__main__":
    cli()
