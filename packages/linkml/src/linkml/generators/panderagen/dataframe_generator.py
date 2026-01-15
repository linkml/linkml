import importlib
import logging
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import ModuleType
from typing import Optional

from jinja2 import Environment, PackageLoader

from linkml.generators.oocodegen import OOCodeGenerator, OODocument
from linkml_runtime.linkml_model.meta import TypeDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase
from linkml_runtime.utils.schemaview import SchemaView

from .class_handler_base import ClassHandlerBase
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
    TYPE_MAP: dict = None

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
        if self.TYPE_MAP is None:
            self.TYPE_MAP = self._default_type_map()
        self.class_handler = ClassHandlerBase(self)
        self.enum_handler = EnumHandlerBase(self)
        # Slot handler will be set by subclasses

    @abstractmethod
    def _default_type_map(self) -> dict:
        """Override in subclasses to provide default TYPE_MAP."""

    def default_value_for_type(self, typ: str) -> str:
        """Allow underlying framework to handle default if not specified."""
        return None

    def map_type(self, t: TypeDefinition, required: bool = False) -> str:
        del required  # unused

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

    @staticmethod
    def compile_package_from_specification(
        specification: list[tuple[str, type, str, str, str]],
        package_name: str,
        schema: str,
        directory: str = None,
        **args,
    ):
        """
        Compile multiple generators from specification tuples as a package to support relative imports.

        Args:
            specification: List of (module_name, generator_class, template_dir, template_file, backing_form) tuples
            package_name: Name of the package to create
            schema: Schema YAML string or file path
            directory: Optional directory to write files to
            **args: Additional arguments to pass to generator constructors

        Returns:
            dict mapping module names to compiled modules if directory is None,
            otherwise None (files written to directory)
        """
        generators = []

        for module_name, generator_class, template_dir, template_file, backing_form in specification:
            gen = generator_class(
                schema=schema,
                backing_form=backing_form,
                **args,
            )
            gen.template_file = template_file
            gen.template_path = template_dir

            if directory is not None:
                # File-only mode: generate and write to disk
                oodoc = gen.render()
                oodoc.name = module_name
                gen.serialize(directory=directory, rendered_module=oodoc)
            else:
                # Memory-only mode: prepare for compilation
                generators.append((module_name, gen))

        # Only compile if not writing to directory
        if directory is None:
            return DataframeGenerator.compile_package(generators, package_name)
        else:
            # Create __init__.py for the package
            init_file = os.path.join(directory, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write('"""Package of generated pandera schemas."""\n')
            return None

    @staticmethod
    def compile_package(generators: list[tuple], package_name: str) -> dict[str, ModuleType]:
        """
        Compile multiple generators as a package to support relative imports.

        Args:
            generators: List of (module_name, generator_instance) tuples
            package_name: Name of the package to create

        Returns:
            dict mapping module names to compiled modules
        """
        # Create package in sys.modules
        package_module = ModuleType(package_name)
        package_module.__package__ = package_name
        package_module.__path__ = []
        sys.modules[package_name] = package_module

        compiled_modules = {}

        for module_name, generator in generators:
            code = generator.serialize()
            full_module_name = f"{package_name}.{module_name}"

            # Compile with package context
            module = compile_python(code, module_name=full_module_name)
            module.__package__ = package_name

            compiled_modules[module_name] = module

        return compiled_modules

    @staticmethod
    def cleanup_package(package_name: str) -> None:
        """
        Remove temporary package and its modules from sys.modules.
        """
        modules_to_remove = [
            name for name in sys.modules.keys() if name == package_name or name.startswith(f"{package_name}.")
        ]
        for module_name in modules_to_remove:
            del sys.modules[module_name]

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

        for c in self.class_handler.ordered_classes():
            if c.name in self.schemaview.all_enums():
                continue
            cn = c.name
            safe_cn = self.get_class_name(cn)
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
        return camelcase(self.clean(cn))

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
        Return the metamodel version of the aliased slot name if name is a slot. Prepend ``unknown_`` if the name
        isn't valid.
        """
        slot = self.slot_for(name)

        if slot is None:
            raise ValueError(f"Unknown slot: {name}")

        return self.get_metamodel_slot_name(self.aliased_slot_name(slot))
