import inspect
import logging
import os
import re
import textwrap
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import ClassVar, Literal, Optional, TypeVar, Union, overload

import click
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, Template
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ElementName,
    SchemaDefinition,
    SlotDefinition,
    TypeDefinition,
)
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.formatutils import camelcase, remove_empty_items, underscore
from linkml_runtime.utils.schemaview import SchemaView
from pydantic.version import VERSION as PYDANTIC_VERSION

from linkml._version import __version__
from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.common.type_designators import get_accepted_type_designator_values, get_type_designator_value
from linkml.generators.oocodegen import OOCodeGenerator
from linkml.generators.pydanticgen import includes
from linkml.generators.pydanticgen.array import ArrayRangeGenerator, ArrayRepresentation
from linkml.generators.pydanticgen.build import ClassResult, SlotResult, SplitResult
from linkml.generators.pydanticgen.template import (
    Import,
    Imports,
    ObjectImport,
    PydanticAttribute,
    PydanticBaseModel,
    PydanticClass,
    PydanticModule,
    PydanticTemplateModel,
)
from linkml.generators.python.python_ifabsent_processor import PythonIfAbsentProcessor
from linkml.utils import deprecation_warning
from linkml.utils.generator import shared_arguments

logger = logging.getLogger(__name__)


if int(PYDANTIC_VERSION[0]) == 1:
    deprecation_warning("pydantic-v1")


def _get_pyrange(t: TypeDefinition, sv: SchemaView) -> str:
    pyrange = t.repr if t is not None else None
    if pyrange is None:
        pyrange = t.base
    if t.base == "XSDDateTime":
        pyrange = "datetime "
    if t.base == "XSDDate":
        pyrange = "date"
    if pyrange is None and t.typeof is not None:
        pyrange = _get_pyrange(sv.get_type(t.typeof), sv)
    if pyrange is None:
        raise Exception(f"No python type for range: {t.name} // {t}")
    return pyrange


DEFAULT_IMPORTS = (
    Imports()
    + Import(module="__future__", objects=[ObjectImport(name="annotations")])
    + Import(
        module="datetime", objects=[ObjectImport(name="datetime"), ObjectImport(name="date"), ObjectImport(name="time")]
    )
    + Import(module="decimal", objects=[ObjectImport(name="Decimal")])
    + Import(module="enum", objects=[ObjectImport(name="Enum")])
    + Import(module="re")
    + Import(module="sys")
    + Import(
        module="typing",
        objects=[
            ObjectImport(name="Any"),
            ObjectImport(name="ClassVar"),
            ObjectImport(name="Literal"),
            ObjectImport(name="Optional"),
            ObjectImport(name="Union"),
        ],
    )
    + Import(
        module="pydantic",
        objects=[
            ObjectImport(name="BaseModel"),
            ObjectImport(name="ConfigDict"),
            ObjectImport(name="Field"),
            ObjectImport(name="RootModel"),
            ObjectImport(name="field_validator"),
        ],
    )
)

DEFAULT_INJECTS = [includes.LinkMLMeta]


class MetadataMode(str, Enum):
    FULL = "full"
    """
    all metadata from the source schema will be included, even if it is represented by the template classes,
    and even if it is represented by some child class (eg. "classes" will be included with schema metadata
    """
    EXCEPT_CHILDREN = "except_children"
    """
    all metadata from the source schema will be included, even if it is represented by the template classes,
    except if it is represented by some child template class (eg. "classes" will be excluded from schema metadata)
    """
    AUTO = "auto"
    """
    Only the metadata that isn't represented by the template classes or excluded with ``meta_exclude`` will be included
    """
    NONE = None
    """
    No metadata will be included.
    """


class SplitMode(str, Enum):
    FULL = "full"
    """
    Import all classes defined in imported schemas
    """

    AUTO = "auto"
    """
    Only import those classes that are actually used in the generated schema as

    * parents (``is_a``)
    * mixins
    * slot ranges
    """


DefinitionType = TypeVar("DefinitionType", bound=Union[SchemaDefinition, ClassDefinition, SlotDefinition])
TemplateType = TypeVar("TemplateType", bound=Union[PydanticModule, PydanticClass, PydanticAttribute])


