import logging
import os
import shutil
import tempfile
import unittest
from copy import copy
from typing import List

from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.docgen import DocGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
LATEX_DIR = env.expected_path("kitchen_sink_tex")
MD_DIR = env.expected_path("kitchen_sink_md")
META_MD_DIR = env.expected_path("meta_md")
MD_DIR2 = env.expected_path("kitchen_sink_md2")
HTML_DIR = env.expected_path("kitchen_sink_html")
EXAMPLE_DIR = env.input_path("examples")



def assert_mdfile_does_not_contain(*args, **kwargs) -> None:
    assert_mdfile_contains(*args, **kwargs, invert=True)


def assert_mdfile_contains(
    filename,
    text,
    after: str = None,
    followed_by: List[str] = None,
    outdir=MD_DIR,
    invert=False,
) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(outdir, filename)) as stream:
        lines = stream.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
                if found and followed_by:
                    todo = copy(followed_by)
                    for j in range(i + 1, len(lines)):
                        subsequent_line = lines[j]
                        if len(todo) > 0 and todo[0] in subsequent_line:
                            todo = todo[1:]
                    if len(todo) > 0:
                        if not invert:
                            logging.error(f"Did not find: {todo}")
                        assert invert
                    else:
                        return
            if after is not None and after in line:
                is_after = True
    if not found and not invert:
        logging.error(f"Failed to find {text} in {filename}")
    if invert:
        assert not found
    else:
        assert found


