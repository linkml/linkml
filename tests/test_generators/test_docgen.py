"""
Tests generation of markdown and similar documents

Note that docgen replaces markdowngen
"""

import logging
import os
from collections import Counter
from copy import copy
from typing import List

import yaml
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.docgen import DocGenerator


def assert_mdfile_does_not_contain(*args, **kwargs) -> None:
    assert_mdfile_contains(*args, **kwargs, invert=True)


def assert_mdfile_contains(
    filename,
    text,
    after: str = None,
    followed_by: List[str] = None,
    invert=False,
) -> None:
    found = False
    is_after = False  # have we reached the after mark?
    with open(filename) as stream:
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


def test_latex_generation(kitchen_sink_path, tmp_path):
    """Tests minimal latex generation"""
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, format="latex")
    gen.serialize(directory=str(tmp_path))


def test_docgen_includes(kitchen_sink_path, input_path, tmp_path):
    """Tests basic document generator functionality"""
    deprecated_specification = str(input_path("deprecation.yaml"))
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, include=deprecated_specification)
    gen.serialize(directory=str(tmp_path))
    assert_mdfile_contains(tmp_path / "index.md", "C1", after="## Classes")


def test_docgen(kitchen_sink_path, input_path, tmp_path):
    """Tests basic document generator functionality"""
    example_dir = str(input_path("examples"))
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, example_directory=example_dir)
    blobs = gen.example_object_blobs("Person")
    assert len(blobs) > 0
    gen.serialize(directory=str(tmp_path))
    # test class docs
    assert_mdfile_contains(tmp_path / "Organization.md", "Organization", after="Inheritance")
    assert_mdfile_contains(tmp_path / "Organization.md", "[aliases](aliases.md)", after="Slots")
    assert_mdfile_contains(
        tmp_path / "Organization.md",
        "URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)",
        after="Class: Organization",
    )
    assert_mdfile_contains(
        tmp_path / "Organization.md",
        "from_schema: https://w3id.org/linkml/tests/kitchen_sink",
        after="Class: Organization",
    )
    assert_mdfile_contains(tmp_path / "Organization.md", "slot_uri: skos:altLabel", after="Induced")
    # test truncating newlines
    assert_mdfile_contains(tmp_path / "index.md", "An organization", after="## Classes", followed_by=["## Slots"])
    # this should be truncated
    assert_mdfile_does_not_contain(tmp_path / "index.md", "Markdown headers")
    # test mermaid
    assert_mdfile_contains(
        tmp_path / "Organization.md",
        "```mermaid",
        after="# Class",
        followed_by=["```", "## Inheritance", "## Slots"],
    )
    assert_mdfile_contains(
        tmp_path / "Organization.md",
        "HasAliases <|-- Organization",
        after="```mermaid",
        followed_by=["Organization : name", "```"],
    )

    # test yaml
    assert_mdfile_contains(
        tmp_path / "Organization.md",
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
        tmp_path / "Organization.md",
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
        tmp_path / "PhoneNumberType.md",
        "URI: [xsd:string](http://www.w3.org/2001/XMLSchema#string)",
        after="PhoneNumberType",
    )
    # test enum docs
    assert_mdfile_contains(
        tmp_path / "EmploymentEventType.md",
        "codes for different kinds of employment/HR related events",
        after="EmploymentEventType",
    )
    assert_mdfile_contains(
        tmp_path / "EmploymentEventType.md",
        "PROMOTION | bizcodes:003 | promotion event",
        after="Permissible Values",
    )
    # test slot docs
    assert_mdfile_contains(
        tmp_path / "aliases.md",
        "http://www.w3.org/2004/02/skos/core#altLabel",
        after="aliases",
    )
    # test index docs
    assert_mdfile_contains(
        tmp_path / "index.md",
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
        tmp_path / "index.md",
        "[EmploymentEventType](EmploymentEventType.md)",
        after="Enumerations",
    )
    assert_mdfile_contains(tmp_path / "index.md", "a provence-generating activity", after="Classes")
    # test default ordering (currently name)
    assert_mdfile_contains(
        tmp_path / "index.md",
        "Agent",
        after="Activity",
        followed_by=["Company", "Dataset", "MedicalEvent", "Organization"],
    )
    assert_mdfile_contains(
        tmp_path / "index.md",
        "addresses",
        after="activities",
        followed_by=["ceo", "city", "diagnosis", "persons"],
    )

    # test subset docs
    assert_mdfile_contains(tmp_path / "SubsetA.md", "test subset A", after="SubsetA")

    assert_mdfile_contains(
        tmp_path / "SubsetA.md",
        "SubsetA",
        followed_by=["## Identifier and Mapping Information", "### Schema Source"],
    )

    assert_mdfile_contains(tmp_path / "SubsetB.md", "## Slots in subset", after="### Schema Source")

    assert_mdfile_does_not_contain(tmp_path / "SubsetB.md", "## Classes in subset")

    assert_mdfile_does_not_contain(tmp_path / "SubsetB.md", "## Enumerations in subset")

    # test internal links
    assert_mdfile_contains(tmp_path / "ceo.md", "Range: [Person](Person.md)", after="Properties")
    # TODO: external links

    # test slot hierarchy
    assert_mdfile_contains(tmp_path / "tree_slot_B.md", "tree_slot_C", after="tree_slot_B")

    # test mixin page
    assert_mdfile_contains(tmp_path / "mixin_slot_I.md", "## Mixin Usage")

    # test that mixin page is hyperlinked
    assert_mdfile_contains(tmp_path / "tree_slot_C.md", "[mixin_slot_I](mixin_slot_I.md)")

    # test see_also hyperlinking
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "[https://en.wikipedia.org/wiki/Person](https://en.wikipedia.org/wiki/Person)",
        after="## See Also",
    )
    assert_mdfile_contains(tmp_path / "Person.md", "[schema:Person](http://schema.org/Person)", after="## See Also")

    # test that Aliases is showing from common metadata
    assert_mdfile_contains(tmp_path / "EmploymentEventType.md", "* HR code", after="## Aliases")

    # test that slots for enums are being rendered
    assert_mdfile_contains(
        tmp_path / "LifeStatusEnum.md",
        "life_st",
        after="## Slots",
        followed_by=[
            "## Identifier and Mapping Information",
            "### Schema Source",
            "## LinkML Source",
        ],
    )
    assert_mdfile_contains(
        tmp_path / "LifeStatusEnum.md",
        "is_livin",
        after="## Slots",
        followed_by=[
            "## Identifier and Mapping Information",
            "### Schema Source",
            "## LinkML Source",
        ],
    )
    # test slot usage overrides. See https://github.com/linkml/linkml/issues/1208
    assert_mdfile_contains(
        tmp_path / "FamilialRelationship.md",
        (
            "| [started_at_time](started_at_time.md) "
            "| 0..1 <br/> [Date](Date.md) |  "
            "| [Relationship](Relationship.md) |"
        ),
        after="## Slots",
    )
    assert_mdfile_contains(
        tmp_path / "FamilialRelationship.md",
        ("| [related_to](related_to.md) | 1 <br/> [Person](Person.md) |  | [Relationship](Relationship.md) |"),
        after="## Slots",
    )
    # test inheritance column
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "| [id](id.md) | 1 <br/> [String](String.md) |  | direct |",
        after="## Slots",
    )
    assert_mdfile_contains(
        tmp_path / "Person.md",
        ("| [aliases](aliases.md) | * <br/> [String](String.md) |  | [HasAliases](HasAliases.md) |"),
        after="## Slots",
    )
    # Examples
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "Example: Person",
        after="## Examples",
    )
    # Minimum Value showing up even if value is 0
    assert_mdfile_contains(tmp_path / "age_in_years.md", "Minimum Value: 0", after="## Properties")
    # Maximum Value
    assert_mdfile_contains(tmp_path / "age_in_years.md", "Maximum Value: 999", after="## Properties")
    #
    assert_mdfile_contains(
        tmp_path / "species_name.md",
        r"Regex pattern: `^[A-Z]+[a-z]+(-[A-Z]+[a-z]+)?\\.[A-Z]+(-[0-9]{4})?$`",
        after="## Properties",
    )

    # test that slots with ranges modified using any_of have union/cup
    # separated ranges
    assert_mdfile_contains(tmp_path / "EmploymentEvent.md", "[CordialnessEnum](CordialnessEnum.md)", after="## Slots")
    assert_mdfile_contains(tmp_path / "EmploymentEvent.md", "&nbsp;or&nbsp;<br />", after="## Slots")
    assert_mdfile_contains(
        tmp_path / "EmploymentEvent.md", "[EmploymentEventType](EmploymentEventType.md)", after="## Slots"
    )

    # checks correctness of the YAML representation of source schema
    person_source = gen.yaml(gen.schemaview.get_class("Person"))
    person_dict = yaml.load(person_source, Loader=yaml.Loader)
    # consider the species name slot
    # species name has the Person class repeated multiple times in domain_of
    domain_of_species_name = person_dict["slot_usage"]["species name"]["domain_of"]
    assert len(set(domain_of_species_name)) == len(domain_of_species_name)


