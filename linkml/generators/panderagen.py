import logging
import os
from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import List, Optional

import click
from jinja2 import Environment, PackageLoader
from linkml_runtime.linkml_model import ClassDefinitionName
from linkml_runtime.linkml_model.meta import TypeDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.oocodegen import OOClass, OOCodeGenerator, OODocument, OOField
from linkml.utils.generator import shared_arguments

logger = logging.getLogger(__name__)

default_template = """
"""  # noqa: E501

# several of these are stubbed in
TYPEMAP = {
    "xsd:string": "str",
    "xsd:integer": "int",
    "xsd:float": "float",
    "xsd:double": "float",
    "xsd:boolean": "bool",
    "xsd:dateTime": "Time(time_zone_agnostic=True)",
    "xsd:date": "DateTime(time_zone_agnostic=True)",
    "xsd:time": "Time(time_zone_agnostic=True)",
    "xsd:anyURI": "str",
    "xsd:decimal": "int",
}

TYPE_DEFAULTS = {"boolean": "false", "int": "0", "float": "0f", "double": "0d", "String": '""'}


class TemplateEnum(Enum):
    CLASS_BASED = "class_based"
    OBJECT_BASED = "object_based"


@dataclass
class PanderaGenerator(OOCodeGenerator):
    """
    Generates Pandera python classes from a LinkML schema.

    Two styles are supported:

    - class-based
    - schema-based (not implemented)
    """

    DEFAULT_TEMPLATE_PATH = "pandera.class_based.jinja2"

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["python"]
    file_extension = "py"
    java_style = False

    # ObjectVars
    template_file: Optional[str] = None

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

    def default_value_for_type(self, typ: str) -> str:
        return TYPE_DEFAULTS.get(typ, "null")

    @staticmethod
    def make_multivalued(range: str) -> str:
        return f"List[{range}]"

    # this is based on sqlagen, but it only accounts for inheritance,
    # not associations to other models
    # for now these are cast to str to avoid import issues (resulting in an incorrect model)
    @staticmethod
    def order_classes_by_hierarchy(sv: SchemaView) -> List[ClassDefinitionName]:
        olist = sv.class_roots()
        unprocessed = [cn for cn in sv.all_classes() if cn not in olist]
        while len(unprocessed) > 0:
            ext_list = [cn for cn in unprocessed if not any(p for p in sv.class_parents(cn) if p not in olist)]
            if len(ext_list) == 0:
                raise ValueError(f"Cycle in hierarchy, cannot process: {unprocessed}")
            olist += ext_list
            unprocessed = [cn for cn in unprocessed if cn not in olist]
        return olist

    # this is a very rough implementation based on javagen / oocodegen
    def map_type(self, t: TypeDefinition, required: bool = False) -> str:
        if t.uri:
            # only return a Integer, Double Float when required == false
            typ = TYPEMAP.get(t.uri)
            return typ
        elif t.typeof:
            return self.map_type(self.schemaview.get_type(t.typeof))
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    # prefer loading jinja2 templates via the packageloader
    def load_template(self, template_filename):
        jinja_env = Environment(loader=PackageLoader("linkml.generators", "panderagen"))
        return jinja_env.get_template(template_filename)

    # based on sqlagen, needs cleanup.
    def compile_pandera(
        self,
        model_path=None,
        template: TemplateEnum = TemplateEnum.CLASS_BASED,
        **kwargs,
    ) -> ModuleType:
        """
        Generates and compiles Pandera model

        - If template is CLASS_BASED, then the class-based Pandera is used
        - If template is OBJECT_BASED then the object-based Pandera API is used

        :param model_path:
        :param template:
        :param kwargs:
        :return:
        """

        if model_path is None:
            model_path = self.schema.name

        pandera_code = self.generate_pandera(**kwargs)
        logger.info(f"generated Pandera model:\n{pandera_code}")

        return compile_python(pandera_code, package_path=model_path)

    # Based on javagen
    def generate_pandera(self, **kwargs):
        template_obj = self.load_template(PanderaGenerator.DEFAULT_TEMPLATE_PATH)

        oodocs = self.create_documents()

        code = template_obj.render(
            docs=oodocs,
            metamodel_version=self.schema.metamodel_version,
            model_version=self.schema.version,
        )

        return code

    # This was copied from javagen, which created multiple files.
    # Would need cleanup for a multi-class python file.
    def serialize(self, directory: str, **kwargs) -> None:
        self.directory = directory

        code = self.generate_pandera()

        os.makedirs(directory, exist_ok=True)
        filename = "pandera.out.py"
        path = os.path.join(directory, filename)
        with open(path, "w", encoding="UTF-8") as stream:
            stream.write(code)

    ## This was copied over from OOCodeGen and is only a rough implementation
    def create_documents(self) -> List[OODocument]:
        """
        Currently hardcoded for java-style
        :return:
        """
        DEFAULT_RANGE = "string"
        DEFAULT_VALUE = "null"
        sv: SchemaView
        sv = self.schemaview
        docs = []

        ordered_classes = [sv.get_class(cn, strict=True) for cn in self.order_classes_by_hierarchy(sv)]

        for c in ordered_classes:
            # c = sv.get_class(cn)
            cn = c.name
            safe_cn = camelcase(cn)
            oodoc = OODocument(name=safe_cn, package=self.package, source_schema=sv.schema)
            docs.append(oodoc)
            ooclass = OOClass(
                name=safe_cn,
                description=c.description,
                package=self.package,
                fields=[],
                source_class=c,
            )
            # currently hardcoded for java style, one class per doc
            oodoc.classes = [ooclass]
            if c.mixin:
                ooclass.mixin = c.mixin
            if c.mixins:
                ooclass.mixins = [(x) for x in c.mixins]
            if c.abstract:
                ooclass.abstract = c.abstraccamelcaset
            if c.is_a:
                ooclass.is_a = self.get_class_name(c.is_a)
                parent_slots = sv.class_slots(c.is_a)
            else:
                parent_slots = []
            for sn in sv.class_slots(cn):
                safe_sn = self.get_slot_name(sn)
                slot = sv.induced_slot(sn, cn)
                range = slot.range
                default_value = DEFAULT_VALUE

                logging.info(f"RANGE: {cn}.{sn} -> {range}")

                if range is None:
                    # TODO: schemaview should infer this
                    range = sv.schema.default_range

                if range is None:
                    range = "str"
                elif range in sv.all_classes():
                    # TODO: account for declaring in order, then use real ranges
                    range = "str"
                    # range = self.get_class_name(range)
                    default_value = DEFAULT_VALUE
                elif range in sv.all_types():
                    t = sv.get_type(range)
                    range = self.map_type(t, slot.required)
                    if range is None:  # If mapping fails,
                        range = self.map_type(sv.all_types().get(DEFAULT_RANGE))
                elif range in sv.all_enums():
                    range = self.map_type(sv.all_types().get(DEFAULT_RANGE))
                else:
                    raise Exception(f"Unknown range {range}")

                logging.info(f"RANGE 2: {range}")

                # Set default values for
                if range == "boolean":
                    default_value = "false"
                elif range == "integer":
                    default_value = "0"
                elif range == "String":
                    default_value = '""'

                # TODO:
                #  default_value = default_value_for_type(range)

                if slot.multivalued:
                    range = self.make_multivalued(range)
                    default_value = "List.of()"
                oofield = OOField(
                    name=safe_sn,
                    source_slot=slot,
                    range=range,
                    default_value=default_value,
                )
                if sn not in parent_slots:
                    ooclass.fields.append(oofield)
                ooclass.all_fields.append(oofield)

        return docs


@shared_arguments(PanderaGenerator)
@click.option(
    "--output-directory",
    default="output",
    show_default=True,
    help="Output directory for individually generated class files",
)
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.version_option(__version__, "-V", "--version")
@click.command(name="gen-pandera")
def cli(
    yamlfile,
    output_directory=None,
    package=None,
    template_file=None,
    slots=True,
    **args,
):
    """Generate Pandera classes to represent a LinkML model"""
    PanderaGenerator(
        yamlfile,
        package=package,
        template_file=template_file,
        gen_slots=slots,
        **args,
    ).serialize(output_directory, **args)


if __name__ == "__main__":
    cli()
