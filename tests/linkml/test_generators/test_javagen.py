import logging

import pytest
from click.testing import CliRunner

from linkml.generators.javagen import JavaBundle, JavaGenerator, cli
from linkml.generators.oocodegen import OOEnum, OOEnumValue
from tests.linkml.utils.fileutils import assert_file_contains

PACKAGE = "org.sink.kitchen"


def test_javagen_records(kitchen_sink_path, tmp_path):
    """Generate java records"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path), template_variant="records")
    assert_file_contains(
        tmp_path / "Address.java",
        "public record Address(String street, String city, BigDecimal altitude)",
        after="package org.sink.kitchen",
    )


def test_javagen_primitive_types(input_path, tmp_path):
    """Test that primitive types are boxed unless they are required."""
    gen = JavaGenerator(input_path("primitive_types.yaml"))
    gen.serialize(directory=str(tmp_path))
    expected = [
        "int requiredInteger",
        "Integer optionalInteger",
        "float requiredFloat",
        "Float optionalFloat",
        "double requiredDouble",
        "Double optionalDouble",
        "boolean requiredBoolean",
        "Boolean optionalBoolean",
    ]
    for decl in expected:
        assert_file_contains(tmp_path / "SimpleClass.java", decl)


def test_javagen_with_custom_template(kitchen_sink_path, tmp_path):
    """Generate java records with a custom template.

    This should yield the same code as the test above, but by forcefully
    specifying the class-records template, instead of specifying the "records"
    variant and letting the generator pick the corresponding template.
    """

    gen = JavaGenerator(
        kitchen_sink_path,
        package=PACKAGE,
        template_file="packages/linkml/src/linkml/generators/javagen/class-records.jinja2",
    )
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(
        tmp_path / "Address.java",
        "public record Address(String street, String city, BigDecimal altitude)",
        after="package org.sink.kitchen",
    )


def test_javagen_classes(kitchen_sink_path, tmp_path):
    """Generate java classes"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "Address.java", "public class Address", after="package org.sink.kitchen")


def test_javagen_classes_and_enums(kitchen_sink_path, tmp_path):
    """Generate both Java classes and enums."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE, true_enums=True)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(
        tmp_path / "CordialnessEnum.java", "public enum CordialnessEnum", after="package org.sink.kitchen"
    )
    assert_file_contains(
        tmp_path / "Relationship.java", "private CordialnessEnum cordialness;", after="package org.sink.kitchen"
    )


def test_generate_enum_objects(kitchen_sink_path):
    """Generate object representation of enums.

    Note that this is really a feature of OOCodeGenerator and not of
    JavaGenerator, but since OOCodeGenerator is abstract it has to be
    tested through a derived concrete class.
    """
    gen = JavaGenerator(kitchen_sink_path)
    enum_definitions = gen.schemaview.all_enums()
    enum_objects = gen.generate_enum_objects(enum_definitions)

    # Check that all enums are present
    for name in enum_definitions.keys():
        assert name in enum_objects

    # Check that one enum is complete
    expected_enum = OOEnum(
        name="FamilialRelationshipType",
        enum_uri="https://w3id.org/linkml/tests/kitchen_sink/FamilialRelationshipType",
    )
    expected_enum.values = [
        OOEnumValue(label="SIBLING_OF", text="SIBLING_OF"),
        OOEnumValue(label="PARENT_OF", text="PARENT_OF"),
        OOEnumValue(label="CHILD_OF", text="CHILD_OF"),
    ]
    assert expected_enum == enum_objects["FamilialRelationshipType"]

    # Same, but with an enum with names that must be transformed
    expected_enum = OOEnum(
        name="OtherCodes",
        enum_uri="https://w3id.org/linkml/tests/kitchen_sink/OtherCodes",
    )
    expected_enum.values = [OOEnumValue(label="a_b", text="a b")]
    assert expected_enum == enum_objects["other codes"]


def test_create_documents_includes_enums(kitchen_sink_path):
    """Check that the code generator generates documents for enums."""
    # Default mode: enums should not be included
    gen = JavaGenerator(kitchen_sink_path, true_enums=False)
    docs = gen.create_documents()
    assert not [doc for doc in docs if doc.enums]

    # "True enums" mode: one document per enum
    gen = JavaGenerator(kitchen_sink_path, true_enums=True)
    docs = gen.create_documents()
    enum_docs = [doc for doc in docs if doc.enums]
    assert len(enum_docs) == 8  # 7 enums in kitchen sink + 1 in core

    # A document contains either a class or an enum, but not both
    assert not [doc for doc in docs if doc.classes and doc.enums]


def test_do_not_generate_linkmlany_class(kitchen_sink_path, tmp_path):
    """Check that linkml:Any is rendered as Object."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    docs = gen.create_documents()
    assert not [doc for doc in docs if doc.name == "AnyObject"]
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "Event.java", "private Object metadata;", after="package org.sink.kitchen")