def test_docgen_no_mergeimports(kitchen_sink_path, tmp_path):
    """Tests when imported schemas are not folded into main schema"""
    gen = DocGenerator(kitchen_sink_path, mergeimports=False, no_types_dir=True)
    gen.serialize(directory=str(tmp_path))

    assert_mdfile_contains(tmp_path / "index.md", "| [Address](Address.md) |  |", after="## Classes")

    assert_mdfile_does_not_contain(
        tmp_path / "index.md",
        "| [Activity](Activity.md) | a provence-generating activity |",
        after="## Classes",
    )

    assert_mdfile_does_not_contain(
        tmp_path / "index.md",
        "| [acted_on_behalf_of](acted_on_behalf_of.md) |  |",
        after="## Slots",
    )

    assert_mdfile_does_not_contain(
        tmp_path / "index.md",
        "| [AgeInYearsType](AgeInYearsType.md) |  |",
        after="## Types",
    )

    # test that slots modifying classes are being rendered
    assert_mdfile_contains(
        tmp_path / "type.md",
        "[FamilialRelationship](FamilialRelationship.md) |  |  yes  |",
        after="## Applicable Classes",
        followed_by=["## Properties", "* Range"],
    )

    assert_mdfile_contains(
        tmp_path / "type.md",
        "[EmploymentEvent](EmploymentEvent.md) |  |  yes  |",
        after="## Applicable Classes",
        followed_by=["## Properties", "* Range"],
    )


