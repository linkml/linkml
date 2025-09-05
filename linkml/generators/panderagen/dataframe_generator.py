import importlib
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Optional

from jinja2 import Environment, PackageLoader
from linkml_runtime.linkml_model.meta import TypeDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.oocodegen import OOCodeGenerator, OODocument

from .class_generator_mixin import ClassGeneratorMixin
from .enum_generator_mixin import EnumGeneratorMixin
from .render_adapters.dataframe_class import DataframeClass


@dataclass
class DataframeGenerator(OOCodeGenerator, EnumGeneratorMixin, ClassGeneratorMixin, ABC):
    """
    Abstract base class for generating dataframe classes from a LinkML schema.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorstem = PurePosixPath(generatorname).stem
    generatorversion = "0.0.1"
    valid_formats = ["python"]
    file_extension = "py"
    java_style = False

    # ObjectVars
    template_file: Optional[str] = None
    template_path: Optional[str] = None

    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

    roll_up_slots: bool = False
    """whether to include all slots from parents and mixins explicitly in the generated model."""

    def __post_init__(self):
        super().__post_init__()
        # Validate template path if provided
        if self.template_path is not None:
            from .panderagen import ALLOWED_TEMPLATE_DIRECTORIES

            if self.template_path not in ALLOWED_TEMPLATE_DIRECTORIES:
                raise ValueError(
                    f"Template path {self.template_path} not supported. Available: {ALLOWED_TEMPLATE_DIRECTORIES}"
                )

    def default_value_for_type(self, typ: str) -> str:
        """Allow underlying framework to handle default if not specified."""
        return None

    @staticmethod
    @abstractmethod
    def make_multivalued(range: str) -> str:
        """Convert a type to its multivalued equivalent."""
        pass

    @abstractmethod
    def uri_type_map(self, xsd_uri: str, template: str = None):
        """Map XSD URI to framework-specific type."""
        pass

    @abstractmethod
    def map_type(self, t: TypeDefinition) -> str:
        """Map a LinkML type definition to framework-specific type."""
        pass

    @abstractmethod
    def get_type_map(self) -> dict:
        """Get the type map for this generator."""
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
            type_map=self.get_type_map(),
            template_path=self.template_path,
            pandera_validator_code=pandera_validator_code,
            schema_view=self.schemaview,
            generator=self,
        )
        return code

    def compile_dataframe_model(self):
        """
        Generates and compiles Dataframe model
        """
        dataframe_code = self.serialize()
        return compile_python(dataframe_code)

    def render(self) -> OODocument:
        """
        Create a data structure ready to pass to the serialization templates.
        """
        sv: SchemaView = self.schemaview

        module_name = camelcase(sv.schema.name)

        oodoc = OODocument(name=module_name, package=self.package, source_schema=sv.schema)

        self.append_classes(oodoc)

        return oodoc

    def append_classes(self, oodoc: OODocument):
        classes = []

        # TODO: move to class mixin
        for c in self.ordered_classes():
            cn = c.name
            safe_cn = camelcase(cn)
            annotations = {}
            identifier_or_key_slot = self.get_identifier_or_key_slot(cn)
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
            oofield = self.handle_slot(schemaview_class.name, sn)
            if sn not in parent_slots:
                ooclass.fields.append(oofield)
            ooclass.all_fields.append(oofield)