def test_oo_objects_have_uris(kitchen_sink_path):
    """Check that OOClass and OOField objects contain URIs."""
    gen = JavaGenerator(kitchen_sink_path)
    docs = gen.create_documents()
    witness = [doc for doc in docs if doc.name == "Company"][0]
    assert witness.classes[0].class_uri == "https://w3id.org/linkml/tests/kitchen_sink/Company"
    assert witness.classes[0].fields[0].slot_uri == "http://schema.org/ceo"


def test_slot_aliases_used_when_required(input_path, tmp_path):
    """Check that field names are based on slot aliases when present."""
    gen = JavaGenerator(input_path("personinfo.yaml"), use_aliases=True)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "Person.java", "private Integer age;")


def test_visitor_generation(kitchen_sink_path, tmp_path):
    """Check that we can generator a visitor interface."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path), visitors=["Concept"])
    assert_file_contains(tmp_path / "IConceptVisitor.java", "public void visit(DiagnosisConcept visited);")
    assert_file_contains(tmp_path / "ProcedureConcept.java", "public void accept(IConceptVisitor visitor)")


def test_generation_for_org_incenp_linkml_runtime(kitchen_sink_path, tmp_path):
    """Check that we can generate code suitable for incenp.org's LinkML-Java runtime."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path), template_variant="org.incenp.linkml")
    assert_file_contains(tmp_path / "Concept.java", '@LinkURI("https://w3id.org/linkml/tests/kitchen_sink/Concept")')
    assert_file_contains(tmp_path / "Concept.java", '@LinkURI("https://w3id.org/linkml/tests/core/id")')
    assert_file_contains(tmp_path / "Concept.java", '@SlotName("in_code_system")')


def test_org_incenp_linkml_primitive_equals(input_path, tmp_path):
    """Primitive fields in org.incenp.linkml template must generate valid equals()."""
    gen = JavaGenerator(input_path("primitive_types.yaml"))
    gen.serialize(directory=str(tmp_path), template_variant="org.incenp.linkml")
    assert_file_contains(tmp_path / "SimpleClass.java", "this$requiredBoolean != other$requiredBoolean")


def test_org_incenp_linkml_uriorcurie_rendered_as_string(input_path, tmp_path):
    """Uriorcurie-typed slots in org.incenp.linkml templates should be rendered as String fields."""
    gen = JavaGenerator(input_path("personinfo.yaml"))
    gen.serialize(directory=str(tmp_path), template_variant="org.incenp.linkml")
    assert_file_contains(tmp_path / "NamedThing.java", "private String id")


def test_refined_slots(input_path, tmp_path):
    """Test that OOCodeGen provides required infos about refined slots."""
    gen = JavaGenerator(input_path("refined_derived_slots.yaml"))
    expected = {
        ("Foo", "bar"): [],
        ("Foo", "bars"): [],
        ("FirstDerivedFoo", "bar"): ["Bar"],
        ("FirstDerivedFoo", "bars"): ["List<Bar>"],
        ("SecondDerivedFoo", "bar"): [],
        ("SecondDerivedFoo", "bars"): [],
        ("ThirdDerivedFoo", "bar"): ["FirstDerivedBar", "Bar"],
        ("ThirdDerivedFoo", "bars"): ["List<FirstDerivedBar>", "List<Bar>"],
    }
    for doc in gen.create_documents():
        for klass in doc.classes:
            for field in klass.all_fields:
                exp = expected[(klass.name, field.name)]
                if exp is not None:
                    assert exp == field.refined_ranges


def test_refined_ranges(input_path):
    """Test that OOCodeGen correctly infers refined ranges."""
    gen = JavaGenerator(input_path("refined_derived_slots.yaml"))

    # Refined ranges in subclasses
    # - Subclasses of Foo refine the bar slot twice
    assert gen.get_refined_ranges("bar", "Foo") == ["FirstDerivedBar", "SecondDerivedBar"]
    # - Subclasses of FirstDerivedFoo refine it once
    assert gen.get_refined_ranges("bar", "FirstDerivedFoo") == ["SecondDerivedBar"]
    # - Likewise, subclasses of SecondDerivedFoo refine the slot once
    assert gen.get_refined_ranges("bar", "SecondDerivedFoo") == ["SecondDerivedBar"]
    # - No more refinement from ThirdDerivedFoo
    assert gen.get_refined_ranges("bar", "ThirdDerivedFoo") == []

    # Refined ranges in superclasses
    # - Foo is the defining class for the slot, no refinement possible
    assert gen.get_refined_ranges("bar", "Foo", upwards=True) == []
    # - FirstDerivedFoo refines the slot compared to its parent Foo
    assert gen.get_refined_ranges("bar", "FirstDerivedFoo", upwards=True) == ["Bar"]
    # - SecondDerivedFoo does not refine the slot compared to its parent FirstDerivedFoo
    assert gen.get_refined_ranges("bar", "SecondDerivedFoo", upwards=True) == []
    # - ThirdDerivedFoo refines the slot compared to its parent SecondDerivedFoo;
    #   this is the second refinement in the hierarchy since the defining class
    assert gen.get_refined_ranges("bar", "ThirdDerivedFoo", upwards=True) == ["FirstDerivedBar", "Bar"]


