import json
from typing import Union, TextIO, Optional, Dict, Type

from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot


class JSONLoader(Loader):

    def load(self, source: Union[str, dict, TextIO], target_class: Type[YAMLRoot], *, base_dir: Optional[str] = None,
             metadata: Optional[FileInfo] = None, **_) -> YAMLRoot:
        def loader(data: Union[str, dict], _: FileInfo) -> Optional[Dict]:
            data_as_dict = json.loads(data) if isinstance(data, str) else data
            typ = data_as_dict.pop('@type', None)
            if typ and typ != target_class.__name__:
                # TODO: connect this up with the logging facility or warning?
                print(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")
            return self.json_clean(data_as_dict)

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir
        return self.load_source(source, loader, target_class,
                                accept_header="application/ld+json, application/json, text/json", metadata=metadata)
