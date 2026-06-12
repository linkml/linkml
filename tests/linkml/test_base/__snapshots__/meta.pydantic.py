from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
        coerce_numbers_to_str = True,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root




def _coerce_keyed_collection(value: Any, key_name: str, value_name: str | None = None) -> Any:
    """
    Normalize the input forms of a multivalued, inlined-as-dict slot to a dict
    of dicts, injecting the dict key into each value's key/identifier slot
    (``key_name``). A scalar entry value is assigned to ``value_name`` when
    given (the positional second-slot semantics of the dataclass metamodel,
    e.g. ``annotations: {tag: v}`` or ``prefixes: {pfx: url}``). Mirrors the
    normalization YAMLRoot performs for the equivalent dataclass models.
    """
    if isinstance(value, str):
        return {value: {key_name: value}}
    if isinstance(value, dict):
        if key_name in value and isinstance(value[key_name], (str, int, float)) and not isinstance(value[key_name], bool):
            # flat single-object form, e.g. annotations: {tag: t, value: v} --
            # only when the key field holds a scalar (a None/dict body means an
            # entry whose dict key happens to equal the key slot's name)
            return {value[key_name]: dict(value)}
        out = {}
        for key, item in value.items():
            if not isinstance(key, str):
                key = str(key)
            if item is None:
                out[key] = {key_name: key}
            elif isinstance(item, dict):
                if key_name not in item:
                    out[key] = {key_name: key, **item}
                elif item[key_name] != key:
                    raise ValueError(f"{key_name} mismatch: dict key {key!r} != {item[key_name]!r}")
                else:
                    out[key] = item
            elif value_name is not None and isinstance(item, (str, int, float, bool)):
                # simple form: dict key + scalar value, e.g. prefixes: {pfx: url}
                out[key] = {key_name: key, value_name: item}
            else:
                out[key] = item
        return out
    if isinstance(value, list):
        out = {}
        for item in value:
            if isinstance(item, dict):
                if key_name not in item:
                    raise ValueError(f"Missing {key_name} in list item {item!r}")
                out[item[key_name]] = item
            elif isinstance(item, (str, int, float)):
                out[item] = {key_name: item}
            elif hasattr(item, key_name):
                out[getattr(item, key_name)] = item
            else:
                raise ValueError(f"Cannot key list item {item!r} by {key_name}")
        return out
    return value




def _coerce_inlined_list(value: Any, key_name: str) -> Any:
    """
    Normalize the input forms of a multivalued slot inlined as a list of
    objects: a dict keyed by ``key_name`` (the identifier/key slot of the
    range class, or its first required slot) becomes a list with the keys
    injected, and a single object is wrapped into a singleton list. Mirrors
    the normalization YAMLRoot performs for the equivalent dataclass models.
    """
    if value is None or isinstance(value, list):
        return value
    if isinstance(value, dict):
        if key_name in value and isinstance(value[key_name], (str, int, float)) and not isinstance(value[key_name], bool):
            # flat single-object form, e.g. structured_aliases: {literal_form: x, ...}
            return [value]
        out = []
        for key, item in value.items():
            if item is None:
                out.append({key_name: key})
            elif isinstance(item, dict) and key_name not in item:
                out.append({key_name: key, **item})
            else:
                out.append(item)
        return out
    return [value]


linkml_meta = LinkMLMeta({'default_curi_maps': ['semweb_context'],
     'default_prefix': 'linkml',
     'default_range': 'string',
     'description': 'The metamodel for schemas defined using the Linked Data '
                    'Modeling Language framework.\n'
                    '\n'
                    'For more information on LinkML:\n'
                    '\n'
                    '* [linkml.io](https://linkml.io) main website\n'
                    '* '
                    '[specification](https://w3id.org/linkml/docs/specification/)\n'
                    '\n'
                    'LinkML is self-describing. Every LinkML schema consists of '
                    'elements\n'
                    'that instantiate classes in this metamodel.\n'
                    '\n'
                    'Core metaclasses:\n'
                    '\n'
                    '* '
                    '[SchemaDefinition](https://w3id.org/linkml/SchemaDefinition)\n'
                    '* [ClassDefinition](https://w3id.org/linkml/ClassDefinition)\n'
                    '* [SlotDefinition](https://w3id.org/linkml/SlotDefinition)\n'
                    '* [TypeDefinition](https://w3id.org/linkml/TypeDefinition)\n'
                    '\n'
                    'There are many subsets of *profiles* of the metamodel, for '
                    'different purposes:\n'
                    '\n'
                    '* [MinimalSubset](https://w3id.org/linkml/MinimalSubset)\n'
                    '* [BasicSubset](https://w3id.org/linkml/BasicSubset)\n'
                    '\n'
                    'For canonical reference documentation on any metamodel '
                    'construct,\n'
                    'refer to the official URI for each construct, e.g.\n'
                    '[https://w3id.org/linkml/is_a](https://w3id.org/linkml/is_a)',
     'emit_prefixes': ['linkml',
                       'rdf',
                       'rdfs',
                       'xsd',
                       'skos',
                       'dcterms',
                       'OIO',
                       'owl',
                       'pav'],
     'generation_date': '2000-01-01T00:00:00',
     'id': 'https://w3id.org/linkml/meta',
     'imports': ['linkml:types',
                 'linkml:mappings',
                 'linkml:extensions',
                 'linkml:annotations',
                 'linkml:units'],
     'license': 'https://creativecommons.org/publicdomain/zero/1.0/',
     'name': 'meta',
     'prefixes': {'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'},
                  'OIO': {'prefix_prefix': 'OIO',
                          'prefix_reference': 'http://www.geneontology.org/formats/oboInOwl#'},
                  'SIO': {'prefix_prefix': 'SIO',
                          'prefix_reference': 'http://semanticscience.org/resource/SIO_'},
                  'bibo': {'prefix_prefix': 'bibo',
                           'prefix_reference': 'http://purl.org/ontology/bibo/'},
                  'cdisc': {'prefix_prefix': 'cdisc',
                            'prefix_reference': 'http://rdf.cdisc.org/mms#'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'oslc': {'prefix_prefix': 'oslc',
                           'prefix_reference': 'http://open-services.net/ns/core#'},
                  'owl': {'prefix_prefix': 'owl',
                          'prefix_reference': 'http://www.w3.org/2002/07/owl#'},
                  'pav': {'prefix_prefix': 'pav',
                          'prefix_reference': 'http://purl.org/pav/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'qb': {'prefix_prefix': 'qb',
                         'prefix_reference': 'http://purl.org/linked-data/cube#'},
                  'qudt': {'prefix_prefix': 'qudt',
                           'prefix_reference': 'http://qudt.org/schema/qudt/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'sh': {'prefix_prefix': 'sh',
                         'prefix_reference': 'http://www.w3.org/ns/shacl#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'skosxl': {'prefix_prefix': 'skosxl',
                             'prefix_reference': 'http://www.w3.org/2008/05/skos-xl#'},
                  'swrl': {'prefix_prefix': 'swrl',
                           'prefix_reference': 'http://www.w3.org/2003/11/swrl#'},
                  'vann': {'prefix_prefix': 'vann',
                           'prefix_reference': 'https://vocab.org/vann/'}},
     'source_file': '/Users/kschaper/Monarch/linkml-pydantic-meta/packages/linkml_runtime/src/linkml_runtime/linkml_model/model/schema/meta.yaml',
     'source_file_date': '2000-01-01T00:00:00',
     'source_file_size': 1,
     'subsets': {'BasicSubset': {'description': 'An extension of MinimalSubset '
                                                'that avoids advanced constructs '
                                                'and can be implemented by a broad '
                                                'variety of tools.\n'
                                                '\n'
                                                'This subset roughly corresponds '
                                                'to the union of most standard '
                                                'constructs used in relational '
                                                'datamodel modeling,\n'
                                                'object oriented modeling, and '
                                                'simple JSON-style modeling, while '
                                                'avoiding more advanced constructs '
                                                'from these languages.\n'
                                                '\n'
                                                'It is often possible to translate '
                                                'from a more expressive schema to '
                                                'a BasicSubset schema, through a '
                                                'schema derivation\n'
                                                'process',
                                 'from_schema': 'https://w3id.org/linkml/meta',
                                 'name': 'BasicSubset',
                                 'rank': 1,
                                 'title': 'basic subset'},
                 'MinimalSubset': {'description': 'The absolute minimal set of '
                                                  'elements necessary for defining '
                                                  'any schema.\n'
                                                  '\n'
                                                  'schemas conforming to the '
                                                  'minimal subset consist of '
                                                  'classes, with all slots\n'
                                                  'inlined as attributes. There '
                                                  'are no enums.',
                                   'from_schema': 'https://w3id.org/linkml/meta',
                                   'name': 'MinimalSubset',
                                   'rank': 0,
                                   'title': 'minimal subset'},
                 'ObjectOrientedProfile': {'description': 'A profile that includes '
                                                          'all the metamodel '
                                                          'elements whose '
                                                          'semantics can be '
                                                          'expressed using a '
                                                          'minimal\n'
                                                          'implementation of the '
                                                          'object oriented '
                                                          'metamodel as employed '
                                                          'by languages such as '
                                                          'Java and Python, or\n'
                                                          'in modeling frameworks '
                                                          'like UML',
                                           'from_schema': 'https://w3id.org/linkml/meta',
                                           'name': 'ObjectOrientedProfile',
                                           'rank': 4,
                                           'title': 'object oriented profile'},
                 'OwlProfile': {'description': 'A profile that includes all the '
                                               'metamodel elements whose semantics '
                                               'can be expressed in OWL',
                                'from_schema': 'https://w3id.org/linkml/meta',
                                'name': 'OwlProfile',
                                'title': 'owl profile'},
                 'RelationalModelProfile': {'description': 'A profile that '
                                                           'includes all the '
                                                           'metamodel elements '
                                                           'whose semantics can be '
                                                           'expressed using the '
                                                           'classic Relational '
                                                           'Model.\n'
                                                           'The Relational Model '
                                                           'excludes collections '
                                                           '(multivalued slots) as '
                                                           'first class entities. '
                                                           'Instead, these must '
                                                           'be\n'
                                                           'mapped to '
                                                           'backreferences\n'
                                                           '\n'
                                                           'The classic Relational '
                                                           'Model excludes '
                                                           'inheritance and '
                                                           'polymorphism -- these '
                                                           'must be rolled down '
                                                           'to\n'
                                                           'concrete classes or '
                                                           'otherwise transformed.',
                                            'from_schema': 'https://w3id.org/linkml/meta',
                                            'name': 'RelationalModelProfile',
                                            'rank': 3,
                                            'title': 'relational model profile'},
                 'SpecificationSubset': {'description': 'A subset that includes '
                                                        'all the metamodel '
                                                        'elements that form part '
                                                        'of the normative LinkML '
                                                        'specification.\n'
                                                        '\n'
                                                        'The complete LinkML '
                                                        'specification can be '
                                                        'found at '
                                                        '[linkml:specification](https://w3id.org/linkml/specification)',
                                         'from_schema': 'https://w3id.org/linkml/meta',
                                         'name': 'SpecificationSubset',
                                         'rank': 2,
                                         'title': 'specification subset'}},
     'title': 'LinkML Schema Metamodel'} )

class PvFormulaOptions(str, Enum):
    """
    The formula used to generate the set of permissible values from the code_set values
    """
    CODE = "CODE"
    """
    The permissible values are the set of possible codes in the code set
    """
    CURIE = "CURIE"
    """
    The permissible values are the set of CURIES in the code set
    """
    URI = "URI"
    """
    The permissible values are the set of code URIs in the code set
    """
    FHIR_CODING = "FHIR_CODING"
    """
    The permissible values are the set of FHIR coding elements derived from the code set
    """
    LABEL = "LABEL"
    """
    The permissible values are the set of human readable labels in the code set
    """


class PresenceEnum(str, Enum):
    """
    enumeration of conditions by which a slot value should be set
    """
    UNCOMMITTED = "UNCOMMITTED"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class RelationalRoleEnum(str, Enum):
    """
    enumeration of roles a slot on a relationship class can play
    """
    SUBJECT = "SUBJECT"
    """
    a slot with this role connects a relationship to its subject/source node
    """
    OBJECT = "OBJECT"
    """
    a slot with this role connects a relationship to its object/target node
    """
    PREDICATE = "PREDICATE"
    """
    a slot with this role connects a relationship to its predicate/property
    """
    NODE = "NODE"
    """
    a slot with this role connects a symmetric relationship to a node that represents either subject or object node
    """
    OTHER_ROLE = "OTHER_ROLE"
    """
    a slot with this role connects a relationship to a node that is not subject/object/predicate
    """


class AliasPredicateEnum(str, Enum):
    """
    permissible values for the relationship between an element and an alias
    """
    EXACT_SYNONYM = "EXACT_SYNONYM"
    RELATED_SYNONYM = "RELATED_SYNONYM"
    BROAD_SYNONYM = "BROAD_SYNONYM"
    NARROW_SYNONYM = "NARROW_SYNONYM"


class ObligationLevelEnum(str, Enum):
    """
    The level of obligation or recommendation strength for a metadata element
    """
    REQUIRED = "REQUIRED"
    """
    The metadata element is required to be present in the model
    """
    RECOMMENDED = "RECOMMENDED"
    """
    The metadata element is recommended to be present in the model
    """
    OPTIONAL = "OPTIONAL"
    """
    The metadata element is optional to be present in the model
    """
    EXAMPLE = "EXAMPLE"
    """
    The metadata element is an example of how to use the model
    """
    DISCOURAGED = "DISCOURAGED"
    """
    The metadata element is allowed but discouraged to be present in the model
    """



