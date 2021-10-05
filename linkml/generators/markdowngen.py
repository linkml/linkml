import os
from contextlib import redirect_stdout
from io import StringIO
from typing import Union, TextIO, Optional, Set, List, Any, Callable, Dict

import click
from jsonasobj2 import JsonObj, values

from linkml.generators.yumlgen import YumlGenerator
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Element, ClassDefinitionName, \
    TypeDefinition, EnumDefinition, SubsetDefinition
from linkml_runtime.utils.formatutils import camelcase, be, underscore
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.typereferences import References


class MarkdownGenerator(Generator):
    """
    Generates markdown documentation for a LinkML schema

    Each schema element (class, slot, type, enum) is translated into its own markdown file;
    additionally, an index.md is generated that links everything together.

    The markdown is suitable for deployment as a MkDocs or Sphinx site
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.1"
    directory_output = True
    valid_formats = ["md"]
    visit_all_class_slots = False

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], no_types_dir: bool = False,
                 noyuml: bool = False, warn_on_exist:bool = False, **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.directory: Optional[str] = None
        self.image_directory: Optional[str] = None
        self.noimages: bool = False
        self.noyuml = noyuml
        self.no_types_dir = no_types_dir
        self.warn_on_exist = warn_on_exist
        self.gen_classes: Optional[Set[ClassDefinitionName]] = None
        self.gen_classes_neighborhood: Optional[References] = None
        self.BASE = None

    def visit_schema(self, directory: str = None, classes: Set[ClassDefinitionName] = None, image_dir: bool = False,
                     index_file: str = 'index.md',
                     noimages: bool = False, **_) -> None:
        self.gen_classes = classes if classes else []
        for cls in self.gen_classes:
            if cls not in self.schema.classes:
                raise ValueError("Unknown class name: {cls}")
        if self.gen_classes:
            self.gen_classes_neighborhood = self.neighborhood(list(self.gen_classes))

        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)
        elif image_dir:
            raise ValueError(f"Image directory can only be used with '-d' option")
        if image_dir:
            self.image_directory = os.path.join(directory, 'images')
            if not noimages:
                os.makedirs(self.image_directory, exist_ok=True)
        self.noimages = noimages
        if not self.no_types_dir:
            os.makedirs(os.path.join(directory, 'types'), exist_ok=True)

        with open(self.exist_warning(directory, index_file), 'w') as ixfile:
            with redirect_stdout(ixfile):
                self.frontmatter(f"{self.schema.name} schema")
                self.para(be(self.schema.description))

                self.header(3, 'Classes')
                for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
                    if not cls.is_a and not cls.mixin and self.is_secondary_ref(cls.name):
                        self.class_hier(cls)

                self.header(3, 'Mixins')
                for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
                    if cls.mixin and self.is_secondary_ref(cls.name):
                        self.class_hier(cls)

                self.header(3, 'Slots')
                for slot in sorted(self.schema.slots.values(), key=lambda s: s.name):
                    if not slot.is_a and self.is_secondary_ref(slot.name):
                        self.pred_hier(slot)

                self.header(3, 'Enums')
                for enu in sorted(self.schema.enums.values(), key=lambda e: e.name):
                    self.enum_hier(enu)

                self.header(3, 'Subsets')
                for subset in sorted(self.schema.subsets.values(), key=lambda s: s.name):
                    self.bullet(self.subset_link(subset, use_desc=True), 0)

                self.header(3, 'Types')
                self.header(4, 'Built in')
                for builtin_name in sorted(self.synopsis.typebases.keys()):
                    self.bullet(f'**{builtin_name}**')
                self.header(4, 'Defined')
                for typ in sorted(self.schema.types.values(), key=lambda t: t.name):
                    if self.is_secondary_ref(typ.name):
                        if typ.typeof:
                            typ_typ = self.type_link(typ.typeof)
                        else:
                            typ_typ = f'**{typ.base}**'

                        self.bullet(self.type_link(typ, after_link=f' ({typ_typ})', use_desc=True))

    def visit_class(self, cls: ClassDefinition) -> bool:

        # allow client to relabel metamodel
        mixin_local_name = self.get_metamodel_slot_name('Mixin')
        class_local_name = self.get_metamodel_slot_name('Class')

        if self.gen_classes and cls.name not in self.gen_classes:
            return False

        with open(self.exist_warning(self.dir_path(cls)), 'w') as clsfile:
            with redirect_stdout(clsfile):
                class_curi = self.namespaces.uri_or_curie_for(self.namespaces._base, camelcase(cls.name))
                class_uri = self.namespaces.uri_for(class_curi)
                self.element_header(cls, cls.name, class_curi, class_uri)
                print()
                if not self.noyuml:
                    if self.image_directory:
                        yg = YumlGenerator(self)
                        yg.serialize(classes=[cls.name], directory=self.image_directory, load_image=not self.noimages)
                        img_url = os.path.join('images', os.path.basename(yg.output_file_name))
                    else:
                        yg = YumlGenerator(self)
                        img_url = yg.serialize(classes=[cls.name])\
                            .replace('?', '%3F').replace(' ', '%20').replace('|', '&#124;')

                    print(f'[![img]({img_url})]({img_url})')

                self.mappings(cls)



                if cls.id_prefixes:
                    self.header(2, 'Identifier prefixes')
                    for p in cls.id_prefixes:
                        self.bullet(f'{p}')

                if cls.is_a is not None:
                    self.header(2, 'Parents')
                    self.bullet(f' is_a: {self.class_link(cls.is_a, use_desc=True)}')
                if cls.mixins:
                    self.header(2, f'Uses {mixin_local_name}')
                    for mixin in cls.mixins:
                        self.bullet(f' mixin: {self.class_link(mixin, use_desc=True)}')

                if cls.name in self.synopsis.isarefs:
                    self.header(2, 'Children')
                    for child in sorted(self.synopsis.isarefs[cls.name].classrefs):
                        self.bullet(f'{self.class_link(child, use_desc=True)}')

                if cls.name in self.synopsis.mixinrefs:
                    self.header(2, f'{mixin_local_name} for')
                    for mixin in sorted(self.synopsis.mixinrefs[cls.name].classrefs):
                        self.bullet(f'{self.class_link(mixin, use_desc=True, after_link="(mixin)")}')

                if cls.name in self.synopsis.classrefs:
                    self.header(2, f'Referenced by {class_local_name}')
                    for sn in sorted(self.synopsis.classrefs[cls.name].slotrefs):
                        slot = self.schema.slots[sn]
                        if slot.range == cls.name:
                            self.bullet(f' **{self.class_link(slot.domain)}** '
                                        f'*{self.slot_link(slot, add_subset=False)}*{self.predicate_cardinality(slot)}  '
                                        f'**{self.class_type_link(slot.range)}**')

                self.header(2, 'Attributes')

                # List all of the slots that directly belong to the class
                slot_list = [slot for slot in [self.schema.slots[sn] for sn in cls.slots]]
                own_slots = [slot for slot in slot_list if cls.name in slot.domain_of]
                if own_slots:
                    self.header(3, 'Own')
                    for slot in own_slots:
                        self.slot_field(cls, slot)
                        slot_list.remove(slot)

                # List all of the inherited slots
                ancestors = set(self.ancestors(cls))
                inherited_slots = [slot for slot in slot_list if set(slot.domain_of).intersection(ancestors)]
                if inherited_slots:
                    self.header(3, "Inherited from " + cls.is_a + ':')
                    for inherited_slot in inherited_slots:
                        self.slot_field(cls, inherited_slot)
                        slot_list.remove(inherited_slot)

                # List all of the slots acquired through mixing
                mixed_in_classes = set()
                for mixin in cls.mixins:
                    mixed_in_classes.add(mixin)
                    mixed_in_classes.update(set(self.ancestors(self.schema.classes[mixin])))
                for slot in slot_list:
                    mixers = set(slot.domain_of).intersection(mixed_in_classes)
                    for mixer in mixers:
                        self.header(3, "Mixed in from " + mixer + ':')
                        self.slot_field(cls, slot)

                self.element_properties(cls)

        return False

    def visit_type(self, typ: TypeDefinition) -> None:
        with open(self.exist_warning(self.dir_path(typ)), 'w') as typefile:
            with redirect_stdout(typefile):
                type_uri = typ.definition_uri
                type_curie = self.namespaces.curie_for(type_uri)
                self.element_header(typ, typ.name, type_curie, type_uri)

                print("|  |  |  |")
                print("| --- | --- | --- |")
                if typ.typeof:
                    print(f"| Parent type | | {self.class_type_link(typ.typeof)} |")
                print(f"| Root (builtin) type | | **{typ.base}** |")
                if typ.repr:
                    print(f"| Representation | | {typ.repr} |")
                self.element_properties(typ)

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        with open(self.exist_warning(self.dir_path(slot)), 'w') as slotfile:
            with redirect_stdout(slotfile):
                slot_curie = self.namespaces.uri_or_curie_for(self.namespaces._base, underscore(slot.name))
                slot_uri = self.namespaces.uri_for(slot_curie)
                self.element_header(slot,aliased_slot_name, slot_curie, slot_uri)
                self.mappings(slot)

                self.header(2, 'Domain and Range')
                print(f'{self.class_link(slot.domain)} &#8594;{self.predicate_cardinality(slot)} '
                      f'{self.class_type_link(slot.range)}')

                self.header(2, 'Parents')
                if slot.is_a:
                    self.bullet(f' is_a: {self.slot_link(slot.is_a)}')

                self.header(2, 'Children')
                if slot.name in sorted(self.synopsis.isarefs):
                    for child in sorted(self.synopsis.isarefs[slot.name].slotrefs):
                        self.bullet(f' {self.slot_link(child)}')

                self.header(2, 'Used by')
                if slot.name in sorted(self.synopsis.slotrefs):
                    for rc in sorted(self.synopsis.slotrefs[slot.name].classrefs):
                        self.bullet(f'{self.class_link(rc)}')
                if aliased_slot_name == 'relation':
                    if slot.subproperty_of:
                        self.bullet(f' reifies: {self.slot_link(slot.subproperty_of) if slot.subproperty_of in self.schema.slots else slot.subproperty_of}')
                self.element_properties(slot)

    def visit_enum(self, enum: EnumDefinition) -> None:
        with open(self.exist_warning(self.dir_path(enum)), 'w') as enumfile:
            with redirect_stdout(enumfile):
                enum_curie = self.namespaces.uri_or_curie_for(self.namespaces._base, underscore(enum.name))
                enum_uri = self.namespaces.uri_for(enum_curie)
                self.element_header(obj=enum, name=enum.name, curie=enum_curie, uri=enum_uri)
                self.element_properties(enum)

    def visit_subset(self, subset: SubsetDefinition) -> None:
        with open(self.exist_warning(self.dir_path(subset)), 'w') as subsetfile:
            with redirect_stdout(subsetfile):
                curie = self.namespaces.uri_or_curie_for(self.namespaces._base, underscore(subset.name))
                uri = self.namespaces.uri_for(curie)
                self.element_header(obj=subset, name=subset.name, curie=curie, uri=uri)
                # TODO: consider showing hierarchy within a subset
                self.header(3, 'Classes')
                for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
                    if not cls.mixin:
                        if cls.in_subset and subset.name in cls.in_subset:
                            self.bullet(self.class_link(cls, use_desc=True), 0)
                self.header(3, 'Mixins')
                for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
                    if cls.mixin:
                        if cls.in_subset and subset.name in cls.in_subset:
                            self.bullet(self.class_link(cls, use_desc=True), 0)
                self.header(3, 'Slots')
                for slot in sorted(self.schema.slots.values(), key=lambda s: s.name):
                    if slot.in_subset and subset.name in slot.in_subset:
                        self.bullet(self.slot_link(slot, use_desc=True), 0)
                self.header(3, 'Types')
                for type in sorted(self.schema.types.values(), key=lambda s: s.name):
                    if type.in_subset and subset.name in type.in_subset:
                        self.bullet(self.type_link(type, use_desc=True), 0)
                self.header(3, 'Enums')
                for enum in sorted(self.schema.enums.values(), key=lambda s: s.name):
                    if enum.in_subset and subset.name in enum.in_subset:
                        self.bullet(self.enum_link(type, use_desc=True), 0)
                self.element_properties(subset)

    def element_header(self, obj: Element, name: str, curie: str, uri: str) -> None:
        simple_name = curie.split(':', 1)[1]
        if isinstance(obj, TypeDefinition):
            obj_type = 'Type'
        elif isinstance(obj, ClassDefinition):
            obj_type = 'Class'
        elif isinstance(obj, SlotDefinition):
            obj_type = 'Slot'
        elif isinstance(obj, EnumDefinition):
            obj_type = 'Enum'
        elif isinstance(obj, SubsetDefinition):
            obj_type = 'Subset'
        else:
            obj_type = 'Class'

        header_label = f"{obj_type}: ~~{name}~~ _(deprecated)_" if obj.deprecated else f"{obj_type}: {name}"
        self.header(1, header_label)

        self.para(be(obj.description))
        print(f'URI: [{curie}]({uri})')
        print()

    def element_properties(self, obj: Element) -> None:
        def identity(e: Any) -> Any:
            return e

        def prop_list(title: str, entries: Union[List, Dict], formatter: Optional[Callable[[Element], str]] = None) \
                -> None:
            if formatter is None:
                formatter = identity
            if isinstance(entries, (dict, JsonObj)):
                entries = list(values(entries))
            if entries:
                print(f"| **{title}:** | | {formatter(entries[0])} |")
                for entry in entries[1:]:
                    print(f"|  | | {formatter(entry)} |")

        def enum_list(title: str,obj:EnumDefinition) -> None:
            # This data is from the enum provided in the YAML
            self.header(2, title)
            print(f"| Text | Description | Meaning | Other Information |")
            print("| :--- | :---: | :---: | ---: |")

            for item, item_info in obj.permissible_values.items():
                text = ''
                desc = ''
                meaning =''
                other = {}
                for k in item_info:
                    if item_info[k] is not None and len(item_info[k]) > 0:
                        if k == 'text':
                            text = item_info[k]
                        elif k == 'description':
                            desc = item_info[k]
                        elif k == 'meaning':
                            meaning = item_info[k]
                        else:
                            other[k] = item_info[k]
                if not other:
                    other = ''
                print(f'| {text} | {desc} | {meaning} | {other} |')

        attributes = StringIO()
        with redirect_stdout(attributes):
            prop_list('Aliases', obj.aliases)
            prop_list('Local names', obj.local_names, lambda e: f"{e.local_name_value} ({e.local_name_source})")
            prop_list('Mappings', obj.mappings)
            prop_list('Alt Descriptions', obj.alt_descriptions, lambda e: f"{e.description} ({e.source})")
            # todos
            # notes
            prop_list('Comments', obj.comments)
            prop_list('Examples', obj.examples)
            prop_list('In Subsets', obj.in_subset)
            # from_schema
            # imported_from
            prop_list('See also', obj.see_also)
            prop_list('Exact Mappings', obj.exact_mappings)
            prop_list('Close Mappings', obj.close_mappings)
            prop_list('Narrow Mappings', obj.narrow_mappings)
            prop_list('Broad Mappings', obj.broad_mappings)
            prop_list('Related Mappings', obj.related_mappings)
            #       - exact mappings
            #       - close mappings
            #       - related mappings
            #       - deprecated element has exact replacement
            #       - deprecated element has possible replacement
            if type(obj) == EnumDefinition:
                enum_list('Permissible Values', obj)

        if attributes.getvalue():
            self.header(2, 'Other properties')
            print("|  |  |  |")
            print("| --- | --- | --- |")
            print(attributes.getvalue())

    def class_hier(self, cls: ClassDefinition, level=0) -> None:
        self.bullet(self.class_link(cls, use_desc=True), level)
        if cls.name in sorted(self.synopsis.isarefs):
            for child in sorted(self.synopsis.isarefs[cls.name].classrefs):
                self.class_hier(self.schema.classes[child], level+1)

    def pred_hier(self, slot: SlotDefinition, level=0) -> None:
        self.bullet(self.slot_link(slot, use_desc=True), level)
        if slot.name in sorted(self.synopsis.isarefs):
            for child in sorted(self.synopsis.isarefs[slot.name].slotrefs):
                self.pred_hier(self.schema.slots[child], level+1)

    def enum_hier(self, enum: EnumDefinition, level=0) -> None:
        self.bullet(self.enum_link(enum, use_desc=True), level)
        if enum.name in sorted(self.synopsis.isarefs):
            for child in sorted(self.synopsis.isarefs[enum.name].classrefs):
                self.enum_hier(self.schema.enums[child], level+1)

    def dir_path(self, obj: Union[ClassDefinition, SlotDefinition, TypeDefinition, EnumDefinition]) -> str:
        filename = self.formatted_element_name(obj) if isinstance(obj, ClassDefinition) \
            else underscore(obj.name) if isinstance(obj, SlotDefinition) \
            else underscore(obj.name) if isinstance(obj, EnumDefinition) \
            else camelcase(obj.name)
        subdir = '/types' if isinstance(obj, TypeDefinition) and not self.no_types_dir else ''
        return f'{self.directory}{subdir}/{filename}.md'

    def mappings(self, obj: [SlotDefinition, ClassDefinition]) -> None:
        # TODO: get rid of this?
        # self.header(2, 'Mappings')
        # for mapping in obj.mappings:
        #     self.bullet(f"{self.xlink(mapping)} {self.to_uri(mapping)}")
        # if obj.subclass_of:
        #     self.bullet(self.xlink(obj.subclass_of))
        pass

    def is_secondary_ref(self, en: str) -> bool:
        """ Determine whether 'en' is the name of something in the neighborhood of the requested classes

        @param en: element name
        @return: True if 'en' is the name of a slot, class or type in the immediate neighborhood of of what we are
        building
        """
        if not self.gen_classes:
            return True
        elif en in self.schema.classes:
            return en in self.gen_classes_neighborhood.classrefs
        elif en in self.schema.slots:
            return en in self.gen_classes_neighborhood.slotrefs
        elif en in self.schema.types:
            return en in self.gen_classes_neighborhood.typerefs
        else:
            return True

    def slot_field(self, cls: ClassDefinition, slot: SlotDefinition) -> None:
        self.bullet(f'{self.slot_link(slot)}{self.predicate_cardinality(slot)}')
        if slot.description:
            self.bullet(f'Description: {slot.description}', level=1)
        self.bullet(f'Range: {self.class_type_link(slot.range)}', level=1)
        # if slot.subproperty_of:
        #     self.bullet(f'edge label: {self.slot_link(slot.subproperty_of)}', level=1)
        for example in slot.examples:
            self.bullet(f'Example: {getattr(example, "value", " ")} {getattr(example, "description", " ")}', level=1)
        # if slot.name not in self.own_slot_names(cls):
        #     self.bullet(f'inherited from: {self.class_link(slot.domain)}', level=1)
        if slot.in_subset:
            ssl = ','.join(slot.in_subset)
            self.bullet(f'in subsets: ({ssl})', level=1)

    def to_uri(self, uri_or_curie: str) -> str:
        """ Return the URI for the slot if known """
        if ':/' in uri_or_curie:
            return uri_or_curie
        elif self.namespaces.prefix_for(uri_or_curie) in self.namespaces:
            return self.namespaces.uri_for(uri_or_curie)
        else:
            return "*(Unknown namespace)*"

    # --
    # FORMATTING
    # --
    @staticmethod
    def predicate_cardinality(slot: SlotDefinition) -> str:
        """ Emit cardinality for a suffix on a predicate"""
        if slot.multivalued:
            card_str = '1..\\*' if slot.required else '0..\\*'
        else:
            card_str = '1..1' if slot.required else '0..1'
        return f"  <sub>{card_str}</sub>"

    @staticmethod
    def range_cardinality(slot: SlotDefinition) -> str:
        """ Emits cardinality decorator at end of type """
        if slot.multivalued:
            card_str = '1..\\*' if slot.required else '0..\\*'
        else:
            card_str = '1..1' if slot.required else '0..1'
        return f"  <sub><b>{card_str}</b></sub>"

    @staticmethod
    def anchor(id_: str) -> None:
        print(f'<a name="{id_}">', end='')

    @staticmethod
    def anchorend() -> None:
        print('</a>')

    def header(self, level: int, txt: str) -> None:
        txt = self.get_metamodel_slot_name(txt)
        print(f'\n{"#" * level} {txt}\n')

    @staticmethod
    def para(txt: str) -> None:
        print(f'\n{txt}\n')

    @staticmethod
    def bullet(txt: str, level=0) -> None:
        print(f'{"    " * level} * {txt}')

    def frontmatter(self, thingtype: str, layout='default') -> None:
        self.header(1, thingtype)
        # print(f'---\nlayout: {layout}\n---\n')

    def bbin(self, obj: Element) -> str:
        """ Boldify built in types

        @param obj: object name or id
        @return:
        """
        return obj.name if isinstance(obj, Element ) else f'**{obj}**' if obj in self.synopsis.typebases else obj

    def desc_for(self, obj: Element, doing_descs: bool) -> str:
        """ Return a description for object if it is unique (different than its parent)

        @param obj: object to be described
        @param doing_descs: If false, always return an empty string
        @return: text or empty string
        """
        if obj.description and doing_descs:
            if isinstance(obj, SlotDefinition) and obj.is_a:
                parent = self.schema.slots[obj.is_a]
            elif isinstance(obj, ClassDefinition) and obj.is_a:
                parent = self.schema.classes[obj.is_a]
            else:
                parent = None
            return '' if parent and obj.description == parent.description else obj.description
        return ''

    def _link(self, obj: Optional[Element], *, after_link: str = None, use_desc: bool=False,
             add_subset: bool=True) -> str:
        """ Create a link to ref if appropriate.

        @param ref: the name or value of a class, slot, type or the name of a built in type.
        @param after_link: Text to put between link and description
        @param use_desc: True means append a description after the link if available
        @param add_subset: True means add any subset information that is available
        @return:
        """
        nl = '\n'
        if obj is None or not self.is_secondary_ref(obj.name):
            return self.bbin(obj)
        if isinstance(obj, SlotDefinition):
            link_name = ((be(obj.domain) + '➞') if obj.alias else '') + self.aliased_slot_name(obj)
            link_ref = underscore(obj.name)
        elif isinstance(obj, TypeDefinition):
            link_name = camelcase(obj.name)
            link_ref = f"types/{link_name}" if not self.no_types_dir else f"{link_name}"
        elif isinstance(obj, ClassDefinition):
            link_name = camelcase(obj.name)
            link_ref = camelcase(link_name)
        elif isinstance(obj, SubsetDefinition):
            link_name = camelcase(obj.name)
            link_ref = camelcase(link_name)
        else:
            link_name = obj.name
            link_ref = link_name
        desc = self.desc_for(obj, use_desc)
        return f'[{link_name}]' \
               f'({link_ref}.{self.format})' + \
                 (f' {after_link} ' if after_link else '') + (f' - {desc.split(nl)[0]}' if desc else '')

    def type_link(self, ref: Optional[Union[str, TypeDefinition]], *, after_link: str = None, use_desc: bool=False,
             add_subset: bool=True) -> str:
        return self._link(self.schema.types[ref] if isinstance(ref, str) else ref, after_link=after_link,
                         use_desc=use_desc, add_subset=add_subset)

    def slot_link(self, ref: Optional[Union[str, SlotDefinition]], *, after_link: str = None, use_desc: bool=False,
             add_subset: bool=True) -> str:
        return self._link(self.schema.slots[ref] if isinstance(ref, str) else ref, after_link=after_link,
                         use_desc=use_desc, add_subset=add_subset)

    def class_link(self, ref: Optional[Union[str, ClassDefinition]], *, after_link: str = None, use_desc: bool=False,
             add_subset: bool=True) -> str:
        return self._link(self.schema.classes[ref] if isinstance(ref, str) else ref, after_link=after_link,
                         use_desc=use_desc, add_subset=add_subset)

    def class_type_link(self, ref: Optional[Union[str, ClassDefinition, TypeDefinition, EnumDefinition]], *, after_link: str = None,
                        use_desc: bool=False, add_subset: bool=True) -> str:
        if isinstance(ref, ClassDefinition):
            return self.class_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif isinstance(ref, TypeDefinition):
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif isinstance(ref, EnumDefinition):
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset) 
        elif ref in self.schema.classes:
            return self.class_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif ref in self.schema.enums:
            return self.enum_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset) 
        else:
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)

    def enum_link(self, ref:Optional[Union[str, EnumDefinition]], *, after_link: str = None, use_desc: bool=False,
             add_subset: bool=True) -> str:
             return self._link(self.schema.enums[ref] if isinstance(ref, str) else ref, after_link=after_link,
                             use_desc=use_desc, add_subset=add_subset)

    def subset_link(self, ref:Optional[Union[str, SubsetDefinition]], *, after_link: str = None, use_desc: bool=False) -> str:
             return self._link(self.schema.subsets[ref] if isinstance(ref, str) else ref, after_link=after_link,
                             use_desc=use_desc)

    def xlink(self, id_: str) -> str:
        return f'[{id_}]({self.id_to_url(id_)})'

    def exist_warning(self, *fpath: str) -> str:
        """ Create a file name out of fpath and check whether it already exists """
        fname = os.path.join(*fpath)
        if self.warn_on_exist and os.path.exists(fname):
            self.logger.warning(f"File {fname} already exists")
        return fname


    @staticmethod
    def id_to_url(id_: str) -> str:
        uri = id_
        if ':' in id_:
            # TODO! use PC
            if id_.startswith('SIO:'):
                uri = id_.replace('SIO:', 'http://semanticscience.org/resource/SIO_')
            elif id_.startswith('HGNC:'):
                uri = 'https://monarchinitiative.org/gene/' + id_
            else:
                frag = id_.replace(':', '_')
                base = 'http://purl.obolibrary.org/obo/'
                uri = base+frag
        return uri

@shared_arguments(MarkdownGenerator)
@click.command()
@click.option("--dir", "-d", required=True, help="Output directory")
@click.option("--classes", "-c", default=None, multiple=True, help="Class(es) to emit")
@click.option("--map-fields", "-M", default=None, multiple=True, help="Map metamodel fields, e.g. slot=field")
@click.option("--img", "-i",  is_flag=True, help="Download YUML images to 'image' directory")
@click.option("--index-file", "-I", help="Name of markdown file that holds index")
@click.option("--noimages", is_flag=True, help="Do not (re-)generate images")
@click.option("--noyuml", is_flag=True, help="Do not add yUML figures to pages")
@click.option("--notypesdir", is_flag=True, help="Do not create a separate types directory")
@click.option("--warnonexist", is_flag=True, help="Warn if output file already exists")
def cli(yamlfile, map_fields, dir, img, index_file, notypesdir, warnonexist, **kwargs):
    """ Generate markdown documentation of a LinkML model """
    gen = MarkdownGenerator(yamlfile, no_types_dir=notypesdir, warn_on_exist=warnonexist, **kwargs)
    if map_fields is not None:
        gen.metamodel_name_map = {}
        for mf in map_fields:
            [k, v] = mf.split('=')
            gen.metamodel_name_map[k] = v
    gen.serialize(directory=dir, image_dir=img, **kwargs)


if __name__ == '__main__':
    cli()