@dataclass
class PydanticGenerator(OOCodeGenerator, LifecycleMixin):
    """
    Generates Pydantic-compliant classes from a schema

    This is an alternative to the dataclasses-based Pythongen

    Lifecycle methods (see :class:`.LifecycleMixin` ) supported:

    * :meth:`~.LifecycleMixin.before_generate_enums`

    Slot generation is nested within class generation, since the pydantic generator currently doesn't
    create an independent representation of slots aside from their materialization as class fields.
    Accordingly, the ``before_`` and ``after_generate_slots`` are called before and after each class's
    slot generation, rather than all slot generation.

    * :meth:`~.LifecycleMixin.before_generate_classes`
    * :meth:`~.LifecycleMixin.before_generate_class`
    * :meth:`~.LifecycleMixin.after_generate_class`
    * :meth:`~.LifecycleMixin.after_generate_classes`

    * :meth:`~.LifecycleMixin.before_generate_slots`
    * :meth:`~.LifecycleMixin.before_generate_slot`
    * :meth:`~.LifecycleMixin.after_generate_slot`
    * :meth:`~.LifecycleMixin.after_generate_slots`

    * :meth:`~.LifecycleMixin.before_render_template`
    * :meth:`~.LifecycleMixin.after_render_template`

    """

    # ClassVar overrides
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ["pydantic"]
    file_extension = "py"

    # ObjectVars
    array_representations: list[ArrayRepresentation] = field(default_factory=lambda: [ArrayRepresentation.LIST])
    black: bool = False
    """
    If black is present in the environment, format the serialized code with it
    """

    template_dir: Optional[Union[str, Path]] = None
    """
    Override templates for each PydanticTemplateModel.

    Directory with templates that override the default :attr:`.PydanticTemplateModel.template`
    for each class. If a matching template is not found in the override directory,
    the default templates will be used.
    """
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid"
    gen_mixin_inheritance: bool = True
    injected_classes: Optional[list[Union[type, str]]] = None
    """
    A list/tuple of classes to inject into the generated module.

    Accepts either live classes or strings. Live classes will have their source code
    extracted with inspect.get - so they need to be standard python classes declared in a
    source file (ie. the module they are contained in needs a ``__file__`` attr,
    see: :func:`inspect.getsource` )
    """
    injected_fields: Optional[list[str]] = None
    """
    A list/tuple of field strings to inject into the base class.

    Examples:

    .. code-block:: python

        injected_fields = (
            'object_id: Optional[str] = Field(None, description="Unique UUID for each object")',
        )

    """
    imports: Optional[Union[list[Import], Imports]] = None
    """
    Additional imports to inject into generated module.

    Examples:

    .. code-block:: python

        from linkml.generators.pydanticgen.template import (
            ConditionalImport,
            ObjectImport,
            Import,
            Imports
        )

        imports = (Imports() +
            Import(module='sys') +
            Import(module='numpy', alias='np') +
            Import(module='pathlib', objects=[
                ObjectImport(name="Path"),
                ObjectImport(name="PurePath", alias="RenamedPurePath")
            ]) +
            ConditionalImport(
                module="typing",
                objects=[ObjectImport(name="Literal")],
                condition="sys.version_info >= (3, 8)",
                alternative=Import(
                    module="typing_extensions",
                    objects=[ObjectImport(name="Literal")]
                ),
            ).imports
        )

    becomes:

    .. code-block:: python

        import sys
        import numpy as np
        from pathlib import (
            Path,
            PurePath as RenamedPurePath
        )
        if sys.version_info >= (3, 8):
            from typing import Literal
        else:
            from typing_extensions import Literal

    """
    sort_imports: bool = True
    """
    Before returning from :meth:`.PydanticGenerator.render`, sort imports with :meth:`.Imports.sort`

    Default ``True``, but optional in case import order must be explicitly given,
    eg. to avoid circular import errors in complex generator subclasses.
    """
    metadata_mode: Union[MetadataMode, str, None] = MetadataMode.AUTO
    """
    How to include schema metadata in generated pydantic models.

    See :class:`.MetadataMode` for mode documentation
    """
    split: bool = False
    """
    Generate schema that import other schema as separate python modules
    that import from one another, rather than rolling all into a single
    module (default, ``False``).
    """
    split_pattern: str = ".{{ schema.name }}"
    """
    When splitting generation, imported modules need to be generated separately
    and placed in a python package and import from each other. Since the
    location of those imported modules is variable -- e.g. one might want to
    generate schema in multiple packages depending on their version -- this
    pattern is used to generate the module portion of the import statement.

    These patterns should generally yield a relative module import,
    since functions like :func:`.generate_split` will generate and write files
    relative to some base file, though this is not a requirement since custom
    split generation logic is also allowed.

    The pattern is a jinja template string that is given the ``SchemaDefinition``
    of the imported schema in the environment. Additional variables can be passed
    into the jinja environment with the :attr:`.split_context` argument.

    Further modification is possible by using jinja filters.

    After templating, the string is passed through a :attr:`SNAKE_CASE` pattern
    to replace whitespace and other characters that can't be used in module names.

    See also :meth:`.generate_module_import`, which is used to generate the
    module portion of the import statement (and can be overridden in subclasses).

    Examples:

        for a schema named ``ExampleSchema`` and version ``1.2.3`` ...

        ``".{{ schema.name }}"`` (the default) becomes

        ``from .example_schema import ClassA, ...``

        ``"...{{ schema.name }}.v{{ schema.version | replace('.', '_') }}"`` becomes

        ``from ...example_schema.v1_2_3 import ClassA, ...``

    """
    split_context: Optional[dict] = None
    """
    Additional variables to pass into ``split_pattern`` when
    generating imported module names.

    Passed in as ``**kwargs`` , so e.g. if ``split_context = {'myval': 1}``
    then one would use it in a template string like ``{{ myval }}``
    """
    split_mode: SplitMode = SplitMode.AUTO
    """
    How to filter imports from imported schema.

    See :class:`.SplitMode` for description of options
    """

    # ObjectVars (identical to pythongen)
    gen_classvars: bool = True
    gen_slots: bool = True
    genmeta: bool = False
    emit_metadata: bool = True

    # ClassVars
    SNAKE_CASE: ClassVar[str] = r"(((?<!^)(?<!\.))(?=[A-Z][a-z]))|([^\w\.]+)"
    """Substitute CamelCase and non-word characters with _"""

    # Private attributes
    _predefined_slot_values: Optional[dict[str, dict[str, str]]] = None
    _class_bases: Optional[dict[str, list[str]]] = None

    def __post_init__(self):
        super().__post_init__()

    def compile_module(self, **kwargs) -> ModuleType:
        """
        Compiles generated python code to a module
        :return:
        """
        pycode = self.serialize(**kwargs)
        try:
            return compile_python(pycode)
        except NameError as e:
            logger.error(f"Code:\n{pycode}")
            logger.error(f"Error compiling generated python code: {e}")
            raise e

    def _get_classes(self, sv: SchemaView) -> tuple[list[ClassDefinition], Optional[list[ClassDefinition]]]:
        all_classes = sv.all_classes(imports=True).values()

        if self.split:
            local_classes = sv.all_classes(imports=False).values()
            imported_classes = [c for c in all_classes if c not in local_classes]
            return list(local_classes), imported_classes
        else:
            return list(all_classes), None

    @staticmethod
    def sort_classes(
        clist: list[ClassDefinition], imported: Optional[list[ClassDefinition]] = None
    ) -> list[ClassDefinition]:
        """
        sort classes such that if C is a child of P then C appears after P in the list

        Overridden method include mixin classes

        TODO: This should move to SchemaView
        """
        if imported is not None:
            imported = [i.name for i in imported]

        clist = list(clist)
        slist = []  # sorted
        while len(clist) > 0:
            can_add = False
            for i in range(len(clist)):
                candidate = clist[i]
                can_add = False
                if candidate.is_a:
                    candidates = [candidate.is_a] + candidate.mixins
                else:
                    candidates = candidate.mixins

                # remove blocking classes imported from other schemas if in split mode
                if imported:
                    candidates = [c for c in candidates if c not in imported]

                if not candidates:
                    can_add = True
                else:
                    if set(candidates) <= set([p.name for p in slist]):
                        can_add = True
                if can_add:
                    slist = slist + [candidate]
                    del clist[i]
                    break
            if not can_add:
                raise ValueError(f"could not find suitable element in {clist} that does not ref {slist}")
        return slist

    def generate_class(self, cls: ClassDefinition) -> ClassResult:
        pyclass = PydanticClass(
            name=camelcase(cls.name),
            bases=self.class_bases.get(camelcase(cls.name), PydanticBaseModel.default_name),
            description=cls.description.replace('"', '\\"') if cls.description is not None else None,
        )

        imports = self._get_imports(cls) if self.split else None

        result = ClassResult(cls=pyclass, source=cls, imports=imports)

        # Gather slots
        slots = [self.schemaview.induced_slot(sn, cls.name) for sn in self.schemaview.class_slots(cls.name)]
        slots = self.before_generate_slots(slots, self.schemaview)

        slot_results = []
        for slot in slots:
            slot = self.before_generate_slot(slot, self.schemaview)
            slot = self.generate_slot(slot, cls)
            slot = self.after_generate_slot(slot, self.schemaview)
            slot_results.append(slot)
            result = result.merge(slot)

        slot_results = self.after_generate_slots(slot_results, self.schemaview)
        attributes = {slot.attribute.name: slot.attribute for slot in slot_results}

        result.cls.attributes = attributes
        result.cls = self.include_metadata(result.cls, cls)

        return result

    def generate_slot(self, slot: SlotDefinition, cls: ClassDefinition) -> SlotResult:
        slot_args = {
            k: getattr(slot, k, None)
            for k in PydanticAttribute.model_fields.keys()
            if getattr(slot, k, None) is not None
        }
        slot_alias = slot.alias if slot.alias else slot.name
        slot_args["name"] = underscore(slot_alias)
        slot_args["description"] = slot.description.replace('"', '\\"') if slot.description is not None else None
        predef = self.predefined_slot_values.get(camelcase(cls.name), {}).get(slot.name, None)
        if predef is not None:
            slot_args["predefined"] = str(predef)

        pyslot = PydanticAttribute(**slot_args)
        pyslot = self.include_metadata(pyslot, slot)

        slot_ranges = []
        # Confirm that the original slot range (ignoring the default that comes in from
        # induced_slot) isn't in addition to setting any_of
        any_of_ranges = [a.range if a.range else slot.range for a in slot.any_of]
        if any_of_ranges:
            # list comprehension here is pulling ranges from within AnonymousSlotExpression
            slot_ranges.extend(any_of_ranges)
        else:
            slot_ranges.append(slot.range)

        pyranges = [self.generate_python_range(slot_range, slot, cls) for slot_range in slot_ranges]

        pyranges = list(set(pyranges))  # remove duplicates
        pyranges.sort()

        if len(pyranges) == 1:
            pyrange = pyranges[0]
        elif len(pyranges) > 1:
            pyrange = f"Union[{', '.join(pyranges)}]"
        else:
            raise Exception(f"Could not generate python range for {cls.name}.{slot.name}")

        pyslot.range = pyrange

        imports = self._get_imports(slot) if self.split else None

        result = SlotResult(attribute=pyslot, source=slot, imports=imports)

        if slot.array is not None:
            results = self.get_array_representations_range(slot, result.attribute.range)
            if len(results) == 1:
                result.attribute.range = results[0].range
            else:
                result.attribute.range = f"Union[{', '.join([res.range for res in results])}]"
            for res in results:
                result = result.merge(res)

        elif slot.multivalued:
            if slot.inlined or slot.inlined_as_list:
                collection_key = self.generate_collection_key(slot_ranges, slot, cls)
            else:
                collection_key = None
            if slot.inlined is False or collection_key is None or slot.inlined_as_list is True:
                result.attribute.range = f"list[{result.attribute.range}]"
            else:
                simple_dict_value = None
                if len(slot_ranges) == 1:
                    simple_dict_value = self._inline_as_simple_dict_with_value(slot)
                if simple_dict_value:
                    # simple_dict_value might be the range of the identifier of a class when range is a class,
                    # so we specify either that identifier or the range itself
                    if simple_dict_value != result.attribute.range:
                        simple_dict_value = f"Union[{simple_dict_value}, {result.attribute.range}]"
                    result.attribute.range = f"dict[str, {simple_dict_value}]"
                else:
                    result.attribute.range = f"dict[{collection_key}, {result.attribute.range}]"
        if not (slot.required or slot.identifier or slot.key) and not slot.designates_type:
            result.attribute.range = f"Optional[{result.attribute.range}]"
        return result

    @property
    def predefined_slot_values(self) -> dict[str, dict[str, str]]:
        """
        :return: Dictionary of dictionaries with predefined slot values for each class
        """
        if self._predefined_slot_values is None:
            sv = self.schemaview
            ifabsent_processor = PythonIfAbsentProcessor(sv)
            slot_values = defaultdict(dict)
            for class_def in sv.all_classes().values():
                for slot_name in sv.class_slots(class_def.name):
                    slot = sv.induced_slot(slot_name, class_def.name)
                    if slot.designates_type:
                        target_value = get_type_designator_value(sv, slot, class_def)
                        slot_values[camelcase(class_def.name)][slot.name] = f'"{target_value}"'
                        if slot.multivalued:
                            slot_values[camelcase(class_def.name)][slot.name] = (
                                "[" + slot_values[camelcase(class_def.name)][slot.name] + "]"
                            )
                        slot_values[camelcase(class_def.name)][slot.name] = slot_values[camelcase(class_def.name)][
                            slot.name
                        ]
                    elif slot.ifabsent is not None:
                        value = ifabsent_processor.process_slot(slot, class_def)
                        slot_values[camelcase(class_def.name)][slot.name] = value

                self._predefined_slot_values = slot_values

        return self._predefined_slot_values

    @property
    def class_bases(self) -> dict[str, list[str]]:
        """
        Generate the inheritance list for each class from is_a plus mixins
        :return:
        """
        if self._class_bases is None:
            sv = self.schemaview
            parents = {}
            for class_def in sv.all_classes().values():
                class_parents = []
                if class_def.is_a:
                    class_parents.append(camelcase(class_def.is_a))
                if self.gen_mixin_inheritance and class_def.mixins:
                    class_parents.extend([camelcase(mixin) for mixin in class_def.mixins])
                if len(class_parents) > 0:
                    # Use the sorted list of classes to order the parent classes, but reversed to match MRO needs
                    class_parents.sort(
                        key=lambda x: self.sorted_class_names.index(x) if x in self.sorted_class_names else -1
                    )
                    class_parents.reverse()
                    parents[camelcase(class_def.name)] = class_parents
            self._class_bases = parents
        return self._class_bases

    def get_mixin_identifier_range(self, mixin) -> str:
        sv = self.schemaview
        id_ranges = list(
            {
                _get_pyrange(sv.get_type(sv.get_identifier_slot(c).range), sv)
                for c in sv.class_descendants(mixin.name, mixins=True)
                if sv.get_identifier_slot(c) is not None
            }
        )
        if len(id_ranges) == 0:
            return None
        elif len(id_ranges) == 1:
            return id_ranges[0]
        else:
            return f"Union[{'.'.join(id_ranges)}]"

    def get_class_slot_range(self, slot_range: str, inlined: bool, inlined_as_list: bool) -> str:
        sv = self.schemaview
        range_cls = sv.get_class(slot_range)

        # Hardcoded handling for Any
        if range_cls.class_uri == "linkml:Any":
            return "Any"

        # Inline the class itself only if the class is defined as inline, or if the class has no
        # identifier slot and also isn't a mixin.
        if (
            inlined
            or inlined_as_list
            or (sv.get_identifier_slot(range_cls.name, use_key=True) is None and not sv.is_mixin(range_cls.name))
        ):
            if (
                len([x for x in sv.class_induced_slots(slot_range) if x.designates_type]) > 0
                and len(sv.class_descendants(slot_range)) > 1
            ):
                return "Union[" + ",".join([camelcase(c) for c in sv.class_descendants(slot_range)]) + "]"
            else:
                return f"{camelcase(slot_range)}"

        # For the more difficult cases, set string as the default and attempt to improve it
        range_cls_identifier_slot_range = "str"

        # For mixins, try to use the identifier slot of descendant classes
        if self.gen_mixin_inheritance and sv.is_mixin(range_cls.name) and sv.get_identifier_slot(range_cls.name):
            range_cls_identifier_slot_range = self.get_mixin_identifier_range(range_cls)

        # If the class itself has an identifier slot, it can be allowed to overwrite a value from mixin above
        if (
            sv.get_identifier_slot(range_cls.name) is not None
            and sv.get_identifier_slot(range_cls.name).range is not None
        ):
            range_cls_identifier_slot_range = _get_pyrange(
                sv.get_type(sv.get_identifier_slot(range_cls.name).range), sv
            )

        return range_cls_identifier_slot_range

    def generate_python_range(self, slot_range, slot_def: SlotDefinition, class_def: ClassDefinition) -> str:
        """
        Generate the python range for a slot range value
        """
        sv = self.schemaview

        if slot_def.designates_type:
            pyrange = (
                "Literal["
                + ",".join(['"' + x + '"' for x in get_accepted_type_designator_values(sv, slot_def, class_def)])
                + "]"
            )
        elif slot_def.equals_string:
            pyrange = f'Literal["{slot_def.equals_string}"]'
        elif slot_def.equals_string_in:
            pyrange = "Literal[" + ", ".join([f'"{a_string}"' for a_string in slot_def.equals_string_in]) + "]"
        elif slot_range in sv.all_classes():
            pyrange = self.get_class_slot_range(
                slot_range,
                inlined=slot_def.inlined,
                inlined_as_list=slot_def.inlined_as_list,
            )
        elif slot_range in sv.all_enums():
            pyrange = f"{camelcase(slot_range)}"
        elif slot_range in sv.all_types():
            t = sv.get_type(slot_range)
            pyrange = _get_pyrange(t, sv)
        elif slot_range is None:
            pyrange = "str"
        else:
            # TODO: default ranges in schemagen
            # pyrange = 'str'
            # logger.error(f'range: {s.range} is unknown')
            raise Exception(f"range: {slot_range}")
        return pyrange

    def generate_collection_key(
        self,
        slot_ranges: list[str],
        slot_def: SlotDefinition,
        class_def: ClassDefinition,
    ) -> Optional[str]:
        """
        Find the python range value (str, int, etc) for the identifier slot
        of a class used as a slot range.

        If a pyrange value matches a class name, the range of the identifier slot
        will be returned. If more than one match is found and they don't match,
        an exception will be raised.

        :param slot_ranges: list of python range values
        """

        collection_keys: set[str] = set()

        if slot_ranges is None:
            return None

        for slot_range in slot_ranges:
            if slot_range is None or slot_range not in self.schemaview.all_classes():
                continue  # ignore non-class ranges

            identifier_slot = self.schemaview.get_identifier_slot(slot_range, use_key=True)
            if identifier_slot is not None:
                collection_keys.add(self.generate_python_range(identifier_slot.range, slot_def, class_def))
        if len(collection_keys) > 1:
            raise Exception(f"Slot with any_of range has multiple identifier slot range types: {collection_keys}")
        if len(collection_keys) == 1:
            return list(collection_keys)[0]
        return None

    def _clean_injected_classes(self, injected_classes: list[Union[str, type]]) -> Optional[list[str]]:
        """Get source, deduplicate, and dedent injected classes"""
        if len(injected_classes) == 0:
            return None

        injected_classes = list(
            dict.fromkeys([c if isinstance(c, str) else inspect.getsource(c) for c in injected_classes])
        )
        injected_classes = [textwrap.dedent(c) for c in injected_classes]
        return injected_classes

    def _inline_as_simple_dict_with_value(self, slot_def: SlotDefinition) -> Optional[str]:
        """
        Determine if a slot should be inlined as a simple dict with a value.

        For example, if we have a class such as Prefix, with two slots prefix and expansion,
        then an inlined list of prefixes can be serialized as:

        .. code-block:: yaml

            prefixes:
                prefix1: expansion1
                prefix2: expansion2
                ...

        Provided that the prefix slot is the identifier slot for the Prefix class.

        TODO: move this to SchemaView

        :param slot_def: SlotDefinition
        :param sv: SchemaView
        :return: str
        """
        if slot_def.inlined and not slot_def.inlined_as_list:
            if slot_def.range in self.schemaview.all_classes():
                id_slot = self.schemaview.get_identifier_slot(slot_def.range, use_key=True)
                if id_slot is not None:
                    range_cls_slots = self.schemaview.class_induced_slots(slot_def.range)
                    if len(range_cls_slots) == 2:
                        non_id_slots = [slot for slot in range_cls_slots if slot.name != id_slot.name]
                        if len(non_id_slots) == 1:
                            value_slot = non_id_slots[0]
                            value_slot_range_type = self.schemaview.get_type(value_slot.range)
                            if value_slot_range_type is not None:
                                return _get_pyrange(value_slot_range_type, self.schemaview)
        return None

    def _template_environment(self) -> Environment:
        env = PydanticTemplateModel.environment()
        if self.template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
            env.loader = loader
        return env

    def get_array_representations_range(self, slot: SlotDefinition, range: str) -> list[SlotResult]:
        """
        Generate the python range for array representations
        """
        array_reps = []
        for repr in self.array_representations:
            generator = ArrayRangeGenerator.get_generator(repr)
            result = generator(slot.array, range).make()
            array_reps.append(result)

        if len(array_reps) == 0:
            raise ValueError("No array representation generated, but one was requested!")

        return array_reps

    @overload
    def include_metadata(self, model: PydanticModule, source: SchemaDefinition) -> PydanticModule: ...

    @overload
    def include_metadata(self, model: PydanticClass, source: ClassDefinition) -> PydanticClass: ...

    @overload
    def include_metadata(self, model: PydanticAttribute, source: SlotDefinition) -> PydanticAttribute: ...

    def include_metadata(self, model: TemplateType, source: DefinitionType) -> TemplateType:
        """
        Include metadata from the source schema that is otherwise not represented in the pydantic template models.

        Metadata inclusion mode is dependent on :attr:`.metadata_mode` - see:

        - :class:`.MetadataMode`
        - :meth:`.PydanticTemplateModel.exclude_from_meta`

        """
        if self.metadata_mode is None or self.metadata_mode == MetadataMode.NONE:
            return model
        elif self.metadata_mode in (MetadataMode.AUTO, MetadataMode.AUTO.value):
            meta = {k: v for k, v in remove_empty_items(source).items() if k not in model.exclude_from_meta()}
        elif self.metadata_mode in (MetadataMode.EXCEPT_CHILDREN, MetadataMode.EXCEPT_CHILDREN.value):
            meta = {}
            for k, v in remove_empty_items(source).items():
                if k in ("slots", "classes") and isinstance(model, PydanticModule):
                    # FIXME: Special-case removal of slots until we generate class-level slots
                    continue

                if not hasattr(model, k):
                    meta[k] = v
                    continue

                model_attr = getattr(model, k)
                if isinstance(model_attr, list) and not any(
                    [isinstance(item, PydanticTemplateModel) for item in model_attr]
                ):
                    meta[k] = v
                elif isinstance(model_attr, dict) and not any(
                    [isinstance(item, PydanticTemplateModel) for item in model_attr.values()]
                ):
                    meta[k] = v
                elif not isinstance(model_attr, (list, dict, PydanticTemplateModel)):
                    meta[k] = v

        elif self.metadata_mode in (MetadataMode.FULL, MetadataMode.FULL.value):
            meta = remove_empty_items(source)
        else:
            raise ValueError(
                f"Unknown metadata mode '{self.metadata_mode}', needs to be one of "
                f"{[mode for mode in MetadataMode]}"
            )

        model.meta = meta
        return model

    def _get_imports(self, element: Union[ClassDefinition, SlotDefinition, None] = None) -> Imports:
        """
        Get imports that are implied by their usage in slots or classes
        (and thus need to be imported when generating schemas in :attr:`.split` == ``True`` mode).

        **Note:**
        Since in pydantic (currently) the only things that are materialized are classes, we don't
        import class slots from imported schemas and abandon slots, directly expressing them
        in the model.

        This is a parent placeholder method in case that changes, "give me something and return
        a set of imports" that calls subordinate methods. If slots become materialized, keep
        this as the directly called method rather than spaghetti-ing out another
        independent method. This method is also isolated in anticipation of structured imports,
        where we will need to revise our expectations of what is imported when.

        Args:
            element (:class:`.ClassDefinition` , :class:`.SlotDefinition` , None): The element
                to get import for. If ``None`` , get all needed imports (see :attr:`.split_mode`
        """
        # import from local references, rather than serializing every class in every file
        if not self.split or (self.split_mode == SplitMode.FULL and element is not None):
            # we are either compiling this whole thing in one big file (default)
            # or going to import all classes from the imported schemas,
            # so we don't import anything
            return Imports()

        # gather a list of class names,
        # remove local classes and transform to Imports later.
        needed_classes = []

        # fine to call rather than pass bc it's cached
        all_classes = self.schemaview.all_classes(imports=True)
        local_classes = self.schemaview.all_classes(imports=False)

        if isinstance(element, ClassDefinition):
            if element.is_a:
                needed_classes.append(element.is_a)
            if element.mixins:
                needed_classes.extend(element.mixins)

        elif isinstance(element, SlotDefinition):
            # collapses `slot.range`, `slot.any_of`, and `slot.one_of` to a list
            slot_ranges = self.schemaview.slot_range_as_union(element)
            needed_classes.extend([a_range for a_range in slot_ranges if a_range in all_classes])

        elif element is None:
            # get all imports
            needed_classes.extend([cls for cls in all_classes if cls not in local_classes])

        else:
            raise ValueError(f"Unsupported type of element to get imports from: f{type(element)}")

        # SPECIAL CASE: classes that are not generated for structural reasons.
        # TODO: Do we want to have a general means of skipping class generation?
        skips = ("AnyType",)

        class_imports = [
            self._get_element_import(cls) for cls in needed_classes if (cls not in local_classes and cls not in skips)
        ]
        imports = Imports(imports=class_imports)

        return imports

    def generate_module_import(self, schema: SchemaDefinition, context: Optional[dict] = None) -> str:
        """
        Generate the module string for importing from python modules generated from imported schemas
        when in :attr:`.split` mode.

        Use the :attr:`.split_pattern` as a jinja template rendered with the :class:`.SchemaDefinition`
        and any passed ``context``. Apply the :attr:`.SNAKE_CASE` regex to substitute matches with
        ``_`` and ensure lowercase.
        """
        if context is None:
            context = {}
        module = Template(self.split_pattern).render(schema=schema, **context)
        module = re.sub(self.SNAKE_CASE, "_", module) if self.SNAKE_CASE else module
        module = module.lower()
        return module

    def _get_element_import(self, class_name: ElementName) -> Import:
        """
        Make an import object for an element from another schema, using the
        :attr:`.split_import_pattern` to generate the module import part.
        """
        schema_name = self.schemaview.element_by_schema_map()[class_name]
        schema = [s for s in self.schemaview.schema_map.values() if s.name == schema_name][0]
        module = self.generate_module_import(schema, self.split_context)
        return Import(module=module, objects=[ObjectImport(name=camelcase(class_name))], is_schema=True)

    def render(self) -> PydanticModule:
        """
        Render the schema to a :class:`PydanticModule` model
        """
        sv: SchemaView
        sv = self.schemaview

        # imports
        imports = DEFAULT_IMPORTS
        if self.imports is not None:
            if isinstance(self.imports, Imports):
                imports += self.imports
            else:
                for i in self.imports:
                    imports += i
        if self.split_mode == SplitMode.FULL:
            imports += self._get_imports()

        # injected classes
        injected_classes = DEFAULT_INJECTS.copy()
        if self.injected_classes is not None:
            injected_classes += self.injected_classes.copy()

        # enums
        enums = self.before_generate_enums(list(sv.all_enums().values()), sv)
        enums = self.generate_enums({e.name: e for e in enums})

        base_model = PydanticBaseModel(extra_fields=self.extra_fields, fields=self.injected_fields)

        # schema classes
        class_results = []
        source_classes, imported_classes = self._get_classes(sv)
        source_classes = self.sort_classes(source_classes, imported_classes)
        # Don't want to generate classes when class_uri is linkml:Any, will
        # just swap in typing.Any instead down below
        source_classes = [c for c in source_classes if c.class_uri != "linkml:Any"]
        source_classes = self.before_generate_classes(source_classes, sv)
        self.sorted_class_names = [camelcase(c.name) for c in source_classes]
        for cls in source_classes:
            cls = self.before_generate_class(cls, sv)
            result = self.generate_class(cls)
            result = self.after_generate_class(result, sv)
            class_results.append(result)
            if result.imports is not None:
                imports += result.imports
            if result.injected_classes is not None:
                injected_classes.extend(result.injected_classes)

        class_results = self.after_generate_classes(class_results, sv)

        classes = {r.cls.name: r.cls for r in class_results}
        injected_classes = self._clean_injected_classes(injected_classes)

        imports.render_sorted = self.sort_imports

        module = PydanticModule(
            metamodel_version=self.schema.metamodel_version,
            version=self.schema.version,
            python_imports=imports,
            base_model=base_model,
            injected_classes=injected_classes,
            enums=enums,
            classes=classes,
        )
        module = self.include_metadata(module, self.schemaview.schema)
        module = self.before_render_template(module, self.schemaview)
        return module

    def serialize(self, rendered_module: Optional[PydanticModule] = None) -> str:
        """
        Serialize the schema to a pydantic module as a string

        Args:
            rendered_module ( :class:`.PydanticModule` ): Optional, if schema was previously
                rendered with :meth:`~.PydanticGenerator.render` , use that,
                otherwise :meth:`~.PydanticGenerator.render` fresh.
        """
        if rendered_module is not None:
            module = rendered_module
        else:
            module = self.render()
        serialized = module.render(self._template_environment(), self.black)
        serialized = self.after_render_template(serialized, self.schemaview)
        return serialized

    def default_value_for_type(self, typ: str) -> str:
        return "None"

    @classmethod
    def generate_split(
        cls,
        schema: Union[str, Path, SchemaDefinition],
        output_path: Union[str, Path] = Path("."),
        split_pattern: Optional[str] = None,
        split_context: Optional[dict] = None,
        split_mode: SplitMode = SplitMode.AUTO,
        **kwargs,
    ) -> list[SplitResult]:
        """
        Generate a schema that imports from other schema as a set of python modules that
        import from one another, rather than generating all imported classes in a single schema.

        Uses ``output_path`` for the main schema from ``schema`` , and then
        generates any imported schema (from which classes are actually used)
        to modules whose locations are determined by the module names generated
        by the ``split_pattern`` (see :attr:`.PydanticGenerator.split_pattern` ).

        For example, for

        * a ``output_path`` of ``my_dir/v1_2_3/main.py``
        * a schema ``main`` with a version ``v1.2.3``
        * that imports from ``s2`` with version ``v4.5.6``,
        * and a ``split_pattern`` of ``..{{ schema.version | replace('.', '_') }}.{{ schema.name }}``

        One would get:
        * ``my_dir/v1_2_3/main.py`` , as expected
        * that imports ``from ..v4_5_6.s2``
        * a module at ``my_dir/v4_5_6/s2.py``

        ``__init__.py`` files are generated for any directories that are between
        the generated modules and their highest common directory.

        Args:
            schema (str, :class:`.Path` , :class:`.SchemaDefinition` ): Main schema to generate
            output_path (str, :class:`.Path` ): Python ``.py`` module to generate main schema to
            split_pattern (str): Pattern to use to generate module names, see :attr:`.PydanticGenerator.split_pattern`
            split_context (dict): Additional variables to pass into jinja context when generating module import names.

        Returns:
            list[:class:`.SplitResult`]
        """
        output_path = Path(output_path)
        if not output_path.suffix == ".py":
            raise ValueError(f"output path must be a python file to write the main schema to, got {output_path}")

        results = []

        # --------------------------------------------------
        # Main schema
        # --------------------------------------------------
        gen_kwargs = kwargs
        gen_kwargs.update(
            {"split": True, "split_pattern": split_pattern, "split_context": split_context, "split_mode": split_mode}
        )
        generator = cls(schema, **gen_kwargs)
        # Generate the initial schema to figure out which of the imported schema actually need
        # to be generated
        rendered = generator.render()
        # write schema - we use the ``output_path`` for the main schema, and then
        # interpret all imported schema paths as relative to that
        output_path.parent.mkdir(parents=True, exist_ok=True)
        serialized = generator.serialize(rendered_module=rendered)
        with open(output_path, "w", encoding="utf-8") as ofile:
            ofile.write(serialized)

        results.append(
            SplitResult(main=True, source=generator.schemaview.schema, path=output_path, serialized_module=serialized)
        )

        # --------------------------------------------------
        # Imported schemas
        # --------------------------------------------------
        imported_schema = {
            generator.generate_module_import(sch): sch for sch in generator.schemaview.schema_map.values()
        }
        for generated_import in [i for i in rendered.python_imports if i.is_schema]:
            import_generator = cls(imported_schema[generated_import.module], **gen_kwargs)
            serialized = import_generator.serialize()
            rel_path = _import_to_path(generated_import.module)
            abs_path = (output_path.parent / rel_path).resolve()
            abs_path.parent.mkdir(parents=True, exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as ofile:
                ofile.write(serialized)

            results.append(
                SplitResult(
                    main=False,
                    source=imported_schema[generated_import.module],
                    path=abs_path,
                    serialized_module=serialized,
                    module_import=generated_import.module,
                )
            )

        _ensure_inits([r.path for r in results])
        return results


def _subclasses(cls: type):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in _subclasses(c)])


