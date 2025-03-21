import logging
import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import PurePosixPath
from types import ModuleType
from typing import List, Optional

import click
from jinja2 import Environment, PackageLoader
from linkml_runtime.linkml_model import ClassDefinitionName
from linkml_runtime.linkml_model.meta import PermissibleValue, PermissibleValueText, SlotDefinition, TypeDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.generators.oocodegen import OOClass, OOCodeGenerator, OODocument, OOField
from linkml.utils.generator import shared_arguments

logger = logging.getLogger(__name__)


TYPEMAP = {
    "xsd:string": "str",
    "xsd:integer": "int",
    "xsd:float": "float",
    "xsd:double": "float",
    "xsd:boolean": "bool",
    "xsd:dateTime": "DateTime",
    "xsd:date": "Date",
    "xsd:time": "Time",
    "xsd:anyURI": "str" "",
    "xsd:decimal": "float",
}


class TemplateEnum(Enum):
    CLASS_BASED = "class_based"
    OBJECT_BASED = "object_based"


@dataclass
class PanderaGenerator(OOCodeGenerator):
    """
    Generates Pandera python classes from a LinkML schema.

    Status: incompletely implemented

    Two styles are supported:

    - class-based
    - schema-based (not implemented)
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

    def map_type(self, t: TypeDefinition) -> str:
        logger.info(f"type_map definition: {t}")

        if t.uri:
            # only return a Integer, Double Float when required == false
            typ = TYPEMAP.get(t.uri)
            return typ
        elif t.typeof:
            typ = self.map_type(self.schemaview.get_type(t.typeof))
            logger.info(f"typ: {typ}")
            return typ
        else:
            raise ValueError(f"{t} cannot be mapped to a type")

    def ifabsent_default_value(self, slot: SlotDefinition) -> str:
        ifabsent_pattern = re.compile(r"^((string)|(int)|(float)|(date)|(datetime)|([A-Za-z0-9_]+))\((.*)\)$")
        MATCH_GROUP_TYPE_INDEX = 1
        MATCH_GROUP_VALUE_INDEX = 8

        ifabsent = slot.ifabsent
        default_value = None

        if ifabsent is None:
            default_value = None
        elif ifabsent is True or ifabsent == "True":
            default_value = "True"
        elif ifabsent is False or ifabsent == "False":
            default_value = "False"
        else:
            ifabsent_match = ifabsent_pattern.match(ifabsent)

            if ifabsent_match:
                ifabsent_cast = ifabsent_match.group(MATCH_GROUP_TYPE_INDEX)
                ifabsent_value = ifabsent_match.group(MATCH_GROUP_VALUE_INDEX).replace('"', '\\"')

                if ifabsent_cast == "string":
                    default_value = f'"{ifabsent_value}"'
                elif ifabsent_cast == "int":
                    default_value = str(int(ifabsent_value))
                elif ifabsent_cast == "float":
                    default_value = str(float(ifabsent_value))
                elif ifabsent_cast == "date":
                    raise NotImplementedError("ifabsent date not implemented.")
                    # default_value = f"datetime.strptime({ifabsent_value})"
                elif ifabsent_cast == "datetime":
                    raise NotImplementedError("ifabsent datetime not implemented.")
                    # default_value = f"datetime.strptime({ifabsent_value})"
                else:
                    # may need to look up the enum value here
                    pass

        return default_value

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
        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()

        if self.template_path is None:
            self.template_path = PanderaGenerator.DEFAULT_TEMPLATE_PATH

        if self.template_file is None:
            self.template_file = PanderaGenerator.DEFAULT_TEMPLATE_FILE
        template_file = self.template_file

        template_obj = self.load_template(template_file)

        code = template_obj.render(
            doc=module,
            metamodel_version=self.schema.metamodel_version,
            model_version=self.schema.version,
            coerce=self.coerce,
        )
        return code

    def extract_permissible_text(self, pv):
        if isinstance(pv, str) or isinstance(pv, PermissibleValueText):
            return pv.replace("'", "\\'").replace('"', '\\"')
        elif isinstance(pv, PermissibleValue):
            return pv.text.code
        else:
            raise ValueError(f"Invalid permissible value in enum : {pv}")

    def get_enum_permissible_values(self, enum):
        return list(map(self.extract_permissible_text, enum.permissible_values or []))

    def handle_slot(self, cn: str, sn: str):
        safe_sn = self.get_slot_name(sn)
        slot = self.schemaview.induced_slot(sn, cn)
        range = slot.range

        if slot.alias is not None:
            safe_sn = self.get_slot_name(slot.alias)

        if range is None:
            range = self.schema.default_range  # need to figure this out, set at the beginning?
            if range is None:
                range = "str"
        elif range in self.schemaview.all_classes():
            range_info = self.schemaview.all_classes().get(range)

            if range_info["class_uri"] == "linkml:Any":
                range = "Object"
            else:
                range = "str"
        elif range in self.schemaview.all_types():
            t = self.schemaview.get_type(range)
            range = self.map_type(t)
        elif range in self.schemaview.all_enums():
            enum_definition = self.schemaview.all_enums().get(range)
            range = "Enum"
            slot.annotations["permissible_values"] = self.get_enum_permissible_values(enum_definition)
        else:
            raise Exception(f"Unknown range {range}")

        if slot.multivalued:
            if slot.inlined_as_list:
                range = self.make_multivalued(range)
            else:
                pass

        default_value = self.ifabsent_default_value(slot)

        return OOField(
            name=safe_sn,
            source_slot=slot,
            range=range,
            default_value=default_value,
        )

    def render(self) -> OODocument:
        """
        Implementation in progress
        :return:
        """
        sv: SchemaView
        sv = self.schemaview

        module_name = camelcase(sv.schema.name)

        oodoc = OODocument(name=module_name, package=self.package, source_schema=sv.schema)

        # this will need to take into account slot ranges as well.
        ordered_classes = [sv.get_class(cn, strict=True) for cn in self.order_classes_by_hierarchy(sv)]

        classes = []

        for c in ordered_classes:
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
            # if c.abstract:
            #    ooclass.abstract = c.abstraccamelcased
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

        oodoc.classes = reversed(classes)

        return oodoc


@shared_arguments(PanderaGenerator)
@click.option("--package", help="Package name where relevant for generated class files")
@click.option("--template-path", help="Optional jinja2 template directory within module")
@click.option("--template-file", help="Optional jinja2 template to use for class generation")
@click.version_option(__version__, "-V", "--version")
@click.command(name="gen-pandera")
def cli(
    yamlfile,
    package=None,
    template_path=None,
    template_file=None,
    slots=True,
    **args,
):
    """Generate Pandera classes to represent a LinkML model"""
    gen = PanderaGenerator(
        yamlfile,
        package=package,
        template_path=template_path,
        template_file=template_file,
        gen_slots=slots,
        **args,
    )

    print(gen.serialize())


if __name__ == "__main__":
    cli()
