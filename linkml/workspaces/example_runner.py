"""Iterate through all examples in a folder testing them for validity.

"""
import glob
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Union, Any, Mapping

import click
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper, yaml_dumper
from linkml_runtime.linkml_model import ElementName
from linkml_runtime.utils.formatutils import camelcase

from linkml.generators.pythongen import PythonGenerator
from linkml.utils.datavalidator import DataValidator
from linkml.validators import JsonSchemaDataValidator


@dataclass
class ExampleRunner:
    """
    Processes a collection of positive and negative examples.

    Background: https://github.com/linkml/linkml/issues/501
    """

    input_directory: Path = None
    """Directory in which positive instance examples are found."""

    counter_example_input_directory: Path = None
    """Directory in which negative instance examples are found. These are expected to fail."""

    output_directory: Path = None
    """Directory where processed examples are written to."""

    schemaview: SchemaView = None
    """View over schema which all examples adhere to."""

    _python_module: ModuleType = None
    """Module containing classes that all examples instantiate."""

    prefix_map: Mapping[str, str] = None
    """Custom prefix map, for emitting RDF/turtle."""

    _validator: DataValidator = None

    @property
    def python_module(self) -> ModuleType:
        """
        Load the python module containing the classes that all examples instantiate.

        :return:
        """
        if self._python_module is None:
            pygen = PythonGenerator(self.schemaview.schema)
            self._python_module = pygen.compile_module()
        return self._python_module

    @property
    def validator(self) -> DataValidator:
        """
        Get the current validator

        :return:
        """
        if self._validator is None:
            self._validator = JsonSchemaDataValidator(self.schemaview.schema)
        return self._validator

    def process_examples(self):
        """
        Process all examples in the input directory.

        Filenames should be of the form

         - CLASSNAME-EXAMPLENAME.yaml

         E.g Person-001.yaml

        :return:
        """
        input_dir = self.input_directory
        counter_example_dir = self.counter_example_input_directory
        if input_dir is None:
            input_dir = Path.cwd() / "examples"
        if counter_example_dir is None:
            counter_example_dir = Path.cwd() / "counter_examples"
        input_examples = glob.glob(os.path.join(str(input_dir), '*.yaml'))
        input_counter_examples = glob.glob(os.path.join(str(counter_example_dir), '*.yaml'))
        if not input_counter_examples:
            logging.warning(f"No counter examples found in {self.counter_example_input_directory}")
        self.process_examples_from_list(input_examples, False)
        self.process_examples_from_list(input_counter_examples, True)

    def process_examples_from_list(self, input_examples: list, counter_examples: bool = True):
        sv = self.schemaview
        validator = self.validator
        for input_example in input_examples:
            stem = Path(input_example).stem
            base = Path(self.output_directory) / stem
            base.parent.mkdir(exist_ok=True, parents=True)
            parts = stem.split("-")
            tc = parts[0]
            with open(input_example) as file:
                input_dict = yaml.safe_load(file)
                success = True
                try:
                    validator.validate_dict(input_dict, tc, closed=True)
                except Exception as e:
                    success = False
                    if not counter_examples:
                        raise ValueError(f"Example {input_example} failed validation: {e}")
                if counter_examples:
                    if success:
                        raise ValueError(f"Counter example {input_example} succeeded validation")
                    continue
                obj = self._load_from_dict(input_dict, target_class=tc)
                yaml_dumper.dump(obj, to_file=f"{base}.yaml")
                json_dumper.dump(obj, to_file=f"{base}.json")
                rdflib_dumper.dump(obj, to_file=f"{base}.ttl", schemaview=sv, prefix_map=self.prefix_map)

    def _load_from_dict(self, dict_obj: Any, target_class: Union[str, ElementName] = None) -> Any:
        """
        Load an object from a dict, using the target class to determine the type of object to create.

        TODO: move logic into core

        :param dict_obj:
        :param target_class:
        :return:
        """
        sv = self.schemaview
        if target_class is None:
            target_class_names = [c.name for c in sv.all_classes().values() if c.tree_root]
            if len(target_class_names) != 1:
                raise ValueError(f"Cannot determine single target class, found: {target_class_names}")
            target_class = target_class_names[0]
        if isinstance(dict_obj, dict):
            if target_class not in sv.all_classes():
                raise ValueError(f"No such class as {target_class}")
            td_slot = sv.get_type_designator_slot(target_class) if target_class else None
            if td_slot:
                if td_slot.name in dict_obj:
                    target_class = dict_obj[td_slot.name]
            elif "@type" in dict_obj:
                target_class = dict_obj["@type"]
                del dict_obj["@type"]
            if ":" in target_class:
                target_classes = [c for c in sv.all_classes() if sv.get_uri(c) == target_class]
                if len(target_classes) != 1:
                    raise ValueError(f"Cannot find unique class for URI {target_class}; got: {target_classes}")
                target_class = target_classes[0]
            new_dict_obj = {}
            for k, v in dict_obj.items():
                if v is not None:
                    islot = sv.induced_slot(k, target_class)
                    v2 = self._load_from_dict(v, target_class=islot.range)
                    new_dict_obj[k] = v2
            py_target_class = getattr(self.python_module, camelcase(target_class))
            return py_target_class(**new_dict_obj)
        elif isinstance(dict_obj, list):
            return [self._load_from_dict(x, target_class) for x in dict_obj]
        else:
            return dict_obj


@click.command()
@click.option("--schema",
              "-s",
              required=True,
              help="Path to linkml schema yaml file")
@click.option("--prefixes",
              "-P",
              help="Path to prefixes")
@click.option("--input-directory",
              "-e",
              help="folder containing positive examples that MUST pass validation")
@click.option("--counter-example-input-directory",
              "-N",
              help="folder containing counter examples that MUST fail validation")
@click.option("--output-directory",
              "-d",
              required=True,
              help="folder containing positive examples that MUST pass validation")
def cli(schema, prefixes, **kwargs):
    """Process examples.

    Status: testing

    For context, see: https://github.com/linkml/linkml/issues/501
    """
    schemaview = SchemaView(schema)
    prefix_map = yaml.safe_load(open(prefixes)) if prefixes else None
    runner = ExampleRunner(schemaview=schemaview,
                           prefix_map=prefix_map,
                           **kwargs)
    runner.process_examples()


if __name__ == "__main__":
    cli(sys.argv[1:])