def test_inherited_extra_slots(input_path, tmp_path):
    """Test that we don't generate redundant extension holders."""
    gen = JavaGenerator(input_path("redundant_extra_slots.yaml"))
    assert gen.needs_extra_slots(gen.schemaview.get_class("Foo"))
    assert not gen.needs_extra_slots(gen.schemaview.get_class("Bar"))
    gen.serialize(directory=str(tmp_path), template_variant="org.incenp.linkml")
    assert_file_contains(tmp_path / "Foo.java", "private Map<String, Object> extraSlots;")
    assert_file_contains(tmp_path / "Bar.java", "private Map<String, Object> extraSlots;", invert=True)


def test_render_returns_bundle(kitchen_sink_path, tmp_path):
    """`render()` returns a `JavaBundle` with rendered files but touches no disk."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    bundle = gen.render()

    assert isinstance(bundle, JavaBundle)
    assert bundle.package == PACKAGE
    assert "Address.java" in bundle.files
    address_code = bundle.files["Address.java"]
    assert "public class Address" in address_code
    assert f"package {PACKAGE}" in address_code

    # render() must not write anything to disk.
    assert list(tmp_path.iterdir()) == []


def test_render_template_variant(kitchen_sink_path):
    """`render(template_variant=...)` is honoured (records variant here)."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    bundle = gen.render(template_variant="records")

    assert "Address.java" in bundle.files
    assert "public record Address(String street, String city, BigDecimal altitude)" in bundle.files["Address.java"]


def test_render_visitors(kitchen_sink_path, caplog):
    """`render(visitors=[...])` emits the visitor interface and adds `accept()` to visited classes."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    with caplog.at_level(logging.INFO, logger="linkml.generators.javagen"):
        bundle = gen.render(visitors=["Concept", "InexistingClass"])

    assert "IConceptVisitor.java" in bundle.files
    assert "public void visit(DiagnosisConcept visited);" in bundle.files["IConceptVisitor.java"]
    # A class in the visited hierarchy carries the accept() method.
    assert "ProcedureConcept.java" in bundle.files
    assert "public void accept(IConceptVisitor visitor)" in bundle.files["ProcedureConcept.java"]

    # A warning should be emitted if a class to visit can't be found in the schema
    assert any("InexistingClass does not appear to be a valid name" for msg in caplog.messages)


def test_render_true_enums(kitchen_sink_path):
    """With `true_enums=True`, enum-typed files appear in the bundle."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE, true_enums=True)
    bundle = gen.render()

    assert "CordialnessEnum.java" in bundle.files
    assert "public enum CordialnessEnum" in bundle.files["CordialnessEnum.java"]


def test_serialize_accepts_rendered_module(kitchen_sink_path, tmp_path):
    """Passing `rendered_module=` writes the given bundle as-is."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    bundle = gen.render()
    bundle.files["Address.java"] = "// sentinel: pre-rendered bundle content"

    gen.serialize(directory=str(tmp_path), rendered_module=bundle)

    assert_file_contains(tmp_path / "Address.java", "// sentinel: pre-rendered bundle content")


@pytest.mark.parametrize("as_path", [False, True], ids=["str", "Path"])
def test_serialize_accepts_str_or_path_directory(kitchen_sink_path, tmp_path, as_path):
    """`directory` accepts both a ``str`` and a :class:`pathlib.Path`."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    directory = tmp_path if as_path else str(tmp_path)

    gen.serialize(directory=directory)

    assert_file_contains(tmp_path / "Address.java", "public class Address", after=f"package {PACKAGE}")


def _write_minimal_schema(path):
    path.write_text(
        "id: https://example.org/pkg\n"
        "name: pkg\n"
        "imports:\n"
        "  - linkml:types\n"
        "classes:\n"
        "  Thing:\n"
        "    attributes:\n"
        "      id:\n"
        "        range: string\n"
    )
    return path


