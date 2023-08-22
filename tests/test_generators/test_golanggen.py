from linkml.generators.golanggen import GolangGenerator


def test_golanggen(kitchen_sink_path):
    """typescript"""
    code = GolangGenerator(kitchen_sink_path, mergeimports=True).serialize()

    def assert_in(s: str) -> None:
        assert s.replace(" ", "") in code.replace(" ", "")

    assert "package kitchen" in code
    assert_in("type Person struct {")
    assert_in("HasFamilialRelationships []FamilialRelationship")
    assert_in("CodeSystems []CodeSystem")
