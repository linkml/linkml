import json
import unittest
import datetime
from datetime import datetime as datetime2
from collections import namedtuple
from dataclasses import dataclass, field
from decimal import Decimal
from io import StringIO
from pathlib import Path
from typing import Optional, Any, Union

import yaml

from linkml_runtime.dumpers import yaml_dumper, json_dumper
from linkml_runtime.linkml_model import SlotDefinition, SlotDefinitionName, PermissibleValue
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.processing.referencevalidator import (
    ReferenceValidator,
    Report,
    ConstraintType,
    CollectionForm,
)
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader


@dataclass
class MarkdownDocument:
    """
    Convenience class for generating markdown
    """

    writer: StringIO = field(default_factory=lambda: StringIO())

    def h1(self, header: str, text: Optional[str] = None):
        self.h("#", header, text)

    def h2(self, header: str, text: Optional[str] = None):
        self.h("##", header, text)

    def h3(self, header: str, text: Optional[str] = None):
        self.h("###", header, text)

    def h4(self, header: str, text: Optional[str] = None):
        self.h("####", header, text)

    def h(self, level: str, header: str, text: Optional[str] = None):
        self.w(f"\n{level} {header}\n\n")
        if text:
            self.w(f"{text}\n")

    def li(self, item: str):
        self.w(f" * {item}\n")

    def object(self, obj: Any):
        if isinstance(obj, dict):
            obj = yaml.dump(obj)
        self.w(f"```yaml\n{obj}\n```\n\n")

    def text(self, text: str):
        self.w(text)
        self.w("\n\n")

    def italics(self, text: str):
        self.text(f"_{text.replace('_', '-')}_")

    def w(self, text: str):
        self.writer.write(text)

    def th(self, cols: list[str]):
        self.w("\n")
        self.tr(cols)
        self.tr(["---" for _ in cols])

    def tr(self, cols: list[str]):
        self.w(f"|{'|'.join([str(c) for c in cols])}|\n")

    def __repr__(self) -> str:
        return self.writer.getvalue()


OUTPUT_DIRECTORY = Path(__file__).parent / "output" / "suite"
TEST_TIME = datetime.datetime(2023, 1, 21, 17, 24, 36, 385155)


def _add_core_schema_elements(
    sb: SchemaBuilder, test_slot: Optional[SlotDefinition] = None
):
    sb.add_slot("id", range="string", identifier=True)
    sb.add_class("Identified", slots=["id", "name", "description"])
    sb.add_class("NonIdentified", slots=["name", "description"])
    sb.add_class("Simple", slots=["id", "name"])
    if test_slot:
        sb.add_class("TestClass", slots=[test_slot])


METASLOTS = ["range", "multivalued", "inlined", "inlined_as_list"]


def _slot_metaslot_values(slot: SlotDefinition) -> list[Any]:
    return [
        slot.range or "string",
        slot.multivalued or False,
        slot.inlined or False,
        slot.inlined_as_list or False,
    ]


def _serialize(obj: Any) -> str:
    return json.dumps(obj)


def _normalizations(report: Report) -> str:
    return ", ".join(
        [
            f"{f1.value}->{f2.value}"
            for f1, f2 in report.collection_form_normalizations()
        ]
    )

def _errors(report: Report) -> str:
    return ", ".join(
        [
            f"{r.type}"
            for r in report.errors()
        ]
    )



