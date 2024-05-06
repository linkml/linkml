"""Iterate through all examples in a folder testing them for validity.

"""

import glob
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from types import ModuleType
from typing import Any, List, Mapping, Optional, TextIO, Union

import click
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper, rdflib_dumper, yaml_dumper
from linkml_runtime.linkml_model import ElementName
from linkml_runtime.utils.formatutils import camelcase

from linkml._version import __version__
from linkml.generators.pythongen import PythonGenerator
from linkml.validator import Validator, _get_default_validator


@dataclass
class SummaryDocument:
    """
    An object describing the summary for processing a set of examples
    """

    text: StringIO = field(default_factory=lambda: StringIO())

    inputs: List[str] = field(default_factory=list)

    outputs: List[str] = field(default_factory=list)

    def add(self, *lines: str):
        for line in lines:
            self.text.write(line)
            self.text.write("\n")

    def __str__(self) -> str:
        return self.text.getvalue()


@dataclass
class ExampleRunner:
    """
    Processes a collection of positive and negative examples.

    Background: https://github.com/linkml/linkml/issues/501
    """

    input_directory: Optional[Path] = None
    """Directory in which positive instance examples are found."""

    input_formats: Optional[List[str]] = field(default_factory=lambda: ["yaml"])

    counter_example_input_directory: Optional[Path] = None
    """Directory in which negative instance examples are found. These are expected to fail."""

    output_directory: Optional[Path] = None
    """Directory where processed examples are written to."""

    output_formats: Optional[List[str]] = field(default_factory=lambda: ["yaml", "json", "ttl"])

    schemaview: Optional[SchemaView] = None
    """View over schema which all examples adhere to."""

    summary: SummaryDocument = field(default_factory=lambda: SummaryDocument())

    _python_module: Optional[ModuleType] = None
    """Module containing classes that all examples instantiate."""

    prefix_map: Optional[Mapping[str, str]] = None
    """Custom prefix map, for emitting RDF/turtle."""

    _validator: Optional[Validator] = None

    expand_dicts: bool = None
    """If true, then expand all dicts prior to validation."""

    use_type_designators: bool = True

    @property
    def python_module(self) -> ModuleType:
        """
        Load the python module containing the classes that all examples instantiate.

        :return:
        """
        if self._python_module is None:
            # See: https://github.com/linkml/linkml/issues/1219
            src = self.schemaview.schema.source_file
            if not src:
                src = self.schemaview.schema
            pygen = PythonGenerator(src)
            self._python_module = pygen.compile_module()
        return self._python_module

    @property
    def validator(self) -> Validator:
        """
        Get the current validator

        :return:
        """
        if self._validator is None:
            self._validator = _get_default_validator(self.schemaview.schema)
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
        for fmt in self.input_formats:
            input_examples = glob.glob(os.path.join(str(input_dir), f"*.{fmt}"))
            input_counter_examples = glob.glob(os.path.join(str(counter_example_dir), f"*.{fmt}"))
            if not input_counter_examples:
                logging.warning(f"No counter examples found in {self.counter_example_input_directory}")
            self.process_examples_from_list(input_examples, fmt, False)
            self.process_examples_from_list(input_counter_examples, fmt, True)

    def example_source_inputs(self, class_name: str = None) -> List[str]:
        """
        Get the list of example source inputs.

        :param class_name:
        :return:
        """
        input_dir = self.input_directory
        if input_dir is None:
            return []
        all_inputs = []
        for fmt in self.input_formats:
            glob_expr = f"*.{fmt}"
            if class_name is not None:
                glob_expr = f"{class_name}-{glob_expr}"
            input_examples = glob.glob(os.path.join(str(input_dir), glob_expr))
            all_inputs.extend(input_examples)
        return all_inputs

    def process_examples_from_list(self, input_examples: list, input_format: str, counter_examples: bool = True):
        sv = self.schemaview
        validator = self.validator
        summary = self.summary
        for input_example in input_examples:
            stem = Path(input_example).stem
            base = Path(self.output_directory) / stem
            if base in summary.inputs:
                raise ValueError(f"Duplicate example: {base}")
            summary.inputs.append(str(stem))
            base.parent.mkdir(exist_ok=True, parents=True)
            parts = stem.split("-")
            tc = parts[0]
            with open(input_example) as file:
                if input_format == "yaml":
                    input_dict = yaml.safe_load(file)
                elif input_format == "json":
                    input_dict = json.load(file)
                else:
                    raise NotImplementedError(f"Cannot handle format: {input_format}")
                summary.add(f"## {stem}", "### Input", "```yaml", f"{yaml.dump(input_dict)}", "```")
                success = True
                try:
                    report = validator.validate(input_dict, tc)
                    if report.results:
                        raise Exception(
                            "\n".join(f"[{result.severity.value}] {result.message}" for result in report.results)
                        )
                    # json validation is incomplete: also try object instantiation
                    self._load_from_dict(input_dict, target_class=tc)
                except Exception as e:
                    success = False
                    if not counter_examples:
                        raise ValueError(f"Example {input_example} failed validation:\n{e}")
                if counter_examples:
                    if success:
                        raise ValueError(f"Counter example {input_example} succeeded validation")
                    continue
                obj = self._load_from_dict(input_dict, target_class=tc)
                for fmt in self.output_formats:
                    output_file = f"{base}.{fmt}"
                    if fmt == "yaml":
                        yaml_dumper.dump(obj, to_file=output_file)
                    elif fmt == "json":
                        json_dumper.dump(obj, to_file=output_file)
                    elif fmt == "ttl":
                        rdflib_dumper.dump(obj, to_file=output_file, schemaview=sv, prefix_map=self.prefix_map)
                    else:
                        raise NotImplementedError(f"Cannot output in format: {fmt}")
                    summary.outputs.append(f"{stem}.{fmt}")

    def _load_from_dict(self, dict_obj: Any, target_class: Union[str, ElementName] = None) -> Any:
        """
        Load an object from a dict, using the target class to determine the type of object to create.

        TODO: move logic into core

        :param dict_obj:
        :param target_class:
        :return:
        """
        if not self.use_type_designators:
            return dict_obj
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
@click.option("--schema", "-s", required=True, help="Path to linkml schema yaml file")
@click.option("--prefixes", "-P", help="Path to prefixes")
@click.option("--input-directory", "-e", help="folder containing positive examples that MUST pass validation")
@click.option(
    "--counter-example-input-directory",
    "-N",
    help="folder containing counter examples that MUST fail validation",
)
@click.option(
    "--output-directory",
    "-d",
    required=True,
    help="folder containing positive examples that MUST pass validation",
)
@click.option(
    "--input-formats",
    "-f",
    multiple=True,
    default=["yaml"],
    show_default=True,
    help="Target formats to be converted to (yaml, json)",
)
@click.option(
    "--output-formats",
    "-t",
    multiple=True,
    default=["yaml", "json", "ttl"],
    show_default=True,
    help="Target formats to be converted to (yaml, json, ttl)",
)
@click.option(
    "--output",
    "-o",
    default=sys.stdout,
    type=click.File("w", encoding="utf-8"),
    help="Output file for markdown summary",
)
@click.option(
    "--use-type-designators/--no-use-type-designators",
    default=True,
    show_default=True,
    help="If true use type_designators to deepen ranges",
)
@click.version_option(__version__, "-V", "--version")
def cli(schema, prefixes, output: TextIO, **kwargs):
    """Process a folder of examples and a folder of counter examples.

    Each example in the folder

    For context, see: https://github.com/linkml/linkml/issues/501
    """
    schemaview = SchemaView(schema)
    prefix_map = yaml.safe_load(open(prefixes)) if prefixes else None
    runner = ExampleRunner(schemaview=schemaview, prefix_map=prefix_map, **kwargs)
    runner.process_examples()
    output.write(str(runner.summary))


if __name__ == "__main__":
    cli(sys.argv[1:])
