# Auto generated from model.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-09-15T09:31:45
# Schema: conformance
#
# id: https://w3id.org/linkml/conformance/
# description: Schema describing the generic conformance tests for LinkML runtimes, tools, and generators.
#   Implementations of this conformance tests are expected to load instances of classes described here and implement
#   handling for the described actions and assertions generically, which allows the test suite to be decoupled from any
#   specific LinkML implementation.
#
# license: https://creativecommons.org/publicdomain/zero/1.0/
#
# This file has been formatted and lint-fixed with ruff, so it is not byte-identical
# to raw gen-python output. After regenerating it, re-run `uv run tox -e lint` to
# reapply formatting before committing.

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

from jsonasobj2 import as_dict
from rdflib import URIRef

from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.metamodelcore import empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str

metamodel_version = "1.11.0"
version = None

# Namespaces
CONFORMANCE = CurieNamespace("conformance", "https://w3id.org/linkml/conformance/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = CONFORMANCE


# Types


# Class references
class ManifestName(extended_str):
    pass


class TestName(extended_str):
    pass


Any = Any


@dataclass(repr=False)
class Manifest(YAMLRoot):
    """
    A test manifest representing a grouping of related tests
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["Manifest"]
    class_class_curie: ClassVar[str] = "conformance:Manifest"
    class_name: ClassVar[str] = "Manifest"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.Manifest

    name: str | ManifestName = None
    title: str | None = None
    description: str | None = None
    entries: dict[str | TestName, Union[dict, "Test"]] | list[Union[dict, "Test"]] | None = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, ManifestName):
            self.name = ManifestName(self.name)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_dict(slot_name="entries", slot_type=Test, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Test(YAMLRoot):
    """
    A single test consisting of a schema, action, and assertion
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["Test"]
    class_class_curie: ClassVar[str] = "conformance:Test"
    class_name: ClassVar[str] = "Test"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.Test

    name: str | TestName = None
    action: Union[dict, "Action"] = None
    assertion: Union[dict, "Assertion"] = None
    schema: str = None
    title: str | None = None
    description: str | None = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, TestName):
            self.name = TestName(self.name)

        if self._is_empty(self.action):
            self.MissingRequiredField("action")
        if not isinstance(self.action, Action):
            self.action = Action(**as_dict(self.action))

        if self._is_empty(self.assertion):
            self.MissingRequiredField("assertion")
        if not isinstance(self.assertion, Assertion):
            self.assertion = Assertion(**as_dict(self.assertion))

        if self._is_empty(self.schema):
            self.MissingRequiredField("schema")
        if not isinstance(self.schema, str):
            self.schema = str(self.schema)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Action(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["Action"]
    class_class_curie: ClassVar[str] = "conformance:Action"
    class_name: ClassVar[str] = "Action"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.Action

    type: str | None = None
    title: str | None = None
    description: str | None = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        type_designator = "type"
        if type_designator not in kwargs:
            return super().__new__(cls, *args, **kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)

            if target_cls is None:
                raise ValueError(
                    f"Wrong type designator value: class {cls.__name__} "
                    f"has no subclass with ['class_name']='{kwargs[type_designator]}'"
                )
            return super().__new__(target_cls, *args, **kwargs)


@dataclass(repr=False)
class Assertion(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["Assertion"]
    class_class_curie: ClassVar[str] = "conformance:Assertion"
    class_name: ClassVar[str] = "Assertion"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.Assertion

    type: str | None = None
    title: str | None = None
    description: str | None = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self.type = str(self.class_name)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        type_designator = "type"
        if type_designator not in kwargs:
            return super().__new__(cls, *args, **kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_name", type_designator_value)

            if target_cls is None:
                raise ValueError(
                    f"Wrong type designator value: class {cls.__name__} "
                    f"has no subclass with ['class_name']='{kwargs[type_designator]}'"
                )
            return super().__new__(target_cls, *args, **kwargs)


class LoadAction(Action):
    """
    The implementation should load the schema into a string and pass it as the Action result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["LoadAction"]
    class_class_curie: ClassVar[str] = "conformance:LoadAction"
    class_name: ClassVar[str] = "LoadAction"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.LoadAction

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


class DeriveAction(Action):
    """
    The implementation should run the schema derivation procedure as defined in the specification,
    serialize the derived schema, and pass the serialized schema as the Action result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["DeriveAction"]
    class_class_curie: ClassVar[str] = "conformance:DeriveAction"
    class_name: ClassVar[str] = "DeriveAction"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.DeriveAction

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


class LintAction(Action):
    """
    The implementation should run a schema quality analyzer on the specified schema and report any issues found.
    The human-readable output of such a analyzer should be passed as the Action result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["LintAction"]
    class_class_curie: ClassVar[str] = "conformance:LintAction"
    class_name: ClassVar[str] = "LintAction"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.LintAction

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


class GenerateAction(Action):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["GenerateAction"]
    class_class_curie: ClassVar[str] = "conformance:GenerateAction"
    class_name: ClassVar[str] = "GenerateAction"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.GenerateAction

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


class JsonSchemaGenerate(GenerateAction):
    """
    The implementation should use a JSON Schema generator if it has one, skipping the test if it does not.
    The generated JSON Schema should be passed as the Action result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["JsonSchemaGenerate"]
    class_class_curie: ClassVar[str] = "conformance:JsonSchemaGenerate"
    class_name: ClassVar[str] = "JsonSchemaGenerate"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.JsonSchemaGenerate

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


class LoadsAssertion(Assertion):
    """
    An implementation of this assertion must load the result of an Action into an appropriate internal data structure.
    Should the process fail, the assertion fails.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["LoadsAssertion"]
    class_class_curie: ClassVar[str] = "conformance:LoadsAssertion"
    class_name: ClassVar[str] = "LoadsAssertion"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.LoadsAssertion

    def __post_init__(self, *_: str, **kwargs: Any):
        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class StringAssertion(Assertion):
    """
    An implementation of this assertion must load the result of an Action as a string, then, for each value in
    'includes',
    it must check that the value is a substring of the result of an Action, failing if any of the strings are not
    present.
    Should 'includes' be empty, the assertion should pass.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["StringAssertion"]
    class_class_curie: ClassVar[str] = "conformance:StringAssertion"
    class_name: ClassVar[str] = "StringAssertion"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.StringAssertion

    includes: str | list[str] | None = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.includes, list):
            self.includes = [self.includes] if self.includes is not None else []
        self.includes = [v if isinstance(v, str) else str(v) for v in self.includes]

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class JsonPointerAssertion(Assertion):
    """
    An implementation of this assertion must load the result of an Action as a YAML document, and then dereference a
    JSON pointer provided in the 'path' attribute and compare it against the 'value'.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["JsonPointerAssertion"]
    class_class_curie: ClassVar[str] = "conformance:JsonPointerAssertion"
    class_name: ClassVar[str] = "JsonPointerAssertion"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.JsonPointerAssertion

    path: str = None
    value: dict | Any = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.path):
            self.MissingRequiredField("path")
        if not isinstance(self.path, str):
            self.path = str(self.path)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class JsonSchemaAccepts(Assertion):
    """
    An implementation of this assertion must load the result of an Action as a JSON Schema into a JSON Schema
    validator,
    fetch the instance from the specified file, and validate the instance using the validator. The validator should
    accept the instance and not report any issues with it.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["JsonSchemaAccepts"]
    class_class_curie: ClassVar[str] = "conformance:JsonSchemaAccepts"
    class_name: ClassVar[str] = "JsonSchemaAccepts"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.JsonSchemaAccepts

    instance: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.instance):
            self.MissingRequiredField("instance")
        if not isinstance(self.instance, str):
            self.instance = str(self.instance)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


@dataclass(repr=False)
class JsonSchemaRejects(Assertion):
    """
    An implementation of this assertion must load the result of an Action as a JSON Schema into a JSON Schema
    validator,
    fetch the instance from the specified file, and validate the instance using the validator. The validator should
    report a problem with the instance.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CONFORMANCE["JsonSchemaRejects"]
    class_class_curie: ClassVar[str] = "conformance:JsonSchemaRejects"
    class_name: ClassVar[str] = "JsonSchemaRejects"
    class_model_uri: ClassVar[URIRef] = CONFORMANCE.JsonSchemaRejects

    instance: str = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.instance):
            self.MissingRequiredField("instance")
        if not isinstance(self.instance, str):
            self.instance = str(self.instance)

        super().__post_init__(**kwargs)
        self.type = str(self.class_name)


# Enumerations


# Slots
class slots:
    pass


slots.type = Slot(
    uri=CONFORMANCE.type,
    name="type",
    curie=CONFORMANCE.curie("type"),
    model_uri=CONFORMANCE.type,
    domain=None,
    range=Optional[str],
)

slots.title = Slot(
    uri=CONFORMANCE.title,
    name="title",
    curie=CONFORMANCE.curie("title"),
    model_uri=CONFORMANCE.title,
    domain=None,
    range=Optional[str],
)

slots.description = Slot(
    uri=CONFORMANCE.description,
    name="description",
    curie=CONFORMANCE.curie("description"),
    model_uri=CONFORMANCE.description,
    domain=None,
    range=Optional[str],
)

slots.name = Slot(
    uri=CONFORMANCE.name,
    name="name",
    curie=CONFORMANCE.curie("name"),
    model_uri=CONFORMANCE.name,
    domain=None,
    range=URIRef,
)

slots.instance = Slot(
    uri=CONFORMANCE.instance,
    name="instance",
    curie=CONFORMANCE.curie("instance"),
    model_uri=CONFORMANCE.instance,
    domain=None,
    range=str,
)

slots.manifest__entries = Slot(
    uri=CONFORMANCE.entries,
    name="manifest__entries",
    curie=CONFORMANCE.curie("entries"),
    model_uri=CONFORMANCE.manifest__entries,
    domain=None,
    range=Optional[dict[str | TestName, dict | Test] | list[dict | Test]],
)

slots.test__action = Slot(
    uri=CONFORMANCE.action,
    name="test__action",
    curie=CONFORMANCE.curie("action"),
    model_uri=CONFORMANCE.test__action,
    domain=None,
    range=Union[dict, Action],
)

slots.test__assertion = Slot(
    uri=CONFORMANCE.assertion,
    name="test__assertion",
    curie=CONFORMANCE.curie("assertion"),
    model_uri=CONFORMANCE.test__assertion,
    domain=None,
    range=Union[dict, Assertion],
)

slots.test__schema = Slot(
    uri=CONFORMANCE.schema,
    name="test__schema",
    curie=CONFORMANCE.curie("schema"),
    model_uri=CONFORMANCE.test__schema,
    domain=None,
    range=str,
)

slots.stringAssertion__includes = Slot(
    uri=CONFORMANCE.includes,
    name="stringAssertion__includes",
    curie=CONFORMANCE.curie("includes"),
    model_uri=CONFORMANCE.stringAssertion__includes,
    domain=None,
    range=Optional[str | list[str]],
)

slots.jsonPointerAssertion__path = Slot(
    uri=CONFORMANCE.path,
    name="jsonPointerAssertion__path",
    curie=CONFORMANCE.curie("path"),
    model_uri=CONFORMANCE.jsonPointerAssertion__path,
    domain=None,
    range=str,
)

slots.jsonPointerAssertion__value = Slot(
    uri=CONFORMANCE.value,
    name="jsonPointerAssertion__value",
    curie=CONFORMANCE.curie("value"),
    model_uri=CONFORMANCE.jsonPointerAssertion__value,
    domain=None,
    range=Union[dict, Any],
)
