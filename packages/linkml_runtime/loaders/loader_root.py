from abc import ABC, abstractmethod
from typing import TextIO, Union, Optional, Callable, Dict, Type, Any, List

from hbreader import FileInfo, hbread
from jsonasobj2 import as_dict, JsonObj

from linkml_runtime.utils.yamlutils import YAMLRoot


class Loader(ABC):

    @staticmethod
    def json_clean(inp: Any) -> Any:
        """
        Remove empty values and JSON-LD relics from an input file

        :param inp: JSON-LD representation
        :return: JSON representation
        """
        def _is_empty(o) -> bool:
            return o is None or o == [] or o == {}

        if isinstance(inp, list):
            for e in [inp_e for inp_e in inp if _is_empty(inp_e)]:
                del(inp[e])
            for e in inp:
                Loader.json_clean(e)
        elif isinstance(inp, dict):
            for k, v in list(inp.items()):
                if k.startswith('@') or _is_empty(v):
                    del(inp[k])
                else:
                    Loader.json_clean(v)
        return inp

    def load_source(self,
                    source: Union[str, dict, TextIO],
                    loader: Callable[[Union[str, Dict], FileInfo], Optional[Union[Dict, List]]],
                    target_class: Type[YAMLRoot],
                    accept_header: Optional[str] = "text/plain, application/yaml;q=0.9",
                    metadata: Optional[FileInfo] = None) -> Optional[Union[YAMLRoot, List[YAMLRoot]]]:
        """ Base loader - convert a file, url, string, open file handle or dictionary into an instance
        of target_class

        :param source: URL, file name, block of text, Existing Object or open file handle
        :param loader: Take a stringified image or a dictionary and return a loadable dictionary
        :param target_class: Destination class
        :param accept_header: Accept header to use if doing a request
        :param metadata: Metadata about the source.  Filled in as we go along

        :return: Instance of the target class if loader worked
        """

        # Makes coding easier down the line if we've got this, even if it is strictly internal
        if metadata is None:
            metadata = FileInfo()
        if not isinstance(source, dict):
            data = hbread(source, metadata, metadata.base_path, accept_header)
        else:
            data = source
        data_as_dict = loader(data, metadata)
        if data_as_dict:
            if isinstance(data_as_dict, list):
                return [target_class(**as_dict(x)) for x in data_as_dict]
            elif isinstance(data_as_dict, dict):
                return target_class(**data_as_dict)
            elif isinstance(data_as_dict, JsonObj):
                return [target_class(**as_dict(x)) for x in data_as_dict]
            else:
                raise ValueError(f'Unexpected type {data_as_dict}')
        else:
            return None

    def load(self, *args, **kwargs) -> YAMLRoot:
        """
        Load source as an instance of target_class

        :param source: source file/text/url to load
        :param target_class: destination class
        :param base_dir: scoping directory for source if it is a file or url
        :param metadata: metadata about the source
        :param _: extensions
        :return: instance of target_class
        """
        results = self.load_any(*args, **kwargs)
        if isinstance(results, YAMLRoot):
            return results
        else:
            raise ValueError(f'Result is not an instance of YAMLRoot: {type(results)}')

    @abstractmethod
    def load_any(self, source: Union[str, dict, TextIO], target_class: Type[YAMLRoot], *, base_dir: Optional[str] = None,
             metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, List[YAMLRoot]]:
        """
        Load source as an instance of target_class, or list of instances of target_class

        @param source: source file/text/url to load
        @param target_class: destination class
        @param base_dir: scoping directory for source if it is a file or url
        @param metadata: metadata about the source
        @param _: extensions
        @return: instance of target_class
        """
        raise NotImplementedError()

    def loads_any(self, source: str, target_class: Type[YAMLRoot], *, metadata: Optional[FileInfo] = None, **_) -> Union[YAMLRoot, List[YAMLRoot]]:
        """
        Load source as a string as an instance of target_class, or list of instances of target_class
        @param source: source
        @param target_class: destination class
        @param metadata: metadata about the source
        @param _: extensions
        @return: instance of taarget_class
        """
        return self.load_any(source, target_class, metadata=metadata)

    def loads(self, source: str, target_class: Type[YAMLRoot], *, metadata: Optional[FileInfo] = None, **_) -> YAMLRoot:
        """
        Load source as a string
        :param source: source
        :param target_class: destination class
        :param metadata: metadata about the source
        :param _: extensions
        :return: instance of taarget_class
        """
        return self.load(source, target_class, metadata=metadata)
