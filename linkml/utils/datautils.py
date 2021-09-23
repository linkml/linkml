import os
from typing import Optional
from collections import defaultdict

from linkml_runtime.utils.compile_python import compile_python

from linkml_runtime.dumpers.yaml_dumper import YAMLDumper
from linkml_runtime.dumpers.json_dumper import JSONDumper
from linkml_runtime.dumpers.rdf_dumper import RDFDumper
from linkml_runtime.dumpers.csv_dumper import CSVDumper
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.rdf_loader import RDFLoader
from linkml_runtime.loaders.csv_loader import CSVLoader
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinitionName

from linkml.generators.jsonldcontextgen import ContextGenerator

dumpers_loaders = {
    'yaml': (YAMLDumper, YAMLLoader),
    'json': (JSONDumper, JSONLoader),
    'rdf': (RDFDumper, RDFLoader),
    'csv': (CSVDumper, CSVLoader),
    'tsv': (CSVDumper, CSVLoader),
}

aliases = {
    'ttl': 'rdf',
}

def _get_format(path: str, specified_format: str =None, default=None):
    if specified_format is None:
        if path is None:
            if default is None:
                raise Exception(f'Must pass format option OR pass a filename with known file suffix')
            else:
                specified_format = default
        else:
            _, ext = os.path.splitext(path)
            if ext is not None:
                specified_format = ext.replace('.', '')
            else:
                raise Exception(f'Must pass format option OR use known file suffix: {path}')
    specified_format = specified_format.lower()
    if specified_format in aliases:
        specified_format = aliases[specified_format]
    return specified_format

def _is_xsv(fmt: str) -> bool:
    return fmt == 'csv' or fmt == 'tsv'

def get_loader(fmt: str) -> Loader:
    return dumpers_loaders[fmt][1]()
def get_dumper(fmt: str) -> Loader:
    return dumpers_loaders[fmt][0]()

def _get_context(schema) -> str:
    return ContextGenerator(schema).serialize()

def infer_root_class(sv: SchemaView) -> Optional[ClassDefinitionName]:
    refs = defaultdict(int)
    for cn in sv.all_class().keys():
        for sn in sv.class_slots(cn):
            slot = sv.induced_slot(sn, cn)
            r = slot.range
            if r in sv.all_class():
                for a in sv.class_ancestors(r):
                    refs[a] += 1
    candidates = [cn for cn in sv.all_class().keys() if cn not in refs]
    if len(candidates) == 1:
        return candidates[0]
    else:
        return None

def infer_index_slot(sv: SchemaView, root_class: ClassDefinitionName) -> Optional[SlotDefinitionName]:
    index_slots = []
    for sn in sv.class_slots(root_class):
        slot = sv.induced_slot(sn, root_class)
        if slot.multivalued and slot.range in sv.all_class():
            index_slots.append(sn)
    if len(index_slots) == 1:
        return index_slots[0]
    else:
        return None




