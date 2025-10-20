import importlib
import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import ModuleType
from typing import Optional

from jinja2 import Environment, PackageLoader
from linkml_runtime.linkml_model.meta import TypeDefinition
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.oocodegen import OOCodeGenerator, OODocument

from .class_handler_base import ClassHandlerBase
from .compile_python import compile_python
from .enum_handler_base import EnumHandlerBase
from .render_adapters.dataframe_class import DataframeClass

logger = logging.getLogger(__name__)


_DATAFRAME_GENERATOR_VERSION = "0.2.0"


@dataclass
class DataframeGenerator(OOCodeGenerator, ABC):
    """
    Abstract base class for generating dataframe classes from a LinkML schema.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorstem = PurePosixPath(generatorname).stem
    generatorversion = _DATAFRAME_GENERATOR_VERSION
    valid_formats = ["python"]
    file_extension = "py"
    java_style = False

    # ObjectVars
    template_file: str = None
    template_path: str = None

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

    roll_up_slots: bool = False
    """whether to include all slots from parents and mixins explicitly in the generated model."""

    backing_form: str = "serialization"
    """specific storage format that may differ from specified inlined flags"""

    def __post_init__(self):
        super().__post_init__()
        self.class_handler = ClassHandlerBase(self)
        self.enum_handler = EnumHandlerBase(self)
        # Slot handler will be set by subclasses

    def default_value_for_type(self, typ: str) -> str:
        """Allow underlying framework to handle default if not specified."""
        return None

    def map_type(self, t: TypeDefinition) -> str:
        logger.info(f"type_map definition: {t}")

        typ = None

        if t.uri:
            typ = self.TYPE_MAP.get(t.uri, None)
            if typ is None:
                typ = self.map_type(self.schemaview.get_type(t.typeof))
        elif t.typeof:
            typ = self.map_type(self.schemaview.get_type(t.typeof))

        if typ is None:
            raise ValueError(f"{t} cannot be mapped to a type")

        return typ

    @staticmethod
    @abstractmethod
    def make_multivalued(range: str) -> str:
        """Convert a type to its multivalued equivalent."""
        pass

    def default_template_path(self):
        """Get the default template path for this generator."""
        return "panderagen_class_based"

    def load_template(self, template_filename, template_path=None):
        """Load the template for code generation."""
        if template_path is None:
            template_path = self.default_template_path()
        jinja_env = Environment(loader=PackageLoader("linkml.generators.panderagen", template_path))
        return jinja_env.get_template(template_filename)

    def serialize(self, directory: str = None, rendered_module: Optional[OODocument] = None) -> str:
        """
        Serialize the dataframe schema to a Python module as a string
        """
        if self.template_path is None:
            self.template_path = "panderagen_class_based"  # default fallback
        elif self.template_path == "panderagen_polars_schema":
            self.roll_up_slots = True

        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()

        if self.template_file is None:
            self.template_file = "pandera.jinja2"  # default template
        template_file = self.template_file

        template_obj = self.load_template(template_file, self.template_path)

        if getattr(self, "inline_validator_mixin", False):
            linkml_pandera_validator = importlib.import_module("linkml.generators.panderagen.linkml_pandera_validator")
            module_path = linkml_pandera_validator.__file__
            try:
                with open(module_path) as file:
                    pandera_validator_code = file.read().replace("LinkmlPanderaValidator", "_LinkmlPanderaValidator")
            except Exception:
                pandera_validator_code = None
        else:
            pandera_validator_code = None

        code = template_obj.render(
            doc=module,
            metamodel_version=self.schema.metamodel_version,
            model_version=self.schema.version,
            coerce=getattr(self, "coerce", False),
            template_path=self.template_path,
            pandera_validator_code=pandera_validator_code,
            schema_view=self.schemaview,
            generator=self,
        )

        if directory is not None:
            os.makedirs(directory, exist_ok=True)
            filename = f"{module.name}.py"
            filepath = os.path.join(directory, filename)
            with open(filepath, "w") as f:
                f.write(code)

        return code

    def compile_dataframe_model(self, module_name: str = None) -> ModuleType:
        """
        Generates and compiles Dataframe model.

        Make sure module_name doesn't conflict with any imported modules.
        It will produce unexpected errors.
        """
        dataframe_code = self.serialize()

        if module_name is None:
            module_name = self.template_path

        return compile_python(dataframe_code, module_name=module_name)

    def render(self) -> OODocument:
        """
        Create a data structure ready to pass to the serialization templates.
        """
        sv: SchemaView = self.schemaview

        module_name = sv.schema.name

        oodoc = OODocument(name=module_name, package=self.package, source_schema=sv.schema)

        self.append_classes(oodoc)

        return oodoc

    def append_classes(self, oodoc: OODocument):
        classes = []

        # TODO: move to class mixin
        for c in self.class_handler.ordered_classes():
            if c.name in self.schemaview.all_enums():
                continue
            cn = c.name
            safe_cn = camelcase(cn)
            annotations = {}
            identifier_or_key_slot = self.slot_handler.get_identifier_or_key_slot(cn)
            if identifier_or_key_slot:
                annotations["identifier_key_slot"] = identifier_or_key_slot.name
            ooclass = DataframeClass(
                name=safe_cn,
                description=c.description,
                package=self.package,
                fields=[],
                all_fields=[],
                source_class=c,
                annotations=annotations,
            )

            self.append_mixins(c, ooclass)
            self.append_slots(c, ooclass)

            classes.append(ooclass)

        oodoc.classes = classes

    def append_mixins(self, schemaview_class, ooclass: DataframeClass) -> None:
        if schemaview_class.mixin:
            ooclass.mixin = schemaview_class.mixin
        if schemaview_class.mixins:
            ooclass.mixins = [(x) for x in schemaview_class.mixins]

    def append_slots(self, schemaview_class, ooclass: DataframeClass) -> None:
        """
        Append slots to the class.
        """
        if schemaview_class.is_a:
            ooclass.is_a = self.get_class_name(schemaview_class.is_a)
            parent_slots = self.schemaview.class_slots(schemaview_class.is_a)
        else:
            parent_slots = []

        for sn in self.schemaview.class_slots(schemaview_class.name):
            oofield = self.slot_handler.handle_slot(schemaview_class.name, sn)
            if sn not in parent_slots:
                ooclass.fields.append(oofield)
            ooclass.all_fields.append(oofield)

    #
    # Name overrides from OOCodeGenerator and Generator
    #
    def clean(self, name: str) -> str:
        # Replace sequences of non-alphanumeric chars with __ except _ and - which becomes _
        cleaned = re.sub(r"[^a-zA-Z0-9-_]+", "__", name)
        cleaned = re.sub(r"-+", "_", cleaned)
        # If name starts with digit, prepend __
        if cleaned and cleaned[0].isdigit():
            cleaned = "__" + cleaned
        return cleaned

    def get_class_name(self, cn):
        """override from OOCodeGenerator"""
        return self.clean(cn)

    def get_slot_name(self, sn):
        """override from OOCodeGenerator"""
        return self.clean(sn)

    def get_enum_name(self, enum_name: str) -> str:
        """note OOCodeGenerator uses camelcase directly"""
        return self.clean(enum_name)

    def get_metamodel_slot_name(self, slot_name: str) -> str:
        """override from Generator"""
        return self.get_slot_name(slot_name)

    def slot_name(self, name: str) -> str:
        """
        Override from generator to use get_metamodel_slot_name
        Return the  version of the aliased slot name if name is a slot. Prepend ``unknown_`` if the name
        isn't valid.
        """
        slot = self.slot_for(name)
        return self.get_metamodel_slot_name(self.aliased_slot_name(slot) if slot else ("unknown " + name))
