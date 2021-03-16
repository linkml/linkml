from io import StringIO
from typing import Union, TextIO, Optional, Dict, Type

import yaml
from hbreader import FileInfo

from linkml.utils.yamlutils import YAMLRoot, DupCheckYamlLoader

from linkml.loaders.loader_root import load_source


def load(source: Union[str, dict, TextIO], base_dir: Optional[str], target_class: Type[YAMLRoot],
         metadata: Optional[FileInfo] = None) -> YAMLRoot:
    def loader(data: Union[str, dict], _: FileInfo) -> Optional[Dict]:
        return yaml.load(StringIO(data), DupCheckYamlLoader) if isinstance(data, str) else data

    if not metadata:
        metadata = FileInfo()
    if base_dir and not metadata.base_path:
        metadata.base_path = base_dir
    return load_source(source, loader, target_class, accept_header="text/yaml, application/yaml;q=0.9",
                       metadata=metadata)


def loads(source: str, target_class: Type[YAMLRoot], metadata: Optional[FileInfo] = None) -> YAMLRoot:
    return load(source, None, target_class, metadata)
