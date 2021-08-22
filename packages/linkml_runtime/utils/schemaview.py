import os
import uuid
import logging
from functools import lru_cache
from copy import copy
from collections import defaultdict
from typing import List, Any, Dict, Union, Mapping
from dataclasses import dataclass
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.formatutils import camelcase, underscore


from linkml_runtime.utils.context_utils import parse_import_map
from linkml_runtime.linkml_model.meta import *
from linkml_runtime.linkml_model.annotations import Annotation, Annotatable


CACHE_SIZE = 1024


SLOTS = 'slots'
CLASSES = 'classes'
ENUMS = 'enums'
SUBSETS = 'subsets'
TYPES = 'types'

CLASS_NAME = Union[ClassDefinitionName, str]
SLOT_NAME = Union[SlotDefinitionName, str]
SUBSET_NAME = Union[SubsetDefinitionName, str]
TYPE_NAME = Union[TypeDefinitionName, str]
ENUM_NAME = Union[EnumDefinitionName, str]

def _closure(f, x, reflexive=True, **kwargs):
    if reflexive:
        rv = [x]
    else:
        rv = []
    visited = []
    todo = [x]
    while len(todo) > 0:
        i = todo.pop()
        visited.append(i)
        vals = f(i)
        for v in vals:
            if v not in visited:
                todo.append(v)
                rv.append(v)
    return rv

def load_schema_wrap(path: str, **kwargs):
    # import here to avoid circular imports
    from linkml_runtime.loaders.yaml_loader import YAMLLoader
    yaml_loader = YAMLLoader()
    schema: SchemaDefinition
    schema = yaml_loader.load(path, target_class=SchemaDefinition, **kwargs)
    schema.source_file = path
    return schema

@dataclass
class SchemaUsage():
    """
    A usage of an element of a schema
    """
    used_by: ElementName
    slot: SlotDefinitionName
    metaslot: SlotDefinitionName
    used: ElementName


