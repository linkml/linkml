from typing import TextIO, Union, Optional, Callable, Dict, Type

from hbreader import FileInfo, hbread

from linkml.utils.yamlutils import YAMLRoot


def load_source(source: Union[str, dict, TextIO],
                loader: Callable[[Union[str, Dict], FileInfo], Optional[Dict]],
                target_class: Type[YAMLRoot],
                accept_header: Optional[str] = "text/plain, application/yaml;q=0.9",
                metadata: Optional[FileInfo] = None) -> Optional[YAMLRoot]:
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
    return target_class(**data_as_dict) if data_as_dict is not None else None