_TEMPLATE_NAMES = sorted(list(set([c.template for c in _subclasses(PydanticTemplateModel)])))


def _import_to_path(module: str) -> Path:
    """Make a (relative) ``Path`` object from a python module import string"""
    # handle leading .'s separately..
    _, dots, module = re.split(r"(^\.*)(?=\w)", module, maxsplit=1)
    # treat zero or one dots as a relative import to the current directory
    dir_pieces = ["../" for _ in range(max(len(dots) - 1, 0))]
    dir_pieces.extend(module.split("."))
    dir_pieces[-1] = dir_pieces[-1] + ".py"
    return Path(*dir_pieces)


def _ensure_inits(paths: list[Path]):
    """For a set of paths, find the common root and it and all the subdirectories have an __init__.py"""
    # if there is only one file, there is no relative importing to be done
    if len(paths) <= 1:
        return
    common_path = Path(os.path.commonpath(paths))

    if not (ipath := (common_path / "__init__.py")).exists():
        with open(ipath, "w", encoding="utf-8") as ifile:
            ifile.write(" \n")

    for path in paths:
        # ensure __init__ for each directory from this path up to the common path
        path = path.parent
        while path != common_path:
            if not (ipath := (path / "__init__.py")).exists():
                with open(ipath, "w", encoding="utf-8") as ifile:
                    ifile.write(" \n")
            path = path.parent