class DocGeneratorTestCase(unittest.TestCase):
    """
    Tests generation of markdown and similar documents

    Note that docgen replaces markdowngen
    """
    def test_latex_generation(self):
        """Tests minimal latex generation"""
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, format="latex")
        md = gen.serialize(directory=LATEX_DIR)

    def test_docgen(self):
        """Tests basic document generator functionality"""
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, example_directory=EXAMPLE_DIR)
        blobs = gen.example_object_blobs("Person")
        self.assertGreater(len(blobs), 0)
        md = gen.serialize(directory=MD_DIR)
        # test class docs
        assert_mdfile_contains("Organization.md", "Organization", after="Inheritance")
        assert_mdfile_contains(
            "Organization.md", "[aliases](aliases.md)", after="Slots"
        )
        assert_mdfile_contains(
            "Organization.md",
            "URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)",
            after="Class: Organization",
        )
        assert_mdfile_contains(
            "Organization.md",
            "from_schema: https://w3id.org/linkml/tests/kitchen_sink",
            after="Class: Organization",
        )
        assert_mdfile_contains(
            "Organization.md", "slot_uri: skos:altLabel", after="Induced"
        )
        # test truncating newlines
        assert_mdfile_contains(
            "index.md", "An organization", after="## Classes", followed_by=["## Slots"]
        )
        # this should be truncated
        assert_mdfile_does_not_contain("index.md", "Markdown headers")
        # test mermaid
        assert_mdfile_contains(
            "Organization.md",
            "```mermaid",
            after="# Class",
            followed_by=["```", "## Inheritance", "## Slots"],
        )
        assert_mdfile_contains(
            "Organization.md",
            "HasAliases <|-- Organization",
            after="```mermaid",
            followed_by=["Organization : name", "```"],
        )

        # test yaml
        assert_mdfile_contains(
            "Organization.md",
            "<details>",
            after="### Direct",
            followed_by=[
                "```yaml",
                "name: Organization",
                "mixins:",
                "- HasAliases",
                "```",
                "</details>",
                "### Induced",
            ],
        )
        assert_mdfile_contains(
            "Organization.md",
            "<details>",
            after="### Induced",
            followed_by=[
                "```yaml",
                "name: Organization",
                "attributes:",
                "aliases:",
                "multivalued: true",
                "```",
                "</details>",
            ],
        )

        # test type docs
        assert_mdfile_contains(
            "PhoneNumberType.md",
            "URI: [xsd:string](http://www.w3.org/2001/XMLSchema#string)",
            after="PhoneNumberType",
        )
        # test enum docs
        assert_mdfile_contains(
            "EmploymentEventType.md",
            "codes for different kinds of employment/HR related events",
            after="EmploymentEventType",
        )
        assert_mdfile_contains(
            "EmploymentEventType.md",
            "PROMOTION | bizcodes:003 | promotion event",
            after="Permissible Values",
        )
        # test slot docs
        assert_mdfile_contains(
            "aliases.md",
            "http://www.w3.org/2004/02/skos/core#altLabel",
            after="aliases",
        )
        # test index docs
        assert_mdfile_contains(
            "index.md",
            "# Kitchen Sink Schema",
            followed_by=[
                "URI:",
                "Name:",
                "## Classes",
                "## Slots",
                "## Enumerations",
                "## Subsets",
            ],
        )
        assert_mdfile_contains(
            "index.md",
            "[EmploymentEventType](EmploymentEventType.md)",
            after="Enumerations",
        )
        assert_mdfile_contains(
            "index.md", "a provence-generating activity", after="Classes"
        )
        # test default ordering (currently name)
        assert_mdfile_contains(
            "index.md",
            "Agent",
            after="Activity",
            followed_by=["Company", "Dataset", "MedicalEvent", "Organization"],
        )
        assert_mdfile_contains(
            "index.md",
            "addresses",
            after="activities",
            followed_by=["ceo", "city", "diagnosis", "persons"],
        )

        # test subset docs
        assert_mdfile_contains("SubsetA.md", "test subset A", after="SubsetA")

        assert_mdfile_contains(
            "SubsetA.md",
            "SubsetA",
            followed_by=["## Identifier and Mapping Information", "### Schema Source"],
        )

        # test internal links
        assert_mdfile_contains(
            "ceo.md", "Range: [Person](Person.md)", after="Properties"
        )
        # TODO: external links
        
        # test slot hierarchy
        assert_mdfile_contains(
            "tree_slot_B.md", "tree_slot_C", after="tree_slot_B"
        )

        # test mixin page
        assert_mdfile_contains(
            "mixin_slot_I.md", "## Mixin Usage"
        )

        # test that mixin page is hyperlinked
        assert_mdfile_contains(
            "tree_slot_C.md", "[mixin_slot_I](mixin_slot_I.md)"
        )

        # test see_also hyperlinking
        assert_mdfile_contains(
            "Person.md", 
            "[https://en.wikipedia.org/wiki/Person](https://en.wikipedia.org/wiki/Person)",
            after="## See Also"
        )
        assert_mdfile_contains(
            "Person.md", 
            "[schema:Person](http://schema.org/Person)",
            after="## See Also"
        )

        # test that Aliases is showing from common metadata
        assert_mdfile_contains(
            "EmploymentEventType.md", "* HR code", after="## Aliases"
        )

        # test that slots for enums are being rendered
        assert_mdfile_contains(
            "LifeStatusEnum.md", "life_st", after="## Slots",
            followed_by=["## Identifier and Mapping Information", 
                        "### Schema Source", 
                        "## LinkML Source"],
        )
        assert_mdfile_contains(
            "LifeStatusEnum.md", "is_livin", after="## Slots",
            followed_by=["## Identifier and Mapping Information", 
                        "### Schema Source", 
                        "## LinkML Source"],
        )
        # test slot usage overrides. See https://github.com/linkml/linkml/issues/1208
        assert_mdfile_contains(
            "FamilialRelationship.md",
            ("| [started_at_time](started_at_time.md) | "
             "0..1 <br/> [xsd:date](http://www.w3.org/2001/XMLSchema#date) |  | "
             "[Relationship](Relationship.md) |"),
            after="## Slots",
        )
        assert_mdfile_contains(
            "FamilialRelationship.md",
            ("| [related_to](related_to.md) | 1..1 <br/> [Person](Person.md) |  | "
             "[Relationship](Relationship.md) |"),
            after="## Slots",
        )
        # test inheritance column
        assert_mdfile_contains(
            "Person.md",
            "| [id](id.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |",
            after="## Slots",
        )
        assert_mdfile_contains(
            "Person.md",
            ("| [aliases](aliases.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) "
             "|  | [HasAliases](HasAliases.md) |"),
            after="## Slots",
        )
        # Examples
        assert_mdfile_contains(
            "Person.md",
            "Example: Person",
            after="## Examples",)

    def test_docgen_rank_ordering(self):
        """Tests overriding default order"""
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, sort_by="rank")
        md = gen.serialize(directory=MD_DIR)
        # test rank ordering
        assert_mdfile_contains(
            "index.md",
            "Person",
            after="Dataset",
            followed_by=[
                "Organization",
                "FamilialRelationship",
                "EmploymentEvent",
                "ClassWithSpaces",
            ],
        )
        assert_mdfile_contains(
            "index.md",
            "[name]",
            after="[id]",
            followed_by=[
                "has_medical_history",
                "has_employment_history",
                "test_attribute",
            ],
        )

    def test_gen_metamodel(self):
        """Tests generation of docs for metamodel"""
        metamodel_sv = package_schemaview("linkml_runtime.linkml_model.meta")
        gen = DocGenerator(
            metamodel_sv.schema, mergeimports=True, no_types_dir=True, genmeta=True
        )
        gen.serialize(directory=META_MD_DIR)
        assert_mdfile_contains(
            "index.md",
            "ClassDefinition",
            after="## Classes",
            followed_by=["## Slots"],
            outdir=META_MD_DIR,
        )
        assert_mdfile_contains(
            "index.md",
            "exact_mappings",
            after="## Slots",
            followed_by=["## Enumerations"],
            outdir=META_MD_DIR,
        )
        assert_mdfile_contains(
            "index.md",
            "AliasPredicateEnum",
            after="## Enumerations",
            followed_by=["PvFormulaOptions"],
            outdir=META_MD_DIR,
        )
        assert_mdfile_contains(
            "index.md", "String", after="## Types", outdir=META_MD_DIR
        )

    def test_myst_dialect(self):
        """
        Tests mermaid in myst.

        See <https://github.com/linkml/linkml/issues/835>_
        """
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, dialect="myst")
        md = gen.serialize(directory=MD_DIR)
        assert_mdfile_contains(
            "Organization.md",
            "```{mermaid}",
            after="# Class",
            followed_by=["```", "## Inheritance", "## Slots"],
        )

    def test_custom_directory(self):
        """
        tests ability to specify a custom folder of templates;
        these act as overrides, if no template is found the default is used
        """
        tdir = env.input_path("docgen_md_templates")
        gen = DocGenerator(
            SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir
        )
        md = gen.serialize(directory=MD_DIR2)
        # assert_mdfile_contains('Organization.md', 'Organization', after='Inheritance')
        assert_mdfile_contains("Organization.md", "FAKE TEMPLATE", outdir=MD_DIR2)

    def test_html(self):
        """
        Tests ability to specify a complete new set of templates in a different format
        """
        tdir = env.input_path("docgen_html_templates")
        gen = DocGenerator(
            SCHEMA,
            mergeimports=True,
            no_types_dir=True,
            template_directory=tdir,
            format="html",
        )
        assert gen._file_suffix() == "html"
        md = gen.serialize(directory=HTML_DIR)
        assert_mdfile_contains(
            "Organization.html", "Fake example Organization", outdir=HTML_DIR
        )

    def test_class_hierarchy_as_tuples(self):
        """Test for method that seeks to generate hierarchically indented
        list of classes and subclasses
        """
        tdir = env.input_path("docgen_html_templates")
        gen = DocGenerator(
            SCHEMA,
            mergeimports=True,
            no_types_dir=True,
            template_directory=tdir,
            format="html",
        )

        actual_result = gen.class_hierarchy_as_tuples()
        actual_result = list(actual_result)

        # assertion to make sure that children are listed after parents
        # and that siblings, i.e., classes at the same depth are sorted
        # alphabetically
        # parent: class with spaces
        # child at depth 1: subclass test
        # child at depth 2: Sub sub class 2
        # child at depth 2: tub sub class 1

        # classes related by is_a relationship
        # Sub sub class 2 is_a subclass test is_a class with spaces
        # tub sub class 1 is_a subclass test is_a class with spaces

        parent_order = actual_result.index(
            [(dep, cls) for dep, cls in actual_result if cls == "class with spaces"][0]
        )
        sub_class_order = actual_result.index(
            [(dep, cls) for dep, cls in actual_result if cls == "subclass test"][0]
        )
        sub_sub_class_order = actual_result.index(
            [(dep, cls) for dep, cls in actual_result if cls == "Sub sub class 2"][0]
        )
        tub_sub_class_order = actual_result.index(
            [(dep, cls) for dep, cls in actual_result if cls == "tub sub class 1"][0]
        )

        self.assertGreater(tub_sub_class_order, sub_sub_class_order)
        self.assertGreater(sub_sub_class_order, sub_class_order)
        self.assertGreater(sub_class_order, parent_order)
        
        expected_result = [(0, 'activity'), (0, 'Address'), (0, 'agent'), (0, 'AnyObject'), 
                           (0, 'class with spaces'), (1, 'subclass test'), (2, 'Sub sub class 2'), (2, 'tub sub class 1'),
                           (0, 'CodeSystem'), (0, 'Concept'), (1, 'ProcedureConcept'), (1, 'DiagnosisConcept'), 
                           (0, 'Dataset'), (0, 'Event'), (1, 'MarriageEvent'), (1, 'MedicalEvent'), 
                           (1, 'EmploymentEvent'), (1, 'BirthEvent'), (0, 'FakeClass'), (0, 'Friend'), (0, 'HasAliases'), 
                           (0, 'Organization'), (1, 'Company'), (0, 'Person'), (0, 'Place'), (0, 'Relationship'), 
                           (1, 'FamilialRelationship'), (0, 'WithLocation')]
                           
        self.assertCountEqual(actual_result, expected_result)
        
    def test_fetch_slots_of_class(self):
        tdir = env.input_path('docgen_html_templates')
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir, format='html')

        sv = SchemaView(SCHEMA)
        cls = sv.get_class("Address")

        # test assertion for own attributes of a class
        actual_result = gen.get_direct_slot_names(cls)
        expected_result = ["street", "city"]

        self.assertListEqual(expected_result, actual_result)

        # test assertion for inherited attributes of a class
        cls = sv.get_class("EmploymentEvent")
        actual_result = [s.name for s in gen.get_indirect_slots(cls)]
        expected_result = ["ended at time", "metadata", "started at time", "is current"]
        
        self.assertCountEqual(expected_result, actual_result)

        # test assertion for mixed in slots of a class
        cls = sv.get_class("Organization")
        actual_result = gen.get_mixin_inherited_slots(cls)
        expected_result = {"HasAliases": ["aliases"]}

        self.assertDictEqual(actual_result, expected_result)

        cls = sv.get_class("Person")
        self.assertIn("id", gen.get_direct_slot_names(cls))
        self.assertNotIn("aliases", gen.get_direct_slot_names(cls))

    def test_class_slots_inheritance(self):
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True)

        sv = SchemaView(SCHEMA)
        test_class = sv.get_class("BirthEvent")
        test_slot = sv.get_slot("started at time")

        expected_result = ["Event"]
        actual_result = gen.get_slot_inherited_from(class_name=test_class.name, slot_name=test_slot.name)

        self.assertListEqual(expected_result, actual_result)

    def test_use_slot_uris(self):
        tdir = env.input_path("docgen_html_templates")
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir, use_slot_uris=True)

        md_temp_dir = tempfile.mkdtemp()

        md = gen.serialize(directory=md_temp_dir)

        # this is a markdown file created from slot_uri
        assert_mdfile_contains("actedOnBehalfOf.md", "Slot: actedOnBehalfOf", outdir=md_temp_dir)

        # check label and link of documents in inheritance tree 
        # A.md
        assert_mdfile_contains("A.md", "[tree_slot_B](B.md)", after="**tree_slot_A**", outdir=md_temp_dir)

        # B.md
        assert_mdfile_contains("B.md", 
                                "**tree_slot_B**", 
                                after="[tree_slot_A](A.md)", 
                                # followed_by="* [tree_slot_C](C.md) [ [mixin_slot_I](mixin_slot_I.md)]",
                                outdir=md_temp_dir)
                
        shutil.rmtree(md_temp_dir)


if __name__ == "__main__":
    unittest.main()
