from dataclasses import dataclass
from typing import Dict, Any, Optional, ClassVar, List, Union

from rdflib import URIRef

from linkml_model.meta import PermissibleValue, EnumDefinition, PvFormulaOptions
from linkml.utils.curienamespace import CurieNamespace
from linkml.utils.metamodelcore import URIorCURIE, empty_list
from linkml.utils.uritypes_from_tccm import RenderingURI
from linkml.utils.yamlutils import YAMLRoot, extended_str


class PermissibleValueImpl(PermissibleValue):
    """
    Permissible Value implementation
    """
    def __init__(self, *args, defn: EnumDefinition, **kwargs) -> None:
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



#     code_set: Optional[Union[str, URIorCURIE]] = None
#     code_set_tag: Optional[str] = None
#     code_set_version: Optional[str] = None
#     pv_formula: Optional[Union[str, "PvFormulaOptions"]] = None

# This will be imported from the TCCM module when we get everything glued together
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
TCCM = CurieNamespace('tccm', 'https://hotecosystem.org/tccm/')


class EntityReferenceCode(extended_str):
    pass


@dataclass
class EntityReference(YAMLRoot):
    """
    The URI, namespace/name (if known) and a list of code systems that make assertions about the entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = TCCM.EntityReference
    class_class_curie: ClassVar[str] = "tccm:EntityReference"
    class_name: ClassVar[str] = "EntityReference"
    class_model_uri: ClassVar[URIRef] = TCCM.EntityReference

    code: Union[str, EntityReferenceCode]
    about: Optional[URIorCURIE] = None
    designation: Optional[str] = None
    description: Optional[str] = None
    href: Optional[Union[URIorCURIE, RenderingURI]] = None
    see_also: List[Union[URIorCURIE, RenderingURI]] = empty_list()



@dataclass
class TCCMCodeSetService:
    code_set_uri: URIorCURIE
    code_set_tag: Optional[str] = None
    code_set_version: Optional[str] = None
    text_formula: PvFormulaOptions = None

    def entity_reference_for(self, code: str) -> Optional[EntityReference]:
        """
        Return the entity reference that corresponds to code
        @param code:
        @return:
        """

