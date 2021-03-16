import os
from enum import unique, Enum, auto
from json import loads
from typing import Optional, re, Dict, Any

from rdflib import URIRef, Graph, RDF, OWL, SKOS, Literal

from linkml.services.tccm_obo_filter import HPO
from linkml.utils.enumerations import EnumerationHandler
from tests.environment import env


# TODO: Figure ouw where and how to emit this in the python
class AutoName(Enum):
     def _generate_next_value_(name, start, count, last_values):
         return name

@unique
class pv(AutoName):
    CODE = auto()
    CURIE = auto()
    URI = auto()
    FHIR_CODING = auto()

HPO_str = str(HPO)


class TCCMEnumHandler(EnumerationHandler):

    def __init__(self, *args, **kwargs) -> None:
        self._g = Graph()
        self._g.load(os.path.join(env.cwd, 'data', 'hp_f.ttl'), format='turtle')
        super().__init__(*args, **kwargs)

    def __post_init__(self, **kwargs: Dict[str, Any]):
        # Here is where we validate a number of things:
        # 1) We are assuming, for the moment, that the code_set variable is "CS:HPO" -- we need to check this
        # 2) If there is a version or tag, we need to select the correct HPO version (future engineering)
        # 3) If there are permissible values, we need to validate all "meaning" links
        super().__post_init__(**kwargs)

    def __contains__(self, item):
        if self.permissible_values is not None:
            return not self.permissible_values or item in self.permissible_values
        elif self.pv_formula:
            if pv[self.pv_formula] == pv.CODE:
                return (None, SKOS.notation, Literal(item)) in self._g
            elif pv[self.pv_formula] == pv.CURIE:
                ns, code = item.split(':', 1)
                return ns == 'HPO' and (None, SKOS.notation, Literal(item)) in self._g
            elif pv[self.pv_formula] == pv.URI:
                return (URIRef(str(item)) if not isinstance(item, URIRef) else item, SKOS.notation, None) in self.g
            elif pv[self.pv_formula] == pv.FHIR_CODING:
                # Need to determine the rules to convert item to the appropriate JSON object
                if isinstance(item, str):
                    item = loads(item)
                if not item or not 'system' in item or not 'code' in item:
                    return False
                return item['system'] == HPO_str and (None, SKOS.notation, Literal(item.code)) in self._g

            raise ValueError("FILL ME IN -- shouldn't ever get here")


        # TODO: figure out how to generalize this
        # if version is None:
        #     version_url = self.g.value(self.ontologyuri, OWL.versionIRI)
        #     mver = re.match(r'http://purl.obolibrary.org/.*/releases/(2020-10-12)/', str(version_url))
        #     if mver:
        #         self.version = mver

    def __str__(self):
        return f"{self.code}: (lookup label)"