def _java_config_yaml(package: str) -> str:
    """The same `generator_args.java.package` shape used by gen-project's config.yaml."""
    return f"generator_args:\n  java:\n    package: {package}\n"


def test_cli_config_file_sets_package(tmp_path):
    """--config-file's `generator_args.java.package` sets the Java package when --package is not given."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "myconfig.yaml"
    config_path.write_text(_java_config_yaml("org.example.fromconfig"))
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        ["--config-file", str(config_path), "--output-directory", str(out_dir), str(schema_path)],
    )

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package org.example.fromconfig")


def test_cli_explicit_package_overrides_config_file(tmp_path):
    """An explicit --package always takes precedence over --config-file."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "myconfig.yaml"
    config_path.write_text(_java_config_yaml("org.example.fromconfig"))
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        [
            "--config-file",
            str(config_path),
            "--package",
            "org.example.explicit",
            "--output-directory",
            str(out_dir),
            str(schema_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package org.example.explicit")


def test_cli_config_file_without_java_package_falls_back_to_default(tmp_path):
    """A config file with no `generator_args.java.package` falls through to the `example` default."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "myconfig.yaml"
    config_path.write_text("generator_args:\n  owl:\n    mergeimports: true\n")
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        ["--config-file", str(config_path), "--output-directory", str(out_dir), str(schema_path)],
    )

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package example")


def test_cli_invalid_config_package_warns_but_is_used(tmp_path, caplog):
    """An invalid Java package name from the config file warns but is still emitted verbatim."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "myconfig.yaml"
    config_path.write_text(_java_config_yaml("1bad.pkg"))
    out_dir = tmp_path / "out"

    with caplog.at_level(logging.WARNING):
        result = CliRunner().invoke(
            cli,
            ["--config-file", str(config_path), "--output-directory", str(out_dir), str(schema_path)],
        )

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package 1bad.pkg")
    assert any("not a valid Java package name" in record.message for record in caplog.records)


@pytest.mark.parametrize(
    ("config_yaml", "where"),
    [
        pytest.param("- 1\n- 2\n", "the top level", id="top-level-list"),
        pytest.param("generator_args: notamapping\n", "'generator_args'", id="scalar-generator-args"),
        pytest.param(
            "generator_args:\n  java: package=org.example.model\n",
            "'generator_args.java'",
            id="scalar-section",
        ),
    ],
)
def test_cli_config_file_malformed_section_errors(tmp_path, config_yaml, where):
    """A malformed --config-file fails loudly. A malformed `generator_args.java` in
    particular must not be skipped over, leaving the user with the `example` default
    and no clue why their configured package was ignored."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "myconfig.yaml"
    config_path.write_text(config_yaml)

    result = CliRunner().invoke(cli, ["--config-file", str(config_path), str(schema_path)])

    assert result.exit_code != 0
    assert f"expected a YAML mapping at {where}" in str(result.output) + str(result.exception)


def test_cli_config_file_real_project_config_shape(tmp_path):
    """gen-java's --config-file accepts a full, real-world gen-project config.yaml
    (other generators' sections, excludes/includes, etc.) and only reads
    generator_args.java.package out of it, ignoring the rest."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "excludes:\n"
        "  - markdown\n"
        "generator_args:\n"
        "  excel:\n"
        "    mergeimports: true\n"
        "  owl:\n"
        "    mergeimports: true\n"
        "    metaclasses: false\n"
        "  java:\n"
        "    mergeimports: true\n"
        "    package: org.example.fromrealproject\n"
        "  python:\n"
        "    mergeimports: true\n"
    )
    out_dir = tmp_path / "out"

    result = CliRunner().invoke(
        cli,
        ["--config-file", str(config_path), "--output-directory", str(out_dir), str(schema_path)],
    )

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package org.example.fromrealproject")


def test_cli_ignores_config_yaml_in_cwd(tmp_path, monkeypatch):
    """A `config.yaml` in the cwd is never read implicitly: --config-file must be explicit."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    (tmp_path / "config.yaml").write_text(_java_config_yaml("org.example.cwd"))
    out_dir = tmp_path / "out"
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(cli, ["--output-directory", str(out_dir), str(schema_path)])

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package example")


def test_cli_no_config_file_falls_back_to_default(tmp_path, monkeypatch):
    """No --config-file: falls through to the `example` default."""
    schema_path = _write_minimal_schema(tmp_path / "pkg.yaml")
    out_dir = tmp_path / "out"
    monkeypatch.chdir(tmp_path)

    result = CliRunner().invoke(cli, ["--output-directory", str(out_dir), str(schema_path)])

    assert result.exit_code == 0, result.output
    assert_file_contains(out_dir / "Thing.java", "public class Thing", after="package example")
