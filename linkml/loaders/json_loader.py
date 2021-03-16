import json
from typing import Union, TextIO, Optional, Dict, Type, Any

from hbreader import FileInfo

from linkml.loaders.loader_root import load_source
from linkml.utils.yamlutils import YAMLRoot


def json_clean(inp: Any) -> Any:
    """
    Remove empty values and JSON-LD relics from an input file
    @param inp: JSON-LD representation
    @return: JSON representation
    """
    def _is_empty(o) -> bool:
        return o is None or o == [] or o == {}

    if isinstance(inp, list):
        for e in [inpe for inpe in inp if _is_empty(inpe)]:
            del(inp[e])
        for e in inp:
            json_clean(e)
    elif isinstance(inp, dict):
        for k, v in list(inp.items()):
            if k.startswith('@') or _is_empty(v):
                del(inp[k])
            else:
                json_clean(v)
    return inp


def load(source: Union[str, dict, TextIO], base_dir: Optional[str], target_class: Type[YAMLRoot],
         metadata: Optional[FileInfo]) -> YAMLRoot:
    def loader(data: Union[str, dict], _: FileInfo) -> Optional[Dict]:
        data_as_dict = json.loads(data) if isinstance(data, str) else data
        typ = data_as_dict.pop('@type', None)
        # TODO: Remove this when https://github.com/linkml/issues/364 gets fixed
        if not typ:
            typ = data_as_dict.pop('@type', None)
        if typ and typ != target_class.__name__:
            # TODO: connect this up with the logging facility or warning?
            print(f"Warning: input type mismatch. Expected: {target_class.__name__}, Actual: {typ}")
        return json_clean(data_as_dict)

    if not metadata:
        metadata = FileInfo()
    if base_dir and not metadata.base_path:
        metadata.base_path = base_dir
    return load_source(source, loader, target_class, accept_header="application/ld+json, application/json, text/json",
                       metadata=metadata)


def loads(source: str, target_class: Type[YAMLRoot], metadata: Optional[FileInfo] = None) -> YAMLRoot:
    return load(source, None, target_class, metadata)
