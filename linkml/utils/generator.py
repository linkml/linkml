"""
Base class for all generators

Developer Notes
---------------

Subclasses of this class implement specific generators. Each generator is in one of two styles:

1. schemaloader-based, using a Visitor pattern (older)
2. schemaview-based, no visitor pattern (newer)

New generators should always using the latter approach

See: https://github.com/linkml/linkml/issues/923

"""
import abc
import logging
import os
import re
import sys
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import (Callable, Dict, List, Optional, Set, TextIO, Type, Union,
                    cast, Mapping, ClassVar)

import click
from click import Argument, Command, Option
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model.linkml_files import LOCAL_BASE
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              ClassDefinitionName, Definition,
                                              Element, ElementName,
                                              EnumDefinition,
                                              EnumDefinitionName,
                                              PrefixPrefixPrefix,
                                              SchemaDefinition, SlotDefinition,
                                              SlotDefinitionName,
                                              SubsetDefinition,
                                              SubsetDefinitionName,
                                              TypeDefinition,
                                              TypeDefinitionName)
import linkml_runtime.linkml_model.meta as metamodel
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.namespaces import Namespaces

from linkml import LOCAL_METAMODEL_YAML_FILE, META_BASE_URI, METAMODEL_YAML_URI
from linkml.utils.mergeutils import alias_root
from linkml.utils.schemaloader import SchemaLoader
from linkml.utils.typereferences import References

DEFAULT_LOG_LEVEL: str = "WARNING"
DEFAULT_LOG_LEVEL_INT: int = logging.WARNING


