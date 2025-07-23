import logging
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
from types import ModuleType
from typing import Optional

import click
from jinja2 import Environment, PackageLoader
from linkml_runtime.linkml_model.meta import TypeDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.oocodegen import OOClass, OOCodeGenerator, OODocument

from .class_generator_mixin import ClassGeneratorMixin
from .enum_generator_mixin import EnumGeneratorMixin
from .slot_generator_mixin import SlotGeneratorMixin

logger = logging.getLogger(__name__)


# keys are template_path
TYPEMAP = {
    "panderagen_class_based": {
        "xsd:string": "str",
        "xsd:integer": "int",
        "xsd:float": "float",
        "xsd:double": "float",
        "xsd:boolean": "bool",
        "xsd:dateTime": "DateTime",
        "xsd:date": "Date",
        "xsd:time": "Time",
        "xsd:anyURI": "str",
        "xsd:decimal": "float",
    },
}


class TemplateEnum(Enum):
    CLASS_BASED = "panderagen_class_based"


@dataclass
class PanderaGenerator(OOCodeGenerator, EnumGeneratorMixin, ClassGeneratorMixin, SlotGeneratorMixin):
    """
    Generates Pandera python classes from a LinkML schema.

    Status: incompletely implemented

    One styles is supported:

    - panderagen_class_based
    """

    DEFAULT_TEMPLATE_PATH = "panderagen_class_based"
    DEFAULT_TEMPLATE_FILE = "pandera.jinja2"

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorstem = PurePosixPath(generatorname).stem
    generatorversion = "0.0.1"
    valid_formats = ["python"]
    file_extension = "py"
    java_style = False

    # ObjectVars
    template_file: Optional[str] = None
    template_path: str = DEFAULT_TEMPLATE_PATH

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True
    coerce: bool = False

    def default_value_for_type(self, typ: str) -> str:
        """Allow underlying framework to handle default if not specified."""
        return None

    @staticmethod
    def make_multivalued(range: str) -> str:
        return f"List[{range}]"

    def uri_type_map(self, xsd_uri: str, template: str = None):
        if template is None:
            template = self.template_path

        return TYPEMAP[template].get(xsd_uri)

    def map_type(self, t: TypeDefinition) -> str:
        if t.uri:
            typ = self.uri_type_map(t.uri)
            return typ
        elif t.typeof:
            typ = self.map_type(self.schemaview.get_type(t.typeof))
            return typ
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    def load_template(self, template_filename):
        jinja_env = Environment(loader=PackageLoader("linkml.generators.panderagen", self.template_path))
        return jinja_env.get_template(template_filename)

    def compile_pandera(self) -> ModuleType:
        """
        Generates and compiles Pandera model
        """
        pandera_code = self.serialize()

        return compile_python(pandera_code)

    def serialize(self, rendered_module: Optional[OODocument] = None) -> str:
        """
        Serialize the schema to a Pandera module as a string
        """
        if self.template_path is None:
            self.template_path = PanderaGenerator.DEFAULT_TEMPLATE_PATH

        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()

        if self.template_file is None:
            self.template_file = PanderaGenerator.DEFAULT_TEMPLATE_FILE
        template_file = self.template_file

        template_obj = self.load_template(template_file)

        code = template_obj.render(
            doc=module,
            metamodel_version=self.schema.metamodel_version,
            model_version=self.schema.version,
            coerce=self.coerce,
            type_map=TYPEMAP,
            template_path=self.template_path,
        )
        return code

    def render(self) -> OODocument:
        """
        Create a data structure ready to pass to the serialization templates.
        """
        sv: SchemaView = self.schemaview

        module_name = camelcase(sv.schema.name)

        oodoc = OODocument(name=module_name, package=self.package, source_schema=sv.schema)

        classes = []

        for c in self.ordered_classes():
            cn = c.name
            safe_cn = camelcase(cn)
            ooclass = OOClass(
                name=safe_cn,
                description=c.description,
                package=self.package,
                fields=[],
                source_class=c,
            )
            classes.append(ooclass)
            if c.mixin:
                ooclass.mixin = c.mixin
            if c.mixins:
                ooclass.mixins = [(x) for x in c.mixins]
            if c.is_a:
                ooclass.is_a = self.get_class_name(c.is_a)
                parent_slots = sv.class_slots(c.is_a)
            else:
                parent_slots = []
            for sn in sv.class_slots(cn):
                oofield = self.handle_slot(cn, sn)
                if sn not in parent_slots:
                    ooclass.fields.append(oofield)
                ooclass.all_fields.append(oofield)

        oodoc.classes = classes

        return oodoc


@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template-path", help="Optional jinja2 template directory within module")
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.version_option(__version__, "-V", "--version")
@click.argument("yamlfile")
@click.command(name="gen-pandera")
def cli(
    yamlfile,
    package=None,
    template_path=None,
    template_file=None,
    **args,
):
    if template_path is not None and template_path not in TYPEMAP:
        raise Exception(f"Template {template_path} not supported")

    """Generate Pandera classes to represent a LinkML model"""
    gen = PanderaGenerator(
        yamlfile,
        package=package,
        template_path=template_path,
        template_file=template_file,
        **args,
    )

    print(gen.serialize())


if __name__ == "__main__":
    cli()
