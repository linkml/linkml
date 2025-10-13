from linkml.generators.markdowngen import MarkdownGenerator


def assert_mdfile_contains(filename, text, after=None, description=None) -> None:
    found = False
    is_after = False  # have we reached the after mark?
    with open(filename) as stream:
        for line in stream.readlines():
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
            if after is not None and after in line:
                is_after = True
    assert found


def test_markdowngen(kitchen_sink_path, tmp_path):
    """DDL"""
    gen = MarkdownGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True)
    gen.serialize(directory=tmp_path)

    assert_mdfile_contains(tmp_path / "index.md", "Address", after="Classes")
    assert_mdfile_contains(tmp_path / "index.md", "HasAliases", after="Mixins")
    assert_mdfile_contains(tmp_path / "index.md", "acted on behalf of", after="Slots")
    assert_mdfile_contains(tmp_path / "index.md", "DiagnosisType", after="Enums")
    assert_mdfile_contains(tmp_path / "index.md", "test subset A", after="Subsets")

    assert_mdfile_contains(
        tmp_path / "SubsetA.md",
        "* [Person](Person.md)",
        description="person class is declared to be in subset A",
    )

    assert_mdfile_contains(tmp_path / "Person.md", "has medical history", after="Own")
    assert_mdfile_contains(tmp_path / "Person.md", "aliases", after="Mixed in from HasAliases")

    assert_mdfile_contains(tmp_path / "has_medical_history.md", "MedicalEvent", after="Domain and Range")
    assert_mdfile_contains(tmp_path / "has_medical_history.md", "subset B", after="Other properties")


def test_slot_name_mapping(kitchen_sink_path, tmp_path):
    """Tests rewiring names of main metamodel types"""
    gen = MarkdownGenerator(kitchen_sink_path, mergeimports=True, no_types_dir=True)
    gen.metamodel_name_map = {"class": "record", "slot": "field", "mixin": "trait"}
    assert gen.get_metamodel_slot_name("class") == "record"
    assert gen.get_metamodel_slot_name("classes") == "records"
    assert gen.get_metamodel_slot_name("Classes") == "Records"
    assert gen.get_metamodel_slot_name("Mixins") == "Traits"

    gen.metamodel_name_map = {"class": "Record", "slot": "Field", "mixin": "Trait"}
    assert gen.get_metamodel_slot_name("class") == "Record"
    assert gen.get_metamodel_slot_name("classes") == "Records"
    assert gen.get_metamodel_slot_name("Classes") == "Records"
    assert gen.get_metamodel_slot_name("Mixins") == "Traits"

    gen.serialize(directory=tmp_path)
    assert_mdfile_contains(tmp_path / "index.md", "Address", after="Records")
    assert_mdfile_contains(tmp_path / "index.md", "HasAliases", after="Traits")
