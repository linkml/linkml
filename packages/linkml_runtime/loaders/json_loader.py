import json
import logging
from typing import Union, TextIO, Optional, Dict, Type, List

from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot


class JSONLoader(Loader):

    def load_any(self, source: Union[str, dict, TextIO], target_class: Type[YAMLRoot], *, base_dir: Optional[str] = None,
             metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, List[YAMLRoot]]:
        def loader(data: Union[str, dict], _: FileInfo) -> Optional[Dict]:
            data_as_dict = json.loads(data) if isinstance(data, str) else data
            if isinstance(data_as_dict, list):
                return self.json_clean(data_as_dict)
            typ = data_as_dict.pop('@type', None)
            if typ and typ != target_class.__name__:
                logging.warning(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")
            return self.json_clean(data_as_dict)

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir
        return self.load_source(source, loader, target_class,
                                accept_header="application/ld+json, application/json, text/json", metadata=metadata)
