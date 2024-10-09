import os
from io import StringIO
from typing import Union, TextIO, Optional

import yaml
from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot, DupCheckYamlLoader
from pydantic import BaseModel


class YAMLLoader(Loader):
    """
    A Loader that is capable of instantiating LinkML data objects from a YAML file
    """

    def load_as_dict(self, 
                     source: Union[str, dict, TextIO], 
                     *, 
                     base_dir: Optional[str] = None,
                     metadata: Optional[FileInfo] = None) -> Union[dict, list[dict]]:
        if metadata is None:
            metadata = FileInfo()
        if base_dir and not metadata.base_path:
            metadata.base_path = base_dir
        data = self._read_source(source, base_dir=base_dir, metadata=metadata, accept_header="text/yaml, application/yaml;q=0.9")
        if isinstance(data, str):
            data = StringIO(data)
            if metadata and metadata.source_file:
                data.name = os.path.relpath(metadata.source_file, metadata.base_path)
            return yaml.load(data, DupCheckYamlLoader)
        else:
            return data

    def load_any(self,
                 source: Union[str, dict, TextIO],
                 target_class: Union[type[YAMLRoot], type[BaseModel]],
                 *, base_dir: Optional[str] = None,
                 metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, list[YAMLRoot]]:
        data_as_dict = self.load_as_dict(source, base_dir=base_dir, metadata=metadata)
        return self._construct_target_class(data_as_dict, target_class)

    def loads_any(self, source: str, target_class: type[Union[BaseModel, YAMLRoot]], *, metadata: Optional[FileInfo] = None, **_) -> Union[BaseModel, YAMLRoot, list[BaseModel], list[YAMLRoot]]:
        """
        Load source as a string
        @param source: source
        @param target_class: destination class
        @param metadata: metadata about the source
        @param _: extensions
        @return: instance of taarget_class
        """
        return self.load_any(source, target_class, metadata=metadata)