class Extension(ConfiguredBaseModel):
    """
    a tag/value pair used to add non-model information to an entry
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/extensions'})

    tag: str = Field(default=..., description="""a tag associated with an extension""", json_schema_extra = { "linkml_meta": {'domain': 'extension', 'domain_of': ['extension']} })
    value: Any = Field(default=..., description="""the actual annotation""", json_schema_extra = { "linkml_meta": {'annotations': {'simple_dict_value': {'tag': 'simple_dict_value',
                                               'value': True}},
         'domain': 'extension',
         'domain_of': ['extension']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")


class Extensible(ConfiguredBaseModel):
    """
    mixin for classes that support extension
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/extensions', 'mixin': True})

    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")


class Annotatable(ConfiguredBaseModel):
    """
    mixin for classes that support annotations
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/annotations', 'mixin': True})

    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")


class Annotation(Annotatable, Extension):
    """
    a tag/value pair with the semantics of OWL Annotation
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/annotations',
         'mixins': ['annotatable']})

    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    tag: str = Field(default=..., description="""a tag associated with an extension""", json_schema_extra = { "linkml_meta": {'domain': 'extension', 'domain_of': ['extension']} })
    value: Any = Field(default=..., description="""the actual annotation""", json_schema_extra = { "linkml_meta": {'annotations': {'simple_dict_value': {'tag': 'simple_dict_value',
                                               'value': True}},
         'domain': 'extension',
         'domain_of': ['extension']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")


class UnitOfMeasure(ConfiguredBaseModel):
    """
    A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for measuring other quantities the same kind (more generally of equivalent dimension).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'ucum_code': {'name': 'ucum_code',
                                                       'required': True}}},
                    {'slot_conditions': {'iec61360code': {'name': 'iec61360code',
                                                          'required': True}}},
                    {'slot_conditions': {'symbol': {'name': 'symbol',
                                                    'required': True}}},
                    {'slot_conditions': {'exact_mappings': {'name': 'exact_mappings',
                                                            'required': True}}}],
         'class_uri': 'qudt:Unit',
         'from_schema': 'https://w3id.org/linkml/units',
         'slot_usage': {'exact mappings': {'comments': ['Do not use this to encode '
                                                        'mappings to systems for which '
                                                        'a dedicated field exists'],
                                           'description': 'Used to link a unit to '
                                                          'equivalent concepts in '
                                                          'ontologies such as UO, '
                                                          'SNOMED, OEM, OBOE, NCIT',
                                           'name': 'exact mappings'}}})

    symbol: Optional[str] = Field(default=None, description="""name of the unit encoded as a symbol""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure'], 'slot_uri': 'qudt:symbol'} })
    abbreviation: Optional[str] = Field(default=None, description="""An abbreviation for a unit is a short ASCII string that is used in place of the full name for the unit in contexts where non-ASCII characters would be problematic, or where using the abbreviation will enhance readability. When a power of a base unit needs to be expressed, such as squares this can be done using abbreviations rather than symbols (source: qudt)""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure'], 'slot_uri': 'qudt:abbreviation'} })
    descriptive_name: Optional[str] = Field(default=None, description="""the spelled out name of the unit, for example, meter""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure'], 'slot_uri': 'rdfs:label'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT""", json_schema_extra = { "linkml_meta": {'comments': ['Do not use this to encode mappings to systems for which a '
                      'dedicated field exists'],
         'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    ucum_code: Optional[str] = Field(default=None, description="""associates a QUDT unit with its UCUM code (case-sensitive).""", json_schema_extra = { "linkml_meta": {'domain': 'UnitOfMeasure',
         'domain_of': ['UnitOfMeasure'],
         'recommended': True,
         'slot_uri': 'qudt:ucumCode'} })
    derivation: Optional[str] = Field(default=None, description="""Expression for deriving this unit from other units""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure']} })
    has_quantity_kind: Optional[str] = Field(default=None, description="""Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length""", json_schema_extra = { "linkml_meta": {'comments': ['Potential ontologies include but are not limited to PATO, NCIT, '
                      'OBOE, qudt.quantityKind'],
         'domain_of': ['UnitOfMeasure'],
         'slot_uri': 'qudt:hasQuantityKind'} })
    iec61360code: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure'], 'slot_uri': 'qudt:iec61360Code'} })

    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class CommonMetadata(ConfiguredBaseModel):
    """
    Generic metadata shared across definitions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['BasicSubset'],
         'mixin': True})

    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class Element(CommonMetadata, Annotatable, Extensible):
    """
    A named element in the model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'aliases': ['data element', 'object'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['BasicSubset'],
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'see_also': ['https://en.wikipedia.org/wiki/Data_element']})

    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class SchemaDefinition(Element):
    """
    A collection of definitions that make up a schema or a data model.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['data dictionary',
                     'data model',
                     'information model',
                     'logical model',
                     'schema',
                     'model'],
         'close_mappings': ['qb:ComponentSet', 'owl:Ontology'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_dictionary'],
         'slot_usage': {'name': {'description': 'a unique name for the schema that is '
                                                'both human-readable and consists of '
                                                'only characters from the NCName set',
                                 'name': 'name',
                                 'range': 'ncname'}},
         'tree_root': True})

    id: str = Field(default=..., description="""The official schema URI""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'OwlProfile'],
         'rank': 0} })
    version: Optional[str] = Field(default=None, description="""particular version of schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'exact_mappings': ['schema:schemaVersion'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:version'} })
    imports: Optional[list[str]] = Field(default=None, description="""A list of schemas that are to be included in this schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'OwlProfile'],
         'rank': 21} })
    license: Optional[str] = Field(default=None, description="""license for the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'rank': 31,
         'slot_uri': 'dcterms:license'} })
    prefixes: Optional[dict[str, Union[str, Prefix]]] = Field(default=None, description="""A collection of prefix expansions that specify how CURIEs can be expanded to URIs""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 10,
         'slot_uri': 'sh:declare'} })
    emit_prefixes: Optional[list[str]] = Field(default=None, description="""a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition', 'domain_of': ['schema_definition']} })
    default_curi_maps: Optional[list[str]] = Field(default=None, description="""ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset']} })
    default_prefix: Optional[str] = Field(default=None, description="""The prefix that is used for all elements within a schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'ifabsent': 'default_ns',
         'in_subset': ['SpecificationSubset', 'MinimalSubset', 'BasicSubset'],
         'rank': 11} })
    default_range: Optional[str] = Field(default=None, description="""default slot range to be used if range element is omitted from a slot definition""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset', 'MinimalSubset', 'BasicSubset'],
         'rank': 13} })
    subsets: Optional[dict[str, SubsetDefinition]] = Field(default=None, description="""An index to the collection of all subset definitions in the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'exact_mappings': ['OIO:hasSubset'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 8} })
    types: Optional[dict[str, TypeDefinition]] = Field(default=None, description="""An index to the collection of all type definitions in the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset', 'ObjectOrientedProfile', 'OwlProfile'],
         'rank': 6} })
    enums: Optional[dict[str, EnumDefinition]] = Field(default=None, description="""An index to the collection of all enum definitions in the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 5} })
    slots: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""An index to the collection of all slot definitions in the schema""", json_schema_extra = { "linkml_meta": {'comments': ['note the formal name of this element is slot_definitions, but '
                      'it has alias slots, which is the canonical form used in '
                      'yaml/json serializes of schemas.'],
         'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'OwlProfile'],
         'rank': 4} })
    classes: Optional[dict[str, ClassDefinition]] = Field(default=None, description="""An index to the collection of all class definitions in the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 3} })
    metamodel_version: Optional[str] = Field(default=None, description="""Version of the metamodel used to load the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source_file: Optional[str] = Field(default=None, description="""name, uri or description of the source of the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'readonly': 'supplied by the schema loader'} })
    source_file_date: Optional[datetime ] = Field(default=None, description="""modification date of the source of the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'readonly': 'supplied by the loader'} })
    source_file_size: Optional[int] = Field(default=None, description="""size in bytes of the source of the schema""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'readonly': 'supplied by the schema loader or schema view'} })
    generation_date: Optional[datetime ] = Field(default=None, description="""date and time that the schema was loaded/generated""", json_schema_extra = { "linkml_meta": {'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['BasicSubset'],
         'readonly': 'supplied by the schema loader or schema view'} })
    slot_names_unique: Optional[bool] = Field(default=None, description="""if true then induced/mangled slot names are not created for class_usage and attributes""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['schema_definition', 'class_definition'],
         'status': 'testing'} })
    settings: Optional[dict[str, Union[str, Setting]]] = Field(default=None, description="""A collection of global variable settings""", json_schema_extra = { "linkml_meta": {'aliases': ['constants'],
         'comments': ['global variables are used in string interpolation in structured '
                      'patterns'],
         'domain': 'schema_definition',
         'domain_of': ['schema_definition'],
         'in_subset': ['SpecificationSubset'],
         'rank': 20} })
    bindings: Optional[list[EnumBinding]] = Field(default=None, description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['schema_definition', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    name: str = Field(default=..., description="""a unique name for the schema that is both human-readable and consists of only characters from the NCName set""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('prefixes', mode='before')
    def coerce_keyed_prefixes(cls, v):
        return _coerce_keyed_collection(v, "prefix_prefix", value_name="prefix_reference")

    @field_validator('subsets', mode='before')
    def coerce_keyed_subsets(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('types', mode='before')
    def coerce_keyed_types(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('enums', mode='before')
    def coerce_keyed_enums(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('slots', mode='before')
    def coerce_keyed_slots(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('classes', mode='before')
    def coerce_keyed_classes(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('settings', mode='before')
    def coerce_keyed_settings(cls, v):
        return _coerce_keyed_collection(v, "setting_key", value_name="setting_value")

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('imports', mode='before')
    def coerce_list_imports(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('emit_prefixes', mode='before')
    def coerce_list_emit_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('default_curi_maps', mode='before')
    def coerce_list_default_curi_maps(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('bindings', mode='before')
    def coerce_list_bindings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class SubsetDefinition(Element):
    """
    an element that can be used to group other metamodel elements
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 6})

    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class Definition(Element):
    """
    abstract base class for core metaclasses
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['BasicSubset'],
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_definition']})

    is_a: Optional[str] = Field(default=None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    abstract: Optional[bool] = Field(default=None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile']} })
    mixin: Optional[bool] = Field(default=None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[list[str]] = Field(default=None, description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""", json_schema_extra = { "linkml_meta": {'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    apply_to: Optional[list[str]] = Field(default=None, description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    values_from: Optional[list[str]] = Field(default=None, description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    string_serialization: Optional[str] = Field(default=None, description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition', 'type_mapping'],
         'in_subset': ['SpecificationSubset'],
         'inherited': False,
         'see_also': ['https://github.com/linkml/issues/128']} })
    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('mixins', mode='before')
    def coerce_list_mixins(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('apply_to', mode='before')
    def coerce_list_apply_to(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('values_from', mode='before')
    def coerce_list_values_from(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class EnumBinding(CommonMetadata, Annotatable, Extensible):
    """
    A binding of a slot or a class to a permissible value from an enumeration.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset'],
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'slot_usage': {'range': {'name': 'range', 'range': 'enum_definition'}}})

    range: Optional[str] = Field(default=None, description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""", json_schema_extra = { "linkml_meta": {'aliases': ['value domain'],
         'comments': ['range is underspecified, as not all elements can appear as the '
                      'range of a slot.',
                      'to use a URI or CURIE as the range, create a class with the URI '
                      'or curie as the class_uri'],
         'domain': 'slot_definition',
         'domain_of': ['enum_binding', 'slot_expression'],
         'ifabsent': 'default_range',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True} })
    obligation_level: Optional[ObligationLevelEnum] = Field(default=None, description="""The level of obligation or recommendation strength for a metadata element""", json_schema_extra = { "linkml_meta": {'domain_of': ['enum_binding'], 'in_subset': ['SpecificationSubset']} })
    binds_value_of: Optional[str] = Field(default=None, description="""A path to a slot that is being bound to a permissible value from an enumeration.""", json_schema_extra = { "linkml_meta": {'domain': 'enum_binding',
         'domain_of': ['enum_binding'],
         'in_subset': ['SpecificationSubset']} })
    pv_formula: Optional[PvFormulaOptions] = Field(default=None, description="""Defines the specific formula to be used to generate the permissible values.""", json_schema_extra = { "linkml_meta": {'comments': ['you cannot have BOTH the permissible_values and '
                      'permissible_value_formula tag',
                      'code_set must be supplied for this to be valid'],
         'domain_of': ['enum_expression', 'enum_binding'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class MatchQuery(ConfiguredBaseModel):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via a query that matches on properties of the external concepts.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset']})

    identifier_pattern: Optional[str] = Field(default=None, description="""A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'match_query',
         'domain_of': ['match_query'],
         'in_subset': ['SpecificationSubset']} })
    source_ontology: Optional[str] = Field(default=None, description="""An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values""", json_schema_extra = { "linkml_meta": {'aliases': ['terminology', 'vocabulary'],
         'comments': ['examples include schema.org, wikidata, or an OBO ontology',
                      'for obo ontologies we recommend CURIEs of the form obo:cl, '
                      'obo:envo, etc'],
         'domain_of': ['match_query', 'reachability_query'],
         'in_subset': ['SpecificationSubset']} })


class ReachabilityQuery(ConfiguredBaseModel):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a set of source nodes to a set of descendants or ancestors over a set of relationship types.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset']})

    source_ontology: Optional[str] = Field(default=None, description="""An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values""", json_schema_extra = { "linkml_meta": {'aliases': ['terminology', 'vocabulary'],
         'comments': ['examples include schema.org, wikidata, or an OBO ontology',
                      'for obo ontologies we recommend CURIEs of the form obo:cl, '
                      'obo:envo, etc'],
         'domain_of': ['match_query', 'reachability_query'],
         'in_subset': ['SpecificationSubset']} })
    source_nodes: Optional[list[str]] = Field(default=None, description="""A list of nodes that are used in the reachability query""", json_schema_extra = { "linkml_meta": {'domain': 'reachability_query',
         'domain_of': ['reachability_query'],
         'in_subset': ['SpecificationSubset']} })
    relationship_types: Optional[list[str]] = Field(default=None, description="""A list of relationship types (properties) that are used in a reachability query""", json_schema_extra = { "linkml_meta": {'aliases': ['predicates', 'properties'],
         'domain': 'reachability_query',
         'domain_of': ['reachability_query'],
         'in_subset': ['SpecificationSubset']} })
    is_direct: Optional[bool] = Field(default=None, description="""True if the reachability query should only include directly related nodes, if False then include also transitively connected""", json_schema_extra = { "linkml_meta": {'aliases': ['non-transitive'],
         'domain': 'reachability_query',
         'domain_of': ['reachability_query'],
         'in_subset': ['SpecificationSubset']} })
    include_self: Optional[bool] = Field(default=None, description="""True if the query is reflexive""", json_schema_extra = { "linkml_meta": {'aliases': ['reflexive'],
         'domain': 'reachability_query',
         'domain_of': ['reachability_query'],
         'in_subset': ['SpecificationSubset']} })
    traverse_up: Optional[bool] = Field(default=None, description="""True if the direction of the reachability query is reversed and ancestors are retrieved""", json_schema_extra = { "linkml_meta": {'aliases': ['ancestors'],
         'domain': 'reachability_query',
         'domain_of': ['reachability_query'],
         'in_subset': ['SpecificationSubset']} })

    @field_validator('source_nodes', mode='before')
    def coerce_list_source_nodes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('relationship_types', mode='before')
    def coerce_list_relationship_types(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class Expression(ConfiguredBaseModel):
    """
    general mixin for any class that can represent some form of expression
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/linkml/meta', 'mixin': True})

    pass


class TypeExpression(Expression):
    """
    An abstract class grouping named types and anonymous type expressions
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixin': True,
         'slot_usage': {'all_of': {'name': 'all_of',
                                   'range': 'anonymous_type_expression'},
                        'any_of': {'name': 'any_of',
                                   'range': 'anonymous_type_expression'},
                        'exactly_one_of': {'name': 'exactly_one_of',
                                           'range': 'anonymous_type_expression'},
                        'none_of': {'name': 'none_of',
                                    'range': 'anonymous_type_expression'}}})

    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    none_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })

    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class AnonymousTypeExpression(TypeExpression):
    """
    A type expression that is not a top-level named type definition. Used for nesting.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta', 'mixins': ['type_expression']})

    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    none_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })

    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class TypeDefinition(TypeExpression, Element):
    """
    an element that whose instances are atomic scalar values that can be mapped to primitive types
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'OwlProfile'],
         'mixins': ['type_expression'],
         'rank': 4,
         'slot_usage': {'union_of': {'name': 'union_of', 'range': 'type_definition'}}})

    typeof: Optional[str] = Field(default=None, description="""A parent type from which type properties are inherited""", json_schema_extra = { "linkml_meta": {'comments': ['the target type definition of the typeof slot is referred to as '
                      'the "parent type"',
                      'the type definition containing the typeof slot is referred to '
                      'as the "child type"',
                      'type definitions without a typeof slot are referred to as a '
                      '"root type"'],
         'domain': 'type_definition',
         'domain_of': ['type_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 7} })
    base: Optional[str] = Field(default=None, description="""python base type in the LinkML runtime that implements this type definition""", json_schema_extra = { "linkml_meta": {'comments': ['every root type must have a base',
                      'the base is inherited by child types but may be overridden.  '
                      'Base compatibility is not checked.'],
         'domain': 'type_definition',
         'domain_of': ['type_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 8} })
    uri: Optional[str] = Field(default=None, description="""The uri that defines the possible values for the type definition""", json_schema_extra = { "linkml_meta": {'comments': ["uri is typically drawn from the set of URI's defined in OWL "
                      '(https://www.w3.org/TR/2012/REC-owl2-syntax-20121211/#Datatype_Maps)',
                      'every root type must have a type uri'],
         'domain': 'type_definition',
         'domain_of': ['type_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 2} })
    repr: Optional[str] = Field(default=None, description="""the name of the python object that implements this type definition""", json_schema_extra = { "linkml_meta": {'domain': 'type_definition',
         'domain_of': ['type_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 10} })
    union_of: Optional[list[str]] = Field(default=None, description="""indicates that the domain element consists exactly of the members of the element in the range.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['type_definition', 'slot_definition', 'class_definition'],
         'in_subset': ['SpecificationSubset', 'OwlProfile'],
         'notes': ['this only applies in the OWL generation']} })
    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    none_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousTypeExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('union_of', mode='before')
    def coerce_list_union_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class EnumExpression(Expression):
    """
    An expression that constrains the range of a slot
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta'})

    code_set: Optional[str] = Field(default=None, description="""the identifier of an enumeration code set.""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    code_set_tag: Optional[str] = Field(default=None, description="""the version tag of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['enum_expression cannot have both a code_set_tag and a '
                      'code_set_version'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    code_set_version: Optional[str] = Field(default=None, description="""the version identifier of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['we assume that version identifiers lexically sort in temporal '
                      'order. Recommend semver when possible'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    pv_formula: Optional[PvFormulaOptions] = Field(default=None, description="""Defines the specific formula to be used to generate the permissible values.""", json_schema_extra = { "linkml_meta": {'comments': ['you cannot have BOTH the permissible_values and '
                      'permissible_value_formula tag',
                      'code_set must be supplied for this to be valid'],
         'domain_of': ['enum_expression', 'enum_binding'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    permissible_values: Optional[dict[str, PermissibleValue]] = Field(default=None, description="""A list of possible values for a slot range""", json_schema_extra = { "linkml_meta": {'aliases': ['coded values'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'exact_mappings': ['cdisc:PermissibleValue'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    include: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    minus: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    inherits: Optional[list[str]] = Field(default=None, description="""An enum definition that is used as the basis to create a new enum""", json_schema_extra = { "linkml_meta": {'comments': ['All permissible values for all inherited enums are copied to '
                      'form the initial seed set'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    reachable_from: Optional[ReachabilityQuery] = Field(default=None, description="""Specifies a query for obtaining a list of permissible values based on graph reachability""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    matches: Optional[MatchQuery] = Field(default=None, description="""Specifies a match query that is used to calculate the list of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    concepts: Optional[list[str]] = Field(default=None, description="""A list of identifiers that are used to construct a set of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })

    @field_validator('permissible_values', mode='before')
    def coerce_keyed_permissible_values(cls, v):
        return _coerce_keyed_collection(v, "text", value_name="description")

    @field_validator('include', mode='before')
    def coerce_list_include(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('minus', mode='before')
    def coerce_list_minus(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('inherits', mode='before')
    def coerce_list_inherits(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('concepts', mode='before')
    def coerce_list_concepts(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class AnonymousEnumExpression(EnumExpression):
    """
    An enum_expression that is not named
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta', 'mixins': ['enum_expression']})

    code_set: Optional[str] = Field(default=None, description="""the identifier of an enumeration code set.""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    code_set_tag: Optional[str] = Field(default=None, description="""the version tag of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['enum_expression cannot have both a code_set_tag and a '
                      'code_set_version'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    code_set_version: Optional[str] = Field(default=None, description="""the version identifier of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['we assume that version identifiers lexically sort in temporal '
                      'order. Recommend semver when possible'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    pv_formula: Optional[PvFormulaOptions] = Field(default=None, description="""Defines the specific formula to be used to generate the permissible values.""", json_schema_extra = { "linkml_meta": {'comments': ['you cannot have BOTH the permissible_values and '
                      'permissible_value_formula tag',
                      'code_set must be supplied for this to be valid'],
         'domain_of': ['enum_expression', 'enum_binding'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    permissible_values: Optional[dict[str, PermissibleValue]] = Field(default=None, description="""A list of possible values for a slot range""", json_schema_extra = { "linkml_meta": {'aliases': ['coded values'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'exact_mappings': ['cdisc:PermissibleValue'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    include: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    minus: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    inherits: Optional[list[str]] = Field(default=None, description="""An enum definition that is used as the basis to create a new enum""", json_schema_extra = { "linkml_meta": {'comments': ['All permissible values for all inherited enums are copied to '
                      'form the initial seed set'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    reachable_from: Optional[ReachabilityQuery] = Field(default=None, description="""Specifies a query for obtaining a list of permissible values based on graph reachability""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    matches: Optional[MatchQuery] = Field(default=None, description="""Specifies a match query that is used to calculate the list of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    concepts: Optional[list[str]] = Field(default=None, description="""A list of identifiers that are used to construct a set of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })

    @field_validator('permissible_values', mode='before')
    def coerce_keyed_permissible_values(cls, v):
        return _coerce_keyed_collection(v, "text", value_name="description")

    @field_validator('include', mode='before')
    def coerce_list_include(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('minus', mode='before')
    def coerce_list_minus(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('inherits', mode='before')
    def coerce_list_inherits(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('concepts', mode='before')
    def coerce_list_concepts(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class EnumDefinition(EnumExpression, Definition):
    """
    an element whose instances must be drawn from a specified set of permissible values
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['enum',
                     'enumeration',
                     'semantic enumeration',
                     'value set',
                     'term set',
                     'concept set',
                     'code set',
                     'Terminology Value Set',
                     'answer list',
                     'value domain'],
         'close_mappings': ['skos:ConceptScheme'],
         'exact_mappings': ['qb:HierarchicalCodeList',
                            'NCIT:C113497',
                            'cdisc:ValueDomain'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'mixins': ['enum_expression'],
         'rank': 5})

    enum_uri: Optional[str] = Field(default=None, description="""URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""", json_schema_extra = { "linkml_meta": {'aliases': ['public ID'],
         'domain': 'enum_definition',
         'domain_of': ['enum_definition'],
         'ifabsent': 'class_curie',
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    code_set: Optional[str] = Field(default=None, description="""the identifier of an enumeration code set.""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    code_set_tag: Optional[str] = Field(default=None, description="""the version tag of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['enum_expression cannot have both a code_set_tag and a '
                      'code_set_version'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    code_set_version: Optional[str] = Field(default=None, description="""the version identifier of the enumeration code set""", json_schema_extra = { "linkml_meta": {'comments': ['we assume that version identifiers lexically sort in temporal '
                      'order. Recommend semver when possible'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['BasicSubset']} })
    pv_formula: Optional[PvFormulaOptions] = Field(default=None, description="""Defines the specific formula to be used to generate the permissible values.""", json_schema_extra = { "linkml_meta": {'comments': ['you cannot have BOTH the permissible_values and '
                      'permissible_value_formula tag',
                      'code_set must be supplied for this to be valid'],
         'domain_of': ['enum_expression', 'enum_binding'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    permissible_values: Optional[dict[str, PermissibleValue]] = Field(default=None, description="""A list of possible values for a slot range""", json_schema_extra = { "linkml_meta": {'aliases': ['coded values'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'exact_mappings': ['cdisc:PermissibleValue'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    include: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    minus: Optional[list[AnonymousEnumExpression]] = Field(default=None, description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    inherits: Optional[list[str]] = Field(default=None, description="""An enum definition that is used as the basis to create a new enum""", json_schema_extra = { "linkml_meta": {'comments': ['All permissible values for all inherited enums are copied to '
                      'form the initial seed set'],
         'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    reachable_from: Optional[ReachabilityQuery] = Field(default=None, description="""Specifies a query for obtaining a list of permissible values based on graph reachability""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    matches: Optional[MatchQuery] = Field(default=None, description="""Specifies a match query that is used to calculate the list of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    concepts: Optional[list[str]] = Field(default=None, description="""A list of identifiers that are used to construct a set of permissible values""", json_schema_extra = { "linkml_meta": {'domain': 'enum_expression',
         'domain_of': ['enum_expression'],
         'in_subset': ['SpecificationSubset']} })
    is_a: Optional[str] = Field(default=None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    abstract: Optional[bool] = Field(default=None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile']} })
    mixin: Optional[bool] = Field(default=None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[list[str]] = Field(default=None, description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""", json_schema_extra = { "linkml_meta": {'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    apply_to: Optional[list[str]] = Field(default=None, description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    values_from: Optional[list[str]] = Field(default=None, description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    string_serialization: Optional[str] = Field(default=None, description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition', 'type_mapping'],
         'in_subset': ['SpecificationSubset'],
         'inherited': False,
         'see_also': ['https://github.com/linkml/issues/128']} })
    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('permissible_values', mode='before')
    def coerce_keyed_permissible_values(cls, v):
        return _coerce_keyed_collection(v, "text", value_name="description")

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('include', mode='before')
    def coerce_list_include(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('minus', mode='before')
    def coerce_list_minus(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('inherits', mode='before')
    def coerce_list_inherits(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('concepts', mode='before')
    def coerce_list_concepts(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('mixins', mode='before')
    def coerce_list_mixins(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('apply_to', mode='before')
    def coerce_list_apply_to(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('values_from', mode='before')
    def coerce_list_values_from(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class StructuredAlias(Expression, CommonMetadata, Annotatable, Extensible):
    """
    object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skosxl:Label',
         'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['expression', 'extensible', 'annotatable', 'common_metadata'],
         'slot_usage': {'categories': {'description': 'The category or categories of '
                                                      'an alias. This can be drawn '
                                                      'from any relevant vocabulary',
                                       'examples': [{'description': 'An acronym',
                                                     'value': 'https://w3id.org/mod#acronym'}],
                                       'name': 'categories'}}})

    literal_form: str = Field(default=..., description="""The literal lexical form of a structured alias; i.e the actual alias value.""", json_schema_extra = { "linkml_meta": {'aliases': ['alias_name', 'string_value'],
         'domain': 'structured_alias',
         'domain_of': ['structured_alias'],
         'slot_uri': 'skosxl:literalForm'} })
    predicate: Optional[AliasPredicateEnum] = Field(default=None, description="""The relationship between an element and its alias.""", json_schema_extra = { "linkml_meta": {'domain': 'structured_alias',
         'domain_of': ['structured_alias'],
         'recommended': True,
         'slot_uri': 'rdf:predicate'} })
    categories: Optional[list[str]] = Field(default=None, description="""The category or categories of an alias. This can be drawn from any relevant vocabulary""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'examples': [{'description': 'An acronym',
                       'value': 'https://w3id.org/mod#acronym'}],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    contexts: Optional[list[str]] = Field(default=None, description="""The context in which an alias should be applied""", json_schema_extra = { "linkml_meta": {'domain': 'structured_alias', 'domain_of': ['structured_alias']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contexts', mode='before')
    def coerce_list_contexts(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class AnonymousExpression(Expression, CommonMetadata, Annotatable, Extensible):
    """
    An abstract parent class for any nested expression
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'comments': ['anonymous expressions are useful for when it is necessary to '
                      'build a complex expression without introducing a named element '
                      'for each sub-expression'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['expression', 'extensible', 'annotatable', 'common_metadata']})

    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class PathExpression(Expression, CommonMetadata, Annotatable, Extensible):
    """
    An expression that describes an abstract path from an object to another through a sequence of slot lookups
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['expression', 'extensible', 'annotatable', 'common_metadata'],
         'slot_usage': {'all_of': {'name': 'all_of', 'range': 'path_expression'},
                        'any_of': {'name': 'any_of', 'range': 'path_expression'},
                        'exactly_one_of': {'name': 'exactly_one_of',
                                           'range': 'path_expression'},
                        'followed_by': {'name': 'followed_by',
                                        'range': 'path_expression'},
                        'none_of': {'name': 'none_of', 'range': 'path_expression'}}})

    followed_by: Optional[PathExpression] = Field(default=None, description="""in a sequential list, this indicates the next member""", json_schema_extra = { "linkml_meta": {'domain_of': ['path_expression']} })
    none_of: Optional[list[PathExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[PathExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[PathExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[PathExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    reversed: Optional[bool] = Field(default=None, description="""true if the slot is to be inversed""", json_schema_extra = { "linkml_meta": {'domain_of': ['path_expression']} })
    traverse: Optional[str] = Field(default=None, description="""the slot to traverse""", json_schema_extra = { "linkml_meta": {'domain_of': ['path_expression']} })
    range_expression: Optional[AnonymousClassExpression] = Field(default=None, description="""A range that is described as a boolean expression combining existing ranges""", json_schema_extra = { "linkml_meta": {'comments': ['one use for this is being able to describe a range using any_of '
                      'expressions, for example to combine two enums'],
         'domain': 'slot_expression',
         'domain_of': ['path_expression', 'slot_expression', 'extra_slots_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixin': True,
         'slot_usage': {'all_of': {'name': 'all_of',
                                   'range': 'anonymous_slot_expression'},
                        'any_of': {'name': 'any_of',
                                   'range': 'anonymous_slot_expression'},
                        'exactly_one_of': {'name': 'exactly_one_of',
                                           'range': 'anonymous_slot_expression'},
                        'none_of': {'name': 'none_of',
                                    'range': 'anonymous_slot_expression'}}})

    range: Optional[str] = Field(default=None, description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""", json_schema_extra = { "linkml_meta": {'aliases': ['value domain'],
         'comments': ['range is underspecified, as not all elements can appear as the '
                      'range of a slot.',
                      'to use a URI or CURIE as the range, create a class with the URI '
                      'or curie as the class_uri'],
         'domain': 'slot_definition',
         'domain_of': ['enum_binding', 'slot_expression'],
         'ifabsent': 'default_range',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True} })
    range_expression: Optional[AnonymousClassExpression] = Field(default=None, description="""A range that is described as a boolean expression combining existing ranges""", json_schema_extra = { "linkml_meta": {'comments': ['one use for this is being able to describe a range using any_of '
                      'expressions, for example to combine two enums'],
         'domain': 'slot_expression',
         'domain_of': ['path_expression', 'slot_expression', 'extra_slots_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    enum_range: Optional[EnumExpression] = Field(default=None, description="""An inlined enumeration""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    bindings: Optional[list[EnumBinding]] = Field(default=None, description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['schema_definition', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    required: Optional[bool] = Field(default=None, description="""true means that the slot must be present in instances of the class definition""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 8} })
    recommended: Optional[bool] = Field(default=None, description="""true means that the slot should be present in instances of the class definition, but this is not required""", json_schema_extra = { "linkml_meta": {'comments': ['This is to be used where not all data is expected to conform to '
                      'having a required field',
                      'If a slot is recommended, and it is not populated, applications '
                      'must not treat this as an error. Applications may use this to '
                      'inform the user of missing data'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 9,
         'see_also': ['https://github.com/linkml/linkml/issues/177']} })
    multivalued: Optional[bool] = Field(default=None, description="""true means that slot can have more than one value and should be represented using a list or collection structure.""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 7} })
    inlined: Optional[bool] = Field(default=None, description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""", json_schema_extra = { "linkml_meta": {'comments': ['classes without keys or identifiers are necessarily inlined as '
                      'lists',
                      'only applicable in tree-like serializations, e.g json, yaml'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 25,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    inlined_as_list: Optional[bool] = Field(default=None, description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""", json_schema_extra = { "linkml_meta": {'comments': ['The default loader will accept either list or dictionary form '
                      'as input.  This parameter controls internal\n'
                      'representation and output.',
                      'A keyed or identified class with one additional slot can be '
                      'input in a third form, a dictionary whose key\n'
                      'is the key or identifier and whose value is the one additional '
                      'element.  This form is still stored according\n'
                      'to the inlined_as_list setting.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 27,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    value_presence: Optional[PresenceEnum] = Field(default=None, description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""", json_schema_extra = { "linkml_meta": {'comments': ['if set to true this has the same effect as required=true. In '
                      'contrast, required=false allows a value to be present'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_expression: Optional[str] = Field(default=None, description="""the value of the slot must equal the value of the evaluated expression""", json_schema_extra = { "linkml_meta": {'comments': ["for example, a 'length' slot may have an equals_expression with "
                      "value '(end-start)+1'"],
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'see_also': ['https://linkml.io/linkml/developers/inference.html',
                      'https://linkml.io/linkml/schemas/advanced.html#equals-expression']} })
    exact_cardinality: Optional[int] = Field(default=None, description="""the exact number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['if exact_cardinality is set, then minimum_cardinalty and '
                      'maximum_cardinality must be unset or have the same value'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    minimum_cardinality: Optional[int] = Field(default=None, description="""the minimum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['minimum_cardinality cannot be greater than maximum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    maximum_cardinality: Optional[int] = Field(default=None, description="""the maximum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['maximum_cardinality cannot be less than minimum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    has_member: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with at least one member satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    all_members: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with all members satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    none_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    array: Optional[ArrayExpression] = Field(default=None, description="""coerces the value of the slot into an array and defines the dimensions of that array""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'status': 'testing'} })

    @field_validator('bindings', mode='before')
    def coerce_list_bindings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class AnonymousSlotExpression(SlotExpression, AnonymousExpression):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta', 'mixins': ['slot_expression']})

    range: Optional[str] = Field(default=None, description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""", json_schema_extra = { "linkml_meta": {'aliases': ['value domain'],
         'comments': ['range is underspecified, as not all elements can appear as the '
                      'range of a slot.',
                      'to use a URI or CURIE as the range, create a class with the URI '
                      'or curie as the class_uri'],
         'domain': 'slot_definition',
         'domain_of': ['enum_binding', 'slot_expression'],
         'ifabsent': 'default_range',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True} })
    range_expression: Optional[AnonymousClassExpression] = Field(default=None, description="""A range that is described as a boolean expression combining existing ranges""", json_schema_extra = { "linkml_meta": {'comments': ['one use for this is being able to describe a range using any_of '
                      'expressions, for example to combine two enums'],
         'domain': 'slot_expression',
         'domain_of': ['path_expression', 'slot_expression', 'extra_slots_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    enum_range: Optional[EnumExpression] = Field(default=None, description="""An inlined enumeration""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    bindings: Optional[list[EnumBinding]] = Field(default=None, description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['schema_definition', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    required: Optional[bool] = Field(default=None, description="""true means that the slot must be present in instances of the class definition""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 8} })
    recommended: Optional[bool] = Field(default=None, description="""true means that the slot should be present in instances of the class definition, but this is not required""", json_schema_extra = { "linkml_meta": {'comments': ['This is to be used where not all data is expected to conform to '
                      'having a required field',
                      'If a slot is recommended, and it is not populated, applications '
                      'must not treat this as an error. Applications may use this to '
                      'inform the user of missing data'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 9,
         'see_also': ['https://github.com/linkml/linkml/issues/177']} })
    multivalued: Optional[bool] = Field(default=None, description="""true means that slot can have more than one value and should be represented using a list or collection structure.""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 7} })
    inlined: Optional[bool] = Field(default=None, description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""", json_schema_extra = { "linkml_meta": {'comments': ['classes without keys or identifiers are necessarily inlined as '
                      'lists',
                      'only applicable in tree-like serializations, e.g json, yaml'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 25,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    inlined_as_list: Optional[bool] = Field(default=None, description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""", json_schema_extra = { "linkml_meta": {'comments': ['The default loader will accept either list or dictionary form '
                      'as input.  This parameter controls internal\n'
                      'representation and output.',
                      'A keyed or identified class with one additional slot can be '
                      'input in a third form, a dictionary whose key\n'
                      'is the key or identifier and whose value is the one additional '
                      'element.  This form is still stored according\n'
                      'to the inlined_as_list setting.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 27,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    value_presence: Optional[PresenceEnum] = Field(default=None, description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""", json_schema_extra = { "linkml_meta": {'comments': ['if set to true this has the same effect as required=true. In '
                      'contrast, required=false allows a value to be present'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_expression: Optional[str] = Field(default=None, description="""the value of the slot must equal the value of the evaluated expression""", json_schema_extra = { "linkml_meta": {'comments': ["for example, a 'length' slot may have an equals_expression with "
                      "value '(end-start)+1'"],
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'see_also': ['https://linkml.io/linkml/developers/inference.html',
                      'https://linkml.io/linkml/schemas/advanced.html#equals-expression']} })
    exact_cardinality: Optional[int] = Field(default=None, description="""the exact number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['if exact_cardinality is set, then minimum_cardinalty and '
                      'maximum_cardinality must be unset or have the same value'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    minimum_cardinality: Optional[int] = Field(default=None, description="""the minimum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['minimum_cardinality cannot be greater than maximum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    maximum_cardinality: Optional[int] = Field(default=None, description="""the maximum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['maximum_cardinality cannot be less than minimum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    has_member: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with at least one member satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    all_members: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with all members satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    none_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    array: Optional[ArrayExpression] = Field(default=None, description="""coerces the value of the slot into an array and defines the dimensions of that array""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'status': 'testing'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('bindings', mode='before')
    def coerce_list_bindings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class SlotDefinition(SlotExpression, Definition):
    """
    an element that describes how instances are related to other instances
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['slot', 'field', 'property', 'attribute', 'column', 'variable'],
         'close_mappings': ['rdf:Property', 'qb:ComponentProperty'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'OwlProfile'],
         'mixins': ['slot_expression'],
         'rank': 3,
         'slot_usage': {'apply_to': {'name': 'apply_to', 'range': 'slot_definition'},
                        'disjoint_with': {'name': 'disjoint_with',
                                          'range': 'slot_definition'},
                        'is_a': {'description': 'A primary parent slot from which '
                                                'inheritable metaslots are propagated',
                                 'name': 'is_a',
                                 'range': 'slot_definition'},
                        'mixins': {'description': 'A collection of secondary parent '
                                                  'mixin slots from which inheritable '
                                                  'metaslots are propagated',
                                   'name': 'mixins',
                                   'range': 'slot_definition'},
                        'union_of': {'name': 'union_of', 'range': 'slot_definition'}}})

    singular_name: Optional[str] = Field(default=None, description="""a name that is used in the singular form""", json_schema_extra = { "linkml_meta": {'close_mappings': ['skos:altLabel'],
         'comments': ['this may be used in some schema translations where use of a '
                      'singular form is idiomatic, for example RDF'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['BasicSubset']} })
    domain: Optional[str] = Field(default=None, description="""defines the type of the subject of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts that X is an instance of C1
""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True} })
    slot_uri: Optional[str] = Field(default=None, description="""URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.""", json_schema_extra = { "linkml_meta": {'aliases': ['public ID'],
         'comments': ['Assigning slot_uris can provide additional hooks for '
                      'interoperation, indicating a common conceptual model',
                      'To use a URI or CURIE as a range, create a class with the URI '
                      'or CURIE as the class_uri'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'ifabsent': 'slot_curie',
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 2,
         'see_also': ['linkml:definition_uri',
                      'https://linkml.io/linkml/schemas/uris-and-mappings.html']} })
    inherited: Optional[bool] = Field(default=None, description="""true means that the *value* of a slot is inherited by subclasses""", json_schema_extra = { "linkml_meta": {'comments': ['the slot is to be used for defining *metamodels* only',
                      'Inherited applies to slot values.  Parent *slots* are always '
                      'inherited by subclasses'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True} })
    readonly: Optional[str] = Field(default=None, description="""If present, slot is read only.  Text explains why""", json_schema_extra = { "linkml_meta": {'comments': ['the slot is to be used for defining *metamodels* only'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True} })
    ifabsent: Optional[str] = Field(default=None, description="""function that provides a default value for the slot.
  * [Tt]rue -- boolean True
  * [Ff]alse -- boolean False
  * bnode -- blank node identifier
  * class_curie -- CURIE for the containing class
  * class_uri -- URI for the containing class
  * default_ns -- schema default namespace
  * default_range -- schema default range
  * int(value) -- integer value
  * slot_uri -- URI for the slot
  * slot_curie -- CURIE for the slot
  * string(value) -- string value
  * EnumName(PermissibleValue) -- enum value""", json_schema_extra = { "linkml_meta": {'close_mappings': ['sh:defaultValue'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['linkml:equals_expression']} })
    list_elements_unique: Optional[bool] = Field(default=None, description="""If True, then there must be no duplicates in the elements of a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['should only be used with multivalued slots'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True} })
    list_elements_ordered: Optional[bool] = Field(default=None, description="""If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed""", json_schema_extra = { "linkml_meta": {'comments': ['should only be used with multivalued slots'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'status': 'testing'} })
    shared: Optional[bool] = Field(default=None, description="""If True, then the relationship between the slot domain and range is many to one or many to many""", json_schema_extra = { "linkml_meta": {'aliases': ['inverse functional', 'many to one or many'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True} })
    key: Optional[bool] = Field(default=None, description="""True means that the key slot(s) uniquely identify the elements within a single container""", json_schema_extra = { "linkml_meta": {'comments': ['key is inherited',
                      'a given domain can have at most one key slot (restriction to be '
                      'removed in the future)',
                      'identifiers and keys are mutually exclusive.  A given domain '
                      'cannot have both',
                      'a key slot is automatically required.  Keys cannot be optional'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'RelationalModelProfile'],
         'inherited': True,
         'see_also': ['linkml:unique_keys']} })
    identifier: Optional[bool] = Field(default=None, description="""True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container""", json_schema_extra = { "linkml_meta": {'aliases': ['primary key', 'ID', 'UID', 'code'],
         'comments': ['identifier is inherited',
                      'a key slot is automatically required.  Identifiers cannot be '
                      'optional',
                      'a given domain can have at most one identifier',
                      'identifiers and keys are mutually exclusive.  A given domain '
                      'cannot have both'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile'],
         'inherited': True,
         'rank': 5,
         'see_also': ['https://en.wikipedia.org/wiki/Identifier', 'linkml:unique_keys']} })
    designates_type: Optional[bool] = Field(default=None, description="""True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition""", json_schema_extra = { "linkml_meta": {'aliases': ['type designator'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/type-designators.html']} })
    alias: Optional[str] = Field(default=None, description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of alias is used within this metamodel, '
                      'slot_definitions is aliases as slots',
                      'not to be confused with aliases, which indicates a set of terms '
                      'to be used for search purposes.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition', 'class_definition', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'rank': 6,
         'slot_uri': 'skos:prefLabel'} })
    owner: Optional[str] = Field(default=None, description="""the \"owner\" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot""", json_schema_extra = { "linkml_meta": {'deprecated': 'Will be replaced by domain_of and eventually removed',
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'readonly': 'filled in by loader -- either class domain or slot domain'} })
    domain_of: Optional[list[str]] = Field(default=None, description="""the class(es) that reference the slot in a \"slots\" or \"slot_usage\" context""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'exact_mappings': ['schema:domainIncludes', 'SIO:000011'],
         'readonly': 'filled in by the loader'} })
    subproperty_of: Optional[str] = Field(default=None, description="""Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'examples': [{'description': 'this is the RO term for "in homology '
                                      'relationship with", and used as a value of '
                                      'subproperty of this means that any ontological '
                                      'child (related to RO:HOM0000001 via an is_a '
                                      'relationship), is a valid value for the slot '
                                      'that declares this with the subproperty_of '
                                      "tag.  This differs from the 'values_from' meta "
                                      "model component in that 'values_from' requires "
                                      'the id of a value set (said another way, if an '
                                      'entire ontology had a curie/identifier that was '
                                      'the identifier for the entire ontology, then '
                                      'that identifier would be used in '
                                      "'values_from.')",
                       'value': 'RO:HOM0000001'}],
         'slot_uri': 'rdfs:subPropertyOf'} })
    symmetric: Optional[bool] = Field(default=None, description="""If s is symmetric, and i.s=v, then v.s=i""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:SymmetricProperty'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    reflexive: Optional[bool] = Field(default=None, description="""If s is reflexive, then i.s=i for all instances i""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:ReflexiveProperty'],
         'comments': ['it is rare for a property to be reflexive, this characteristic '
                      'is added for completeness, consider instead locally_reflexive'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    locally_reflexive: Optional[bool] = Field(default=None, description="""If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    irreflexive: Optional[bool] = Field(default=None, description="""If s is irreflexive, then there exists no i such i.s=i""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:IrreflexiveProperty'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    asymmetric: Optional[bool] = Field(default=None, description="""If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:AsymmetricProperty'],
         'comments': ['asymmetry is the combination of antisymmetry and irreflexivity'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    transitive: Optional[bool] = Field(default=None, description="""If s is transitive, and i.s=z, and s.s=j, then i.s=j""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:TransitiveProperty'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'relational_logical_characteristic'} })
    inverse: Optional[str] = Field(default=None, description="""indicates that any instance of d s r implies that there is also an instance of r s' d""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'slot_uri': 'owl:inverseOf'} })
    is_class_field: Optional[bool] = Field(default=None, description="""indicates that for any instance, i, the domain of this slot will include an assertion of i s range""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition', 'domain_of': ['slot_definition']} })
    transitive_form_of: Optional[str] = Field(default=None, description="""If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive""", json_schema_extra = { "linkml_meta": {'comments': ['Example: ancestor_of is the transitive_form_of parent_of'],
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset']} })
    reflexive_transitive_form_of: Optional[str] = Field(default=None, description="""transitive_form_of including the reflexive case""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'transitive_form_of'} })
    role: Optional[str] = Field(default=None, description="""a textual descriptor that indicates the role played by the slot range""", json_schema_extra = { "linkml_meta": {'comments': ['the primary use case for this slot is to provide a textual '
                      'descriptor of a generic slot name when used in the context of a '
                      'more specific class'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True} })
    is_usage_slot: Optional[bool] = Field(default=None, description="""True means that this slot was defined in a slot_usage situation""", json_schema_extra = { "linkml_meta": {'deprecated': 'Replaced by usage_slot_name',
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'readonly': 'filled in by the loader'} })
    usage_slot_name: Optional[str] = Field(default=None, description="""The name of the slot referenced in the slot_usage""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'readonly': 'filled in by the loader'} })
    relational_role: Optional[RelationalRoleEnum] = Field(default=None, description="""the role a slot on a relationship class plays, for example, the subject, object or predicate roles""", json_schema_extra = { "linkml_meta": {'aliases': ['reification_role'],
         'comments': ['this should only be used on slots that are applicable to class '
                      'that represent relationships',
                      'in the context of RDF, this should be used for slots that can '
                      'be modeled using the RDF reification vocabulary',
                      'in the context of property graphs, this should be used on edge '
                      'classes to indicate which slots represent the input and output '
                      'nodes'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'status': 'testing'} })
    slot_group: Optional[str] = Field(default=None, description="""allows for grouping of related slots into a grouping slot that serves the role of a group""", json_schema_extra = { "linkml_meta": {'comments': ['slot groups do not change the semantics of a model but are a '
                      'useful way of visually grouping related slots'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'range_expression': {'slot_conditions': {'is_grouping_slot': {'equals_expression': 'True',
                                                                       'name': 'is_grouping_slot'}}},
         'slot_uri': 'sh:group'} })
    is_grouping_slot: Optional[bool] = Field(default=None, description="""true if this slot is a grouping slot""", json_schema_extra = { "linkml_meta": {'close_mappings': ['sh:PropertyGroup'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    path_rule: Optional[PathExpression] = Field(default=None, description="""a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition', 'domain_of': ['slot_definition']} })
    disjoint_with: Optional[list[str]] = Field(default=None, description="""Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['slot_definition', 'class_definition'],
         'in_subset': ['SpecificationSubset']} })
    children_are_mutually_disjoint: Optional[bool] = Field(default=None, description="""If true then all direct is_a children are mutually disjoint and share no instances in common""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['slot_definition', 'class_definition']} })
    union_of: Optional[list[str]] = Field(default=None, description="""indicates that the domain element consists exactly of the members of the element in the range.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['type_definition', 'slot_definition', 'class_definition'],
         'in_subset': ['SpecificationSubset', 'OwlProfile'],
         'notes': ['this only applies in the OWL generation']} })
    type_mappings: Optional[list[str]] = Field(default=None, description="""A collection of type mappings that specify how a slot's range should be mapped or serialized in different frameworks""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_definition']} })
    range: Optional[str] = Field(default=None, description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""", json_schema_extra = { "linkml_meta": {'aliases': ['value domain'],
         'comments': ['range is underspecified, as not all elements can appear as the '
                      'range of a slot.',
                      'to use a URI or CURIE as the range, create a class with the URI '
                      'or curie as the class_uri'],
         'domain': 'slot_definition',
         'domain_of': ['enum_binding', 'slot_expression'],
         'ifabsent': 'default_range',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True} })
    range_expression: Optional[AnonymousClassExpression] = Field(default=None, description="""A range that is described as a boolean expression combining existing ranges""", json_schema_extra = { "linkml_meta": {'comments': ['one use for this is being able to describe a range using any_of '
                      'expressions, for example to combine two enums'],
         'domain': 'slot_expression',
         'domain_of': ['path_expression', 'slot_expression', 'extra_slots_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    enum_range: Optional[EnumExpression] = Field(default=None, description="""An inlined enumeration""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    bindings: Optional[list[EnumBinding]] = Field(default=None, description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['schema_definition', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    required: Optional[bool] = Field(default=None, description="""true means that the slot must be present in instances of the class definition""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 8} })
    recommended: Optional[bool] = Field(default=None, description="""true means that the slot should be present in instances of the class definition, but this is not required""", json_schema_extra = { "linkml_meta": {'comments': ['This is to be used where not all data is expected to conform to '
                      'having a required field',
                      'If a slot is recommended, and it is not populated, applications '
                      'must not treat this as an error. Applications may use this to '
                      'inform the user of missing data'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 9,
         'see_also': ['https://github.com/linkml/linkml/issues/177']} })
    multivalued: Optional[bool] = Field(default=None, description="""true means that slot can have more than one value and should be represented using a list or collection structure.""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile'],
         'inherited': True,
         'rank': 7} })
    inlined: Optional[bool] = Field(default=None, description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""", json_schema_extra = { "linkml_meta": {'comments': ['classes without keys or identifiers are necessarily inlined as '
                      'lists',
                      'only applicable in tree-like serializations, e.g json, yaml'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 25,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    inlined_as_list: Optional[bool] = Field(default=None, description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""", json_schema_extra = { "linkml_meta": {'comments': ['The default loader will accept either list or dictionary form '
                      'as input.  This parameter controls internal\n'
                      'representation and output.',
                      'A keyed or identified class with one additional slot can be '
                      'input in a third form, a dictionary whose key\n'
                      'is the key or identifier and whose value is the one additional '
                      'element.  This form is still stored according\n'
                      'to the inlined_as_list setting.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 27,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    minimum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(default=None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    pattern: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'inherited': True,
         'rank': 35} })
    structured_pattern: Optional[PatternExpression] = Field(default=None, description="""the string value of the slot must conform to the regular expression in the pattern expression""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#structured-patterns']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    implicit_prefix: Optional[str] = Field(default=None, description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""", json_schema_extra = { "linkml_meta": {'domain': 'slot_expression',
         'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })
    value_presence: Optional[PresenceEnum] = Field(default=None, description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""", json_schema_extra = { "linkml_meta": {'comments': ['if set to true this has the same effect as required=true. In '
                      'contrast, required=false allows a value to be present'],
         'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_string: Optional[str] = Field(default=None, description="""the slot must have range string and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    equals_string_in: Optional[list[str]] = Field(default=None, description="""the slot must have range string and the value of the slot must equal one of the specified values""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    equals_number: Optional[int] = Field(default=None, description="""the slot must have range of a number and the value of the slot must equal the specified value""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'status': 'unstable'} })
    equals_expression: Optional[str] = Field(default=None, description="""the value of the slot must equal the value of the evaluated expression""", json_schema_extra = { "linkml_meta": {'comments': ["for example, a 'length' slot may have an equals_expression with "
                      "value '(end-start)+1'"],
         'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant',
         'see_also': ['https://linkml.io/linkml/developers/inference.html',
                      'https://linkml.io/linkml/schemas/advanced.html#equals-expression']} })
    exact_cardinality: Optional[int] = Field(default=None, description="""the exact number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['if exact_cardinality is set, then minimum_cardinalty and '
                      'maximum_cardinality must be unset or have the same value'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    minimum_cardinality: Optional[int] = Field(default=None, description="""the minimum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['minimum_cardinality cannot be greater than maximum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    maximum_cardinality: Optional[int] = Field(default=None, description="""the maximum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['maximum_cardinality cannot be less than minimum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    has_member: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with at least one member satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    all_members: Optional[AnonymousSlotExpression] = Field(default=None, description="""the value of the slot is multivalued with all members satisfying the condition""", json_schema_extra = { "linkml_meta": {'domain_of': ['slot_expression'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'list_value_specification_constant',
         'status': 'testing'} })
    none_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    any_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousSlotExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    array: Optional[ArrayExpression] = Field(default=None, description="""coerces the value of the slot into an array and defines the dimensions of that array""", json_schema_extra = { "linkml_meta": {'domain': 'slot_definition',
         'domain_of': ['slot_expression'],
         'inherited': True,
         'status': 'testing'} })
    is_a: Optional[str] = Field(default=None, description="""A primary parent slot from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    abstract: Optional[bool] = Field(default=None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile']} })
    mixin: Optional[bool] = Field(default=None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[list[str]] = Field(default=None, description="""A collection of secondary parent mixin slots from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    apply_to: Optional[list[str]] = Field(default=None, description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    values_from: Optional[list[str]] = Field(default=None, description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    string_serialization: Optional[str] = Field(default=None, description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition', 'type_mapping'],
         'in_subset': ['SpecificationSubset'],
         'inherited': False,
         'see_also': ['https://github.com/linkml/issues/128']} })
    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('domain_of', mode='before')
    def coerce_list_domain_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('disjoint_with', mode='before')
    def coerce_list_disjoint_with(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('union_of', mode='before')
    def coerce_list_union_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('type_mappings', mode='before')
    def coerce_list_type_mappings(cls, v):
        return _coerce_inlined_list(v, "framework")


    @field_validator('bindings', mode='before')
    def coerce_list_bindings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('equals_string_in', mode='before')
    def coerce_list_equals_string_in(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('mixins', mode='before')
    def coerce_list_mixins(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('apply_to', mode='before')
    def coerce_list_apply_to(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('values_from', mode='before')
    def coerce_list_values_from(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ClassExpression(ConfiguredBaseModel):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixin': True,
         'slot_usage': {'all_of': {'name': 'all_of',
                                   'range': 'anonymous_class_expression'},
                        'any_of': {'name': 'any_of',
                                   'range': 'anonymous_class_expression'},
                        'exactly_one_of': {'name': 'exactly_one_of',
                                           'range': 'anonymous_class_expression'},
                        'none_of': {'name': 'none_of',
                                    'range': 'anonymous_class_expression'}}})

    any_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    none_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    slot_conditions: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""expresses constraints on a group of slots for a class expression""", json_schema_extra = { "linkml_meta": {'domain': 'class_expression',
         'domain_of': ['class_expression'],
         'in_subset': ['SpecificationSubset']} })

    @field_validator('slot_conditions', mode='before')
    def coerce_keyed_slot_conditions(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class AnonymousClassExpression(ClassExpression, AnonymousExpression):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta', 'mixins': ['class_expression']})

    is_a: Optional[str] = Field(default=None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    any_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    none_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    slot_conditions: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""expresses constraints on a group of slots for a class expression""", json_schema_extra = { "linkml_meta": {'domain': 'class_expression',
         'domain_of': ['class_expression'],
         'in_subset': ['SpecificationSubset']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('slot_conditions', mode='before')
    def coerce_keyed_slot_conditions(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ClassDefinition(ClassExpression, Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['table', 'record', 'template', 'message', 'observation'],
         'close_mappings': ['owl:Class'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'mixins': ['class_expression'],
         'rank': 2,
         'slot_usage': {'apply_to': {'name': 'apply_to', 'range': 'class_definition'},
                        'disjoint_with': {'name': 'disjoint_with',
                                          'range': 'class_definition'},
                        'is_a': {'description': 'A primary parent class from which '
                                                'inheritable metaslots are propagated',
                                 'name': 'is_a',
                                 'range': 'class_definition'},
                        'mixins': {'description': 'A collection of secondary parent '
                                                  'mixin classes from which '
                                                  'inheritable metaslots are '
                                                  'propagated',
                                   'name': 'mixins',
                                   'range': 'class_definition'},
                        'rules': {'name': 'rules', 'range': 'class_rule'},
                        'union_of': {'name': 'union_of', 'range': 'class_definition'}}})

    slots: Optional[list[str]] = Field(default=None, description="""collection of slot names that are applicable to a class""", json_schema_extra = { "linkml_meta": {'comments': ['the list of applicable slots is inherited from parent classes',
                      'This defines the set of slots that are allowed to be used for a '
                      'given class. The final list of slots for a class is the '
                      'combination of the parent (is a) slots, mixins slots, apply to '
                      'slots minus the slot usage entries.'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 19} })
    slot_usage: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""the refinement of a slot in the context of the containing class definition.""", json_schema_extra = { "linkml_meta": {'comments': ['Many slots may be reused across different classes, but the '
                      'meaning of the slot may be refined by context. For example, a '
                      'generic association model may use slots '
                      'subject/predicate/object with generic semantics and minimal '
                      'constraints. When this is subclasses, e.g. to disease-phenotype '
                      'associations then slot usage may specify both local naming '
                      '(e.g. subject=disease) and local constraints'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 23} })
    attributes: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""Inline definition of slots""", json_schema_extra = { "linkml_meta": {'comments': ['attributes are an alternative way of defining new slots.  An '
                      'attribute adds a slot to the global space in the form '
                      '<class_name>__<slot_name> (lower case, double underscores).  '
                      'Attributes can be specialized via slot_usage.'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 29} })
    class_uri: Optional[str] = Field(default=None, description="""URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""", json_schema_extra = { "linkml_meta": {'aliases': ['public ID'],
         'comments': ['Assigning class_uris can provide additional hooks for '
                      'interoperation, indicating a common conceptual model'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'ifabsent': 'class_curie',
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 2,
         'see_also': ['linkml:definition_uri',
                      'https://linkml.io/linkml/schemas/uris-and-mappings.html']} })
    subclass_of: Optional[str] = Field(default=None, description="""DEPRECATED -- rdfs:subClassOf to be emitted in OWL generation""", json_schema_extra = { "linkml_meta": {'close_mappings': ['rdfs:subClassOf'],
         'deprecated': 'Use is_a instead',
         'domain': 'class_definition',
         'domain_of': ['class_definition']} })
    union_of: Optional[list[str]] = Field(default=None, description="""indicates that the domain element consists exactly of the members of the element in the range.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['type_definition', 'slot_definition', 'class_definition'],
         'in_subset': ['SpecificationSubset', 'OwlProfile'],
         'notes': ['this only applies in the OWL generation']} })
    defining_slots: Optional[list[str]] = Field(default=None, description="""The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'inherited': True} })
    tree_root: Optional[bool] = Field(default=None, description="""Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'notes': ['each schema should have at most one tree root'],
         'rank': 31,
         'see_also': ['https://linkml.io/linkml/intro/tutorial02.html']} })
    unique_keys: Optional[dict[str, UniqueKey]] = Field(default=None, description="""A collection of named unique keys for this class. Unique keys may be singular or compound.""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'exact_mappings': ['owl:hasKey'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'RelationalModelProfile'],
         'see_also': ['https://linkml.io/linkml/schemas/constraints.html#unique-key']} })
    rules: Optional[list[ClassRule]] = Field(default=None, description="""the collection of rules that apply to all members of this class""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset'],
         'slot_uri': 'sh:rule'} })
    classification_rules: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""The collection of classification rules that apply to all members of this class. Classification rules allow for automatically assigning the instantiated type of an instance.""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'in_subset': ['SpecificationSubset']} })
    slot_names_unique: Optional[bool] = Field(default=None, description="""if true then induced/mangled slot names are not created for class_usage and attributes""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['schema_definition', 'class_definition'],
         'status': 'testing'} })
    represents_relationship: Optional[bool] = Field(default=None, description="""true if this class represents a relationship rather than an entity""", json_schema_extra = { "linkml_meta": {'aliases': ['is_reified'],
         'comments': ['in the context of Entity-Relationship (ER) modeling, this is '
                      'used to state that a class models a relationship between '
                      'entities, and should be drawn with a diamond',
                      'in the context of RDF, this should be used when instances of '
                      'the class are `rdf:Statement`s',
                      'in the context of property graphs, this should be used when a '
                      'class is used to represent an edge that connects nodes'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'inherited': True,
         'see_also': ['rdf:Statement',
                      'https://patterns.dataincubator.org/book/qualified-relation.html'],
         'status': 'testing'} })
    disjoint_with: Optional[list[str]] = Field(default=None, description="""Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['slot_definition', 'class_definition'],
         'in_subset': ['SpecificationSubset']} })
    children_are_mutually_disjoint: Optional[bool] = Field(default=None, description="""If true then all direct is_a children are mutually disjoint and share no instances in common""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['slot_definition', 'class_definition']} })
    extra_slots: Optional[ExtraSlotsExpression] = Field(default=None, description="""How a class instance handles extra data not specified in the class definition.
Note that this does *not* define the constraints that are placed on additional slots defined by inheriting classes.

Possible values:
- `allowed: true` - allow all additional data
- `allowed: false` (or `allowed:` or `allowed: null` while `range_expression` is `null`) -
  forbid all additional data (default)
- `range_expression: ...`  - allow additional data if it matches the slot expression (see examples)
""", json_schema_extra = { "linkml_meta": {'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'examples': [{'description': 'Allow all additional data',
                       'object': {'allowed': True}},
                      {'description': 'Forbid any additional data',
                       'object': {'allowed': False}},
                      {'description': 'Allow additional data that are strings',
                       'object': {'range_expression': {'range': 'string'}}},
                      {'description': 'Allow additional data if they are instances of '
                                      'the class definition "AClassDefinition"',
                       'object': {'range_expression': {'range': 'AClassDefinition'}}},
                      {'description': 'allow additional data if they are either '
                                      'strings or integers',
                       'object': {'range_expression': {'any_of': [{'range': 'string'},
                                                                  {'range': 'integer'}]}}},
                      {'description': 'Allow additional data if they are lists of '
                                      'integers of at most length 5.\n'
                                      'Note that this does *not* mean that a maximum '
                                      'of 5 extra slots are allowed.\n',
                       'object': {'range_expression': {'maximum_cardinality': 5,
                                                       'multivalued': True,
                                                       'range': 'integer'}}},
                      {'description': 'Allow additional data if they are integers.\n'
                                      '`required` is meaningless in this context and '
                                      'ignored, since by definition all "extra" slots '
                                      'are optional.\n',
                       'object': {'range_expression': {'range': 'integer',
                                                       'required': True}}},
                      {'description': 'A semantically *invalid* use of `extra_slots`, '
                                      'as extra slots will be forbidden and the\n'
                                      '`anonymous_slot_expression` will be ignored.\n',
                       'object': {'allowed': False,
                                  'range_expression': {'range': 'string'}}}],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    alias: Optional[str] = Field(default=None, description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of alias is used within this metamodel, '
                      'slot_definitions is aliases as slots',
                      'not to be confused with aliases, which indicates a set of terms '
                      'to be used for search purposes.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition', 'class_definition', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'rank': 6,
         'slot_uri': 'skos:prefLabel'} })
    any_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:or'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:xone'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    none_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:not'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[list[AnonymousClassExpression]] = Field(default=None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression',
                       'path_expression',
                       'slot_expression',
                       'class_expression'],
         'exact_mappings': ['sh:and'],
         'in_subset': ['SpecificationSubset'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    slot_conditions: Optional[dict[str, SlotDefinition]] = Field(default=None, description="""expresses constraints on a group of slots for a class expression""", json_schema_extra = { "linkml_meta": {'domain': 'class_expression',
         'domain_of': ['class_expression'],
         'in_subset': ['SpecificationSubset']} })
    is_a: Optional[str] = Field(default=None, description="""A primary parent class from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    abstract: Optional[bool] = Field(default=None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile']} })
    mixin: Optional[bool] = Field(default=None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'ObjectOrientedProfile'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[list[str]] = Field(default=None, description="""A collection of secondary parent mixin classes from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    apply_to: Optional[list[str]] = Field(default=None, description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    values_from: Optional[list[str]] = Field(default=None, description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""", json_schema_extra = { "linkml_meta": {'domain': 'definition', 'domain_of': ['definition'], 'status': 'testing'} })
    string_serialization: Optional[str] = Field(default=None, description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition', 'type_mapping'],
         'in_subset': ['SpecificationSubset'],
         'inherited': False,
         'see_also': ['https://github.com/linkml/issues/128']} })
    name: str = Field(default=..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'in_subset': ['SpecificationSubset',
                       'OwlProfile',
                       'MinimalSubset',
                       'BasicSubset',
                       'RelationalModelProfile',
                       'ObjectOrientedProfile'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name',
                      'https://linkml.io/linkml/faq/modeling.html#why-are-my-class-names-translated-to-camelcase'],
         'slot_uri': 'rdfs:label'} })
    id_prefixes: Optional[list[str]] = Field(default=None, description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""", json_schema_extra = { "linkml_meta": {'comments': ['Order of elements may be used to indicate priority order',
                      'If identifiers are treated as CURIEs, then the CURIE must start '
                      'with one of the indicated prefixes followed by `:` (_should_ '
                      'start if the list is open)',
                      'If identifiers are treated as URIs, then the URI string must '
                      'start with the expanded for of the prefix (_should_ start if '
                      'the list is open)'],
         'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'see_also': ['https://github.com/linkml/linkml-model/issues/28']} })
    id_prefixes_are_closed: Optional[bool] = Field(default=None, description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'see_also': ['https://github.com/linkml/linkml/issues/194']} })
    definition_uri: Optional[str] = Field(default=None, description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""", json_schema_extra = { "linkml_meta": {'comments': ['Formed by combining the default_prefix with the normalized '
                      'element name'],
         'domain': 'element',
         'domain_of': ['element'],
         'readonly': 'filled in by the schema loader or schema view',
         'see_also': ['linkml:class_uri', 'linkml:slot_uri']} })
    local_names: Optional[dict[str, Union[str, LocalName]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element']} })
    conforms_to: Optional[str] = Field(default=None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['element'],
         'in_subset': ['BasicSubset'],
         'see_also': ['linkml:implements'],
         'slot_uri': 'dcterms:conformsTo'} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('slot_usage', mode='before')
    def coerce_keyed_slot_usage(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('attributes', mode='before')
    def coerce_keyed_attributes(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('unique_keys', mode='before')
    def coerce_keyed_unique_keys(cls, v):
        return _coerce_keyed_collection(v, "unique_key_name", value_name="unique_key_slots")

    @field_validator('slot_conditions', mode='before')
    def coerce_keyed_slot_conditions(cls, v):
        return _coerce_keyed_collection(v, "name", value_name="id_prefixes")

    @field_validator('local_names', mode='before')
    def coerce_keyed_local_names(cls, v):
        return _coerce_keyed_collection(v, "local_name_source", value_name="local_name_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('slots', mode='before')
    def coerce_list_slots(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('union_of', mode='before')
    def coerce_list_union_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('defining_slots', mode='before')
    def coerce_list_defining_slots(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('rules', mode='before')
    def coerce_list_rules(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('classification_rules', mode='before')
    def coerce_list_classification_rules(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('disjoint_with', mode='before')
    def coerce_list_disjoint_with(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('any_of', mode='before')
    def coerce_list_any_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exactly_one_of', mode='before')
    def coerce_list_exactly_one_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('none_of', mode='before')
    def coerce_list_none_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('all_of', mode='before')
    def coerce_list_all_of(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('mixins', mode='before')
    def coerce_list_mixins(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('apply_to', mode='before')
    def coerce_list_apply_to(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('values_from', mode='before')
    def coerce_list_values_from(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('id_prefixes', mode='before')
    def coerce_list_id_prefixes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ClassLevelRule(ConfiguredBaseModel):
    """
    A rule that is applied to classes
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/linkml/meta'})

    pass


class ClassRule(ClassLevelRule, CommonMetadata, Annotatable, Extensible):
    """
    A rule that applies to instances of a class
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['if rule'],
         'close_mappings': ['sh:TripleRule', 'swrl:Imp'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset'],
         'mixins': ['extensible', 'annotatable', 'common_metadata']})

    preconditions: Optional[AnonymousClassExpression] = Field(default=None, description="""an expression that must hold in order for the rule to be applicable to an instance""", json_schema_extra = { "linkml_meta": {'aliases': ['if', 'body', 'antecedents'],
         'close_mappings': ['swrl:body'],
         'domain_of': ['class_rule'],
         'in_subset': ['SpecificationSubset'],
         'rank': 111,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules'],
         'slot_uri': 'sh:condition'} })
    postconditions: Optional[AnonymousClassExpression] = Field(default=None, description="""an expression that must hold for an instance of the class, if the preconditions hold""", json_schema_extra = { "linkml_meta": {'aliases': ['then', 'head', 'consequents'],
         'close_mappings': ['swrl:body'],
         'domain_of': ['class_rule'],
         'in_subset': ['SpecificationSubset'],
         'rank': 113,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    elseconditions: Optional[AnonymousClassExpression] = Field(default=None, description="""an expression that must hold for an instance of the class, if the preconditions no not hold""", json_schema_extra = { "linkml_meta": {'aliases': ['else'],
         'domain_of': ['class_rule'],
         'in_subset': ['SpecificationSubset'],
         'rank': 115,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    bidirectional: Optional[bool] = Field(default=None, description="""in addition to preconditions entailing postconditions, the postconditions entail the preconditions""", json_schema_extra = { "linkml_meta": {'aliases': ['iff', 'if and only if'],
         'domain_of': ['class_rule'],
         'in_subset': ['SpecificationSubset']} })
    open_world: Optional[bool] = Field(default=None, description="""if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these""", json_schema_extra = { "linkml_meta": {'domain_of': ['class_rule'], 'in_subset': ['SpecificationSubset']} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    deactivated: Optional[bool] = Field(default=None, description="""a deactivated rule is not executed by the rules engine""", json_schema_extra = { "linkml_meta": {'domain_of': ['class_rule'], 'slot_uri': 'sh:deactivated'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ArrayExpression(CommonMetadata, Annotatable, Extensible):
    """
    defines the dimensions of an array
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'status': 'testing'})

    exact_number_dimensions: Optional[int] = Field(default=None, description="""exact number of dimensions in the array""", json_schema_extra = { "linkml_meta": {'comments': ['if exact_number_dimensions is set, then '
                      'minimum_number_dimensions and maximum_number_dimensions must be '
                      'unset or have the same value'],
         'domain': 'array_expression',
         'domain_of': ['array_expression'],
         'status': 'testing'} })
    minimum_number_dimensions: Optional[int] = Field(default=None, description="""minimum number of dimensions in the array""", json_schema_extra = { "linkml_meta": {'comments': ['minimum_cardinality cannot be greater than maximum_cardinality'],
         'domain': 'array_expression',
         'domain_of': ['array_expression'],
         'status': 'testing'} })
    maximum_number_dimensions: Optional[Union[bool, int]] = Field(default=None, description="""maximum number of dimensions in the array, or False if explicitly no maximum. If this is unset, and an explicit list of dimensions are passed using dimensions, then this is interpreted as a closed list and the maximum_number_dimensions is the length of the dimensions list, unless this value is set to False""", json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'integer'}, {'range': 'boolean'}],
         'comments': ['maximum_number_dimensions cannot be less than '
                      'minimum_number_dimensions'],
         'domain': 'array_expression',
         'domain_of': ['array_expression'],
         'status': 'testing'} })
    dimensions: Optional[list[DimensionExpression]] = Field(default=None, description="""definitions of each axis in the array""", json_schema_extra = { "linkml_meta": {'aliases': ['axes'],
         'domain': 'array_expression',
         'domain_of': ['array_expression'],
         'list_elements_ordered': True,
         'status': 'testing'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('dimensions', mode='before')
    def coerce_list_dimensions(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class DimensionExpression(CommonMetadata, Annotatable, Extensible):
    """
    defines one of the dimensions of an array
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'status': 'testing'})

    alias: Optional[str] = Field(default=None, description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of alias is used within this metamodel, '
                      'slot_definitions is aliases as slots',
                      'not to be confused with aliases, which indicates a set of terms '
                      'to be used for search purposes.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition', 'class_definition', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'rank': 6,
         'slot_uri': 'skos:prefLabel'} })
    maximum_cardinality: Optional[int] = Field(default=None, description="""the maximum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['maximum_cardinality cannot be less than minimum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    minimum_cardinality: Optional[int] = Field(default=None, description="""the minimum number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['minimum_cardinality cannot be greater than maximum_cardinality'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    exact_cardinality: Optional[int] = Field(default=None, description="""the exact number of entries for a multivalued slot""", json_schema_extra = { "linkml_meta": {'comments': ['if exact_cardinality is set, then minimum_cardinalty and '
                      'maximum_cardinality must be unset or have the same value'],
         'domain_of': ['slot_expression', 'dimension_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True,
         'is_a': 'list_value_specification_constant'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class PatternExpression(CommonMetadata, Annotatable, Extensible):
    """
    a regular expression pattern used to evaluate conformance of a string
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['extensible', 'annotatable', 'common_metadata']})

    syntax: Optional[str] = Field(default=None, description="""the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.""", json_schema_extra = { "linkml_meta": {'domain': 'pattern_expression',
         'domain_of': ['pattern_expression'],
         'in_subset': ['SpecificationSubset'],
         'inherited': True} })
    interpolated: Optional[bool] = Field(default=None, description="""if true then the pattern is first string interpolated""", json_schema_extra = { "linkml_meta": {'domain': 'pattern_expression',
         'domain_of': ['pattern_expression'],
         'in_subset': ['SpecificationSubset']} })
    partial_match: Optional[bool] = Field(default=None, description="""if not true then the pattern must match the whole string, as if enclosed in ^...$""", json_schema_extra = { "linkml_meta": {'domain': 'pattern_expression',
         'domain_of': ['pattern_expression'],
         'in_subset': ['SpecificationSubset']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ImportExpression(CommonMetadata, Annotatable, Extensible):
    """
    an expression describing an import
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'status': 'testing'})

    import_from: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain': 'import_expression',
         'domain_of': ['import_expression'],
         'status': 'testing'} })
    import_as: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'import_expression',
         'domain_of': ['import_expression'],
         'status': 'testing'} })
    import_map: Optional[dict[str, Union[str, Setting]]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain': 'import_expression',
         'domain_of': ['import_expression'],
         'status': 'testing'} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('import_map', mode='before')
    def coerce_keyed_import_map(cls, v):
        return _coerce_keyed_collection(v, "setting_key", value_name="setting_value")

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class Setting(ConfiguredBaseModel):
    """
    assignment of a key to a value
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset']})

    setting_key: str = Field(default=..., description="""the variable name for a setting""", json_schema_extra = { "linkml_meta": {'domain': 'setting',
         'domain_of': ['setting'],
         'in_subset': ['SpecificationSubset']} })
    setting_value: str = Field(default=..., description="""The value assigned for a setting""", json_schema_extra = { "linkml_meta": {'domain': 'setting',
         'domain_of': ['setting'],
         'in_subset': ['SpecificationSubset']} })


class Prefix(ConfiguredBaseModel):
    """
    prefix URI tuple
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 12})

    prefix_prefix: str = Field(default=..., description="""The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.""", json_schema_extra = { "linkml_meta": {'domain': 'prefix',
         'domain_of': ['prefix'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 1,
         'slot_uri': 'sh:prefix'} })
    prefix_reference: str = Field(default=..., description="""The namespace to which a prefix expands to.""", json_schema_extra = { "linkml_meta": {'domain': 'prefix',
         'domain_of': ['prefix'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 2,
         'slot_uri': 'sh:namespace'} })


class LocalName(ConfiguredBaseModel):
    """
    an attributed label
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta'})

    local_name_source: str = Field(default=..., description="""the ncname of the source of the name""", json_schema_extra = { "linkml_meta": {'domain': 'local_name', 'domain_of': ['local_name']} })
    local_name_value: str = Field(default=..., description="""a name assigned to an element in a given ontology""", json_schema_extra = { "linkml_meta": {'domain': 'local_name',
         'domain_of': ['local_name'],
         'slot_uri': 'skos:altLabel'} })


class Example(ConfiguredBaseModel):
    """
    usage example and description
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta', 'in_subset': ['BasicSubset']})

    value: Optional[str] = Field(default=None, description="""example value""", json_schema_extra = { "linkml_meta": {'domain': 'example',
         'domain_of': ['example'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:example'} })
    description: Optional[str] = Field(default=None, description="""description of what the value is doing""", json_schema_extra = { "linkml_meta": {'domain': 'example', 'domain_of': ['example'], 'in_subset': ['BasicSubset']} })
    object: Optional[Any] = Field(default=None, description="""direct object representation of the example""", json_schema_extra = { "linkml_meta": {'domain': 'example', 'domain_of': ['example'], 'in_subset': ['BasicSubset']} })


class AltDescription(ConfiguredBaseModel):
    """
    an attributed description
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['structured description'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['BasicSubset']})

    source: str = Field(default=..., description="""the source of an attributed description""", json_schema_extra = { "linkml_meta": {'domain': 'alt_description',
         'domain_of': ['alt_description'],
         'in_subset': ['BasicSubset']} })
    description: str = Field(default=..., description="""text of an attributed description""", json_schema_extra = { "linkml_meta": {'domain': 'alt_description',
         'domain_of': ['alt_description'],
         'in_subset': ['BasicSubset']} })


class PermissibleValue(CommonMetadata, Annotatable, Extensible):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['PV'],
         'close_mappings': ['skos:Concept'],
         'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'rank': 16,
         'slot_usage': {'is_a': {'name': 'is_a', 'range': 'permissible_value'},
                        'mixins': {'name': 'mixins', 'range': 'permissible_value'}}})

    text: str = Field(default=..., description="""The actual permissible value itself""", json_schema_extra = { "linkml_meta": {'aliases': ['value'],
         'close_mappings': ['skos:notation'],
         'comments': ['there are no constraints on the text of the permissible value, '
                      'but for many applications you may want to consider following '
                      'idiomatic forms and using computer-friendly forms'],
         'domain': 'permissible_value',
         'domain_of': ['permissible_value'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 21} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    meaning: Optional[str] = Field(default=None, description="""the value meaning of a permissible value""", json_schema_extra = { "linkml_meta": {'aliases': ['PV meaning'],
         'domain': 'permissible_value',
         'domain_of': ['permissible_value'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'notes': ['we may want to change the range of this (and other) elements in '
                   'the model to an entitydescription type construct'],
         'rank': 23,
         'see_also': ['https://en.wikipedia.org/wiki/ISO/IEC_11179']} })
    unit: Optional[UnitOfMeasure] = Field(default=None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_expression', 'slot_expression', 'permissible_value'],
         'slot_uri': 'qudt:unit'} })
    instantiates: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element instantiates.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    implements: Optional[list[str]] = Field(default=None, description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""", json_schema_extra = { "linkml_meta": {'domain': 'element', 'domain_of': ['element', 'permissible_value']} })
    is_a: Optional[str] = Field(default=None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True,
         'domain_of': ['definition', 'anonymous_class_expression', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 11} })
    mixins: Optional[list[str]] = Field(default=None, description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""", json_schema_extra = { "linkml_meta": {'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition', 'permissible_value'],
         'in_subset': ['SpecificationSubset',
                       'BasicSubset',
                       'ObjectOrientedProfile',
                       'OwlProfile'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('instantiates', mode='before')
    def coerce_list_instantiates(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('implements', mode='before')
    def coerce_list_implements(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('mixins', mode='before')
    def coerce_list_mixins(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class UniqueKey(CommonMetadata, Annotatable, Extensible):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'RelationalModelProfile'],
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'rank': 20})

    unique_key_name: str = Field(default=..., description="""name of the unique key""", json_schema_extra = { "linkml_meta": {'domain': 'unique_key',
         'domain_of': ['unique_key'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'RelationalModelProfile']} })
    unique_key_slots: list[str] = Field(default=..., description="""list of slot names that form a key. The tuple formed from the values of all these slots should be unique.""", json_schema_extra = { "linkml_meta": {'domain': 'unique_key',
         'domain_of': ['unique_key'],
         'in_subset': ['SpecificationSubset', 'BasicSubset', 'RelationalModelProfile']} })
    consider_nulls_inequal: Optional[bool] = Field(default=None, description="""By default, None values are considered equal for the purposes of comparisons in determining uniqueness. Set this to true to treat missing values as per ANSI-SQL NULLs, i.e NULL=NULL is always False.""", json_schema_extra = { "linkml_meta": {'domain': 'unique_key', 'domain_of': ['unique_key']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('unique_key_slots', mode='before')
    def coerce_list_unique_key_slots(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class TypeMapping(CommonMetadata, Annotatable, Extensible):
    """
    Represents how a slot or type can be serialized to a format.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'in_subset': ['SpecificationSubset'],
         'mixins': ['extensible', 'annotatable', 'common_metadata'],
         'rank': 21})

    framework: str = Field(default=..., description="""The name of a format that can be used to serialize LinkML data. The string value should be a code from the LinkML frameworks vocabulary, but this is not strictly enforced""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_mapping']} })
    type: Optional[str] = Field(default=None, description="""type to coerce to""", json_schema_extra = { "linkml_meta": {'domain_of': ['type_mapping']} })
    string_serialization: Optional[str] = Field(default=None, description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERATE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""", json_schema_extra = { "linkml_meta": {'domain': 'definition',
         'domain_of': ['definition', 'type_mapping'],
         'in_subset': ['SpecificationSubset'],
         'inherited': False,
         'see_also': ['https://github.com/linkml/issues/128']} })
    extensions: Optional[dict[str, Extension]] = Field(default=None, description="""a tag/text tuple attached to an arbitrary element""", json_schema_extra = { "linkml_meta": {'domain': 'extensible', 'domain_of': ['extension', 'extensible']} })
    annotations: Optional[dict[str, Annotation]] = Field(default=None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""", json_schema_extra = { "linkml_meta": {'domain': 'annotatable',
         'domain_of': ['annotatable', 'annotation'],
         'is_a': 'extensions'} })
    description: Optional[str] = Field(default=None, description="""a textual description of the element's purpose and use""", json_schema_extra = { "linkml_meta": {'aliases': ['definition'],
         'domain': 'element',
         'domain_of': ['common_metadata', 'permissible_value'],
         'exact_mappings': ['dcterms:description', 'schema:description'],
         'in_subset': ['BasicSubset'],
         'rank': 5,
         'recommended': True,
         'slot_uri': 'skos:definition'} })
    alt_descriptions: Optional[dict[str, Union[str, AltDescription]]] = Field(default=None, description="""A sourced alternative description for an element""", json_schema_extra = { "linkml_meta": {'aliases': ['alternate definitions'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    title: Optional[str] = Field(default=None, description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""", json_schema_extra = { "linkml_meta": {'aliases': ['long name'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'rank': 3,
         'slot_uri': 'dcterms:title'} })
    deprecated: Optional[str] = Field(default=None, description="""Description of why and when this element will no longer be used""", json_schema_extra = { "linkml_meta": {'close_mappings': ['owl:deprecated'],
         'comments': ['note that linkml does not use a boolean to indicate deprecation '
                      'status - the presence of a string value in this field is '
                      'sufficient to indicate deprecation.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    todos: Optional[list[str]] = Field(default=None, description="""Outstanding issues that needs resolution""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset']} })
    notes: Optional[list[str]] = Field(default=None, description="""editorial notes about an element intended primarily for internal consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:editorialNote'} })
    comments: Optional[list[str]] = Field(default=None, description="""notes and comments about an element intended primarily for external consumption""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['rdfs:comment'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:note'} })
    examples: Optional[list[Example]] = Field(default=None, description="""example usages of an element""", json_schema_extra = { "linkml_meta": {'close_mappings': ['vann:example'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'example'} })
    in_subset: Optional[list[str]] = Field(default=None, description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""", json_schema_extra = { "linkml_meta": {'comments': ['an example of use in the translator_minimal subset in the '
                      'biolink model, holding the minimal set of predicates used in a '
                      'translator knowledge graph'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'OIO:inSubset'} })
    from_schema: Optional[str] = Field(default=None, description="""id of the schema that defined the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['SpecificationSubset'],
         'notes': ['A stronger model would be range schema_definition, but this '
                   "doesn't address the import model"],
         'readonly': 'supplied by the schema loader or schema view',
         'slot_uri': 'skos:inScheme'} })
    imported_from: Optional[str] = Field(default=None, description="""the imports entry that this element was derived from.  Empty means primary source""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'readonly': 'supplied by the schema loader or schema view'} })
    source: Optional[str] = Field(default=None, description="""A related resource from which the element is derived.""", json_schema_extra = { "linkml_meta": {'aliases': ['origin', 'derived from'],
         'close_mappings': ['prov:wasDerivedFrom', 'schema:isBasedOn'],
         'comments': ['The described resource may be derived from the related resource '
                      'in whole or in part'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:source'} })
    in_language: Optional[str] = Field(default=None, description="""the primary language used in the sources""", json_schema_extra = { "linkml_meta": {'comments': ['Recommended to use a string from IETF BCP 47'],
         'conforms_to': 'https://www.rfc-editor.org/rfc/bcp/bcp47.txt',
         'domain_of': ['common_metadata'],
         'slot_uri': 'schema:inLanguage'} })
    see_also: Optional[list[str]] = Field(default=None, description="""A list of related entities or URLs that may be of relevance""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'rdfs:seeAlso'} })
    deprecated_element_has_exact_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be automatically replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['IAO:0100001']} })
    deprecated_element_has_possible_replacement: Optional[str] = Field(default=None, description="""When an element is deprecated, it can be potentially replaced by this uri or curie""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'], 'mappings': ['OIO:consider']} })
    aliases: Optional[list[str]] = Field(default=None, description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""", json_schema_extra = { "linkml_meta": {'aliases': ['synonyms',
                     'alternate names',
                     'alternative labels',
                     'designations'],
         'comments': ['not be confused with the metaslot alias.'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'exact_mappings': ['schema:alternateName'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'skos:altLabel'} })
    structured_aliases: Optional[list[StructuredAlias]] = Field(default=None, description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'see_also': ['linkml:aliases'],
         'slot_uri': 'skosxl:altLabel'} })
    mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""", json_schema_extra = { "linkml_meta": {'aliases': ['xrefs', 'identifiers', 'alternate identifiers', 'alternate ids'],
         'domain_of': ['common_metadata'],
         'slot_uri': 'skos:mappingRelation'} })
    exact_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have identical meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['UnitOfMeasure', 'common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:exactMatch'} })
    close_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have close meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:closeMatch'} })
    related_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have related meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:relatedMatch'} })
    narrow_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have narrower meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:narrowMatch'} })
    broad_mappings: Optional[list[str]] = Field(default=None, description="""A list of terms from different schemas or terminology systems that have broader meaning.""", json_schema_extra = { "linkml_meta": {'domain_of': ['common_metadata'],
         'inherited': False,
         'is_a': 'mappings',
         'slot_uri': 'skos:broadMatch'} })
    created_by: Optional[str] = Field(default=None, description="""agent that created the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdBy'} })
    contributors: Optional[list[str]] = Field(default=None, description="""agent that contributed to the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'dcterms:contributor'} })
    created_on: Optional[datetime ] = Field(default=None, description="""time at which the element was created""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:createdOn'} })
    last_updated_on: Optional[datetime ] = Field(default=None, description="""time at which the element was last updated""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'pav:lastUpdatedOn'} })
    modified_by: Optional[str] = Field(default=None, description="""agent that modified the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'slot_uri': 'oslc:modifiedBy'} })
    status: Optional[str] = Field(default=None, description="""status of the element""", json_schema_extra = { "linkml_meta": {'aliases': ['workflow status'],
         'domain': 'element',
         'domain_of': ['common_metadata'],
         'examples': [{'value': 'bibo:draft'}],
         'in_subset': ['BasicSubset'],
         'see_also': ['https://www.hl7.org/fhir/valueset-publication-status.html',
                      'https://www.hl7.org/fhir/versions.html#std-process'],
         'slot_uri': 'bibo:status'} })
    rank: Optional[int] = Field(default=None, description="""the relative order in which the element occurs, lower values are given precedence""", json_schema_extra = { "linkml_meta": {'aliases': ['order', 'precedence', 'display order'],
         'comments': ['the rank of an element does not affect the semantics'],
         'domain_of': ['common_metadata', 'class_rule'],
         'exact_mappings': ['qudt:order', 'qb:order'],
         'in_subset': ['SpecificationSubset', 'BasicSubset'],
         'rank': 51,
         'slot_uri': 'sh:order'} })
    categories: Optional[list[str]] = Field(default=None, description="""Controlled terms used to categorize an element.""", json_schema_extra = { "linkml_meta": {'comments': ['if you wish to use uncontrolled terms or terms that lack '
                      'identifiers then use the keywords element'],
         'domain_of': ['common_metadata', 'structured_alias'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'category',
         'slot_uri': 'dcterms:subject'} })
    keywords: Optional[list[str]] = Field(default=None, description="""Keywords or tags used to describe the element""", json_schema_extra = { "linkml_meta": {'domain': 'element',
         'domain_of': ['common_metadata'],
         'in_subset': ['BasicSubset'],
         'singular_name': 'keyword',
         'slot_uri': 'schema:keywords'} })

    @field_validator('extensions', mode='before')
    def coerce_keyed_extensions(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('annotations', mode='before')
    def coerce_keyed_annotations(cls, v):
        return _coerce_keyed_collection(v, "tag", value_name="value")

    @field_validator('alt_descriptions', mode='before')
    def coerce_keyed_alt_descriptions(cls, v):
        return _coerce_keyed_collection(v, "source", value_name="description")

    @field_validator('todos', mode='before')
    def coerce_list_todos(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('notes', mode='before')
    def coerce_list_notes(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('comments', mode='before')
    def coerce_list_comments(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('examples', mode='before')
    def coerce_list_examples(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('in_subset', mode='before')
    def coerce_list_in_subset(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('see_also', mode='before')
    def coerce_list_see_also(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('aliases', mode='before')
    def coerce_list_aliases(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('structured_aliases', mode='before')
    def coerce_list_structured_aliases(cls, v):
        return _coerce_inlined_list(v, "literal_form")


    @field_validator('mappings', mode='before')
    def coerce_list_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('exact_mappings', mode='before')
    def coerce_list_exact_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('close_mappings', mode='before')
    def coerce_list_close_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('related_mappings', mode='before')
    def coerce_list_related_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('narrow_mappings', mode='before')
    def coerce_list_narrow_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('broad_mappings', mode='before')
    def coerce_list_broad_mappings(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('contributors', mode='before')
    def coerce_list_contributors(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('categories', mode='before')
    def coerce_list_categories(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]


    @field_validator('keywords', mode='before')
    def coerce_list_keywords(cls, v):
        if v is None or isinstance(v, list):
            return v
        return [v]



class ExtraSlotsExpression(Expression):
    """
    An expression that defines how to handle additional data in an instance of class
    beyond the slots/attributes defined for that class.
    See `extra_slots` for usage examples.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/meta',
         'mixins': ['expression'],
         'slot_usage': {'range_expression': {'name': 'range_expression',
                                             'range': 'anonymous_slot_expression'}}})

    allowed: Optional[bool] = Field(default=None, description="""Whether or not something is allowed. Usage defined by context.""", json_schema_extra = { "linkml_meta": {'domain_of': ['extra_slots_expression'],
         'in_subset': ['SpecificationSubset', 'BasicSubset']} })
    range_expression: Optional[AnonymousSlotExpression] = Field(default=None, description="""A range that is described as a boolean expression combining existing ranges""", json_schema_extra = { "linkml_meta": {'comments': ['one use for this is being able to describe a range using any_of '
                      'expressions, for example to combine two enums'],
         'domain': 'slot_expression',
         'domain_of': ['path_expression', 'slot_expression', 'extra_slots_expression'],
         'in_subset': ['SpecificationSubset'],
         'status': 'testing'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Extension.model_rebuild()
Extensible.model_rebuild()
Annotatable.model_rebuild()
Annotation.model_rebuild()
UnitOfMeasure.model_rebuild()
CommonMetadata.model_rebuild()
Element.model_rebuild()
SchemaDefinition.model_rebuild()
SubsetDefinition.model_rebuild()
Definition.model_rebuild()
EnumBinding.model_rebuild()
MatchQuery.model_rebuild()
ReachabilityQuery.model_rebuild()
Expression.model_rebuild()
TypeExpression.model_rebuild()
AnonymousTypeExpression.model_rebuild()
TypeDefinition.model_rebuild()
EnumExpression.model_rebuild()
AnonymousEnumExpression.model_rebuild()
EnumDefinition.model_rebuild()
StructuredAlias.model_rebuild()
AnonymousExpression.model_rebuild()
PathExpression.model_rebuild()
SlotExpression.model_rebuild()
AnonymousSlotExpression.model_rebuild()
SlotDefinition.model_rebuild()
ClassExpression.model_rebuild()
AnonymousClassExpression.model_rebuild()
ClassDefinition.model_rebuild()
ClassLevelRule.model_rebuild()
ClassRule.model_rebuild()
ArrayExpression.model_rebuild()
DimensionExpression.model_rebuild()
PatternExpression.model_rebuild()
ImportExpression.model_rebuild()
Setting.model_rebuild()
Prefix.model_rebuild()
LocalName.model_rebuild()
Example.model_rebuild()
AltDescription.model_rebuild()
PermissibleValue.model_rebuild()
UniqueKey.model_rebuild()
TypeMapping.model_rebuild()
ExtraSlotsExpression.model_rebuild()