def test_docgen_rank_ordering(kitchen_sink_path, tmp_path):
    """Tests overriding default order"""
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, sort_by="rank")
    gen.serialize(directory=str(tmp_path))
    # test rank ordering
    assert_mdfile_contains(
        tmp_path / "index.md",
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
        tmp_path / "index.md",
        "[name]",
        after="[id]",
        followed_by=[
            "has_medical_history",
            "has_employment_history",
            "test_attribute",
        ],
    )


def test_gen_metamodel(tmp_path):
    """Tests generation of docs for metamodel"""
    metamodel_sv = package_schemaview("linkml_runtime.linkml_model.meta")
    gen = DocGenerator(metamodel_sv.schema, mergeimports=True, no_types_dir=True, genmeta=True)
    gen.serialize(directory=str(tmp_path))
    assert_mdfile_contains(
        tmp_path / "index.md",
        "ClassDefinition",
        after="## Classes",
        followed_by=["## Slots"],
    )
    assert_mdfile_contains(
        tmp_path / "index.md",
        "exact_mappings",
        after="## Slots",
        followed_by=["## Enumerations"],
    )
    assert_mdfile_contains(
        tmp_path / "index.md",
        "AliasPredicateEnum",
        after="## Enumerations",
        followed_by=["PvFormulaOptions"],
    )
    assert_mdfile_contains(tmp_path / "index.md", "String", after="## Types")


def test_myst_dialect(kitchen_sink_path, tmp_path):
    """
    Tests mermaid in myst.

    See <https://github.com/linkml/linkml/issues/835>_
    """
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, dialect="myst")
    gen.serialize(directory=str(tmp_path))
    assert_mdfile_contains(
        tmp_path / "Organization.md",
        "```{mermaid}",
        after="# Class",
        followed_by=["```", "## Inheritance", "## Slots"],
    )


def test_custom_directory(kitchen_sink_path, input_path, tmp_path):
    """
    tests ability to specify a custom folder of templates;
    these act as overrides, if no template is found the default is used
    """
    tdir = input_path("docgen_md_templates")
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True, template_directory=str(tdir))
    gen.serialize(directory=str(tmp_path))
    # assert_mdfile_contains('Organization.md', 'Organization', after='Inheritance')
    assert_mdfile_contains(tmp_path / "Organization.md", "FAKE TEMPLATE")