@dataclass
class Generator(metaclass=abc.ABCMeta):
    """
    Base class for generators

    For usage `Generator Docs <https://linkml.io/linkml/generators/>`_
    """

    # ClassVars
    schema: Union[str, TextIO, SchemaDefinition, "Generator"]
    """metamodel compliant schema.  Can be URI, file name, actual schema, another generator, an
        open file or a pre-parsed schema"""

    generatorname: ClassVar[str] = None
    """ Name of the generator. Override with os.path.basename(__file__)"""

    generatorversion: ClassVar[str] = None  # Generator version identifier
    """Version of the generator. Consider deprecating and instead use overall linkml version"""

    uses_schemaloader: ClassVar[bool] = True
    """Old-style generator that uses the SchemaLoader and visitor pattern"""

    #uses_schemaview: ClassVar[bool] = True
    #"""New-style generator that uses SchemaView"""

    requires_metamodel: ClassVar[bool] = True
    """Generator queries an instance of the metamodel"""

    valid_formats: ClassVar[List[str]] = []
    """Allowed formats - first format is default"""

    visit_all_class_slots: ClassVar[bool] = False
    """Visitor ClassVar: False means only visit own slots, True means visit all slots"""

    visits_are_sorted: ClassVar[bool] = True
    """Visitor ClassVar: True means visit basic types in alphabetial order, false in entry"""

    sort_class_slots: ClassVar[bool] = False
    """Visitor ClassVar: True means visit class slots in alphabetical order"""

    # Object-level Vars
    schemaview: Optional[SchemaView] = None
    """A wrapper onto the schema object"""

    format: Optional[str] = None
    """expected output format"""

    metadata: bool = field(default_factory= lambda: True)
    """True means include date, generator, etc. information in source header if appropriate"""

    useuris: Optional[bool] = None
    """True means declared class slot uri's are used.  False means use model uris"""

    log_level: int = DEFAULT_LOG_LEVEL_INT
    """Logging level, 0 is minimum"""

    mergeimports: Optional[bool] = field(default_factory= lambda: True)
    """True means merge non-linkml sources into importing package.  False means separate packages"""

    source_file_date: Optional[str] = None
    """Modification date of input source file"""

    source_file_size: Optional[int] = None
    """Size of the source file in bytes"""

    logger: Optional[logging.Logger] = None
    """Logger to use for logging messages"""

    verbose: Optional[bool] = None
    """Verbosity"""

    output: Optional[str] = None
    """Path to output file. Note all generators may not implement this uniformly, see https://github.com/linkml/linkml/issues/923"""

    namespaces: Optional[Namespaces] = None
    """All prefix expansions used"""

    directory_output: bool = False
    """True means output is to a directory, False is to stdout"""

    base_dir: str = None  # Base directory of schema
    """Working directory or base URL of sources"""

    metamodel_name_map: Dict[
        str, str
    ] = None
    """Allows mapping of names of metamodel elements such as slot, etc"""

    importmap: Optional[Union[str, Optional[Mapping[str, str]]]] = None
    """File name of import mapping file -- maps import name/uri to target"""

    emit_prefixes: Set[str] = field(default_factory=lambda: set())
    """Prefixes to emit, for RDF-based generators"""

    metamodel: SchemaLoader = None
    """A SchemaLoader instance that points to the LinkML metamodel (meta.yaml)"""

    stacktrace: bool = False
    """True means print stack trace, false just error message"""

    def __post_init__(self) -> None:
        if not self.logger:
            self.logger = logging.getLogger()
        #    logging.basicConfig()
        #    self.logger = logging.getLogger(self.__class__.__name__)
        #    self.logger.setLevel(log_level)
        if not self.stacktrace:
            sys.tracebacklimit = 0
        if self.format is None:
            self.format = self.valid_formats[0]
        if self.format not in self.valid_formats:
            raise ValueError(f"Unrecognized format: {format}; known={self.valid_formats}")
        # legacy: all generators should use "mergeimports"
        # self.merge_imports = self.mergeimports
        if not self.metadata:
            self.source_file_date = None
            self.source_file_size = None
        if self.requires_metamodel:
            if os.path.exists(LOCAL_METAMODEL_YAML_FILE):
                base_dir = str(Path(str(LOCAL_METAMODEL_YAML_FILE)).parent)
                logging.debug(f"BASE={base_dir}")
                self.metamodel = SchemaLoader(
                        LOCAL_METAMODEL_YAML_FILE,
                        importmap={"linkml": base_dir},
                        base_dir=base_dir,
                        mergeimports=self.mergeimports,
                    )
            else:
                raise AssertionError(f"{LOCAL_METAMODEL_YAML_FILE} not found")
            self.metamodel.resolve()
        schema = self.schema
        # TODO: remove aliasing
        self.emit_metadata = self.metadata
        if self.uses_schemaloader:
            self._initialize_using_schemaloader(schema)
        else:
            self.schemaview = SchemaView(schema)
            self.schema = self.schemaview.schema

    def _initialize_using_schemaloader(self, schema: Union[str, TextIO, SchemaDefinition, "Generator"]):
        # currently generators are very liberal in what they accept, including
        # other generators.
        # See https://github.com/linkml/linkml/issues/923 for discussion on how
        # to simplify the overall framework
        if isinstance(schema, Generator):
            logging.warning("Instantiating generator with another generator is deprecated")
            gen = schema
            self.schema = gen.schema
            self.synopsis = gen.synopsis
            self.loaded = gen.loaded
            self.namespaces = gen.namespaces
            self.base_dir = gen.base_dir
            self.importmap = gen.importmap
            self.source_file_data = gen.source_file_date
            self.source_file_size = gen.source_file_size
            self.schema_location = gen.schema_location
            self.schema_defaults = gen.schema_defaults
            self.logger = gen.logger
        else:
            if isinstance(schema, SchemaDefinition):
                # schemaloader based methods require schemas to have been created via SchemaLoader,
                # which prepopulates some fields (e.g definition_url). If the schema has not been processed through the
                # loader, then roundtrip
                if any(c for c in schema.classes.values() if not c.definition_uri):
                    schema = yaml_dumper.dumps(schema)
            loader = SchemaLoader(
                schema,
                self.base_dir,
                useuris=self.useuris,
                importmap=self.importmap,
                logger=self.logger,
                mergeimports=self.mergeimports,
                emit_metadata=self.metadata,
                source_file_date=self.source_file_date,
                source_file_size=self.source_file_size,
            )
            loader.resolve()
            self.schema = loader.schema
            self.synopsis = loader.synopsis
            self.loaded = loader.loaded
            self.namespaces = loader.namespaces
            self.base_dir = loader.base_dir
            self.importmap = loader.importmap
            self.source_file_data = loader.source_file_date
            self.source_file_size = loader.source_file_size
            self.schema_location = loader.schema_location
            self.schema_defaults = loader.schema_defaults
            if self.namespaces is None:
                self.namespaces = Namespaces()
                for prefix in self.schema.prefixes.values():
                    self.namespaces[prefix.prefix_prefix] = prefix.prefix_reference

    def serialize(self, **kwargs) -> str:
        """
        Generate output in the required format

        :param kwargs: Generater specific parameters
        :return: Generated output
        """
        output = StringIO()
        # Note: we currently redirect stdout, this means that print statements within
        # each generator will be redirected to the StringIO object.
        # See https://github.com/linkml/linkml/issues/923 for discussion on simplifying this
        with redirect_stdout(output):
            # the default is to use the Visitor Pattern; each individual generator may
            # choose to override methods {visit,end}_{element}.
            # See https://github.com/linkml/linkml/issues/923
            self.visit_schema(**kwargs)
            for sn, ss in (
                sorted(self.schema.subsets.items(), key=lambda s: s[0].lower())
                if self.visits_are_sorted
                else self.schema.subsets.items()
            ):
                self.visit_subset(ss)
            for tn, typ in (
                sorted(self.schema.types.items(), key=lambda s: s[0].lower())
                if self.visits_are_sorted
                else self.schema.types.items()
            ):
                self.visit_type(typ)
            for enum in (
                sorted(self.schema.enums.values(), key=lambda e: e.name.lower())
                if self.visits_are_sorted
                else self.schema.enums.values()
            ):
                self.visit_enum(enum)
            for sn, slot in (
                sorted(self.schema.slots.items(), key=lambda c: c[0].lower())
                if self.visits_are_sorted
                else self.schema.slots.items()
            ):
                self.visit_slot(self.aliased_slot_name(slot), slot)
            for cls in (
                sorted(self.schema.classes.values(), key=lambda c: c.name.lower())
                if self.visits_are_sorted
                else self.schema.classes.values()
            ):
                if self.visit_class(cls):
                    for slot in (
                        self.all_slots(cls)
                        if self.visit_all_class_slots
                        else self.own_slots(cls)
                    ):
                        self.visit_class_slot(cls, self.aliased_slot_name(slot), slot)
                    self.end_class(cls)
            self.end_schema(**kwargs)
        return output.getvalue()

    def visit_schema(self, **kwargs) -> None:
        """Visited once at the beginning of generation

        @param kwargs: Arguments passed through from CLI -- implementation dependent
        """
        ...

    def end_schema(self, **kwargs) -> None:
        """Visited once at the end of generation

        @param kwargs: Arguments passed through from CLI -- implementation dependent
        """
        ...

    def visit_class(self, cls: ClassDefinition) -> bool:
        """Visited once per schema class

        @param cls: class being visited
        @return: Visit slots and end class.  False means skip and go on
        """
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        """Visited after visit_class_slots (if visit_class returned true)

        @param cls: class being visited
        """
        ...

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        """Visited for each slot in a class.  If class level visit_all_slots is true, this is visited once
        for any class that is inherited (class itself, is_a, mixin, apply_to).  Otherwise just the own slots.

        @param cls: containing class
        @param aliased_slot_name: Aliased slot name.  May not be unique across all class slots
        @param slot: slot being visited
        """
        ...

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        """Visited once for every slot definition in the schema.

        @param aliased_slot_name: Aliased name of the slot.  May not be unique
        @param slot: visited slot
        """
        ...

    def visit_type(self, typ: TypeDefinition) -> None:
        """Visited once for every type definition in the schema

        @param typ: Type definition
        """
        ...

    def visit_subset(self, subset: SubsetDefinition) -> None:
        """Visited once for every subset definition in the schema

        #param subset: Subset definition
        """
        ...

    def visit_enum(self, enum: EnumDefinition) -> None:
        """Visited once for every enum definition in the schema

        @param enum: Enum definition
        """
        ...

    # =============================
    # Helper methods
    # =============================
    def own_slots(
        self, cls: Union[ClassDefinitionName, ClassDefinition]
    ) -> List[SlotDefinition]:
        """Return the list of slots owned the class definition.  An "own slot" is any ``cls`` slot that does not appear
        in the class is_a parent.  Own_slots include:

            * any slot whose domain is cls
            * slot_usage entries
            * slots from mixins entries
            * slots from apply_to entries


        @param cls: class name or class definition name
        @return: list of owned slots.  List is sorted if sort_class_slots is true, otherwise in class order
        """
        if not isinstance(cls, ClassDefinition):
            cls = self.schema.classes[cls]
        parent = self.schema.classes[cls.is_a] if cls.is_a else None
        seen = set()
        rval = []
        for sname in cls.slots:
            sname_base = alias_root(self.schema, sname)
            if sname_base not in seen and (not parent or sname not in parent.slots):
                slot = self.schema.slots[sname]
                rval.append(slot)
                seen.add(sname_base)
        return sorted(rval, key=lambda s: s.name) if self.sort_class_slots else rval

    def own_slot_names(
        self, cls: Union[ClassDefinitionName, ClassDefinition]
    ) -> List[SlotDefinitionName]:
        return [slot.name for slot in self.own_slots(cls)]

    def all_slots(
        self,
        cls: Union[ClassDefinitionName, ClassDefinition],
        *,
        cls_slots_first: bool = False,
        seen: Optional[Set[ClassDefinitionName]] = None,
    ) -> List[SlotDefinition]:
        """Return all slots that are part of the class definition.  This includes all is_a, mixin and apply_to slots
        but does NOT include slot_usage targets.  If class B has a slot_usage entry for slot "s", only the slot
        definition for the redefined slot will be included, not its base.  Slots are added in the order they appear
        in classes, with recursive is_a's being added first followed by mixins and finally apply_tos

        @param cls: class definition or class definition name
        @param cls_slots_first: True means return own slots at the top of the list
        @param seen: List of slots already recorded. Used for internal recursion
        @return: ordered list of slots in the class with slot usages removed
        """
        if not isinstance(cls, ClassDefinition):
            cls = self.schema.classes[cls]
        if seen is None:
            seen = set()
        rval = []

        parent = self.schema.classes[cls.is_a] if cls.is_a else None
        if cls_slots_first:
            for slot in self.own_slots(cls):
                sname_base = alias_root(self.schema, slot.name)
                if sname_base not in seen:
                    rval.append(slot)
                    seen.add(sname_base)
            return rval + (
                self.all_slots(parent, cls_slots_first=cls_slots_first, seen=seen)
                if parent
                else []
            )
        else:
            for sname in cls.slots:
                sname_base = alias_root(self.schema, sname)
                if sname_base not in seen:
                    slot = self.schema.slots[sname]
                    rval.append(slot)
                    seen.add(sname_base)
            return sorted(rval, key=lambda s: s.name) if self.sort_class_slots else rval

    def parent(
        self, element: Union[ClassDefinition, SlotDefinition]
    ) -> Optional[Union[ClassDefinition, SlotDefinition]]:
        """Return the parent of element, if any"""
        return (
            None
            if element.is_a is None
            else self.schema.classes[element.is_a]
            if isinstance(element, ClassDefinition)
            else self.schema.slots[element.is_a]
        )

    def ancestors(
        self, element: Union[ClassDefinition, SlotDefinition]
    ) -> List[ElementName]:
        """Return an ordered list of ancestor names for the supplied slot or class

        @param element: Slot or class name or definition
        @return: Ordered list of of ancestor names
        """
        return [element.name] + (
            [] if element.is_a is None else self.ancestors(self.parent(element))
        )

    def neighborhood(
        self, elements: Union[str, ElementName, List[ElementName]]
    ) -> References:
        """Return a list of all slots, classes and types that touch any element in elements, including the element
        itself

        @param elements: Element names to do proximity with
        @return: All slots and classes that touch element
        """
        if isinstance(elements, (str, ElementName)):
            elements = [elements]
        touches = References()
        for element in elements:
            if element in self.schema.classes:
                touches.classrefs.add(cast(ClassDefinitionName, element))
                cls = self.schema.classes[cast(ClassDefinitionName, element)]
                if cls.is_a:
                    touches.classrefs.add(cls.is_a)
                # Mixins include apply_to's
                touches.classrefs.update(set(cls.mixins))
                for slotname in cls.slots:
                    slot = self.schema.slots[slotname]
                    if slot.range in self.schema.classes:
                        touches.classrefs.add(cast(ClassDefinitionName, slot.range))
                    elif slot.range in self.schema.types:
                        touches.typerefs.add(cast(TypeDefinitionName, slot.range))
                for cv in self.schema.classes.values():
                    if cv.is_a == element:
                        touches.classrefs.add(cv.name)
                if element in self.synopsis.rangerefs:
                    for slotname in self.synopsis.rangerefs[element]:
                        touches.slotrefs.add(slotname)
                        if self.schema.slots[slotname].domain:
                            touches.classrefs.add(self.schema.slots[slotname].domain)
                if cls.in_subset:
                    touches.subsetrefs.update(cls.in_subset)
            if element in self.schema.slots:
                touches.slotrefs.add(cast(SlotDefinitionName, element))
                slot = self.schema.slots[cast(SlotDefinitionName, element)]
                touches.slotrefs.update(set(slot.mixins))
                if slot.is_a:
                    touches.slotrefs.add(slot.is_a)
                if element in self.synopsis.inverses:
                    touches.slotrefs.update(
                        self.synopsis.inverses[cast(SlotDefinitionName, element)]
                    )
                if slot.domain:
                    touches.classrefs.add(slot.domain)
                if slot.range in self.schema.classes:
                    touches.classrefs.add(cast(ClassDefinitionName, slot.range))
                elif slot.range in self.schema.types:
                    touches.typerefs.add(cast(TypeDefinitionName, slot.range))
                if slot.in_subset:
                    touches.subsetrefs.update(slot.in_subset)
                for sv in self.schema.slots.values():
                    if sv.is_a == element:
                        touches.slotrefs.add(sv.name)
            if element in self.schema.types:
                touches.typerefs.add(cast(TypeDefinitionName, element))
                typ = self.schema.types[cast(TypeDefinitionName, element)]
                if element in self.synopsis.rangerefs:
                    touches.slotrefs.update(self.synopsis.rangerefs[element])
                if typ.typeof:
                    touches.typerefs.add(cast(TypeDefinitionName, typ.typeof))
                if typ.in_subset:
                    touches.subsetrefs.update(typ.in_subset)
                for tv in self.schema.types.values():
                    if tv.typeof == element:
                        touches.slotrefs.add(tv.name)
            if element in self.schema.subsets:
                touches.subsetrefs.add(cast(SubsetDefinitionName, element))
                if element in self.synopsis.subsetrefs:
                    touches.update(
                        self.synopsis.subsetrefs[cast(SubsetDefinitionName, element)]
                    )
            if not bool(touches):
                self.logger.warning(f"neighborhood({element}) - {element} is undefined")

        return touches

    def range_type_path(self, typ: TypeDefinition) -> List[str]:
        """
        Return a formatted list of range types from the base up

        :param typ: type definition whose name is to be formatted
        :return: List of possible types with base at the leftmost
        """
        formatted_typ_name = self.class_or_type_name(typ.name)
        if typ.typeof:
            return self.range_type_path(
                self.schema.types[cast(TypeDefinitionName, typ.typeof)]
            ) + [formatted_typ_name]
        elif typ.repr:
            return [typ.repr, formatted_typ_name]
        else:
            return [formatted_typ_name]

    def class_identifier(
        self, def_or_name: Union[str, ClassDefinition, TypeDefinition]
    ) -> Optional[SlotDefinitionName]:
        """
        Return the class identifier if any

        :param def_or_name: class name or definition
        :return: name of class key (or identifier) if one exists
        """
        if isinstance(def_or_name, ClassDefinition):
            cls = def_or_name
        elif def_or_name in self.schema.classes:
            cls = self.schema.classes[cast(ClassDefinitionName, def_or_name)]
        else:
            return None
        for slotname in cls.slots:
            slot = self.schema.slots[slotname]
            if slot.identifier or slot.key:
                return slotname
        return None

    def enum_identifier_path(
        self, enum_or_enumname: Union[str, EnumDefinition]
    ) -> List[str]:
        """Return an enum_identifier path"""
        return [
            "str",
            camelcase(
                enum_or_enumname.name
                if isinstance(enum_or_enumname, EnumDefinition)
                else enum_or_enumname
            ),
        ]

    def class_identifier_path(
        self, cls_or_clsname: Union[str, ClassDefinition], force_non_key: bool
    ) -> List[str]:
        """
        Return the path closure to a class identifier if the class has a key and force_non_key is false otherwise
        return a dictionary closure.

        :param cls_or_clsname: class definition
        :param force_non_key: True means inlined even if the class has a key
        :return: path
        """
        cls = (
            cls_or_clsname
            if isinstance(cls_or_clsname, ClassDefinition)
            else self.schema.classes[ClassDefinitionName(cls_or_clsname)]
        )

        # Determine whether the class has a key
        identifier_slot = None
        if not force_non_key:
            identifier_slot = self.class_identifier(cls)

        # No key or inlined, its closure is a dictionary
        if identifier_slot is None:
            return ["dict", self.class_or_type_name(cls.name)]

        # We're dealing with a reference
        pathname = camelcase(cls.name + " " + self.aliased_slot_name(identifier_slot))
        if cls.is_a:
            parent_identifier_slot = self.class_identifier(cls.is_a)
            if parent_identifier_slot:
                return self.class_identifier_path(cls.is_a, False) + [pathname]
        return self.slot_range_path(identifier_slot) + [pathname]

    def slot_range_path(self, slot_or_name: Union[str, SlotDefinition]) -> List[str]:
        """
        Return a ordered list of slot ranges from distal to proximal

        :param slot_or_name: slot whose range is being typed
        :return: ordered list of types from base type forward
        """
        slot = (
            slot_or_name
            if isinstance(slot_or_name, SlotDefinition)
            else self.schema.slots[cast(SlotDefinitionName, slot_or_name)]
        )
        if slot.range in self.schema.types:
            # Type
            return self.range_type_path(
                self.schema.types[cast(TypeDefinitionName, slot.range)]
            )
        elif slot.range in self.schema.enums:
            return self.enum_identifier_path(slot.range)
        else:
            # Class
            return self.class_identifier_path(slot.range, bool(slot.inlined))

    def aliased_slot_name(
        self, slot: Union[SlotDefinitionName, SlotDefinition]
    ) -> SlotDefinitionName:
        """Return the overloaded slot name -- the alias if one exists otherwise the actual name

        @param slot: either a slot name or a definition
        @return: overloaded name
        """
        if isinstance(slot, str):
            slot = self.schema.slots[cast(SlotDefinitionName, slot)]
        return slot.alias if slot.alias else slot.name

    def class_or_type_for(self, name: str) -> Optional[Element]:
        """
        Return the corresponding class or type for name
        """
        if name in self.schema.classes:
            return self.schema.classes[ClassDefinitionName(name)]
        elif name in self.schema.types:
            return self.schema.types[TypeDefinitionName(name)]
        elif name in self.schema.enums:
            return self.schema.enums[EnumDefinitionName(name)]
        return None

    def class_or_type_name(self, name: str) -> str:
        """
        Return the camelcase representation of clsname if it is a valid class or type.  Prepend "Unknown"
        if the name isn't valid
        """
        if name in self.schema.classes:
            return camelcase(name)
        elif name in self.schema.types:
            typ = self.schema.types[cast(TypeDefinitionName, name)]
            if typ.typeof:
                return camelcase(name)
            else:
                return typ.base
        else:
            return "Unknown_" + camelcase(name)

    def slot_for(self, name: str) -> Optional[Element]:
        return self.schema.slots.get(name)

    def slot_name(self, name: str) -> str:
        """
        Return the underscored version of the aliased slot name if name is a slot. Prepend "unknown_" if the name
        isn't valid.
        """
        slot = self.slot_for(name)
        return underscore(self.aliased_slot_name(slot) if slot else ("unknown " + name))

    def subset_for(self, name: str) -> Optional[Element]:
        return self.schema.subsets.get(name)

    def subset_name(self, name: str) -> str:
        subset = self.subset_for(name)
        return ("" if subset else "Unknown_") + camelcase(name)

    def formatted_element_name(
        self, el_or_elname: Union[ElementName, Element], is_range_name: bool = False
    ) -> Optional[str]:
        """
        Return the default format for the name or the referenced element.  Slots are under_scored, all others are
        CamelCased. Slot names are the alias, not the actual name

        :param el_or_elname: element or name to map
        :param is_range_name: True means that we're looking for a class or type.  False means Slot or Subset. Only
        applies if el_or_elname is an ElementName (otherwise we know what we've got
        :return: Formatted name if type can be known else None
        """
        if isinstance(el_or_elname, str):
            if is_range_name:
                return (
                    self.class_or_type_name(el_or_elname)
                    if el_or_elname in self.schema.classes
                    or el_or_elname in self.schema.types
                    or el_or_elname == self.schema.default_range
                    else None
                )
            elif el_or_elname in self.schema.slots:
                return self.slot_name(cast(SlotDefinitionName, el_or_elname))
            elif el_or_elname in self.schema.subsets:
                return self.subset_name(el_or_elname)
            return None
        elif isinstance(el_or_elname, (ClassDefinition, TypeDefinition)):
            return self.class_or_type_name(el_or_elname.name)
        elif isinstance(el_or_elname, SlotDefinition):
            return self.slot_name(el_or_elname.name)
        elif isinstance(el_or_elname, SubsetDefinition):
            return self.subset_name(el_or_elname.name)
        else:
            return None

    def obj_for(
        self, el_or_elname: str, is_range_name: bool = False
    ) -> Optional[Element]:
        if is_range_name:
            return (
                self.class_or_type_for(el_or_elname)
                if el_or_elname in self.schema.classes
                or el_or_elname in self.schema.types
                or el_or_elname == self.schema.default_range
                else None
            )
        elif el_or_elname in self.schema.slots:
            return self.slot_for(cast(SlotDefinitionName, el_or_elname))
        elif el_or_elname in self.schema.subsets:
            return self.subset_for(el_or_elname)
        else:
            return self.class_or_type_for(el_or_elname)

    def default_prefix(self) -> Optional[str]:
        """Return the default prefix for the schema

        @return: URI or NCNAME of default prefix"""
        if "://" in self.schema.default_prefix:
            return self.schema.default_prefix
        else:
            # Basic loader tests for valid default prefix
            return self.schema.prefixes[
                PrefixPrefixPrefix(self.schema.default_prefix)
            ].prefix_reference

    # TODO: add lru cache once we get identity into the classes
    def domain_slots(self, cls: ClassDefinition) -> List[SlotDefinition]:
        """Return all slots in the class definition that are owned by the class"""
        return [
            slot
            for slot in [self.schema.slots[sn] for sn in cls.slots]
            if cls.name in slot.domain_of
            or (set(cls.mixins).intersection(slot.domain_of))
        ]

    def add_mappings(self, defn: Definition) -> None:
        """
        Process any mappings in defn, adding all of the mappings prefixes to the namespace map
        :param defn: Class or Slot Definition
        """
        self.add_id_prefixes(defn)
        mappings = (
            defn.mappings
            + defn.related_mappings
            + defn.close_mappings
            + defn.narrow_mappings
            + defn.broad_mappings
            + defn.exact_mappings
        )
        # see https://github.com/linkml/linkml/pull/283
        if isinstance(defn, ClassDefinition):
            mappings.append(defn.class_uri)
        if isinstance(defn, SlotDefinition):
            mappings.append(defn.slot_uri)
        for mapping in mappings:
            if "://" in str(mapping):
                mcurie = self.namespaces.curie_for(mapping)
                if mcurie is None:
                    self.logger.warning(f"No namespace defined for URI: {mapping}")
                    return  # Absolute path - no prefix/name
                else:
                    mapping = mcurie
            if ":" not in mapping or len(mapping.split(":")) != 2:
                raise ValueError(
                    f"Definition {defn.name} - unrecognized mapping: {mapping}"
                )
            ns = mapping.split(":")[0]
            logging.debug(f"Adding {ns} from {mapping} // {defn}")
            if ns:
                self.add_prefix(ns)

    def add_id_prefixes(self, element: Element) -> None:
        for id_prefix in element.id_prefixes:
            self.add_prefix(id_prefix)

    def add_prefix(self, ncname: str) -> None:
        """Add a prefix to the list of prefixes to emit

        @param ncname: name to add
        """
        if ncname not in self.namespaces:
            self.logger.warning(f"Unrecognized prefix: {ncname}")
            self.namespaces[ncname] = f"http://example.org/UNKNOWN/{ncname}/"
        self.emit_prefixes.add(ncname)

    def get_metamodel_slot_name(self, slot_name: str) -> str:
        """
        Allows for localization of some generators, such as markdown generator

        The client can control how metamodel elements are displayed; e.g.
        mapping the metamodel slot "slot" to "field"

        This method also takes care of pluralization; e.g. if "slot" is mapped to
        "field", then "slots" will be mapped to "fields"

        :param slot_name:
        :return:
        """
        is_capitalized = slot_name[0].isupper()

        def capitalize(s: str):
            if is_capitalized:
                return f"{s[0].upper()}{s[1:]}"
            else:
                return s

        slot_name_normalized = underscore(slot_name).lower()
        slot_name_normalized_singular = re.sub(r"s$", "", slot_name_normalized)
        if slot_name_normalized == "classes":
            slot_name_normalized_singular = "class"
        if (
            self.metamodel_name_map is not None
            and slot_name_normalized in self.metamodel_name_map
        ):
            return capitalize(self.metamodel_name_map[slot_name_normalized])
        elif (
            self.metamodel_name_map is not None
            and slot_name_normalized_singular in self.metamodel_name_map
        ):
            return capitalize(
                f"{self.metamodel_name_map[slot_name_normalized_singular]}s"
            )
        else:
            return slot_name

    def is_class_unconstrained(self, cls: ClassDefinition):
        """
        Determine if the class is mapped to typing.Any, i.e the unconstrained class

        :param cls: class definition
        :return: true if the class is unconstrained
        """
        return cls.class_uri == "linkml:Any"


