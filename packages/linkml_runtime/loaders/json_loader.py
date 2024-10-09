import json
import logging
from pathlib import Path
from typing import Union, TextIO, Optional

from hbreader import FileInfo

from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class JSONLoader(Loader):

    def load_as_dict(self, 
                     source: Union[str, dict, TextIO],
                     *, 
                     base_dir: Optional[str] = None,
                     metadata: Optional[FileInfo] = None) -> Union[dict, list[dict]]:
        data = self._read_source(source, base_dir=base_dir, metadata=metadata, accept_header="application/ld+json, application/json, text/json")
        data_as_dict = json.loads(data) if isinstance(data, str) else data
        return self.json_clean(data_as_dict)

    def load_any(self, 
                 source: Union[str, dict, TextIO, Path],
                 target_class: type[Union[BaseModel, YAMLRoot]],
                 *, 
                 base_dir: Optional[str] = None,
                 metadata: Optional[FileInfo] = None, 
                 **_) -> Union[BaseModel, YAMLRoot, list[BaseModel], list[YAMLRoot]]:
        """
        Load the JSON in source into the python target_class structure

        :param source: JSON data source. Can be a URL, a file name, a JSON string, a resolveable filepath or an existing graph
        :param target_class: LinkML class to load the JSON into
        :param base_dir: Base directory that can be used if file name or URL.  This is copied into metadata if present
        :param metadata: source information. Used by some loaders to record where information came from
        :return: data instances of target_class
        """

        # see https://github.com/linkml/linkml/issues/2458, this works around a limitation in hbreader
        if isinstance(source, Path):
            full_path = source.resolve()
            try:
                with full_path.open("r", encoding="utf-8") as file:
                    new_source = json.load(file)
                    source = new_source
            except FileNotFoundError as e:
                raise ValueError(f"File not found: {source}") from e
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {source}: {e}")
        data_as_dict = self.load_as_dict(source, base_dir=base_dir, metadata=metadata)

        if isinstance(data_as_dict, dict):
            typ = data_as_dict.pop('@type', None)
            if typ and typ != target_class.__name__:
                logger.warning(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")

        return self._construct_target_class(data_as_dict, target_class)
