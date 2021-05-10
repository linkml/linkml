from dataclasses import dataclass
from typing import Dict, Any, Optional, ClassVar, List, Union

from rdflib import URIRef

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import URIorCURIE, empty_list, URI
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from utils.enumerations import EnumDefinitionImpl

LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')

RenderingURI = URI

class PermissibleValueText(extended_str):
    pass

@dataclass
class PermissibleValue(YAMLRoot):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML.PermissibleValue
    class_class_curie: ClassVar[str] = "linkml:PermissibleValue"
    class_name: ClassVar[str] = "permissible_value"
    class_model_uri: ClassVar[URIRef] = LINKML.PermissibleValue

    text: Union[str, PermissibleValueText] = None
    description: Optional[str] = None
    meaning: Optional[Union[str, URIorCURIE]] = None
    deprecated: Optional[str] = None
    todos: Optional[Union[str, List[str]]] = empty_list()
    notes: Optional[Union[str, List[str]]] = empty_list()
    comments: Optional[Union[str, List[str]]] = empty_list()
    from_schema: Optional[Union[str, URI]] = None
    imported_from: Optional[str] = None
    see_also: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    deprecated_element_has_exact_replacement: Optional[Union[str, URIorCURIE]] = None
    deprecated_element_has_possible_replacement: Optional[Union[str, URIorCURIE]] = None
    is_a: Optional[Union[str, PermissibleValueText]] = None
    mixins: Optional[Union[Union[str, PermissibleValueText], List[Union[str, PermissibleValueText]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.text is None:
            raise ValueError("text must be supplied")
        if not isinstance(self.text, PermissibleValueText):
            self.text = PermissibleValueText(self.text)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.meaning is not None and not isinstance(self.meaning, URIorCURIE):
            self.meaning = URIorCURIE(self.meaning)

        if self.deprecated is not None and not isinstance(self.deprecated, str):
            self.deprecated = str(self.deprecated)

        if self.todos is None:
            self.todos = []
        if not isinstance(self.todos, list):
            self.todos = [self.todos]
        self.todos = [v if isinstance(v, str) else str(v) for v in self.todos]

        if self.notes is None:
            self.notes = []
        if not isinstance(self.notes, list):
            self.notes = [self.notes]
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if self.comments is None:
            self.comments = []
        if not isinstance(self.comments, list):
            self.comments = [self.comments]
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if self.from_schema is not None and not isinstance(self.from_schema, URI):
            self.from_schema = URI(self.from_schema)

        if self.imported_from is not None and not isinstance(self.imported_from, str):
            self.imported_from = str(self.imported_from)

        if self.see_also is None:
            self.see_also = []
        if not isinstance(self.see_also, list):
            self.see_also = [self.see_also]
        self.see_also = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.see_also]

        if self.deprecated_element_has_exact_replacement is not None and not isinstance(self.deprecated_element_has_exact_replacement, URIorCURIE):
            self.deprecated_element_has_exact_replacement = URIorCURIE(self.deprecated_element_has_exact_replacement)

        if self.deprecated_element_has_possible_replacement is not None and not isinstance(self.deprecated_element_has_possible_replacement, URIorCURIE):
            self.deprecated_element_has_possible_replacement = URIorCURIE(self.deprecated_element_has_possible_replacement)

        if self.is_a is not None and not isinstance(self.is_a, PermissibleValueText):
            self.is_a = PermissibleValueText(self.is_a)

        if self.mixins is None:
            self.mixins = []
        if not isinstance(self.mixins, list):
            self.mixins = [self.mixins]
        self.mixins = [v if isinstance(v, PermissibleValueText) else PermissibleValueText(v) for v in self.mixins]

        super().__post_init__(**kwargs)


# Enumerations
class PvFormulaOptions(EnumDefinitionImpl):
    """
    The formula used to generate the set of permissible values from the code_set values
    """
    CODE = PermissibleValue(text="CODE",
                               description="The permissible values are the set of possible codes in the code set")
    CURIE = PermissibleValue(text="CURIE",
                                 description="The permissible values are the set of CURIES in the code set")
    URI = PermissibleValue(text="URI",
                             description="The permissible values are the set of code URIs in the code set")
    FHIR_CODING = PermissibleValue(text="FHIR_CODING",
                                             description="The permissible values are the set of FHIR coding elements derived from the code set")

    _defn = EnumDefinition(
        name="PvFormulaOptions",
        description="The formula used to generate the set of permissible values from the code_set values",
    )

class PermissibleValueImpl(PermissibleValue):
    """
    Permissible Value implementation
    """
    def __init__(self, *args, defn: EnumDefinitionImpl, **kwargs) -> None:
        """ Record the referencing definition to allow the entry to be fleshed out from a terminology service """
        super().__init__(*args, **kwargs)
        self._defn = defn

    def __post_init__(self, **kwargs: Dict[str, Any]) -> None:
        """ Make sure that we are correctly situated in the containing definition """
        if self.text in self._defn:
            if self._defn.permissible_values[self.text] != self:
                raise TypeError(f"Permissible value for code: {self.text} is already assigned")
        if self not in self._defn.permissible_values:
            if not self._defn.code_set:
                # Fixed set of values -- no terminology reference
                raise TypeError("{self}: Permissible value not in definition set")
