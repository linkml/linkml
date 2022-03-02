from io import StringIO
from typing import Union, TextIO, Optional, Dict, Type, List

import yaml
from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot, DupCheckYamlLoader


class YAMLLoader(Loader):
    """
    A Loader that is capable of instantiating LinkML data objects from a YAML file
    """

    def load_any(self, source: Union[str, dict, TextIO], target_class: Type[YAMLRoot], *, base_dir: Optional[str] = None,
                 metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, List[YAMLRoot]]:
        def loader(data: Union[str, dict], _: FileInfo) -> Optional[Dict]:
            return yaml.load(StringIO(data), DupCheckYamlLoader) if isinstance(data, str) else data

        if not metadata:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir
        return self.load_source(source, loader, target_class, accept_header="text/yaml, application/yaml;q=0.9",
                                metadata=metadata)

    def loads_any(self, source: str, target_class: Type[YAMLRoot], *, metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, List[YAMLRoot]]:
        """
        Load source as a string
        @param source: source
        @param target_class: destination class
        @param metadata: metadata about the source
        @param _: extensions
        @return: instance of taarget_class
        """
        return self.load_any(source, target_class, metadata=metadata)