class ReferenceValidatorTestCase(unittest.TestCase):
    """
    This unit test will run the core LinkML validation suite.

    This test is auto-documenting:

    A side-effect of running this test is a markdown file
    that generates a report of all inputs and outputs;
    this is to be copied back to the linkml-model repo where
    it resides as an appendix to the specification.
    """

    @classmethod
    def setUpClass(cls):
        """Class-level setup.

        Sets up a document object that each test will contribute to.
        """
        print("Setting up class...")
        doc = MarkdownDocument()
        doc.h1("Validation Suite")
        doc.text("This document describes the validation suite for the LinkML model.")
        doc.h2("Core schema")
        doc.text("Most tests use the core minimal test schema:")
        sb = SchemaBuilder()
        _add_core_schema_elements(sb)
        doc.object(yaml_dumper.dumps(sb.schema))
        doc.text("The 3 classes used here are to define different kinds of *references*:")
        doc.li("Identified: has an `identifier` slot (*referenced* rather than inlined)")
        doc.li("NonIdentified: does not have an `identifier` slot (*necessarily* inlined)")
        doc.li("Simple: has a single non-identifier slot which is atomic (default *CompactDict* form)")
        cls.doc = doc

    def setUp(self) -> None:
        OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Write out the document object to a markdown file."""
        cls.doc.h2("Additional metadata")
        cls.doc.li(f"Generated using {__file__} in the linkml-runtime repo.")
        cls.doc.li(f"Generated on: {datetime2.today().strftime('%Y-%m-%d')}")
        with open(str(OUTPUT_DIRECTORY / "results.md"), "w", encoding="UTF-8") as f:
            f.write(str(cls.doc))

    def _get_normalizer(self, sb: Optional[SchemaBuilder] = None) -> ReferenceValidator:
        if sb is None:
            sb = SchemaBuilder()
        sb.add_defaults()
        sv = SchemaView(sb.schema)
        return ReferenceValidator(sv)

    def _assert_unrepaired_types_the_same(
        self, report: Report, expected_unrepaired, input_object: Any, output_object: Any
    ):
        # TODO: simplify after https://github.com/linkml/linkml/issues/1203
        unrepaired_problem_types = report.unrepaired_problem_types()

        def _as_type(x: Union[ConstraintType, PermissibleValue]) -> str:
            if not isinstance(x, ConstraintType):
                return ConstraintType(x.text)
            return x

        expected_unrepaired_vals = [_as_type(v) for v in expected_unrepaired]
        unrepaired_problem_types_vals = [_as_type(v) for v in unrepaired_problem_types]
        self.assertCountEqual(
            expected_unrepaired_vals,
            unrepaired_problem_types_vals,
            f"{input_object} -> {output_object}",
        )

    def test_01_infer_collection_form(self):
        """Test that we can infer the collection form of a slot."""
        doc = self.doc
        doc.h2(
            "Collection Form Inference Tests",
            "Tests that the correct CollectionForm is inferred based on slot properties.",
        )
        cases = [
            (SlotDefinition("s", multivalued=False), CollectionForm.NonCollection),
            (
                SlotDefinition("s", multivalued=False, range="string"),
                CollectionForm.NonCollection,
            ),
            (
                SlotDefinition("s", multivalued=False, range="Simple"),
                CollectionForm.NonCollection,
            ),
            (
                SlotDefinition("s", multivalued=False, range="Identified"),
                CollectionForm.NonCollection,
            ),
            (
                SlotDefinition("s", multivalued=False, range="NonIdentified"),
                CollectionForm.NonCollection,
            ),
            (SlotDefinition("s", multivalued=True), CollectionForm.List),
            (
                SlotDefinition("s", multivalued=True, range="string"),
                CollectionForm.List,
            ),
            (
                SlotDefinition("s", multivalued=True, range="NonIdentified"),
                CollectionForm.List,
            ),
            (
                SlotDefinition("s", multivalued=True, range="Identified"),
                CollectionForm.List,
            ),
            (
                SlotDefinition("s", multivalued=True, range="Simple"),
                CollectionForm.List,
            ),
            (
                SlotDefinition("s", multivalued=True, inlined=True, range="Identified"),
                CollectionForm.CompactDict,
            ),
            (
                SlotDefinition(
                    "s", multivalued=True, inlined=True, range="NonIdentified"
                ),
                CollectionForm.CompactDict,
            ),
            (
                SlotDefinition("s", multivalued=True, inlined=True, range="Simple"),
                CollectionForm.SimpleDict,
            ),
            (
                SlotDefinition(
                    "s", multivalued=True, inlined_as_list=True, range="Identified"
                ),
                CollectionForm.List,
            ),
            (
                SlotDefinition(
                    "s", multivalued=True, inlined_as_list=True, range="NonIdentified"
                ),
                CollectionForm.List,
            ),
            (
                SlotDefinition(
                    "s", multivalued=True, inlined_as_list=True, range="Simple"
                ),
                CollectionForm.List,
            ),
        ]
        doc.text(
            "Expected collection form for different combinations of slot properties:"
        )
        doc.th(METASLOTS + ["CollectionForm"])
        for slot, expected in cases:
            sb = SchemaBuilder()
            _add_core_schema_elements(sb, slot)
            normalizer = self._get_normalizer(sb)
            self.assertEqual(
                expected,
                normalizer.infer_slot_collection_form(slot),
                f"{slot} -> {expected}",
            )
            doc.tr(_slot_metaslot_values(slot) + [expected])
            normalizer.expand_all = True
            inferred_form = normalizer.infer_slot_collection_form(slot)
            if expected in [CollectionForm.SimpleDict, CollectionForm.CompactDict]:
                expected = CollectionForm.ExpandedDict
            self.assertEqual(expected, inferred_form, f"expand_all={normalizer.expand_all}")


    def test_02_ensure_collection_forms(self):
        """Test normalization into a collection form."""
        doc = self.doc
        doc.h2(
            "Collection Form Coercion Tests",
            "Test cases for coercing input objects to a specified collection form.",
        )
        obj_identified_minimal = {"id": "id1"}
        obj_non_identified_minimal = {"name": "name1"}
        obj_simple = {"id": "id1", "name": "name1"}
        # cases = form, slot, examples
        #   example = input, expected_repairs, expected_unrepaired, expected_output
        cases = [
            (
                CollectionForm.NonCollection,
                SlotDefinition("s", range="string"),
                [
                    ("x", [], [], "x"),
                    ("", [], [], ""),
                    (
                        ["x"],
                        [(CollectionForm.List, CollectionForm.NonCollection)],
                        [],
                        "x",
                    ),
                    (
                        [],
                        [(CollectionForm.List, CollectionForm.NonCollection)],
                        [],
                        None,
                    ),
                ],
            ),
            (
                CollectionForm.NonCollection,
                SlotDefinition("s", range="NonIdentified"),
                [
                    (obj_non_identified_minimal, [], [], obj_non_identified_minimal),
                    (
                        [obj_non_identified_minimal],
                        [(CollectionForm.List, CollectionForm.NonCollection)],
                        [],
                        obj_non_identified_minimal,
                    ),
                ],
            ),
            (
                CollectionForm.NonCollection,
                SlotDefinition("s", range="Identified", inlined=False),
                [
                    ("id1", [], [], "id1"),
                    (
                        ["id1"],
                        [(CollectionForm.List, CollectionForm.NonCollection)],
                        [],
                        "id1",
                    ),
                ],
            ),
            (
                CollectionForm.NonCollection,
                SlotDefinition("s", range="Simple", inlined=True),
                [
                    (obj_simple, [], [], obj_simple),
                    # ({"id1": obj_simple}, [], [], obj_simple),
                ],
            ),
            (
                CollectionForm.List,
                SlotDefinition("s", range="string", multivalued=True),
                [
                    (["x"], [], [], ["x"]),
                    (
                        "x",
                        [(CollectionForm.NonCollection, CollectionForm.List)],
                        [],
                        ["x"],
                    ),
                    ([], [], [], []),
                ],
            ),
            (
                CollectionForm.List,
                SlotDefinition(
                    "s", range="NonIdentified", multivalued=True
                ),  # inlined is inferred
                [
                    (
                        [obj_non_identified_minimal],
                        [],
                        [],
                        [obj_non_identified_minimal],
                    ),
                    # indistinguishable from dict
                    # (obj_non_identified_minimal, [(CollectionForm.NonCollection, CollectionForm.List)], [], [obj_non_identified_minimal]),
                ],
            ),
            (
                CollectionForm.List,
                SlotDefinition("s", range="Identified", multivalued=True, inlined=True),
                [
                    ([obj_identified_minimal], [], [], [obj_identified_minimal]),
                    (
                        {"id1": obj_identified_minimal},
                        [(CollectionForm.ExpandedDict, CollectionForm.List)],
                        [],
                        [obj_identified_minimal],
                    ),
                    (
                        {"id1": obj_simple},
                        [(CollectionForm.ExpandedDict, CollectionForm.List)],
                        [],
                        [obj_simple],
                    ),
                    # TODO: SimpleDict to List
                    # ({"id1": "name1"}, [(CollectionForm.SimpleDict, CollectionForm.List)], [], [obj_simple]),
                ],
            ),
            (
                CollectionForm.List,
                SlotDefinition(
                    "s", range="Identified", multivalued=True, inlined=False
                ),
                [
                    (["id1"], [], [], ["id1"]),
                ],
            ),
            (
                CollectionForm.List,
                SlotDefinition("s", range="Simple", multivalued=True, inlined=True),
                [
                    ([obj_simple], [], [], [obj_simple]),
                ],
            ),
            (
                CollectionForm.ExpandedDict,
                SlotDefinition("s", range="Identified", multivalued=True, inlined=True),
                [
                    (
                        {"id1": obj_identified_minimal},
                        [],
                        [],
                        {"id1": obj_identified_minimal},
                    ),
                    (
                        {"id1": obj_identified_minimal,
                         "id2": obj_identified_minimal},
                        [],
                        [],
                        {"id1": obj_identified_minimal,
                         "id2": obj_identified_minimal},
                    ),
                    (
                        {"id1": None},
                        [],
                        [],
                        {"id1": obj_identified_minimal},
                    ),
                    (
                        {"id1": {}},
                        [],
                        [],
                        {"id1": obj_identified_minimal},
                    ),
                ],
            ),
            (
                CollectionForm.ExpandedDict,
                SlotDefinition("s", range="Simple", multivalued=True, inlined=True),
                [
                    ({"id1": {}}, [], [], {"id1": obj_identified_minimal}),
                    ({"id1": None}, [], [], {"id1": obj_identified_minimal}),
                    (
                        {"id1": "name1"},
                        [(CollectionForm.SimpleDict, CollectionForm.ExpandedDict)],
                        [],
                        {"id1": obj_simple},
                    ),
                ],
            ),
            (
                CollectionForm.CompactDict,
                {"range": "Identified", "inlined": True},
                [
                    ({}, [], [], {}),
                    ({"id1": {"name": "name1"}}, [], [], {"id1": {"name": "name1"}}),
                    ({"id1": {}}, [], [], {"id1": {}}),
                    ({"id1": None}, [], [], {"id1": None}),
                    (
                        {"id1": {"id": "id1", "name": "name1"}},
                        [(CollectionForm.ExpandedDict, CollectionForm.CompactDict)],
                        [],
                        {"id1": {"name": "name1"}},
                    ),
                ],
            ),
            (
                CollectionForm.SimpleDict,
                {"range": "Simple", "inlined": True},
                [
                    ({}, [], [], {}),
                    ({"id1": "name1"}, [], [], {"id1": "name1"}),
                    ({"id1": None}, [], [], {"id1": None}),
                    # ([{"id1": "name1"}], [(CollectionForm.List, CollectionForm.SimpleDict)], [], {"id1": "name1"}),
                    (
                        {"id1": obj_simple},
                        [(CollectionForm.ExpandedDict, CollectionForm.SimpleDict)],
                        [],
                        {"id1": "name1"},
                    ),
                    (
                        {"id1": {"name": "name1"}},
                        [(CollectionForm.CompactDict, CollectionForm.SimpleDict)],
                        [],
                        {"id1": "name1"},
                    ),
                    (
                        [obj_simple],
                        [(CollectionForm.List, CollectionForm.SimpleDict)],
                        [],
                        {"id1": "name1"},
                    ),
                    ([], [(CollectionForm.List, CollectionForm.SimpleDict)], [], {}),
                ],
            ),
        ]
        doc.th(METASLOTS + ["input", "output", "coerced_form", "normalizations"])
        for case in cases:
            form, slot_info, examples = case
            sb = SchemaBuilder()
            if isinstance(slot_info, dict):
                slot = SlotDefinition("s", **slot_info)
            else:
                slot = slot_info
            slot.multivalued = form != CollectionForm.NonCollection
            _add_core_schema_elements(sb, slot)
            normalizer = self._get_normalizer(sb)
            if slot.range in ["Identified", "Simple"]:
                pk_slot_name = SlotDefinitionName("id")
            else:
                pk_slot_name = None
            for example in examples:
                input, expected_repairs, expected_unrepaired, expected_output = example
                report = Report()
                if form == CollectionForm.NonCollection:
                    output = normalizer.ensure_non_collection(
                        input, slot, pk_slot_name, report
                    )
                elif form == CollectionForm.List:
                    output = normalizer.ensure_list(input, slot, pk_slot_name, report)
                elif form == CollectionForm.ExpandedDict:
                    output = normalizer.ensure_expanded_dict(
                        input, slot, pk_slot_name, report
                    )
                elif form == CollectionForm.CompactDict:
                    output = normalizer.ensure_compact_dict(
                        input, slot, pk_slot_name, report
                    )
                elif form == CollectionForm.SimpleDict:
                    output = normalizer.ensure_simple_dict(
                        input, slot, pk_slot_name, report
                    )
                else:
                    raise AssertionError(f"{form} unrecognized")
                doc.tr(
                    _slot_metaslot_values(slot)
                    + [
                        _serialize(input),
                        _serialize(output),
                        form.value,
                        _normalizations(report),
                    ]
                )
                self.assertEqual(expected_output, output)
                self.assertEqual(
                    len(expected_unrepaired),
                    len(report.results_excluding_normalized()),
                    f"case: {case} {report.results_excluding_normalized()}",
                )
                self.assertEqual(
                    len(expected_repairs),
                    len(report.normalized_results()),
                    f"case: {case} {report.normalized_results()}",
                )

    def test_03_slot_values(self):
        doc = self.doc
        doc.h2("Slot Value Tests")
        doc.text("Validation and normalization of collection forms.")
        doc.text("These tests use the core schema above, with different combinations of slots.")
        Inst_nt = namedtuple(
            "Inst",
            [
                "desc",
                "svs",
                "expected_repairs",
                "expected_unrepaired",
                "expected_output",
            ],
        )
        ref1 = {"id": "id1", "name": "name1"}
        ref1ni = {"name": "name1"}
        cases = [
            (
                SlotDefinition(
                    "s",
                    multivalued=True,
                    range="Identified",
                    inlined=True,
                    inlined_as_list=True,
                    description="List of inlined objects",
                ),
                [
                    Inst_nt("empty parent object", {}, [], [], {}),
                    Inst_nt(
                        "slot value is valid empty list", {"s": []}, [], [], {"s": []}
                    ),
                    Inst_nt(
                        "slot value is valid list", {"s": [ref1]}, [], [], {"s": [ref1]}
                    ),
                    Inst_nt(
                        "slot value is expanded dict",
                        {"s": {ref1["id"]: ref1}},
                        [(CollectionForm.ExpandedDict, CollectionForm.List)],
                        [],
                        {"s": [ref1]},
                    ),
                    Inst_nt(
                        "slot valid is empty dict",
                        {"s": {}},
                        [(CollectionForm.ExpandedDict, CollectionForm.List)],
                        [],
                        {"s": []},
                    ),
                    Inst_nt(
                        "incorrect slot",
                        {"t": "x"},
                        [],
                        [ConstraintType.ClosedClassConstraint],
                        {"t": "x"},
                    ),
                    Inst_nt(
                        "slot value is a list containing a non-object",
                        {"s": ["x"]},
                        [],
                        [ConstraintType.DictCollectionFormConstraint],
                        {"s": ["x"]},
                    ),
                    # Note: this is indistinguishable from a dict serialization
                    # Inst_nt("...", {"s": ref1}, [(Form.Atom, Form.List)], [], {"s": [ref1]}),
                ],
            ),
            (
                SlotDefinition(
                    "s",
                    multivalued=True,
                    range="NonIdentified",
                    description="List of necessarily inlined objects",
                ),
                [
                    Inst_nt("parent object is empty", {}, [], [], {}),
                    Inst_nt(
                        "slot value is valid empty list", {"s": []}, [], [], {"s": []}
                    ),
                    Inst_nt(
                        "slot value is object list",
                        {"s": [ref1ni]},
                        [],
                        [],
                        {"s": [ref1ni]},
                    ),
                    # Inst_nt("...", {"s": ref1ni}, [(Form.NonCollection, Form.List)], [], {"s": [ref1ni]}),
                    # Inst_nt("...", {"s": {}}, [(Form.ExpandedDict, Form.List)], [], {"s": []}),
                    Inst_nt(
                        "incorrect slot",
                        {"t": "x"},
                        [],
                        [ConstraintType.ClosedClassConstraint],
                        {"t": "x"},
                    ),
                ],
            ),
            (
                SlotDefinition(
                    "s",
                    multivalued=True,
                    range="Identified",
                    inlined=True,
                    inlined_as_list=False,
                    description="Dict of inlined objects",
                ),
                [
                    Inst_nt("parent object is empty", {}, [], [], {}),
                    Inst_nt(
                        "slot value is empty dictionary", {"s": {}}, [], [], {"s": {}}
                    ),
                    Inst_nt(
                        "slot value is inlined list",
                        {"s": [ref1]},
                        [(CollectionForm.List, CollectionForm.CompactDict)],
                        [],
                        {"s": {ref1["id"]: {"name": "name1"}}},
                    ),
                    Inst_nt(
                        "slot value is expanded dict",
                        {"s": {ref1["id"]: ref1}},
                        [(CollectionForm.ExpandedDict, CollectionForm.CompactDict)],
                        [],
                        {"s": {ref1["id"]: {"name": "name1"}}},
                    ),
                    Inst_nt(
                        "slot value is compact dict",
                        {"s": {ref1["id"]: {"name": "name1"}}},
                        [],
                        [],
                        {"s": {ref1["id"]: {"name": "name1"}}},
                    ),
                    Inst_nt(
                        "slot value is empty list",
                        {"s": []},
                        [(CollectionForm.List, CollectionForm.ExpandedDict)],
                        [],
                        {"s": {}},
                    ),
                    Inst_nt(
                        "incorrect slot",
                        {"t": "x"},
                        [],
                        [ConstraintType.ClosedClassConstraint],
                        {"t": "x"},
                    ),
                    # Inst_nt("...", {"s": ref1}, [(Form.Atom, Form.List)], [], {"s": [ref1]}),
                ],
            ),
            (
                SlotDefinition(
                    "s",
                    multivalued=True,
                    range="Simple",
                    inlined=True,
                    description="Simple dict",
                ),
                [
                    Inst_nt("empty parent object", {}, [], [], {}),
                    Inst_nt(
                        "slot value is simple dict",
                        {"s": {"id1": "name1"}},
                        [],
                        [],
                        {"s": {"id1": "name1"}},
                    ),
                    # Inst_nt(
                    #    "slot value is empty dict",
                    #    {"s": {"id1": None}},
                    #    [],
                    #    [],
                    #    {"s": {"id1": None}},
                    # ),
                    Inst_nt(
                        "slot value is expanded dict",
                        {"s": {ref1["id"]: ref1}},
                        [(CollectionForm.ExpandedDict, CollectionForm.SimpleDict)],
                        [],
                        {"s": {"id1": "name1"}},
                    ),
                    Inst_nt(
                        "slot value is compact dict",
                        {"s": {ref1["id"]: {"name": "name1"}}},
                        [(CollectionForm.CompactDict, CollectionForm.SimpleDict)],
                        [],
                        {"s": {"id1": "name1"}},
                    ),
                    Inst_nt(
                        "slot value is list of objects",
                        {"s": [ref1]},
                        # TODO: compress into single operation
                        [
                            (CollectionForm.List, CollectionForm.SimpleDict),
                        ],
                        [],
                        {"s": {"id1": "name1"}},
                    ),
                ],
            ),
            (
                SlotDefinition(
                    "s",
                    multivalued=True,
                    range="Identified",
                    inlined=False,
                    description="List of references",
                ),
                [
                    Inst_nt("parent object is empty", {}, [], [], {}),
                    Inst_nt(
                        "slot value is list of references",
                        {"s": ["x"]},
                        [],
                        [],
                        {"s": ["x"]},
                    ),
                    Inst_nt(
                        "slot value is a single reference",
                        {"s": "x"},
                        [(CollectionForm.NonCollection, CollectionForm.List)],
                        [],
                        {"s": ["x"]},
                    ),
                    Inst_nt(
                        "non-allowed slot",
                        {"t": "x"},
                        [],
                        [ConstraintType.ClosedClassConstraint],
                        {"t": "x"},
                    ),
                ],
            ),
            (
                SlotDefinition(
                    "s",
                    multivalued=False,
                    range="Identified",
                    inlined=True,
                    description="Single inlined object",
                ),
                [
                    Inst_nt("empty object", {}, [], [], {}),
                    Inst_nt("inlined singleton object", {"s": ref1}, [], [], {"s": ref1}),
                    Inst_nt(
                        "inlined list of objects",
                        {"s": [ref1]},
                        [(CollectionForm.List, CollectionForm.NonCollection)],
                        [],
                        {"s": ref1},
                    ),
                    Inst_nt(
                        "non-allowed slot",
                        {"t": "x"},
                        [],
                        [ConstraintType.ClosedClassConstraint],
                        {"t": "x"},
                    ),
                ],
            ),
        ]
        for slot, examples in cases:
            doc.h3(f"Case: {slot.description}")
            doc.text("Slot Properties:")
            doc.object(yaml_dumper.dumps(slot))
            sb = SchemaBuilder()
            sb.add_slot("id", range="string", identifier=True)
            sb.add_class("Identified", slots=["id", "name", "description"])
            sb.add_class("NonIdentified", slots=["name", "description"])
            sb.add_class("Simple", slots=["id", "name"])
            sb.add_class("TestClass", slots=[slot])
            normalizer = self._get_normalizer(sb)
            base_name = slot.description.lower().replace(" ", "-")
            yaml_dumper.dump(
                normalizer.derived_schema,
                OUTPUT_DIRECTORY / f"SchemaDefinition-{base_name}-derived.yaml",
            )
            tc = normalizer.derived_schema.classes["TestClass"]
            doc.th(["Description", "Input", "Output", "Normalizations", "Errors"])
            for example in examples:
                (
                    inst_description,
                    inst,
                    expected_repairs,
                    expected_unrepaired,
                    expected_output,
                ) = example
                inst_yaml = yaml_dumper.dumps(inst)
                report = Report()
                output_object = normalizer.normalize_object(inst, tc, report)
                self.assertEqual(
                    inst_yaml,
                    yaml_dumper.dumps(inst),
                    f"input should be immutable; {inst_yaml} changed to {yaml_dumper.dumps(inst)}",
                )
                self.assertEqual(
                    expected_output,
                    output_object,
                    f"Mismatch for {slot.description} => {inst_description}",
                )
                self.assertEqual(
                    len(expected_repairs),
                    len(report.normalized_results()),
                    f"Mismatch for {slot.description} =>  => {inst_description} . {report.normalized_results()}",
                )
                self._assert_unrepaired_types_the_same(
                    report, expected_unrepaired, inst, output_object
                )
                #doc.h4("Example")

                if False:
                    if report.normalized_results():
                        doc.text("Normalized Output:")
                        doc.object(output_object)
                        doc.text("Normalizations Applied:")
                        for r in report.normalized_results():
                            doc.li(str(r))
                    if report.results_excluding_normalized():
                        doc.text("Validation Errors (Post-Normalization)")
                        for r in report.results_excluding_normalized():
                            doc.object(r)
                doc.tr([inst_description,
                       _serialize(inst),
                       _serialize(output_object),
                       _normalizations(report),
                       _errors(report),
                        ])

    def test_05_type_ranges(self):
        cases = [
            ("maximum_value", "integer", 10, [5, 10], [11]),
            ("minimum_value", "integer", 10, [11, 10], [5]),
            ("pattern", "string", "^[a-z]+$", ["a", "abc"], ["", "a b", "A"]),
            ("equals_string", "string", "abc", ["abc"], ["ab"]),
            ("equals_expression", "integer", "5*5", [25], [24]),
        ]
        for metaslot, range, metaval, valid_examples, invalid_examples in cases:
            sb = SchemaBuilder()
            sb.add_slot("s", range=range, **{metaslot: metaval})
            sb.add_class("TestClass", slots=["s"])
            normalizer = self._get_normalizer(sb)
            derived_schema = normalizer.derived_schema
            tc = derived_schema.classes["TestClass"]
            for ex in valid_examples:
                report = Report()
                normalizer.normalize_object({"s": ex}, tc, report)
                self.assertEqual([], report.results, f"{metaslot} = {ex}")
            for ex in invalid_examples:
                report = Report()
                normalizer.normalize_object({"s": ex}, tc, report)
                self.assertNotEqual([], report.results, f"{metaslot} = {ex}")

    def test_06_object_ranges(self):
        cases = [
            ("TestClass", {"aref_A": {"id": "a", "name": "n", "ms": "v"}}, []),
            (
                "TestClass",
                {"aref_A": {"id": "a", "name": "n", "m1s": "v"}},
                [ConstraintType.ClosedClassConstraint],
            ),
            ("TestClass", {"aref_A1": {"id": "a", "a1s": "v", "m1s": "v"}}, []),
            ("TestClass", {"aref_A": {"id": "a", "type": "A"}}, []),
            ("TestClass", {"aref_A": {"id": "a", "type": "A1"}}, []),
            (
                "TestClass",
                {"aref_A11": {"id": "a", "type": "A12"}},
                [ConstraintType.DesignatesTypeConstraint],
            ),
        ]
        sb = SchemaBuilder()
        sb.add_slot("id", identifier=True)
        sb.add_slot("type", designates_type=True)
        sb.add_class("A", slots=["id", "name", "type"], mixins=["M"])
        sb.add_class("A1", slots=["a1s"], is_a="A", mixins=["M1"])
        sb.add_class("A11", slots=["a11s"], is_a="A1", mixins=["M11"])
        sb.add_class("A12", slots=["a12s"], is_a="A1", mixins=["M12"])
        sb.add_class("M", slots=["ms", "self"], mixin=True)
        sb.add_class("M1", slots=["m1s"], mixin=True)
        sb.add_class("M11", slots=["m11s"], mixin=True)
        sb.add_class("M12", slots=["m12s"], mixin=True)
        sb.add_class("TestClass", slots=["s", "type"])
        for c in sb.schema.classes.values():
            c.slot_usage["self"] = SlotDefinition("self", range=c.name, inlined=True)
            sb.add_slot(f"aref_{c.name}", range=c.name, inlined=True)
            sb.schema.classes["TestClass"].slots.append(f"aref_{c.name}")
        normalizer = self._get_normalizer(sb)
        derived_schema = normalizer.derived_schema
        for case in cases:
            cn, inst, expected_problems = case
            report = Report()
            normalizer.normalize_object(inst, derived_schema.classes[cn], report)
            self._assert_unrepaired_types_the_same(
                report, expected_problems, inst, inst
            )

    def test_07_normalize_enums(self):
        sb = SchemaBuilder()
        self.doc.h2("Enum Tests")
        sb.add_enum("TestEnum", permissible_values=["A", "B", "C"])
        normalizer = self._get_normalizer(sb)
        derived_schema = normalizer.derived_schema
        cases = [
            ("A", [], [], "A"),
            ("D", [], [ConstraintType.PermissibleValueConstraint], "D"),
        ]
        for (
            input_object,
            expected_repairs,
            expected_unrepaired,
            expected_output,
        ) in cases:
            report = Report()
            output = normalizer.normalize_enum(
                input_object, derived_schema.enums["TestEnum"], report
            )
            self.assertEqual(expected_output, output)
            self.assertCountEqual(expected_repairs, report.normalized_results())
            self._assert_unrepaired_types_the_same(
                report, expected_unrepaired, input_object, output
            )

    def test_08_normalize_types(self):
        doc = self.doc
        doc.h2("Type Tests")
        sb = SchemaBuilder()
        cases = {
            "string": [
                ("foo", [], [], "foo"),
                ("", [], [], ""),
                (5, [("integer", "string")], [], "5"),
                (5.0, [("float", "string")], [], "5.0"),
                (None, [], [], None),
            ],
            "integer": [
                (5, [], [], 5),
                ("5", [("string", "integer")], [], 5),
                (5.0, [("float", "integer")], [], 5),
                (5.5, [("float", "integer")], [], 5),
                ("5x", [], [ConstraintType.TypeConstraint], "5x"),
                (None, [], [], None),
            ],
            "float": [
                (5.5, [], [], 5.5),
                ("5.5", [("string", "float")], [], 5.5),
                (5, [("integer", "float")], [], 5.0),
                ("5x", [], [ConstraintType.TypeConstraint], "5x"),
                (None, [], [], None),
            ],
            "double": [
                (5.5, [], [], 5.5),
                ("5.5", [("string", "float")], [], 5.5),
                (5, [("integer", "float")], [], 5.0),
                ("5x", [], [ConstraintType.TypeConstraint], "5x"),
                (None, [], [], None),
            ],
            "decimal": [
                (Decimal("5"), [], [], Decimal("5")),
                (Decimal("5.5"), [], [], Decimal("5.5")),
                (Decimal(5), [], [], Decimal(5)),
                (Decimal(5.5), [], [], Decimal(5.5)),
                ("5.5", [("string", "decimal")], [], Decimal(5.5)),
                (5, [("integer", "decimal")], [], Decimal(5)),
                ("5x", [], [ConstraintType.TypeConstraint], "5x"),
                (None, [], [], None),
            ],
            "boolean": [
                (True, [], [], True),
                (False, [], [], False),
                ("True", [("string", "boolean")], [], True),
                ("False", [("string", "boolean")], [], False),
                ("true", [("string", "boolean")], [], True),
                ("false", [("string", "boolean")], [], False),
                ("", [], [ConstraintType.TypeConstraint], ""),
                (1, [("integer", "boolean")], [], True),
                (0, [("integer", "boolean")], [], False),
                (2, [], [ConstraintType.TypeConstraint], 2),
                (None, [], [], None),
            ],
            "uriorcurie": [
                ("X:1", [], [], "X:1"),
                ("http://example.org", [], [], "http://example.org"),
                ("", [], [], ""),
                ("a b", [], [ConstraintType.TypeConstraint], "a b"),
                (None, [], [], None),
            ],
            "uri": [
                ("http://example.org", [], [], "http://example.org"),
                ("a b", [], [ConstraintType.TypeConstraint], "a b"),
                (None, [], [], None),
            ],
            "date": [
                ("2020-01-01", [], [], "2020-01-01"),
                ("not-a-date", [], [ConstraintType.TypeConstraint], "not-a-date"),
                (None, [], [], None),
            ],
            "datetime": [
                # TODO: fix metamodelcore
                # (TEST_TIME.isoformat(), [], [], TEST_TIME.isoformat()),
                (
                    "not-a-datetime",
                    [],
                    [ConstraintType.TypeConstraint],
                    "not-a-datetime",
                ),
                (None, [], [], None),
            ],
            "time": [
                ("17:24:36", [], [], "17:24:36"),
                (datetime.time(0), [], [], "00:00:00"),
                ("not-a-time", [], [ConstraintType.TypeConstraint], "not-a-time"),
                (None, [], [], None),
            ],
            "ncname": [
                ("foo", [], [], "foo"),
                ("foo bar", [], [ConstraintType.TypeConstraint], "foo bar"),
                (None, [], [], None),
            ],
        }
        for t in cases.keys():
            sb.add_type(f"my_{t}", typeof=t)
        sb.add_defaults()
        sv = SchemaView(sb.schema)
        normalizer = ReferenceValidator(sv)
        derived_schema = normalizer.derived_schema
        for t, examples in cases.items():
            for v, expected_repairs, expected_unrepaired, expected_value in examples:
                # test with custom type
                report = Report()
                normalized_value = normalizer.normalize_type(
                    v, derived_schema.types[f"my_{t}"], report
                )
                self.assertEqual(
                    expected_value, normalized_value, f"Failed to normalize {v} to {t}"
                )
                self.assertEqual(
                    len(report.normalized_results()),
                    len(expected_repairs),
                    f"{v} -> {expected_value} type {t}: Expected {expected_repairs} repairs, got {report.normalized_results()}",
                )
                self._assert_unrepaired_types_the_same(
                    report, expected_unrepaired, v, expected_value
                )
                # test with built-in type
                report = Report()
                normalized_value = normalizer.normalize_type(
                    v, derived_schema.types[t], report
                )
                self.assertEqual(expected_value, normalized_value)
                self.assertEqual(len(report.normalized_results()), len(expected_repairs))
                self._assert_unrepaired_types_the_same(
                    report, expected_unrepaired, v, expected_value
                )

    def test_derived_schema_for_metadata(self):
        view = package_schemaview("linkml_runtime.linkml_model.meta")
        validator = ReferenceValidator(view)
        derived_schema = validator.derived_schema
        self.assertIsNotNone(view.get_identifier_slot("prefix", use_key=True))
        sdc = derived_schema.classes["schema_definition"]
        prefix_slot = sdc.attributes["prefixes"]
        self.assertEqual(prefix_slot.range, "prefix")

    def test_line_number(self):
        view = package_schemaview("linkml_runtime.linkml_model.meta")
        validator = ReferenceValidator(view)
        s = """
        id: s1
        name: schema1
        invented_field: foo
        description: test
        """
        obj = yaml.load(s, DupCheckYamlLoader)
        report = validator.validate(obj)
        for r in report.results_excluding_normalized():
            print(yaml_dumper.dumps(r))
        self.assertEqual(1, len(report.results_excluding_normalized()))
        r = report.results_excluding_normalized()[0]
        self.assertEqual(3, r.source_line_number)
        self.assertEqual(8, r.source_column_number)

    def test_examples_against_metamodel(self):
        view = package_schemaview("linkml_runtime.linkml_model.meta")
        validator = ReferenceValidator(view)
        derived_schema = validator.derived_schema
        self.assertIsNotNone(view.get_identifier_slot("prefix", use_key=True))
        sdc = derived_schema.classes["schema_definition"]
        prefixes_slot = sdc.attributes["prefixes"]
        cf = validator.infer_slot_collection_form(prefixes_slot)
        simple_dict_value_slot = validator._slot_as_simple_dict_value_slot(
            sdc.attributes["prefixes"]
        )
        # print(simple_dict_value_slot.name)
        # print(cf)
        self.assertEqual(CollectionForm.SimpleDict, cf)
        sb = SchemaBuilder("test")
        sb.add_slot("s1", range="string", description="test1")
        sb.add_class("C", ["s1", "s2"])
        sb.add_defaults()
        for s in ["imports", "prefixes", "slot_definitions", "classes"]:
            att = sdc.attributes[s]
            # print(yaml_dumper.dumps(att))
        self.assertFalse(sdc.attributes["prefixes"].inlined_as_list)
        schema_dict = json_dumper.to_dict(sb.schema)
        # print(schema_dict)
        report = Report()
        schema_norm = validator.normalize(schema_dict, target=sdc.name, report=report)
        self.assertEqual(dict, type(schema_norm["prefixes"]))
        for r in report.results_excluding_normalized():
            print(yaml_dumper.dumps(r))
        self.assertEqual(len(report.errors()), 0)
        # for r in report.repaired():
        #    print(r)
        self.assertEqual(len(report.normalized_results()), 3)
        report = validator.validate(schema_norm, target=sdc.name)
        self.assertEqual(0, len(report.errors()))
        self.assertEqual(0, len(report.normalized_results()))

    def test_metamodel(self):
        view = package_schemaview("linkml_runtime.linkml_model.meta")
        validator = ReferenceValidator(view)
        derived_schema = validator.derived_schema
        sdc = derived_schema.classes["schema_definition"]
        self.assertIn("name", sdc.attributes)
        schema_string = yaml_dumper.dumps(view.schema)
        report = Report()
        schema_dict = yaml.load(schema_string, DupCheckYamlLoader)
        schema_norm = validator.normalize(schema_dict, target=sdc.name, report=report)
        self.assertEqual([], report.errors())
        num_warnings = len(report.warnings())
        report = validator.validate(schema_norm, target=sdc.name)
        self.assertEqual(0, len(report.errors()))
        self.assertEqual(0, len(report.normalized_results()))
        # normalization should not change the number of warnings
        self.assertEqual(num_warnings, len(report.warnings()))


if __name__ == "__main__":
    unittest.main()