import os
import sys
import uuid
import logging
import collections
from functools import lru_cache
from copy import copy, deepcopy
from collections import defaultdict, deque
from pathlib import Path, PurePath
from typing import Optional, TypeVar
from collections.abc import Mapping
import warnings
from urllib.parse import urlparse

from linkml_runtime.utils.namespaces import Namespaces
from deprecated.classic import deprecated
from linkml_runtime.utils.context_utils import parse_import_map, map_import
from linkml_runtime.utils.formatutils import is_empty, underscore, camelcase
from linkml_runtime.utils.pattern import PatternResolver
from linkml_runtime.linkml_model.meta import *
from linkml_runtime.exceptions import OrderingError
from enum import Enum

logger = logging.getLogger(__name__)

MAPPING_TYPE = str  ## e.g. broad, exact, related, ...
CACHE_SIZE = 1024

SLOTS = 'slots'
CLASSES = 'classes'
ENUMS = 'enums'
SUBSETS = 'subsets'
TYPES = 'types'
WINDOWS = sys.platform == 'win32'

CLASS_NAME = Union[ClassDefinitionName, str]
SLOT_NAME = Union[SlotDefinitionName, str]
SUBSET_NAME = Union[SubsetDefinitionName, str]
TYPE_NAME = Union[TypeDefinitionName, str]
ENUM_NAME = Union[EnumDefinitionName, str]

ElementType = TypeVar("ElementType", bound=Element)
ElementNameType = TypeVar("ElementNameType", bound=Union[ElementName, str])
DefinitionType = TypeVar("DefinitionType", bound=Definition)
DefinitionNameType = TypeVar("DefinitionNameType", bound=Union[DefinitionName, str])
ElementDict = dict[ElementNameType, ElementType]
DefDict = dict[DefinitionNameType, DefinitionType]


class OrderedBy(Enum):
    RANK = "rank"
    LEXICAL = "lexical"
    PRESERVE = "preserve"
    INHERITANCE = "inheritance"
    """
    Order according to inheritance such that if C is a child of P then C appears after P
    """


def _closure(f, x, reflexive=True, depth_first=True, **kwargs):
    if reflexive:
        rv = [x]
    else:
        rv = []
    visited = []
    todo = [x]
    while len(todo) > 0:
        if depth_first:
            i = todo.pop()
        else:
            i = todo[0]
            todo = todo[1:]
        visited.append(i)
        vals = f(i)
        if vals is not None:
            for v in vals:
                if v not in visited and v not in rv:
                    todo.append(v)
                    rv.append(v)
    return rv


def load_schema_wrap(path: str, **kwargs):
    # import here to avoid circular imports
    from linkml_runtime.loaders.yaml_loader import YAMLLoader
    yaml_loader = YAMLLoader()
    schema: SchemaDefinition
    schema = yaml_loader.load(path, target_class=SchemaDefinition, **kwargs)
    if "\n" not in path:
        # if "\n" not in path and "://" not in path:
        # only set path if the input is not a yaml string or URL.
        # Setting the source path is necessary for relative imports;
        # while initializing a schema with a yaml string is possible, there
        # should be no expectation of relative imports working.
        schema.source_file = path
    return schema


def is_absolute_path(path: str) -> bool:
    if path.startswith("/"):
        return True
    # windows
    if not os.path.isabs(path):
        return False
    norm_path = os.path.normpath(path)
    if norm_path.startswith("\\\\") or ":" not in norm_path:
        return False
    drive, tail = os.path.splitdrive(norm_path)
    return bool(drive and tail)

def _resolve_import(source_sch: str, imported_sch: str) -> str:
    if os.path.isabs(imported_sch):
        # Absolute import paths are not modified
        return imported_sch
    if urlparse(imported_sch).scheme:
        # File with URL schemes are not modified
        return imported_sch
    
    if WINDOWS:
        path = PurePath(os.path.normpath(PurePath(source_sch).parent / imported_sch)).as_posix()
    else:
        path = os.path.normpath(str(Path(source_sch).parent / imported_sch))

    if imported_sch.startswith(".") and not path.startswith("."):
        # Above condition handles cases where both source schema and imported schema are relative paths: these should remain relative
        return f"./{path}"

    return path


@dataclass
class SchemaUsage:
    """
    A usage of an element of a schema
    """
    used_by: ElementName
    slot: SlotDefinitionName
    metaslot: SlotDefinitionName
    used: ElementName
    inferred: bool = None


