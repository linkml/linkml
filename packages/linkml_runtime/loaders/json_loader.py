import json
import logging
from typing import Union, TextIO, Optional, Dict, Type, List

from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

class JSONLoader(Loader):

    def load_as_dict(self, 
                     source: Union[str, dict, TextIO], 
                     *, 
                     base_dir: Optional[str] = None,
                     metadata: Optional[FileInfo] = None) -> Union[dict, List[dict]]:
        data = self._read_source(source, base_dir=base_dir, metadata=metadata, accept_header="application/ld+json, application/json, text/json")
        data_as_dict = json.loads(data) if isinstance(data, str) else data
        return self.json_clean(data_as_dict)

    def load_any(self, 
                 source: Union[str, dict, TextIO], 
                 target_class: Type[Union[BaseModel, YAMLRoot]], 
                 *, 
                 base_dir: Optional[str] = None,
                 metadata: Optional[FileInfo] = None, 
                 **_) -> Union[BaseModel, YAMLRoot, List[BaseModel], List[YAMLRoot]]:
        data_as_dict = self.load_as_dict(source, base_dir=base_dir, metadata=metadata)

        if isinstance(data_as_dict, dict):
            typ = data_as_dict.pop('@type', None)
            if typ and typ != target_class.__name__:
                logging.warning(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")

        return self._construct_target_class(data_as_dict, target_class)
