
""" Metadata filters for test cases -- various tools to remove metadata from output """
import re
from json import loads

from jsonasobj2 import as_json

def ldcontext_metadata_filter(s: str) -> str:
    """
    Metafilter for jsonld context
    :param s: jsonld context string
    :return: string stripped of metadata
    """
    return re.sub(r'Auto generated from .*? by', 'Auto generated from ... by',
                  re.sub(r'Generation date: .*?\\n', r'Generation date: \\n', s))


def json_metadata_filter(s: str) -> str:
    return re.sub(r'("source_file_date": )".*"', r'\1"Friday Sep 27 12:00:00 2003"',
           re.sub(r'("generation_date": )".*"', r'\1"Friday Sep 27 12:00:00 2003"',
           re.sub(r'("source_file_size": )".*"', r'\1 23600', s)))


def json_metadata_context_filter(s: str) -> str:
    return re.sub(r'file:///.*/', r'', json_metadata_filter(s))


def metadata_filter(s: str) -> str:
    return re.sub(r'(# Auto generated from ).*(\.yaml by pythongen\.py version:) .*', r'\1\2',
                  re.sub(r'(# Generation date:) .*', r'\1', re.sub(r'\r\n', '\n', s)))


def yaml_filter(s: str) -> str:
    # source_file_date: Thu Jul  9 14:37:10 2020
    # source_file_size: 671
    # generation_date: 2020-07-09 15:43
    return re.sub(r'(source_file_date: ).*', r'\1Friday Sep 27 12:00:00 2003',
           re.sub(r'(generation_date: ).*', r'\1Friday Sep 27 12:00:00 2003',
           re.sub(r'(source_file_size: ).*', r'\1 23600', s)))


def nb_filter(s: str) -> str:
    """ Filter for jupyter (ipynb) notebooks """
    # It is easier to deal with notebook content in JSON
    s_json = loads(ldcontext_metadata_filter(s))
    for cell in s_json.cells:
        if hasattr(cell, 'execution_count'):
            cell.execution_count = 1
        if hasattr(cell, 'metadata'):
            delattr(cell, 'metadata')
        if hasattr(cell, 'outputs'):
            del_outputs = []
            for output in cell.outputs:
                to_del = []
                if hasattr(output, 'text'):
                    for line in output.text:
                        if 'WARNING: You are using pip' in line or\
                           'You should consider upgrading via' in line or\
                           'Requirement already satisfied:' in line:
                            to_del.append(line)
                    for del_line in to_del:
                        output.text.remove(del_line)
                    if not output.text:
                        del_outputs.append(output)
            if del_outputs:
                for del_output in del_outputs:
                    cell.outputs.remove(del_output)
    if hasattr(s_json.metadata, 'language_info'):
        if hasattr(s_json.metadata.language_info, 'version'):
            s_json.metadata.language_info.version = '3'

    return as_json(s_json)