def test_gen_custom_named_index(kitchen_sink_path, tmp_path):
    """Tests that the name of the index page can be customized"""
    gen = DocGenerator(kitchen_sink_path, index_name="custom-index")
    gen.serialize(directory=str(tmp_path))
    assert_mdfile_contains(tmp_path / "custom-index.md", "# Kitchen Sink Schema")
    # Additionally test that the default index.md has NOT been created
    assert not os.path.exists(tmp_path / "index.md")


def test_html(kitchen_sink_path, input_path, tmp_path):
    """
    Tests ability to specify a complete new set of templates in a different format
    """
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        no_types_dir=True,
        template_directory=str(tdir),
        format="html",
    )
    assert gen._file_suffix() == "html"
    gen.serialize(directory=str(tmp_path))
    assert_mdfile_contains(tmp_path / "Organization.html", "Fake example Organization")


def test_class_hierarchy_as_tuples(kitchen_sink_path, input_path):
    """Test for method that seeks to generate hierarchically indented
    list of classes and subclasses
    """
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        no_types_dir=True,
        template_directory=str(tdir),
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

    parent_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "class with spaces"][0])
    sub_class_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "subclass test"][0])
    sub_sub_class_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "Sub sub class 2"][0])
    tub_sub_class_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "tub sub class 1"][0])

    assert tub_sub_class_order > sub_sub_class_order
    assert sub_sub_class_order > sub_class_order
    assert sub_class_order > parent_order

    expected_result = [
        (0, "activity"),
        (0, "Address"),
        (0, "agent"),
        (0, "AnyObject"),
        (0, "AnyOfClasses"),
        (0, "AnyOfEnums"),
        (0, "AnyOfMix"),
        (0, "EqualsString"),
        (0, "EqualsStringIn"),
        (0, "AnyOfSimpleType"),
        (0, "class with spaces"),
        (1, "subclass test"),
        (2, "Sub sub class 2"),
        (2, "tub sub class 1"),
        (0, "CodeSystem"),
        (0, "Concept"),
        (1, "ProcedureConcept"),
        (1, "DiagnosisConcept"),
        (0, "Dataset"),
        (0, "Event"),
        (1, "MarriageEvent"),
        (1, "MedicalEvent"),
        (1, "EmploymentEvent"),
        (1, "BirthEvent"),
        (0, "FakeClass"),
        (0, "Friend"),
        (0, "HasAliases"),
        (0, "Organization"),
        (1, "Company"),
        (0, "Person"),
        (0, "Place"),
        (0, "Relationship"),
        (1, "FamilialRelationship"),
        (0, "WithLocation"),
    ]

    assert Counter(actual_result) == Counter(expected_result)


def test_class_hierarchy_as_tuples_no_mergeimports(kitchen_sink_path, input_path):
    """Test to ensure that imported schema classes are not generated
    even in the method that hierarchically lists classes on index page
    when mergeimports=False.
    """
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=False,
        no_types_dir=True,
        template_directory=str(tdir),
        format="html",
    )
    actual_result = gen.class_hierarchy_as_tuples()
    actual_result = list(actual_result)

    assert (0, "activity") not in actual_result
    assert (0, "agent") not in actual_result


def test_fetch_slots_of_class(kitchen_sink_path, input_path):
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        no_types_dir=True,
        template_directory=str(tdir),
        format="html",
    )

    sv = SchemaView(kitchen_sink_path)
    cls = sv.get_class("Address")

    # test assertion for own attributes of a class
    actual_result = gen.get_direct_slot_names(cls)
    expected_result = ["street", "city", "altitude"]

    assert expected_result == actual_result

    # test assertion for inherited attributes of a class
    cls = sv.get_class("EmploymentEvent")
    actual_result = [s.name for s in gen.get_indirect_slots(cls)]
    expected_result = ["ended at time", "metadata", "started at time", "is current"]

    assert Counter(expected_result) == Counter(actual_result)

    # test assertion for mixed in slots of a class
    cls = sv.get_class("Organization")
    actual_result = gen.get_mixin_inherited_slots(cls)
    expected_result = {"HasAliases": ["aliases"]}

    assert actual_result == expected_result

    cls = sv.get_class("Person")
    assert "id" in gen.get_direct_slot_names(cls)
    assert "aliases" not in gen.get_direct_slot_names(cls)