@dataclass
class SchemaView(object):
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
    schema_map: Dict[SchemaDefinitionName, SchemaDefinition] = None
    importmap: Optional[Mapping[str, str]] = None
    modifications: int = 0
    uuid: str = None


    def __init__(self, schema: Union[str, SchemaDefinition],
                 importmap: Optional[Mapping[str, str]] = None):
        if isinstance(schema, str):
            schema = load_schema_wrap(schema)
        self.schema = schema
        self.schema_map = {schema.name: schema}
        self.importmap = parse_import_map(importmap, self.base_dir) if self.importmap is not None else dict()
        self.uuid = str(uuid.uuid4())

    def __key(self):
        return (self.schema.id, self.uuid, self.modifications)

    def __eq__(self, other):
        if isinstance(other, SchemaView):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    @lru_cache()
    def namespaces(self) -> Namespaces:
        namespaces = Namespaces()
        for s in self.schema_map.values():
            for prefix in s.prefixes.values():
                namespaces[prefix.prefix_prefix] = prefix.prefix_reference
            for cmap in self.schema.default_curi_maps:
                namespaces.add_prefixmap(cmap, include_defaults=False)
        return namespaces


    def load_import(self, imp: str, from_schema: SchemaDefinition = None):
        if from_schema is None:
            from_schema = self.schema
        # TODO: this code is copied from linkml.utils.schemaloader; put this somewhere reusable
        sname = self.importmap.get(str(imp), imp)               # Import map may use CURIE
        sname = self.namespaces().uri_for(sname) if ':' in sname else sname
        sname = self.importmap.get(str(sname), sname)               # It may also use URI or other forms
        print(f'Loading schema {sname} from {from_schema.source_file}')
        schema = load_schema_wrap(sname + '.yaml',
                                  base_dir=os.path.dirname(from_schema.source_file) if from_schema.source_file else None)
        return schema

    @lru_cache()
    def imports_closure(self, traverse=True) -> List[SchemaDefinitionName]:
        """
        Return all imports

        :param traverse: if true, traverse recursively
        :return: all schema names in the transitive reflexive imports closure
        """
        if self.schema_map is None:
            self.schema_map = {self.schema.name: self.schema}
        closure = []
        visited = set()
        todo = [self.schema.name]
        if not traverse:
            return todo
        while len(todo) > 0:
            sn = todo.pop()
            visited.add(sn)
            if sn not in self.schema_map:
                imported_schema = self.load_import(sn)
                self.schema_map[sn] = imported_schema
            s = self.schema_map[sn]
            if sn not in closure:
                closure.append(sn)
            for i in s.imports:
                if i not in visited:
                    todo.append(i)
        return closure

    @lru_cache()
    def all_schema(self, imports: True) -> List[SchemaDefinition]:
        """
        :param imports: include imports closure
        :return: all schemas
        """
        m = self.schema_map
        return [m[sn] for sn in self.imports_closure(imports)]

    @lru_cache()
    def all_class(self, imports=True) -> Dict[ClassDefinitionName, ClassDefinition]:
        """
        :param imports: include imports closure
        :return: all classes in schema view
        """
        return self._get_dict(CLASSES, imports)

    @lru_cache()
    def all_slot(self, imports=True) -> Dict[SlotDefinitionName, SlotDefinition]:
        """
        :param imports: include imports closure
        :return: all slots in schema view
        """
        return self._get_dict(SLOTS, imports)

    @lru_cache()
    def all_enum(self, imports=True) -> Dict[EnumDefinitionName, EnumDefinition]:
        """
        :param imports: include imports closure
        :return: all enums in schema view
        """
        return self._get_dict(ENUMS, imports)

    @lru_cache()
    def all_type(self, imports=True) -> Dict[TypeDefinitionName, TypeDefinition]:
        """
        :param imports: include imports closure
        :return: all types in schema view
        """
        return self._get_dict(TYPES, imports)

    @lru_cache()
    def all_subset(self, imports=True) -> Dict[SubsetDefinitionName, SubsetDefinition]:
        """
        :param imports: include imports closure
        :return: all subsets in schema view
        """
        return self._get_dict(SUBSETS, imports)

    @lru_cache()
    def all_element(self, imports=True) -> Dict[ElementName, Element]:
        """
        :param imports: include imports closure
        :return: all elements in schema view
        """
        all_c = self.all_class(imports)
        all_s = self.all_slot(imports)
        all_e = self.all_enum(imports)
        all_t = self.all_type(imports)
        all_v = self.all_subset(imports)
        return {**all_c, **all_s, **all_e, **all_t, **all_v}

    def _get_dict(self, slot_name: str, imports=True) -> Dict:
        schemas = self.all_schema(imports)
        d = {}
        for s in schemas:
            d1 = getattr(s, slot_name, {})
            d = {**d, **d1}
        return d

    @lru_cache()
    def in_schema(self, element_name: ElementName) -> SchemaDefinitionName:
        """
        :param element_name:
        :return: name of schema in which element is defined
        """
        ix = self.element_by_schema_map()
        return ix[element_name]

    @lru_cache()
    def element_by_schema_map(self) -> Dict[ElementName, SchemaDefinitionName]:
        ix = {}
        schemas = self.all_schema(True)
        for schema in schemas:
            for type_key in [CLASSES, SLOTS, TYPES, ENUMS, SUBSETS]:
                for k, v in getattr(schema, type_key, {}).items():
                    ix[k] = schema.name
        return ix

    @lru_cache()
    def get_class(self, class_name: CLASS_NAME, imports=True) -> ClassDefinition:
        """
        :param class_name: name of the class to be retrieved
        :param imports: include import closure
        :return: class definition
        """
        return self.all_class(imports).get(class_name, None)

    @lru_cache()
    def get_slot(self, slot_name: SLOT_NAME, imports=True, attributes=False) -> SlotDefinition:
        """
        :param slot_name: name of the slot to be retrieved
        :param imports: include import closure
        :return: slot definition
        """
        slot = self.all_slot(imports).get(slot_name, None)
        if slot is None and attributes:
            for c in self.all_class(imports).values():
                if slot_name in c.attributes:
                    if slot is not None:
                        # slot name is ambiguous, no results
                        return None
                    slot = c.attributes[slot_name]
        return slot

    @lru_cache()
    def get_subset(self, subset_name: SUBSET_NAME, imports=True) -> SubsetDefinition:
        """
        :param subset_name: name of the subsey to be retrieved
        :param imports: include import closure
        :return: subset definition
        """
        return self.all_subset(imports).get(subset_name, None)

    @lru_cache()
    def get_enum(self, enum_name: ENUM_NAME, imports=True) -> EnumDefinition:
        """
        :param enum_name: name of the enum to be retrieved
        :param imports: include import closure
        :return: enum definition
        """
        return self.all_enum(imports).get(enum_name, None)

    @lru_cache()
    def get_type(self, type_name: TYPE_NAME, imports=True) -> TypeDefinition:
        """
        :param type_name: name of the type to be retrieved
        :param imports: include import closure
        :return: type definition
        """
        return self.all_type(imports).get(type_name, None)

    def _parents(self, e: Element, imports=True, mixins=True) -> List[ElementName]:
        if mixins:
            parents = copy(e.mixins)
        else:
            parents = []
        if e.is_a is not None:
            parents.append(e.is_a)
        return parents

    @lru_cache()
    def class_parents(self, class_name: CLASS_NAME, imports=True, mixins=True) -> List[ClassDefinitionName]:
        """
        :param class_name: child class name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct parent class names (is_a and mixins)
        """
        cls = self.get_class(class_name, imports)
        return self._parents(cls, imports, mixins)

    @lru_cache()
    def slot_parents(self, slot_name: SLOT_NAME, imports=True, mixins=True) -> List[SlotDefinitionName]:
        """
        :param slot_name: child slot name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct parent slot names (is_a and mixins)
        """
        s = self.get_slot(slot_name, imports)
        return self._parents(s, imports, mixins)

    @lru_cache()
    def class_children(self, class_name: CLASS_NAME, imports=True, mixins=True) -> List[ClassDefinitionName]:
        """
        :param class_name: parent class name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct child class names (is_a and mixins)
        """
        elts = [self.get_class(x) for x in self.all_class(imports)]
        return [x.name for x in elts if x.is_a == class_name or (mixins and class_name in x.mixins)]

    @lru_cache()
    def slot_children(self, slot_name: SLOT_NAME, imports=True, mixins=True) -> List[SlotDefinitionName]:
        """
        :param slot_name: parent slot name
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :return: all direct child slot names (is_a and mixins)
        """
        elts = [self.get_slot(x) for x in self.all_slot(imports)]
        return [x.name for x in elts if x.is_a == slot_name or (mixins and slot_name in x.mixins)]

    @lru_cache()
    def class_ancestors(self, class_name: CLASS_NAME, imports=True, mixins=True, reflexive=True) -> List[ClassDefinitionName]:
        """
        Closure of class_parents method

        :param class_name: query class
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param reflexive: include self in set of ancestors
        :return: ancestor class names
        """
        return _closure(lambda x: self.class_parents(x, imports=imports, mixins=mixins), class_name, reflexive=reflexive)

    @lru_cache()
    def slot_ancestors(self, slot_name: SLOT_NAME, imports=True, mixins=True, reflexive=True) -> List[SlotDefinitionName]:
        """
        Closure of slot_parents method

        :param slot_name: query slot
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param reflexive: include self in set of ancestors
        :return: ancestor slot names
        """
        return _closure(lambda x: self.slot_parents(x, imports=imports, mixins=mixins), slot_name, reflexive=reflexive)

    @lru_cache()
    def class_descendants(self, class_name: CLASS_NAME, imports=True, mixins=True, reflexive=True) -> List[ClassDefinitionName]:
        """
        Closure of class_children method

        :param class_name: query class
        :param imports: include import closure
        :param mixins: include mixins (default is True)
        :param reflexive: include self in set of descendants
        :return: descendants class names
        """
        return _closure(lambda x: self.class_children(x, imports=imports, mixins=mixins), class_name, reflexive=reflexive)


    @lru_cache()
    def class_roots(self, class_name: CLASS_NAME, imports=True, mixins=True) -> List[ClassDefinitionName]:
        """
        All classes that have no parents
        :param class_name:
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_class(imports=imports)
                if self.class_parents(c, mixins=mixins, imports=imports) == []]

    @lru_cache()
    def class_leaves(self, class_name: CLASS_NAME, imports=True, mixins=True) -> List[ClassDefinitionName]:
        """
        All classes that have no children
        :param class_name:
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_class(imports=imports)
                if self.class_children(c, mixins=mixins, imports=imports) == []]


    @lru_cache()
    def slot_roots(self, slot_name: SLOT_NAME, imports=True, mixins=True) -> List[SlotDefinitionName]:
        """
        All slotes that have no parents
        :param slot_name:
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_slot(imports=imports)
                if self.slot_parents(c, mixins=mixins, imports=imports) == []]

    @lru_cache()
    def slot_leaves(self, slot_name: SLOT_NAME, imports=True, mixins=True) -> List[SlotDefinitionName]:
        """
        All slotes that have no children
        :param slot_name:
        :param imports:
        :param mixins:
        :return:
        """
        return [c
                for c in self.all_slot(imports=imports)
                if self.slot_children(c, mixins=mixins, imports=imports) == []]


    def get_element(self, element: Union[ElementName, Element], imports=True) -> Element:
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


    def get_uri(self, element: Union[ElementName, Element], imports=True, expand=False, native=False) -> str:
        """
        Return the CURIE or URI for a schema element. If the schema defines a specific URI, this is
        used, otherwise this is constructed from the default prefix combined with the element name

        :param element_name: name of schema element
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
            raise Exception(f'Must be class or slot or type: {e}')
        if uri is None or native:
            schema = self.schema_map[self.in_schema(e.name)]
            ns = self.namespaces()
            pfx = schema.default_prefix
            uri = f'{pfx}:{e_name}'
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

    @lru_cache()
    def get_mappings(self, element_name: ElementName = None, imports=True, expand=False) -> Dict[str, List[URIorCURIE]]:
        e = self.get_element(element_name, imports=imports)
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
        if expand:
            for k, vs in m_dict.items():
                m_dict[k] = [self.expand_curie(v) for v in vs]

        return m_dict


    @lru_cache()
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

    @lru_cache()
    def annotation_dict(self, element_name: ElementName, imports=True) -> Dict[URIorCURIE, Any]:
        """
        Return a dictionary where keys are annotation tags and values are annotation values for any given element.

        Note this will not include higher-order annotations

        :param element_name:
        :param imports:
        :return: annotation dictionary
        """
        e = self.get_element(element_name, imports=imports)
        return {k: v.value for k, v in e.annotations.items()}


    @lru_cache()
    def class_slots(self, class_name: CLASS_NAME = None, imports=True, direct=False, attributes=True) -> List[SlotDefinitionName]:
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

    @lru_cache()
    def induced_slot(self, slot_name: SLOT_NAME, class_name: CLASS_NAME = None, imports=True) -> SlotDefinition:
        """
        Given a slot, in the context of a particular class, yield a dynamic SlotDefinition that
        has all properties materialized.

        This makes use of schema slots, such as attributes, slot_usage. It also uses ancestor relationships
        to infer missing values

        :param slot_name: slot to be queries
        :param class_name: class used as context
        :param imports: include imports closure
        :return: dynamic slot constructed by inference
        """
        slot = self.get_slot(slot_name, imports)
        cls = self.get_class(class_name, imports)
        islot = None
        if slot is not None:
            islot = copy(slot)
        else:
            for an in self.class_ancestors(class_name):
                a = self.get_class(an, imports)
                if slot_name in a.attributes:
                    islot = copy(a.attributes[slot_name])
                    break
        if islot is None:
            raise Exception(f'No such slot: {slot_name} and no attribute by that name in ancestors of {class_name}')

        COMBINE = {
            'maximum_value': lambda x, y: min(x, y),
            'minimum_value': lambda x, y: max(x, y),
        }
        for metaslot_name in SlotDefinition._inherited_slots:
            v = getattr(islot, metaslot_name, None)
            for an in self.class_ancestors(class_name):
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
                        break
            if v is None:
                if metaslot_name == 'range':
                    v = self.schema.default_range
            if v is not None:
                setattr(islot, metaslot_name, v)
        return islot

    @lru_cache()
    def get_identifier_slot(self, cn: CLASS_NAME, imports=True) -> Optional[SlotDefinition]:
        """
        :param cn: class name
        :param imports:
        :return: the slot that acts as identifier
        """
        for sn in self.class_slots(cn, imports=imports):
            s = self.induced_slot(sn, cn, imports=imports)
            if s.identifier:
                return s
        return None

    def is_inlined(self, slot: SlotDefinition, imports=True) -> bool:
        """
        True if slot is inferred or asserted inline
        
        :param slot:
        :param imports:
        :return:
        """
        if slot.inlined:
            return True
        else:
            range = slot.range
            id_slot = self.get_identifier_slot(range, imports=imports)
            if id_slot is None:
                # must be inlined as has no identifier
                return True
            else:
                # not explicitly declared inline and has an identifier: assume is ref, not inlined
                return False

    @lru_cache()
    def usage_index(self) -> Dict[ElementName, List[SchemaUsage]]:
        """
        :return: dictionary keyed by used elements
        """
        ROLES = ['domain', 'range']
        ix = defaultdict(list)
        for cn, c in self.all_class().items():
            for sn in self.class_slots(cn):
                s = self.induced_slot(sn, cn)
                for k in ROLES:
                    v = getattr(s, k)
                    if isinstance(v, list):
                        vl = v
                    else:
                        vl = [v]
                    for x in vl:
                        u = SchemaUsage(used_by=cn, slot=sn, metaslot=k, used=x)
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

    def delete_class(self, class_name: ClassDefinitionName) -> None:
        """
        :param class_name: class to be deleted
        :return:
        """
        del self.schema.classes[class_name]
        self.set_modified()

    def delete_slot(self, slot_name: SlotDefinitionName) -> None:
        """
        :param slot_name: slot to be deleted
        :return:
        """
        del self.schema.slotes[slot_name]
        self.set_modified()

    def delete_enum(self, enum_name: EnumDefinitionName) -> None:
        """
        :param enum_name: enum to be deleted
        :return:
        """
        del self.schema.enumes[enum_name]
        self.set_modified()

    def delete_type(self, type_name: TypeDefinitionName) -> None:
        """
        :param type_name: type to be deleted
        :return:
        """
        del self.schema.typees[type_name]
        self.set_modified()

    def delete_subset(self, subset_name: SubsetDefinitionName) -> None:
        """
        :param subset_name: subset to be deleted
        :return:
        """
        del self.schema.subsetes[subset_name]
        self.set_modified()

    def merge_schema(self, schema: SchemaDefinition) -> None:
        """
        merges another schema into this one
        :param schema: schema to be merged
        """
        dest = self.schema
        for k, v in schema.prefixes.items():
            if k not in dest.prefixes:
                dest.prefixes[k] = copy(y)
        for k, v in schema.classes.items():
            if k not in dest.classes:
                dest.classes[k] = copy(y)
        for k, v in schema.slots.items():
            if k not in dest.slots:
                dest.slots[k] = copy(y)
        for k, v in schema.types.items():
            if k not in dest.types:
                dest.types[k] = copy(y)
        for k, v in schema.enums.items():
            if k not in dest.types:
                dest.enums[k] = copy(y)
        self.set_modified()




    def set_modified(self) -> None:
        self.modifications += 1