@dataclass
class SchemaView:
    """
    A SchemaView provides a virtual schema layered on top of a schema plus its import closure

    Most operations are parameterized by `imports`. If this is set to True (default), then the full
    import closure is considered when answering

    This class utilizes caching for efficient lookup operations.

    TODO: decide how to use this in conjunction with the existing schemaloader, which injects
    into the schema rather than providing dynamic methods.

    See:
     - https://github.com/linkml/linkml/issues/59
     - https://github.com/linkml/linkml/discussions/144
     - https://github.com/linkml/linkml/issues/48
     - https://github.com/linkml/linkml/issues/270
    """

    schema: SchemaDefinition = None
    schema_map: dict[SchemaDefinitionName, SchemaDefinition] = None
    importmap: Optional[Mapping[str, str]] = None
    """Optional mapping between schema names and local paths/URLs"""
    modifications: int = 0
    uuid: str = None

    ## private vars --------
    # cached hash
    _hash: Optional[int] = None


    def __init__(self, schema: Union[str, Path, SchemaDefinition],
                 importmap: Optional[dict[str, str]] = None, merge_imports: bool = False, base_dir: str = None):
        if isinstance(schema, Path):
            schema = str(schema)
        if isinstance(schema, str):
            schema = load_schema_wrap(schema)
        self.schema = schema
        self.schema_map = {schema.name: schema}
        self.importmap = parse_import_map(importmap, base_dir) if importmap is not None else dict()
        if merge_imports:
            self.merge_imports()
        self.uuid = str(uuid.uuid4())

    def __key(self):
        return self.schema.id, self.uuid, self.modifications

    def __eq__(self, other):
        if isinstance(other, SchemaView):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.__key())
        return self._hash

    @lru_cache(None)
    def namespaces(self) -> Namespaces:
        namespaces = Namespaces()
        for s in self.schema_map.values():
            for cmap in self.schema.default_curi_maps:
                namespaces.add_prefixmap(cmap, include_defaults=False)
            for prefix in s.prefixes.values():
                namespaces[prefix.prefix_prefix] = prefix.prefix_reference
        return namespaces

    def load_import(self, imp: str, from_schema: SchemaDefinition = None):
        """
        Handles import directives.

        The value of the import can be:

        - a URL (specified as either a full URL or a CURIE)
        - a local file path

        The import should leave off the .yaml suffix.

        If the import is a URL then the import is fetched over the network UNLESS this is a metamodel
        import, in which case it is fetched from within the linkml_runtime package, where the yaml
        is distributed. This ensures that the version of the metamodel imported matches the version
        of the linkml_runtime package.

        In future, this mechanism may be extended to arbitrary modules, such that we avoid
        network dependence at runtime in general.

        For local paths, the import is resolved relative to the directory containing the source file,
        or the URL of the source file, if it is a URL.

        :param imp:
        :param from_schema:
        :return:
        """
        if from_schema is None:
            from_schema = self.schema
        from linkml_runtime import SCHEMA_DIRECTORY
        default_import_map = {
            "linkml:": str(SCHEMA_DIRECTORY)
        }
        importmap = {**default_import_map, **self.importmap}
        sname = map_import(importmap, self.namespaces, imp)
        if from_schema.source_file and not is_absolute_path(sname):
            base_dir = os.path.dirname(from_schema.source_file)
        else:
            base_dir = None
        logger.info(f'Importing {imp} as {sname} from source {from_schema.source_file}; base_dir={base_dir}')
        schema = load_schema_wrap(sname + '.yaml', base_dir=base_dir)
        return schema

    @lru_cache(None)
    def imports_closure(self, imports: bool = True, traverse: Optional[bool] = None, inject_metadata=True) -> list[
        SchemaDefinitionName]:
        """
        Return all imports

        Objects in imported classes override one another in a "python-like" order -
        from the point of view of the importing schema, imports will override one
        another from first to last, recursively for each layer of imports.

        An import tree like::

            - main
              - s1
                - s1_1
                - s1_2
                    - s1_2_1
                    - s1_2_2
              - s2
                - s2_1
                - s2_2

        will override objects with the same name, in order::

            ['s1_1', 's1_2_1', 's1_2_2', 's1_2', 's1', 's2_1', 's2_2', 's2']

        :param imports: bool (default: ``True`` ) include imported schemas, recursively
        :param traverse: bool, optional (default: ``True`` ) (Deprecated, use
            ``imports`` ). if true, traverse recursively
        :return: all schema names in the transitive reflexive imports closure
        """
        if self.schema_map is None:
            self.schema_map = {self.schema.name: self.schema}

        closure = deque()
        visited = set()
        todo = [self.schema.name]

        if traverse is not None:
            warnings.warn(
                'traverse behaves identically to imports and will be removed in a future version. Use imports instead.',
                DeprecationWarning
            )

        if not imports or (not traverse and traverse is not None):
            return todo

        while len(todo) > 0:
            # visit item
            sn = todo.pop()
            if sn not in self.schema_map:
                imported_schema = self.load_import(sn)
                self.schema_map[sn] = imported_schema

            # resolve item's imports if it has not been visited already
            # we will get duplicates, but not cycles this way, and
            # filter out dupes, preserving the first entry, at the end.
            if sn not in visited:
                for i in self.schema_map[sn].imports:
                    # no self imports ;)
                    if i == sn:
                        continue

                    # resolve relative imports relative to the importing schema, rather than the
                    # origin schema. Imports can be a URI or Curie, and imports from the same
                    # directory don't require a ./, so if the current (sn) import is a relative
                    # path, and the target import doesn't have : (as in a curie or a URI)
                    # we prepend the relative path. This WILL make the key in the `schema_map` not
                    # equal to the literal text specified in the importing schema, but this is
                    # essential to sensible deduplication: eg. for
                    # - main.yaml (imports ./types.yaml, ./subdir/subschema.yaml)
                    # - types.yaml
                    # - subdir/subschema.yaml (imports ./types.yaml)
                    # - subdir/types.yaml
                    # we should treat the two `types.yaml` as separate schemas from the POV of the
                    # origin schema.
                    i = _resolve_import(sn, i)
                    todo.append(i)

            # add item to closure
            # append + pop (above) is FILO queue, which correctly extends tree leaves,
            # but in backwards order.
            closure.appendleft(sn)
            visited.add(sn)

        # filter duplicates, keeping first entry
        closure = list({k: None for k in closure}.keys())

        if inject_metadata:
            for s in self.schema_map.values():
                # It is important to merge element definitions as a list as multiple elements of different kinds can
                # have the same name which means they have the same dict key.
                elements = []
                elements.extend(s.classes.values())
                elements.extend(s.enums.values())
                elements.extend(s.slots.values())
                elements.extend(s.subsets.values())
                elements.extend(s.types.values())

                for x in elements:
                    x.from_schema = s.id
                for c in s.classes.values():
                    for a in c.attributes.values():
                        a.from_schema = s.id
        return closure

    @lru_cache(None)
    def all_schema(self, imports: bool = True) -> list[SchemaDefinition]:
        """
        :param imports: include imports closure
        :return: all schemas
        """
        m = self.schema_map
        return [m[sn] for sn in self.imports_closure(imports)]

    @deprecated("Use `all_classes` instead")
    @lru_cache(None)
    def all_class(self, imports=True) -> dict[ClassDefinitionName, ClassDefinition]:
        """
        :param imports: include imports closure
        :return: all classes in schema view
        """
        return self._get_dict(CLASSES, imports)

    def ordered(self, elements: ElementDict, ordered_by: Optional[OrderedBy] = None) -> ElementDict:
        """
        Order a dictionary of elements with some ordering method in :class:`.OrderedBy`
        """
        if ordered_by in (OrderedBy.LEXICAL, OrderedBy.LEXICAL.value):
            return self._order_lexically(elements)
        elif ordered_by in (OrderedBy.RANK, OrderedBy.RANK.value):
            return self._order_rank(elements)
        elif ordered_by in (OrderedBy.INHERITANCE, OrderedBy.INHERITANCE.value):
            return self._order_inheritance(elements)
        elif ordered_by is None or ordered_by in (OrderedBy.PRESERVE, OrderedBy.PRESERVE.value):
            return elements
        else:
            raise ValueError(f"ordered_by must be in OrderedBy or None, got {ordered_by}")

    def _order_lexically(self, elements: ElementDict) -> ElementDict:
        """
        :param element: slots or class type to order
        :param imports
        :return: all classes or slots sorted lexically in schema view
        """
        ordered_list_of_names = []
        ordered_elements = {}
        for c in elements:
            ordered_list_of_names.append(c)
        ordered_list_of_names.sort()
        for name in ordered_list_of_names:
            ordered_elements[self.get_element(name).name] = self.get_element(name)
        return ordered_elements

    def _order_rank(self, elements: ElementDict) -> ElementDict:
        """
        :param elements: slots or classes to order
        :return: all classes or slots sorted by their rank in schema view
        """

        rank_map = {}
        unranked_map = {}
        rank_ordered_elements = {}
        for name, definition in elements.items():
            if definition.rank is None:
                unranked_map[self.get_element(name).name] = self.get_element(name)

            else:
                rank_map[definition.rank] = name
        rank_ordered_map = collections.OrderedDict(sorted(rank_map.items()))
        for k, v in rank_ordered_map.items():
            rank_ordered_elements[self.get_element(v).name] = self.get_element(v)

        rank_ordered_elements.update(unranked_map)
        return rank_ordered_elements

    def _order_inheritance(self, elements: DefDict) -> DefDict:
        """
        sort classes such that if C is a child of P then C appears after P in the list
        """
        clist = list(elements.values())
        slist = []  # sorted
        can_add = False
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
                raise OrderingError(f"could not find suitable element in {clist} that does not ref {slist}")

        return {s.name: s for s in slist}

    @lru_cache(None)
    def all_classes(self, ordered_by=OrderedBy.PRESERVE, imports=True) -> dict[ClassDefinitionName, ClassDefinition]:
        """
        :param ordered_by: an enumerated parameter that returns all the classes in the order specified.
        :param imports: include imports closure
        :return: all classes in schema view
        """
        classes = copy(self._get_dict(CLASSES, imports))
        classes = self.ordered(classes, ordered_by=ordered_by)
        return classes

    @deprecated("Use `all_slots` instead")
    @lru_cache(None)
    def all_slot(self, **kwargs) -> dict[SlotDefinitionName, SlotDefinition]:
        """
        :param imports: include imports closure
        :return: all slots in schema view
        """
        return self.all_slots(**kwargs)

    @lru_cache(None)
    def all_slots(self, ordered_by=OrderedBy.PRESERVE, imports=True, attributes=True) -> dict[
        SlotDefinitionName, SlotDefinition]:
        """
        :param ordered_by: an enumerated parameter that returns all the slots in the order specified.
        :param imports: include imports closure
        :param attributes: include attributes as slots or not, default is to include.
        :return: all slots in schema view
        """

        slots = copy(self._get_dict(SLOTS, imports))
        if attributes:
            for c in self.all_classes().values():
                for aname, a in c.attributes.items():
                    if aname not in slots:
                        slots[aname] = a

        slots = self.ordered(slots, ordered_by=ordered_by)
        return slots

    @deprecated("Use `all_enums` instead")
    @lru_cache(None)
    def all_enum(self, imports=True) -> dict[EnumDefinitionName, EnumDefinition]:
        """
        :param imports: include imports closure
        :return: all enums in schema view
        """
        return self._get_dict(ENUMS, imports)

    @lru_cache(None)
    def all_enums(self, imports=True) -> dict[EnumDefinitionName, EnumDefinition]:
        """
        :param imports: include imports closure
        :return: all enums in schema view
        """
        return self._get_dict(ENUMS, imports)

    @deprecated("Use `all_types` instead")
    @lru_cache(None)
    def all_type(self, imports=True) -> dict[TypeDefinitionName, TypeDefinition]:
        """
        :param imports: include imports closure
        :return: all types in schema view
        """
        return self._get_dict(TYPES, imports)

    @lru_cache(None)
    def all_types(self, imports=True) -> dict[TypeDefinitionName, TypeDefinition]:
        """
        :param imports: include imports closure
        :return: all types in schema view
        """
        return self._get_dict(TYPES, imports)

    @deprecated("Use `all_subsets` instead")
    def all_subset(self, imports=True) -> dict[SubsetDefinitionName, SubsetDefinition]:
        """
        :param imports: include imports closure
        :return: all subsets in schema view
        """
        return self._get_dict(SUBSETS, imports)

    @lru_cache(None)
    def all_subsets(self, imports=True) -> dict[SubsetDefinitionName, SubsetDefinition]:
        """
        :param imports: include imports closure
        :return: all subsets in schema view
        """
        return self._get_dict(SUBSETS, imports)

    @deprecated("Use `all_elements` instead")
    @lru_cache(None)
    def all_element(self, imports=True) -> dict[ElementName, Element]:
        """
        :param imports: include imports closure
        :return: all elements in schema view
        """
        all_classes = self.all_classes(imports=imports)
        all_slots = self.all_slots(imports=imports)
        all_enums = self.all_enums(imports=imports)
        all_types = self.all_types(imports=imports)
        all_subsets = self.all_subsets(imports=imports)
        # {**a,**b} syntax merges dictionary a and b into a single dictionary, removing duplicates.
        return {**all_classes, **all_slots, **all_enums, **all_types, **all_subsets}

    @lru_cache(None)
    def all_elements(self, imports=True) -> dict[ElementName, Element]:
        """
        :param imports: include imports closure
        :return: all elements in schema view
        """
        all_classes = self.all_classes(imports=imports)
        all_slots = self.all_slots(imports=imports)
        all_enums = self.all_enums(imports=imports)
        all_types = self.all_types(imports=imports)
        all_subsets = self.all_subsets(imports=imports)
        # {**a,**b} syntax merges dictionary a and b into a single dictionary, removing duplicates.
        return {**all_classes, **all_slots, **all_enums, **all_types, **all_subsets}

    def _get_dict(self, slot_name: str, imports=True) -> dict:
        schemas = self.all_schema(imports)
        d = {}
        # pdb.set_trace()
        # iterate through all schemas and merge the list together
        for s in schemas:
            # get the value of element name from the schema, if empty, return empty dictionary.
            d1 = getattr(s, slot_name, {})
            # {**d,**d1} syntax merges dictionary d and d1 into a single dictionary, removing duplicates.
            d = {**d, **d1}

        return d

    @lru_cache(None)
    def slot_name_mappings(self) -> dict[str, SlotDefinition]:
        """
        Mapping between processed safe slot names (following naming conventions)  and slots.

        For example, a slot may have name 'lives at', the code-safe version is `lives_at`

        :return: mapping from safe names to slot
        """
        m = {}
        for s in self.all_slots().values():
            m[underscore(s.name)] = s
        return m

    @lru_cache(None)
    def class_name_mappings(self) -> dict[str, ClassDefinition]:
        """
        Mapping between processed safe class names (following naming conventions) and classes.

        For example, a class may have name 'named thing', the code-safe version is `NamedThing`

        :return: mapping from safe names to class
        """
        m = {}
        for s in self.all_classes().values():
            m[camelcase(s.name)] = s
        return m

    @lru_cache(None)
    def in_schema(self, element_name: ElementName) -> SchemaDefinitionName:
        """
        :param element_name:
        :return: name of schema in which element is defined
        """
        ix = self.element_by_schema_map()
        if element_name not in ix:
            raise ValueError(f'Element {element_name} not in any schema')
        return ix[element_name]

    @lru_cache(None)
    def element_by_schema_map(self) -> dict[ElementName, SchemaDefinitionName]:
        ix = {}
        schemas = self.all_schema(True)
        for schema in schemas:
            for type_key in [CLASSES, SLOTS, TYPES, ENUMS, SUBSETS]:
                for k, v in getattr(schema, type_key, {}).items():
                    ix[k] = schema.name
            for c in schema.classes.values():
                for aname, a in c.attributes.items():
                    ix[aname] = schema.name
        return ix

    @lru_cache(None)
    def get_class(self, class_name: CLASS_NAME, imports=True, strict=False) -> ClassDefinition:
        """
        :param class_name: name of the class to be retrieved
        :param imports: include import closure
        :return: class definition
        """
        c = self.all_classes(imports=imports).get(class_name, None)
        if strict and c is None:
            raise ValueError(f'No such class as "{class_name}"')
        else:
            return c

    @lru_cache(None)
    def get_slot(self, slot_name: SLOT_NAME, imports=True, attributes=True, strict=False) -> SlotDefinition:
        """
        :param slot_name: name of the slot to be retrieved
        :param imports: include import closure
        :param attributes: include attributes
        :param strict: raise ValueError is not found
        :return: slot definition
        """
        slot = self.all_slots(imports=imports, attributes=False).get(slot_name, None)
        if slot is None and attributes:
            for c in self.all_classes(imports=imports).values():
                if slot_name in c.attributes:
                    if slot is not None:
                        # slot name is ambiguous: return a stub slot
                        return SlotDefinition(slot_name)
                    slot = copy(c.attributes[slot_name])
                    slot.from_schema = c.from_schema
                    slot.owner = c.name
        if strict and slot is None:
            raise ValueError(f'No such slot as "{slot_name}"')
        return slot

    @lru_cache(None)
    def get_subset(self, subset_name: SUBSET_NAME, imports=True, strict=False) -> SubsetDefinition:
        """
        :param subset_name: name of the subsey to be retrieved
        :param imports: include import closure
        :return: subset definition
        """
        s = self.all_subsets(imports).get(subset_name, None)
        if strict and s is None:
            raise ValueError(f'No such subset as "{subset_name}"')
        else:
            return s

    @lru_cache(None)
    def get_enum(self, enum_name: ENUM_NAME, imports=True, strict=False) -> EnumDefinition:
        """
        :param enum_name: name of the enum to be retrieved
        :param imports: include import closure
        :return: enum definition
        """
        e = self.all_enums(imports).get(enum_name, None)
        if strict and e is None:
            raise ValueError(f'No such subset as "{enum_name}"')
        else:
            return e

    @lru_cache(None)
    def get_type(self, type_name: TYPE_NAME, imports=True, strict=False) -> TypeDefinition:
        """
        :param type_name: name of the type to be retrieved
        :param imports: include import closure
        :return: type definition
        """
        t = self.all_types(imports).get(type_name, None)
        if strict and t is None:
            raise ValueError(f'No such subset as "{type_name}"')
        else:
            return t

    def _parents(self, e: Element, imports=True, mixins=True, is_a=True) -> list[ElementName]:
        if mixins:
            parents = copy(e.mixins)
        else:
            parents = []
        if e.is_a is not None and is_a:
            parents.append(e.is_a)
        return parents

    @lru_cache(None)
    def class_parents(self, class_name: CLASS_NAME, imports=True, mixins=True, is_a=True) -> list[ClassDefinitionName]:
        """
        :param class_name: child class name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct parent class names (is_a and mixins)
        """
        cls = self.get_class(class_name, imports, strict=True)
        return self._parents(cls, imports, mixins, is_a)

    @lru_cache(None)
    def enum_parents(self, enum_name: ENUM_NAME, imports=False, mixins=False, is_a=True) -> list[EnumDefinitionName]:
        """
        :param enum_name: child enum name
        :param imports: include import closure (False)
        :param mixins: include mixins (default is False)
        :return: all direct parent enum names (is_a and mixins)
        """
        e = self.get_enum(enum_name, strict=True)
        return self._parents(e, imports, mixins, is_a=is_a)

    @lru_cache(None)
    def permissible_value_parent(self, permissible_value: str, enum_name: ENUM_NAME) -> Union[
        str, PermissibleValueText, None, ValueError]:
        """
        :param enum_name: child enum name
        :param permissible_value: permissible value
        :return: all direct parent enum names (is_a)
        """
        enum = self.get_enum(enum_name, strict=True)
        if enum:
            if permissible_value in enum.permissible_values:
                pv = enum.permissible_values[permissible_value]
                if pv.is_a:
                    return [pv.is_a]
        else:
            return []

    @lru_cache(None)
    def permissible_value_children(self, permissible_value: str, enum_name: ENUM_NAME) -> Union[
        str, PermissibleValueText, None, ValueError]:
        """
        :param enum_name: parent enum name
        :param permissible_value: permissible value
        :return: all direct child permissible values (is_a)

        CAT:
        LION:
          is_a: CAT
        ANGRY_LION:
          is_a: LION
        TABBY:
          is_a: CAT
        BIRD:
        EAGLE:
          is_a: BIRD

        """

        enum = self.get_enum(enum_name, strict=True)
        children = []
        if enum:
            if permissible_value in enum.permissible_values:
                pv = enum.permissible_values[permissible_value]
                for isapv in enum.permissible_values:
                    isapv_entity = enum.permissible_values[isapv]
                    if isapv_entity.is_a and pv.text == isapv_entity.is_a:
                        children.append(isapv)
                return children
        else:
            raise ValueError(f'No such enum as "{enum_name}"')

    @lru_cache(None)
    def slot_parents(self, slot_name: SLOT_NAME, imports=True, mixins=True, is_a=True) -> list[SlotDefinitionName]:
        """
        :param slot_name: child slot name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct parent slot names (is_a and mixins)
        """
        s = self.get_slot(slot_name, imports, strict=True)
        if s:
            return self._parents(s, imports, mixins, is_a)
        else:
            return []

    @lru_cache(None)
    def type_parents(self, type_name: TYPE_NAME, imports=True) -> list[TypeDefinitionName]:
        """
        :param type_name: child type name
        :param imports: include import closure
        :return: all direct parent enum names (is_a and mixins)
        """
        typ = self.get_type(type_name, imports, strict=True)
        if typ.typeof:
            return [typ.typeof]
        else:
            return []

    @lru_cache(None)
    def get_children(self, name: str, mixin: bool = True) -> list[str]:
        """
        get the children of an element (any class, slot, enum, type)
        :param name: name of the parent element
        :param mixin: include mixins
        :return: list of child element
        """
        children = []
        for e, el in self.all_elements().items():
            if isinstance(el, (ClassDefinition, SlotDefinition, EnumDefinition)):
                if el.is_a and el.is_a == name:
                    children.append(el.name)
                if mixin and el.mixins and name in el.mixins:
                    children.append(el.name)
        return children

    @lru_cache(None)
    def class_children(self, class_name: CLASS_NAME, imports=True, mixins=True, is_a=True) -> list[ClassDefinitionName]:
        """
        :param class_name: parent class name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :return: all direct child class names (is_a and mixins)
        """
        elts = [self.get_class(x) for x in self.all_classes(imports=imports)]
        return [x.name for x in elts if (x.is_a == class_name and is_a) or (mixins and class_name in x.mixins)]

    @lru_cache(None)
    def slot_children(self, slot_name: SLOT_NAME, imports=True, mixins=True, is_a=True) -> list[SlotDefinitionName]:
        """
        :param slot_name: parent slot name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :return: all direct child slot names (is_a and mixins)
        """
        elts = [self.get_slot(x) for x in self.all_slots(imports=imports)]
        return [x.name for x in elts if (x.is_a == slot_name and is_a) or (mixins and slot_name in x.mixins)]

    @lru_cache(None)
    def class_ancestors(self, class_name: CLASS_NAME, imports=True, mixins=True, reflexive=True, is_a=True,
                        depth_first=True) -> list[ClassDefinitionName]:
        """
        Closure of class_parents method

        :param class_name: query class
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :param reflexive: include self in set of ancestors
        :param depth_first:
        :return: ancestor class names
        """
        return _closure(lambda x: self.class_parents(x, imports=imports, mixins=mixins, is_a=is_a),
                        class_name,
                        reflexive=reflexive, depth_first=depth_first)

    @lru_cache(None)
    def permissible_value_ancestors(self, permissible_value_text: str,
                                    enum_name: ENUM_NAME,
                                    reflexive=True,
                                    depth_first=True) -> list[str]:
        """
        Closure of permissible_value_parents method
        :enum
        """

        return _closure(lambda x: self.permissible_value_parent(x, enum_name),
                        permissible_value_text,
                        reflexive=reflexive,
                        depth_first=depth_first)

    @lru_cache(None)
    def permissible_value_descendants(self, permissible_value_text: str,
                                      enum_name: ENUM_NAME,
                                      reflexive=True,
                                      depth_first=True) -> list[str]:
        """
        Closure of permissible_value_children method
        :enum
        """

        return _closure(lambda x: self.permissible_value_children(x, enum_name),
                        permissible_value_text,
                        reflexive=reflexive,
                        depth_first=depth_first)

    @lru_cache(None)
    def enum_ancestors(self, enum_name: ENUM_NAME, imports=True, mixins=True, reflexive=True, is_a=True,
                       depth_first=True) -> list[EnumDefinitionName]:
        """
        Closure of enum_parents method

        :param enum_name: query enum
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :param reflexive: include self in set of ancestors
        :param depth_first:
        :return: ancestor enum names
        """
        return _closure(lambda x: self.enum_parents(x, imports=imports, mixins=mixins, is_a=is_a),
                        enum_name,
                        reflexive=reflexive, depth_first=depth_first)

    @lru_cache(None)
    def type_ancestors(self, type_name: TYPES, imports=True, reflexive=True, depth_first=True) -> list[
        TypeDefinitionName]:
        """
        All ancestors of a type via typeof

        :param type_name: query type
        :param imports: include import closure
        :param reflexive: include self in set of ancestors
        :param depth_first:
        :return: ancestor class names
        """
        return _closure(lambda x: self.type_parents(x, imports=imports),
                        type_name,
                        reflexive=reflexive, depth_first=depth_first)

    @lru_cache(None)
    def slot_ancestors(self, slot_name: SLOT_NAME, imports=True, mixins=True, reflexive=True, is_a=True) -> list[
        SlotDefinitionName]:
        """
        Closure of slot_parents method

        :param slot_name: query slot
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :param reflexive: include self in set of ancestors
        :return: ancestor slot names
        """
        return _closure(lambda x: self.slot_parents(x, imports=imports, mixins=mixins, is_a=is_a),
                        slot_name,
                        reflexive=reflexive)

    @lru_cache(None)
    def class_descendants(self, class_name: CLASS_NAME, imports=True, mixins=True, reflexive=True, is_a=True) -> list[
        ClassDefinitionName]:
        """
        Closure of class_children method

        :param class_name: query class
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :param reflexive: include self in set of descendants
        :return: descendants class names
        """
        return _closure(lambda x: self.class_children(x, imports=imports, mixins=mixins, is_a=is_a), class_name,
                        reflexive=reflexive)

    @lru_cache(None)
    def slot_descendants(self, slot_name: SLOT_NAME, imports=True, mixins=True, reflexive=True, is_a=True) -> list[
        SlotDefinitionName]:
        """
        Closure of slot_children method

        :param slot_name: query slot
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param is_a: include is_a parents (default is True)
        :param reflexive: include self in set of descendants
        :return: descendants slot names
        """
        return _closure(lambda x: self.slot_children(x, imports=imports, mixins=mixins, is_a=is_a), slot_name,
                        reflexive=reflexive)

    @lru_cache(None)
    def class_roots(self, imports=True, mixins=True, is_a=True) -> list[ClassDefinitionName]:
        """
        All classes that have no parents
        :param imports:
        :param mixins:
        :param is_a: include is_a parents (default is True)
        :return:
        """
        return [c
                for c in self.all_classes(imports=imports)
                if self.class_parents(c, mixins=mixins, is_a=is_a, imports=imports) == []]

    @lru_cache(None)
    def class_leaves(self, imports=True, mixins=True, is_a=True) -> list[ClassDefinitionName]:
        """
        All classes that have no children
        :param imports:
        :param mixins:
        :param is_a: include is_a parents (default is True)
        :return:
        """
        return [c
                for c in self.all_classes(imports=imports)
                if self.class_children(c, mixins=mixins, is_a=is_a, imports=imports) == []]

    @lru_cache(None)
    def slot_roots(self, imports=True, mixins=True) -> list[SlotDefinitionName]:
        """
        All slotes that have no parents
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_slots(imports=imports)
                if self.slot_parents(c, mixins=mixins, imports=imports) == []]

    @lru_cache(None)
    def slot_leaves(self, imports=True, mixins=True) -> list[SlotDefinitionName]:
        """
        All slotes that have no children
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_slots(imports=imports)
                if self.slot_children(c, mixins=mixins, imports=imports) == []]

    @lru_cache(None)
    def is_multivalued(self, slot_name: SlotDefinition) -> bool:
        """
        returns True if slot is multivalued, else returns False
        :param slot_name: slot to test for multivalued
        :return boolean:
        """
        induced_slot = self.induced_slot(slot_name)
        return True if induced_slot.multivalued else False

    @lru_cache(None)
    def slot_is_true_for_metadata_property(self, slot_name: SlotDefinition, metadata_property: str) -> bool:
        """
        Returns true if the value of the provided "metadata_property" is True.  For example,
        sv.slot_is_true_for_metadata_property('id','identifier')
        will return True if the slot id has the identifier property set to True.

        :param slot_name: slot to test for multivalued
        :param metadata_property: controlled vocabulary for boolean attribtues
        :return: boolean
        """

        induced_slot = self.induced_slot(slot_name)
        if type(getattr(induced_slot, metadata_property)) == bool:
            return True if getattr(induced_slot, metadata_property) else False
        else:
            raise ValueError(f'property to introspect must be of type "boolean"')

    def get_element(self, element: Union[ElementName, Element], imports=True) -> Element:
        """
        Fetch an element by name

        :param element: query element
        :param imports: include imports closure
        :return:
        """
        if isinstance(element, Element):
            return element
        e = self.get_class(element, imports=imports)
        if e is None:
            e = self.get_slot(element, imports=imports)
        if e is None:
            e = self.get_type(element, imports=imports)
        if e is None:
            e = self.get_enum(element, imports=imports)
        if e is None:
            e = self.get_subset(element, imports=imports)
        return e

    def get_uri(self, element: Union[ElementName, Element], imports=True, expand=False, native=False, use_element_type=False) -> str:
        """
        Return the CURIE or URI for a schema element. If the schema defines a specific URI, this is
        used, otherwise this is constructed from the default prefix combined with the element name

        :param element: name of schema element
        :param imports: include imports closure
        :param native: return the native CURIE or URI rather than what is declared in the uri slot
        :param expand: expand the CURIE to a URI; defaults to False
        :return: URI or CURIE as a string
        """
        e = self.get_element(element, imports=imports)
        e_name = e.name
        if isinstance(e, ClassDefinition):
            uri = e.class_uri
            e_name = camelcase(e.name)
        elif isinstance(e, SlotDefinition):
            uri = e.slot_uri
            e_name = underscore(e.name)
        elif isinstance(e, TypeDefinition):
            uri = e.uri
            e_name = underscore(e.name)
        else:
            raise ValueError(f'Must be class or slot or type: {e}')
        if uri is None or native:
            if e.from_schema is not None:
                schema = next((sc for sc in self.schema_map.values() if sc.id == e.from_schema), None)
                if schema is None:
                    raise ValueError(f'Cannot find {e.from_schema} in schema_map')
            else:
                schema = self.schema_map[self.in_schema(e.name)]
            pfx = schema.default_prefix
            if use_element_type:
                e_type = e.class_name.split("_",1)[0]  # for example "class_definition"
                e_type_path = f"{e_type}/" 
            else:
                e_type_path = ""
            uri = f'{pfx}:{e_type_path}{e_name}'
        if expand:
            return self.expand_curie(uri)
        else:
            return uri

    def expand_curie(self, uri: str) -> str:
        """
        Expands a URI or CURIE to a full URI
        :param uri:
        :return: URI as a string
        """
        if ':' in uri:
            parts = uri.split(':')
            if len(parts) == 2:
                [pfx, local_id] = parts
                ns = self.namespaces()
                if pfx in ns:
                    return ns[pfx] + local_id
        return uri

    @lru_cache(CACHE_SIZE)
    def get_elements_applicable_by_identifier(self, identifier: str) -> list[str]:
        """
        Get a model element by identifier.  The model element corresponding to the given identifier as available via
        the id_prefixes mapped to that element.

        :param identifier:
        :return: Optional[str]

        """
        elements = self.get_elements_applicable_by_prefix(self.namespaces().prefix_for(identifier))
        if len(elements) == 0:
            logger.warning("no element found for the given curie using id_prefixes attribute"
                           ": %s, try get_mappings method?", identifier)
        return elements

    @lru_cache(CACHE_SIZE)
    def get_elements_applicable_by_prefix(self, prefix: str) -> list[str]:
        """
        Get a model element by prefix. The model element corresponding to the given prefix as available via
        the id_prefixes mapped to that element.

        :param prefix: the prefix of a CURIE
        :return: Optional[str]

        """
        applicable_elements = []
        elements = self.all_elements()
        for category, category_element in elements.items():
            if hasattr(category_element, 'id_prefixes') and prefix in category_element.id_prefixes:
                applicable_elements.append(category_element.name)

        return applicable_elements

    @lru_cache(None)
    def all_aliases(self) -> list[str]:
        """
        Get the aliases

        :return: list of aliases
        """
        element_aliases = {}

        for e, el in self.all_elements().items():
            if el.name not in element_aliases.keys():
                element_aliases[el.name] = []
            if el.aliases and el.aliases is not None:
                for a in el.aliases:
                    element_aliases[el.name].append(a)
            if el.structured_aliases and el.structured_aliases is not None:
                for sa in el.structured_aliases:
                    element_aliases[el.name].append(sa)

        return element_aliases

    @lru_cache(None)
    def get_mappings(self, element_name: ElementName = None, imports=True, expand=False) -> dict[
        MAPPING_TYPE, list[URIorCURIE]]:
        """
        Get all mappings for a given element

        :param element_name: the query element
        :param imports: include imports closure
        :param expand: expand CURIEs to URIs
        :return: index keyed by mapping type
        """
        e = self.get_element(element_name, imports=imports)
        if isinstance(e, ClassDefinition) or isinstance(e, SlotDefinition) or isinstance(e, TypeDefinition):
            m_dict = {
                'self': [self.get_uri(element_name, imports=imports, expand=False)],
                'native': [self.get_uri(element_name, imports=imports, expand=False, native=True)],
                'exact': e.exact_mappings,
                'narrow': e.narrow_mappings,
                'broad': e.broad_mappings,
                'related': e.related_mappings,
                'close': e.close_mappings,
                'undefined': e.mappings
            }
        else:
            m_dict = {}
        if expand:
            for k, vs in m_dict.items():
                m_dict[k] = [self.expand_curie(v) for v in vs]

        return m_dict

    @lru_cache(None)
    def is_mixin(self, element_name: Union[ElementName, Element]):
        """
        Determines whether the given name is the name of a mixin
        in the model. An element is a mixin if one of its properties is "is_mixin:true"

        :param element_name: The name or alias of an element in the model
        :return: boolean
        """

        element = self.get_element(element_name)
        is_mixin = element.mixin if isinstance(element, Definition) else False
        return is_mixin

    @lru_cache(None)
    def inverse(self, slot_name: SlotDefinition):
        """
        Determines whether the given name is a relationship, and if that relationship has an inverse, returns
        the inverse.

        :param slot_name: The name or alias of an element in the model
        :return: inverse_name

        """
        element = self.get_element(slot_name)
        inverse = element.inverse if isinstance(element, SlotDefinition) else False
        if not inverse:
            for inv_slot_name, slot_definition in self.all_slots().items():
                if slot_definition.inverse == element.name:
                    inverse = slot_definition.name
        return inverse

    def get_element_by_mapping(self, mapping_id: URIorCURIE) -> list[str]:
        model_elements = []
        elements = self.all_elements()
        for el in elements:
            element = self.get_element(el)
            mappings = element.exact_mappings + element.close_mappings + element.narrow_mappings + element.broad_mappings
            if mapping_id in mappings:
                model_elements.append(element.name)
        return model_elements

    def get_mapping_index(self, imports=True, expand=False) -> dict[URIorCURIE, list[tuple[MAPPING_TYPE, Element]]]:
        """
        Returns an index of all elements keyed by the mapping value.
        The index values are tuples of mapping type and element

        :param imports:
        :param expand: if true the index will be keyed by expanded URIs, not CURIEs
        :return: index
        """
        ix = defaultdict(list)
        for en in self.all_elements(imports=imports):
            for mapping_type, vs in self.get_mappings(en, imports=imports, expand=expand).items():
                for v in vs:
                    ix[v].append((mapping_type, self.get_element(en, imports=imports)))
        return ix

    @lru_cache(None)
    def is_relationship(self, class_name: CLASS_NAME = None, imports=True) -> bool:
        """
        Tests if a class represents a relationship or reified statement

        :param class_name:
        :param imports:
        :return: true if the class represents a relationship
        """
        STMT_TYPES = ['rdf:Statement', 'owl:Axiom']
        for an in self.class_ancestors(class_name, imports=imports):
            if self.get_uri(an) in STMT_TYPES:
                return True
            a = self.get_class(an, imports=imports)
            for m in a.exact_mappings:
                if m in STMT_TYPES:
                    return True
        return False

    @lru_cache(None)
    def annotation_dict(self, element_name: ElementName, imports=True) -> dict[URIorCURIE, Any]:
        """
        Return a dictionary where keys are annotation tags and values are annotation values for any given element.

        Note this will not include higher-order annotations

        See also: https://github.com/linkml/linkml/issues/296

        :param element_name:
        :param imports:
        :return: annotation dictionary
        """
        e = self.get_element(element_name, imports=imports)
        return {k: v.value for k, v in e.annotations.items()}

    @lru_cache(None)
    def class_slots(self, class_name: CLASS_NAME, imports=True, direct=False, attributes=True) -> list[
        SlotDefinitionName]:
        """
        :param class_name:
        :param imports: include imports closure
        :param direct: only returns slots directly associated with a class (default is False)
        :param attributes: include attribute declarations as well as slots (default is True)
        :return: all slot names applicable for a class
        """
        if direct:
            ancs = [class_name]
        else:
            ancs = self.class_ancestors(class_name, imports=imports)
        slots = []
        for an in ancs:
            a = self.get_class(an, imports)
            slots += a.slots
            if attributes:
                slots += a.attributes.keys()
        slots_nr = []
        for s in slots:
            if s not in slots_nr:
                slots_nr.append(s)
        return slots_nr

    @lru_cache(None)
    def induced_slot(self, slot_name: SLOT_NAME, class_name: CLASS_NAME = None, imports=True,
                     mangle_name=False) -> SlotDefinition:
        """
        Given a slot, in the context of a particular class, yield a dynamic SlotDefinition that
        has all properties materialized.

        This makes use of schema slots, such as attributes, slot_usage. It also uses ancestor relationships
        to infer missing values, for inheritable slots

        :param slot_name: slot to be queries
        :param class_name: class used as context
        :param imports: include imports closure
        :return: dynamic slot constructed by inference
        """
        if class_name:
            cls = self.get_class(class_name, imports, strict=True)
        else:
            cls = None

        # attributes take priority over schema-level slot definitions, IF
        # the attributes is declared for the class or an ancestor
        slot_comes_from_attribute = False
        if cls is not None:
            slot = self.get_slot(slot_name, imports, attributes=False)
            # traverse ancestors (reflexive), starting with
            # the main class
            for an in self.class_ancestors(class_name):
                a = self.get_class(an, imports)
                if slot_name in a.attributes:
                    slot = a.attributes[slot_name]
                    slot_comes_from_attribute = True
                    break
        else:
            slot = self.get_slot(slot_name, imports, attributes=True)

        if slot is None:
            raise ValueError(f"No such slot {slot_name} as an attribute of {class_name} ancestors "
                             "or as a slot definition in the schema")

        # copy the slot, as it will be modified
        induced_slot = copy(slot)
        if not slot_comes_from_attribute:
            slot_anc_names = self.slot_ancestors(slot_name, reflexive=True)
            # inheritable slot: first propagate from ancestors
            for anc_sn in reversed(slot_anc_names):
                anc_slot = self.get_slot(anc_sn, attributes=False)
                for metaslot_name in SlotDefinition._inherited_slots:
                    if getattr(anc_slot, metaslot_name, None):
                        setattr(induced_slot, metaslot_name, copy(getattr(anc_slot, metaslot_name)))
        COMBINE = {
            'maximum_value': lambda x, y: min(x, y),
            'minimum_value': lambda x, y: max(x, y),
        }
        # iterate through all metaslots, and potentially populate metaslot value for induced slot
        for metaslot_name in self._metaslots_for_slot():
            # inheritance of slots; priority order
            #   slot-level assignment < ancestor slot_usage < self slot_usage
            v = getattr(induced_slot, metaslot_name, None)
            if cls is None:
                propagated_from = []
            else:
                propagated_from = self.class_ancestors(class_name, reflexive=True, mixins=True)
            for an in reversed(propagated_from):
                induced_slot.owner = an
                a = self.get_class(an, imports)
                anc_slot_usage = a.slot_usage.get(slot_name, {})
                v2 = getattr(anc_slot_usage, metaslot_name, None)
                if v is None:
                    v = v2
                else:
                    if metaslot_name in COMBINE:
                        if v2 is not None:
                            v = COMBINE[metaslot_name](v, v2)
                    else:
                        # can rewrite below as:
                        # 1. if v2:
                        # 2. if v2 is not None and
                        #    (
                        #      (isinstance(v2, (dict, list)) and v2) or
                        #      (isinstance(v2, JsonObj) and as_dict(v2))
                        #    )
                        if not is_empty(v2):
                            v = v2
                            logger.debug(f'{v} takes precedence over {v2} for {induced_slot.name}.{metaslot_name}')
            if v is None:
                if metaslot_name == 'range':
                    v = self.schema.default_range
            if v is not None:
                setattr(induced_slot, metaslot_name, v)
        if slot.inlined_as_list:
            slot.inlined = True
        if slot.identifier or slot.key:
            slot.required = True
        if mangle_name:
            mangled_name = f'{camelcase(class_name)}__{underscore(slot_name)}'
            induced_slot.name = mangled_name
        if not induced_slot.alias:
            induced_slot.alias = underscore(slot_name)
        for c in self.all_classes().values():
            if induced_slot.name in c.slots or induced_slot.name in c.attributes:
                if c.name not in induced_slot.domain_of:
                    induced_slot.domain_of.append(c.name)
        return induced_slot

    @lru_cache(None)
    def _metaslots_for_slot(self):
        fake_slot = SlotDefinition('__FAKE')
        return vars(fake_slot).keys()

    @lru_cache(None)
    def class_induced_slots(self, class_name: CLASS_NAME = None, imports=True) -> list[SlotDefinition]:
        """
        All slots that are asserted or inferred for a class, with their inferred semantics

        :param class_name:
        :param imports:
        :return: inferred slot definition
        """
        return [self.induced_slot(sn, class_name, imports=imports) for sn in self.class_slots(class_name)]

    @lru_cache(None)
    def induced_class(self, class_name: CLASS_NAME = None) -> ClassDefinition:
        """
        Generate an induced class

        - the class will have no slots
        - the class will have one attribute per `class_induced_slots`

        Induced slots are represented as attributes as these are fully locally owner by the class
        :param class_name: base class name
        :param imports:
        :return: induced class
        """
        c = deepcopy(self.get_class(class_name))
        attrs = self.class_induced_slots(c.name)
        for a in attrs:
            c.attributes[a.name] = a
        c.slots = []
        return c

    @lru_cache(None)
    def induced_type(self, type_name: TYPE_NAME = None) -> TypeDefinition:
        """

        :param type_name:
        :return:
        """
        t = deepcopy(self.get_type(type_name))
        if t.typeof:
            parent = self.induced_type(t.typeof)
            if t.uri is None:
                t.uri = parent.uri
            if t.base is None:
                t.base = parent.base
            if t.repr is None:
                t.repr = parent.repr
        return t

    @lru_cache(None)
    def induced_enum(self, enum_name: ENUM_NAME = None) -> EnumDefinition:
        """

        :param enum_name:
        :return:
        """
        e = deepcopy(self.get_enum(enum_name))
        return e

    @lru_cache(None)
    def get_identifier_slot(self, cn: CLASS_NAME, use_key=False, imports=True) -> Optional[SlotDefinition]:
        """
        Find the slot that is the identifier for the given class

        :param cn: class name
        :param imports:
        :return: name of slot that acts as identifier
        """
        for sn in self.class_slots(cn, imports=imports):
            s = self.induced_slot(sn, cn, imports=imports)
            if s.identifier:
                return s
        if use_key:
            return self.get_key_slot(cn, imports=imports)
        else:
            return None

    @lru_cache(None)
    def get_key_slot(self, cn: CLASS_NAME, imports=True) -> Optional[SlotDefinition]:
        """
        Find the slot that is the key for the given class

        :param cn: class name
        :param imports:
        :return: name of slot that acts as key
        """
        for sn in self.class_slots(cn, imports=imports):
            s = self.induced_slot(sn, cn, imports=imports)
            if s.key:
                return s
        return None

    @lru_cache(None)
    def get_type_designator_slot(self, cn: CLASS_NAME, imports=True) -> Optional[SlotDefinition]:
        """
        :param cn: class name
        :param imports:
        :return: name of slot that acts as type designator for the given class
        """
        for sn in self.class_slots(cn, imports=imports):
            s = self.induced_slot(sn, cn, imports=imports)
            if s.designates_type:
                return s
        return None

    def is_inlined(self, slot: SlotDefinition, imports=True) -> bool:
        """
        True if slot is inferred or asserted inline

        :param slot:
        :param imports:
        :return:
        """
        range = slot.range
        if range in self.all_classes():
            if slot.inlined:
                return True
            elif slot.inlined_as_list:
                return True

            id_slot = self.get_identifier_slot(range, imports=imports)
            if id_slot is None:
                # must be inlined as has no identifier
                return True
            else:
                # not explicitly declared inline and has an identifier: assume is ref, not inlined
                return False
        else:
            return False

    def slot_applicable_range_elements(self, slot: SlotDefinition) -> list[ClassDefinitionName]:
        """
        Returns all applicable metamodel elements for a slot range
        (metamodel class names returned: class_definition, enum_definition, type_definition)

        Typically any given slot has exactly one range, and one metamodel element type,
        but a proposed feature in LinkML 1.2 is range expressions, where ranges can be defined as unions

        Additionally, if linkml:Any is a class_uri then this maps to the any element

        :param slot:
        :return: list of element types
        """
        is_any = False
        range_types = []
        for r in self.slot_range_as_union(slot):
            if r in self.all_classes():
                range_types.append(ClassDefinition.class_name)
                rc = self.get_class(r)
                if rc.class_uri == 'linkml:Any':
                    is_any = True
            if is_any or r in self.all_enums():
                range_types.append(EnumDefinition.class_name)
            if is_any or r in self.all_types():
                range_types.append(TypeDefinition.class_name)
        if not range_types:
            raise ValueError(f'Unrecognized range: {r}')
        return range_types

    def slot_range_as_union(self, slot: SlotDefinition) -> list[ElementName]:
        """
        Returns all applicable ranges for a slot

        Typically, any given slot has exactly one range, and one metamodel element type,
        but a proposed feature in LinkML 1.2 is range expressions, where ranges can be defined as unions

        :param slot:
        :return: list of ranges
        """
        r = slot.range
        range_union_of = [r]
        for x in slot.exactly_one_of + slot.any_of:
            if x.range:
                range_union_of.append(x.range)
        return range_union_of

    def get_classes_by_slot(
            self, slot: SlotDefinition, include_induced: bool = False
    ) -> list[ClassDefinitionName]:
        """Get all classes that use a given slot, either as a direct or induced slot.

        :param slot: slot in consideration
        :param include_induced: supplement all direct slots with induced slots, defaults to False
        :return: list of slots, either direct, or both direct and induced
        """
        classes_set = set()  # use set to avoid duplicates
        all_classes = self.all_classes()

        for c_name, c in all_classes.items():
            if slot.name in c.slots:
                classes_set.add(c_name)

        if include_induced:
            for c_name in all_classes:
                induced_slot_names = [
                    ind_slot.name for ind_slot in self.class_induced_slots(c_name)
                ]
                if slot.name in induced_slot_names:
                    classes_set.add(c_name)

        return list(classes_set)

    @lru_cache(None)
    def get_slots_by_enum(self, enum_name: ENUM_NAME = None) -> list[SlotDefinition]:
        """Get all slots that use a given enum: schema defined, attribute, or slot_usage.

        :param enum_name: enum in consideration
        :return: list of slots, either schem or both class attribute defined
        """
        enum_slots = []
        for s in self.all_slots().values():
            if s.range == enum_name and s not in enum_slots:
                enum_slots.append(s)
        for class_definition in self.all_classes().values():
            if class_definition.slot_usage:
                for slot_definition in class_definition.slot_usage.values():
                    if slot_definition.range == enum_name and slot_definition not in enum_slots:
                        enum_slots.append(slot_definition)
        return enum_slots

    def get_classes_modifying_slot(self, slot: SlotDefinition) -> list[ClassDefinition]:
        """Get all ClassDefinitions that modify a given slot.

        :param slot_name: slot in consideration
        :return: list of ClassDefinitions modifying the slot of interest
        """
        modifying_classes = []
        for class_definition in self.all_classes().values():
            if class_definition.slot_usage:
                for slot_definition in class_definition.slot_usage.values():
                    if slot_definition.name == slot.name:
                        modifying_classes.append(class_definition.name)

        return modifying_classes

    def is_slot_percent_encoded(self, slot: SlotDefinitionName) -> bool:
        """
        True if slot or its range is has a percent_encoded annotation.

        This is true for type fields that are the range of identifier columns,
        where the identifier is not guaranteed to be a valid URI or CURIE

        :param slot:
        :return:
        """
        if "percent_encoded" in slot.annotations:
            return True
        if slot.range in self.all_types():
            id_slot_ranges = self.type_ancestors(slot.range)
            for t in id_slot_ranges:
                anns = self.get_type(t).annotations
                return "percent_encoded" in anns

    @lru_cache(None)
    def usage_index(self) -> dict[ElementName, list[SchemaUsage]]:
        """
        Fetch an index that shows the ways in which each element is used

        :return: dictionary of SchemaUsages keyed by used elements
        """
        ROLES = ['domain', 'range', 'any_of', 'exactly_one_of', 'none_of', 'all_of']
        ix = defaultdict(list)
        for cn, c in self.all_classes().items():
            direct_slots = c.slots
            for sn in self.class_slots(cn):
                s = self.induced_slot(sn, cn)
                for k in ROLES:
                    v = getattr(s, k)
                    if isinstance(v, list):
                        vl = v
                    else:
                        vl = [v]
                    for x in vl:
                        if x is not None:
                            if isinstance(x, AnonymousSlotExpression):
                                x = x.range
                                k = f"{k}[range]"
                            k = k.split("[")[0] + "[range]" if "[range]" in k else k
                            u = SchemaUsage(used_by=cn, slot=sn, metaslot=k, used=x)
                            u.inferred = sn in direct_slots
                            ix[x].append(u)
        return ix

    # MUTATION OPERATIONS

    def add_class(self, cls: ClassDefinition) -> None:
        """
        :param cls: class to be added
        :return:
        """
        self.schema.classes[cls.name] = cls
        self.set_modified()

    def add_slot(self, slot: SlotDefinition) -> None:
        """
        :param slot: slot to be added
        :return:
        """
        self.schema.slots[slot.name] = slot
        self.set_modified()

    def add_enum(self, enum: EnumDefinition) -> None:
        """
        :param enum: enum to be added
        :return:
        """
        self.schema.enums[enum.name] = enum
        self.set_modified()

    def add_type(self, type: TypeDefinition) -> None:
        """
        :param type: type to be added
        :return:
        """
        self.schema.types[type.name] = type
        self.set_modified()

    def add_subset(self, subset: SubsetDefinition) -> None:
        """
        :param subset: subset to be added
        :return:
        """
        self.schema.subsets[subset.name] = type
        self.set_modified()

    def delete_class(self, class_name: ClassDefinitionName, delete_references=True) -> None:
        """
        :param class_name: class to be deleted
        :return:
        """
        children = self.class_children(class_name)
        del self.schema.classes[class_name]
        if delete_references:
            for chn in children:
                ch = self.get_class(chn)
                if ch.is_a is not None and ch.is_a == class_name:
                    del ch.is_a
                if class_name in ch.mixins:
                    ch.mixins.remove(class_name)
            # TODO: remove other references, including range
        self.set_modified()

    def delete_slot(self, slot_name: SlotDefinitionName) -> None:
        """
        :param slot_name: slot to be deleted
        :return:
        """
        del self.schema.slots[slot_name]
        self.set_modified()

    def delete_enum(self, enum_name: EnumDefinitionName) -> None:
        """
        :param enum_name: enum to be deleted
        :return:
        """
        del self.schema.enums[enum_name]
        self.set_modified()

    def delete_type(self, type_name: TypeDefinitionName) -> None:
        """
        :param type_name: type to be deleted
        :return:
        """
        del self.schema.types[type_name]
        self.set_modified()

    def delete_subset(self, subset_name: SubsetDefinitionName) -> None:
        """
        :param subset_name: subset to be deleted
        :return:
        """
        del self.schema.subsets[subset_name]
        self.set_modified()

    # def rename(self, old_name: str, new_name: str):
    #   todo: add to runtime

    def merge_schema(self, schema: SchemaDefinition, clobber=False) -> None:
        """
        merges another schema into this one.

        If the other schema has an element with the same name as an element in this schema,
        then this element is NOT copied.

        :param schema: schema to be merged
        :param clobber: if True, then overwrite existing elements
        """
        dest = self.schema
        for k, v in schema.prefixes.items():
            if clobber or k not in dest.prefixes:
                dest.prefixes[k] = copy(v)
        for k, v in schema.classes.items():
            if clobber or k not in dest.classes:
                dest.classes[k] = copy(v)
        for k, v in schema.slots.items():
            if clobber or k not in dest.slots:
                dest.slots[k] = copy(v)
        for k, v in schema.types.items():
            if clobber or k not in dest.types:
                dest.types[k] = copy(v)
        for k, v in schema.enums.items():
            if clobber or k not in dest.enums:
                dest.enums[k] = copy(v)
        for k, v in schema.subsets.items():
            if clobber or k not in dest.subsets:
                dest.subsets[k] = copy(v)
        self.set_modified()

    def merge_imports(self):
        """
        Merges the full imports closure

        :return:
        """
        schema = self.schema
        to_merge = [s2 for s2 in self.all_schema(imports=True) if s2 != schema]
        for s2 in to_merge:
            self.merge_schema(s2)
        schema.imports = []
        self.set_modified()

    def copy_schema(self, new_name: str = None) -> SchemaDefinition:
        s2 = copy(self.schema)
        if new_name is not None:
            s2.name = new_name
        return s2

    def set_modified(self) -> None:
        self._hash = None
        self.modifications += 1

    def materialize_patterns(self) -> None:
        """Materialize schema by expanding structured patterns 
        into regular expressions based on composite patterns 
        provided in the settings dictionary.
        """
        resolver = PatternResolver(self)

        def materialize_pattern_into_slot_definition(slot_definition: SlotDefinition) -> None:
            if not slot_definition.structured_pattern:
                return
            pattern = slot_definition.structured_pattern.syntax
            slot_definition.pattern = resolver.resolve(pattern)

        for slot_definition in self.all_slots().values():
            materialize_pattern_into_slot_definition(slot_definition)

        for class_definition in self.all_classes().values():
            if class_definition.slot_usage:
                for slot_definition in class_definition.slot_usage.values():
                    materialize_pattern_into_slot_definition(slot_definition)

            if class_definition.attributes:
                for slot_definition in class_definition.attributes.values():
                    materialize_pattern_into_slot_definition(slot_definition)

    def materialize_derived_schema(self) -> SchemaDefinition:
        """ Materialize a schema view into a schema definition """
        derived_schema = deepcopy(self.schema)
        derived_schemaview = SchemaView(derived_schema)
        derived_schemaview.merge_imports()
        for typ in [deepcopy(t) for t in self.all_types().values()]:
            for typ_anc_name in self.type_ancestors(typ.name, reflexive=False):
                a = derived_schema.types[typ_anc_name]
                if not typ.uri:
                    typ.uri = a.uri
                if not typ.base:
                    typ.base = a.base
                if not typ.pattern:
                    typ.pattern = a.pattern
            derived_schema.types[typ.name] = typ
        for cls in [deepcopy(c) for c in self.all_classes().values()]:
            for slot in self.class_induced_slots(cls.name):
                slot_range_element = self.get_element(slot.range)
                if isinstance(slot_range_element, TypeDefinition):
                    for metaslot in ["pattern", "maximum_value", "minimum_value"]:
                        metaslot_val = getattr(slot_range_element, metaslot, None)
                        if metaslot_val is not None:
                            setattr(slot, metaslot, metaslot_val)
                slot_range_pk_slot_name = None
                if isinstance(slot_range_element, ClassDefinition):
                    slot_range_pk_slot_name = self.get_identifier_slot(slot_range_element.name, use_key=True)
                if not slot_range_pk_slot_name:
                    slot.inlined = True
                    slot.inlined_as_list = True
                if slot.inlined_as_list:
                    slot.inlined = True
                if slot.identifier or slot.key:
                    slot.required = True
                cls.attributes[slot.name] = slot
            derived_schema.classes[cls.name] = cls
        for subset in [deepcopy(s) for s in self.all_subsets().values()]:
            derived_schema.subsets[subset.name] = subset
        for enum in [deepcopy(e) for e in self.all_enums().values()]:
            derived_schema.enums[enum.name] = enum
        return derived_schema
