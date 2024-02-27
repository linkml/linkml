"""
Generate GOlr YAML schema definitions.

These can be converted to solr schema-xml, and used in amigo-bbop tools

See the golr-views directory in this repo for examples

"""

import os
from dataclasses import dataclass
from typing import List, Optional

import click
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.yamlutils import YAMLRoot, as_yaml

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class GOLRField(YAMLRoot):
    id: str
    description: str
    display_name: str
    property: List = empty_list()
    cardinality: Optional[str] = None


@dataclass
class GOLRClass(YAMLRoot):
    id: str
    schema_generating: bool
    description: str
    display_name: str
    document_category: str
    weight: int
    fields: List[GOLRField] = empty_list()


@dataclass
class GolrSchemaGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    directory_output = True
    valid_formats = ["golr"]
    visit_all_class_slots = True
    uses_schemaloader = True
    requires_metamodel = False

    # ObjectVars
    directory: str = None
    class_obj: Optional[GOLRClass] = None

    def generate_header(self):
        headers = [f"# metamodel_version: {self.schema.metamodel_version}"]
        if self.schema.version:
            headers.append(f"# version: {self.schema.version}")
        return headers

    def visit_schema(self, directory: str, **_) -> None:
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)
        # write_golr_yaml_to_dir(schema, dir)

    def visit_class(self, cls: ClassDefinition) -> bool:
        if not (cls.mixin or cls.abstract):
            self.class_obj = GOLRClass(
                id=underscore(cls.name),
                schema_generating=True,
                description=cls.description,
                display_name=cls.name,
                document_category=cls.name,
                weight=20,
            )
            return True
        else:
            return False

    def end_class(self, cls: ClassDefinition) -> None:
        fn = os.path.join(self.directory, underscore(cls.name + "-config.yaml"))
        if len(self.class_obj.fields) > 1:
            with open(fn, "w", encoding="UTF-8") as f:
                f.write("".join(self.generate_header()))
                f.write(as_yaml(self.class_obj))

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        field = GOLRField(
            id=underscore(aliased_slot_name),
            description=slot.description,
            display_name=slot.name,
        )
        if slot.multivalued:
            field.cardinality = "multi"
        self.class_obj.fields.append(field)


@shared_arguments(GolrSchemaGenerator)
@click.command()
@click.option("--dir", "-d", default="golr-views", show_default=True, help="Output directory")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, dir=None, **args):
    """Generate GOLR representation of a LinkML model"""
    print(GolrSchemaGenerator(yamlfile, directory=dir, **args).serialize(directory=dir, **args))


if __name__ == "__main__":
    cli()