def test_class_slots_inheritance(kitchen_sink_path):
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True)

    sv = SchemaView(kitchen_sink_path)
    test_class = sv.get_class("BirthEvent")
    test_slot = sv.get_slot("started at time")

    expected_result = ["Event"]
    actual_result = gen.get_slot_inherited_from(class_name=test_class.name, slot_name=test_slot.name)

    assert expected_result == actual_result


def test_use_slot_uris(kitchen_sink_path, input_path, tmp_path):
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        no_types_dir=True,
        template_directory=str(tdir),
        use_slot_uris=True,
    )

    gen.serialize(directory=str(tmp_path))

    # this is a markdown file created from slot_uri
    assert_mdfile_contains(tmp_path / "actedOnBehalfOf.md", "Slot: acted on behalf of")

    # check label and link of documents in inheritance tree
    # A.md
    assert_mdfile_contains(tmp_path / "A.md", "[tree_slot_B](B.md)", after="**tree_slot_A**")

    # B.md
    assert_mdfile_contains(
        tmp_path / "B.md",
        "**tree_slot_B**",
        after="[tree_slot_A](A.md)",
        # followed_by="* [tree_slot_C](C.md) [ [mixin_slot_I](mixin_slot_I.md)]",
    )


def test_use_class_uris(kitchen_sink_path, input_path, tmp_path):
    tdir = input_path("docgen_html_templates")
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        no_types_dir=True,
        template_directory=str(tdir),
        use_class_uris=True,
    )

    gen.serialize(directory=str(tmp_path))

    # this is a markdown file created from class_uri
    assert_mdfile_contains(tmp_path / "Any.md", "Class: AnyObject")

    # check that the classes table on index page has correct class names and
    # are linked to the correct class doc pages
    assert_mdfile_contains(tmp_path / "index.md", "[AnyObject](Any.md)")


def test_hierarchical_class_view(kitchen_sink_path, tmp_path):
    """Test to check if class table view on index page follows hierarchical view"""
    gen = DocGenerator(kitchen_sink_path, mergeimports=True, hierarchical_class_view=True)

    gen.serialize(directory=str(tmp_path))

    assert_mdfile_contains(tmp_path / "index.md", "Event", after="Dataset")

    assert_mdfile_contains(tmp_path / "index.md", "BirthEvent", after="Event")

    assert_mdfile_contains(tmp_path / "index.md", "EmploymentEvent", after="BirthEvent")

    assert_mdfile_contains(tmp_path / "index.md", "MarriageEvent", after="EmploymentEvent")


def test_uml_diagram_er(kitchen_sink_path, tmp_path):
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        diagram_type="er_diagram",
        include_top_level_diagram=True,
    )

    gen.serialize(directory=str(tmp_path))

    # check if ER diagram has been included at top level, i.e., on the index page
    assert_mdfile_contains(
        tmp_path / "index.md",
        "## Schema Diagram",
        after="Name: kitchen_sink",
        followed_by=["```mermaid", "erDiagram"],
    )

    # pick a random class documentation markdown file and check if there
    # is a mermaid ER diagram in it
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "# Class: Person",
        followed_by=["```mermaid", "erDiagram", "Person"],
    )


def test_uml_diagram_classr(kitchen_sink_path, tmp_path):
    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        diagram_type="mermaid_class_diagram",
    )

    gen.serialize(directory=str(tmp_path))

    # pick a random class documentation markdown file and check if there
    # is a mermaid class diagram in it
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "# Class: Person",
        followed_by=["```mermaid", "classDiagram", "Person"],
    )

    gen = DocGenerator(
        kitchen_sink_path,
        mergeimports=True,
        diagram_type="plantuml_class_diagram",
    )

    gen.serialize(directory=str(tmp_path))

    # pick a random class documentation markdown file and check if there
    # is a mermaid class diagram in it
    assert_mdfile_contains(
        tmp_path / "Person.md",
        "# Class: Person",
        followed_by=["```puml", "@startuml", 'class "Person" [[{A person, living or dead}]] {', "@enduml"],
    )