def shared_arguments(g: Type[Generator]) -> Callable[[Command], Command]:
    _LOG_LEVEL_STRINGS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

    def _log_level_string_to_int(log_level_string: str) -> int:
        log_level_string = log_level_string.upper()
        level = [e for e in log_level_string if e.startswith(log_level_string)]
        if not level:
            pass
        log_level_int = getattr(logging, log_level_string[0], logging.INFO)
        assert isinstance(log_level_int, int)
        return log_level_int

    def verbosity_callback(ctx, param, verbose):
        if verbose >= 2:
            logging.basicConfig(level=logging.DEBUG)
        elif verbose == 1:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)

    def log_level_callback(ctx, param, value):
        logging.basicConfig(level=_log_level_string_to_int(value))

    def decorator(f: Command) -> Command:
        f.params.append(
            Argument(("yamlfile",), type=click.Path(exists=True, dir_okay=False))
        )
        f.params.append(
            Option(
                ("--format", "-f"),
                type=click.Choice(g.valid_formats),
                default=g.valid_formats[0],
                show_default=True,
                help=f"Output format",
            )
        )
        f.params.append(
            Option(
                ("--metadata/--no-metadata",),
                default=True,
                show_default=True,
                help="Include metadata in output",
            )
        )
        f.params.append(
            Option(
                ("--useuris/--metauris",),
                default=True,
                show_default=True,
                help="Include metadata in output",
            )
        )
        f.params.append(
            Option(
                ("--importmap", "-im"), type=click.File(), help="Import mapping file"
            )
        )
        f.params.append(
            Option(
                ("--log_level",),
                type=click.Choice(_LOG_LEVEL_STRINGS),
                help=f"Logging level",
                default=DEFAULT_LOG_LEVEL,
                show_default=True,
                callback=log_level_callback,
            )
        )
        f.params.append(
            Option(
                ("--verbose", "-v"),
                count=True,
                help=f"verbosity",
                callback=verbosity_callback,
            )
        )
        f.params.append(
            Option(
                ("--mergeimports/--no-mergeimports",),
                default=True,
                help="Merge imports into source file (default=mergeimports)",
            )
        )
        f.params.append(
            Option(
                ("--stacktrace/--no-stacktrace",),
                default=False,
                help="Print a stack trace when an error occurs (default=stacktrace)",
            )
        )

        return f

    return decorator