@shared_arguments(PydanticGenerator)
@click.option("--template-file", hidden=True)
@click.option(
    "--template-dir",
    type=click.Path(),
    help="""
Optional jinja2 template directory to use for class generation.

Pass a directory containing templates with the same name as any of the default
:class:`.PydanticTemplateModel` templates to override them. The given directory will be
searched for matching templates, and use the default templates as a fallback
if an override is not found

Available templates to override:

\b
"""
    + "\n".join(["- " + name for name in _TEMPLATE_NAMES]),
)
@click.option(
    "--array-representations",
    type=click.Choice([k.value for k in ArrayRepresentation]),
    multiple=True,
    default=["list"],
    help="List of array representations to accept for array slots. Default is list of lists.",
)
@click.option(
    "--extra-fields",
    type=click.Choice(["allow", "ignore", "forbid"], case_sensitive=False),
    default="forbid",
    help="How to handle extra fields in BaseModel.",
)
@click.option(
    "--black",
    is_flag=True,
    default=False,
    help="Format generated models with black (must be present in the environment)",
)
@click.option(
    "--meta",
    type=click.Choice([k for k in MetadataMode]),
    default="auto",
    help="How to include linkml schema metadata in generated pydantic classes. "
    "See docs for MetadataMode for full description of choices. "
    "Default (auto) is to include all metadata that can't be otherwise represented",
)
@click.version_option(__version__, "-V", "--version")
@click.command(name="pydantic")
def cli(
    yamlfile,
    template_file=None,
    template_dir: Optional[str] = None,
    head=True,
    genmeta=False,
    classvars=True,
    slots=True,
    array_representations=list("list"),
    extra_fields: Literal["allow", "forbid", "ignore"] = "forbid",
    black: bool = False,
    meta: MetadataMode = "auto",
    **args,
):
    """Generate pydantic classes to represent a LinkML model"""
    if template_file is not None:
        raise DeprecationWarning(
            "Passing a single template_file is deprecated. Pass a directory of template files instead. "
            "See help string for --template-dir"
        )

    if template_dir is not None:
        if not Path(template_dir).exists():
            raise FileNotFoundError(f"The template directory {template_dir} does not exist!")

    gen = PydanticGenerator(
        yamlfile,
        array_representations=[ArrayRepresentation(x) for x in array_representations],
        extra_fields=extra_fields,
        emit_metadata=head,
        genmeta=genmeta,
        gen_classvars=classvars,
        gen_slots=slots,
        template_dir=template_dir,
        black=black,
        metadata_mode=meta,
        **args,
    )
    print(gen.serialize())


if __name__ == "__main__":
    cli()
