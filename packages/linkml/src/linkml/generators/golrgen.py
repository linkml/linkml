"""
Generate GOlr YAML schema definitions.

These can be converted to solr schema-xml, and used in amigo-bbop tools

See the golr-views directory in this repo for examples

"""

import os
from dataclasses import dataclass

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.yamlutils import YAMLRoot, as_yaml


@dataclass
class GOLRField(YAMLRoot):
    id: str
    description: str
    display_name: str
    property: list = empty_list()
    cardinality: str | None = None


@dataclass
class GOLRClass(YAMLRoot):
    id: str
    schema_generating: bool
    description: str
    display_name: str
    document_category: str
    weight: int
    fields: list[GOLRField] = empty_list()


@dataclass
class GolrSchemaGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    directory_output = True
    valid_formats = ["golr"]
    uses_schemaloader = False

    # ObjectVars
    directory: str = None
    class_obj: GOLRClass | None = None

    def generate_header(self):
        headers = [f"# metamodel_version: {self.schema.metamodel_version}"]
        if self.schema.version:
            headers.append(f"# version: {self.schema.version}")
        return headers

    def _golr_class(self, cls: ClassDefinition) -> GOLRClass:
        class_obj = GOLRClass(
            id=underscore(cls.name),
            schema_generating=True,
            description=cls.description,
            display_name=cls.name,
            document_category=cls.name,
            weight=20,
        )
        for slot in self.induced_slots_legacy_order(cls.name):
            field = GOLRField(
                id=underscore(slot.alias if slot.alias else slot.name),
                description=slot.description,
                display_name=slot.name,
            )
            if slot.multivalued:
                field.cardinality = "multi"
            class_obj.fields.append(field)
        return class_obj

    def serialize(self, directory: str | None = None, **kwargs) -> str:
        """Write one GOlr YAML config per concrete class into ``directory``."""
        directory = directory or self.directory
        self.directory = directory
        if directory:
            os.makedirs(directory, exist_ok=True)
        for cls in sorted(self.schemaview.all_classes().values(), key=lambda c: c.name.casefold()):
            if cls.mixin or cls.abstract:
                continue
            class_obj = self._golr_class(cls)
            if len(class_obj.fields) > 1:
                fn = os.path.join(directory, underscore(cls.name + "-config.yaml"))
                with open(fn, "w", encoding="UTF-8") as f:
                    f.write("".join(self.generate_header()))
                    f.write(as_yaml(class_obj))
        return "\n"


@shared_arguments(GolrSchemaGenerator)
@click.command(name="golr-views")
@click.option("--dir", "-d", default="golr-views", show_default=True, help="Output directory")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, dir=None, **args):
    """Generate GOLR representation of a LinkML model"""
    print(GolrSchemaGenerator(yamlfile, directory=dir, **args).serialize(directory=dir, **args))


if __name__ == "__main__":
    cli()
