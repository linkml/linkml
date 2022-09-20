"""
Packaging for working with LinkML distributions
"""
import logging
import pkgutil
from pathlib import PurePath
from typing import List, Type



def get_default_paths(file_type: str) -> List[PurePath]:
    """
    Return candidate relative paths for a file type

    :param file_type:
    :return: candidate paths
    """
    paths = []
    rel_dirs = []
    # TODO: introspect this information
    srcp = PurePath('src')
    if file_type == 'yaml':
        rel_dirs = [PurePath('model') /'schema',
                    PurePath('schema'),
                    PurePath('linkml'),
                    srcp / 'linkml',
                    srcp / 'model',
                    srcp / 'model' / 'schema',
                    srcp / 'schema',
                    ]
    elif file_type == 'schema.json':
        rel_dirs = [PurePath('jsonschema')]
    elif file_type == 'context.jsonld':
        rel_dirs = [PurePath('jsonld')]
    elif '.' in file_type:
        # e.g. 'owl.ttl' --> 'owl'
        rel_dirs = [PurePath(file_type.split('.')[0])]
    else:
        rel_dirs = []
    for rel_dir in rel_dirs:
        paths.append(rel_dir)
    # YAML files may be in the same directory as the python
    paths.append(PurePath('.'))
    logging.debug(f"Paths to search: {paths}")
    return paths

def get_packaged_file_as_str(package: str, file_type: str, rel_paths: List[PurePath]=[], encoding="utf-8") -> str:
    """
    Retrieve the value of a data file distributed alongside a python package

    :param package: Python package as string, e.g. linkml_runtime.linkml_model.meta
    :param file_type: e.g. 'yaml', 'schema.json', 'owl.ttl'
    :param rel_path: optional relative path from python package to
    :param encoding:
    :return:
    """
    parts = package.split('.')
    package_name = parts[-1]
    suffix = file_type
    data = None
    for path in get_default_paths(file_type) + rel_paths:
        try:
            full_path = path / f'{package_name}.{suffix}'
            data = pkgutil.get_data(package, str(full_path))
            if data:
                break
        except FileNotFoundError:
            logging.debug(f'candidate {path} not found')
    if not data:
        raise FileNotFoundError(f'package: {package} file: {file_type}')
    return data.decode(encoding)

def get_schema_string(package: str, **kwargs) -> str:
    return get_packaged_file_as_str(package, file_type='yaml', **kwargs)

def get_jsonschema_string(package: str, **kwargs) -> str:
    return get_packaged_file_as_str(package, file_type='schema.json', **kwargs)
