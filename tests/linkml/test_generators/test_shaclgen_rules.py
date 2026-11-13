import logging

from linkml.generators.shaclgen import ShaclGenerator


def test_supported_rules_do_not_warn(input_path, caplog):
    schema = input_path("supported_rules.yaml")
    with caplog.at_level(logging.WARNING):
        ShaclGenerator(str(schema)).serialize()
    assert "Rule not emitted" not in caplog.text


def test_unsupported_rules_warn(input_path, caplog):
    schema = input_path("rule_probe.yaml")
    with caplog.at_level(logging.WARNING):
        ShaclGenerator(str(schema)).serialize()
    assert "Rule not emitted as SHACL" in caplog.text
    assert "Numeric" in caplog.text
    assert "Disjunction" in caplog.text


def test_no_warn_when_emit_rules_false(input_path, caplog):
    schema = input_path("rule_probe.yaml")
    with caplog.at_level(logging.WARNING):
        ShaclGenerator(str(schema), emit_rules=False).serialize()
    assert "Rule not emitted" not in caplog.text
