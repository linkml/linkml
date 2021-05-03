from typing import Optional, Union

from rdflib import Namespace, URIRef


class CurieNamespace(Namespace):
    def __new__(cls, prefix: str, value: Union[str, URIRef]):
        value = str(value)
        try:
            rt = str.__new__(cls, value)
        except UnicodeDecodeError:
            rt = str.__new__(cls, value, 'utf-8')
        rt.prefix = prefix
        return rt

    def curie(self, reference: Optional[str] = '') -> str:
        return self.prefix + ':' + reference
