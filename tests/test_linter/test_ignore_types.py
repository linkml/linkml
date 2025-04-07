import yaml

from linkml.linter.linter import Linter
from linkml.utils.schema_builder import SchemaBuilder


def test_class_empty_title_forbidden():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    # print("\n")
    # for m in messages:
    #     print(m)

    assert len(messages) == 1
    assert any("Class 'MyClass' has no title" in m for m in messages)


def test_class_empty_title_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - class_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_slot_empty_title_forbidden():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 1
    assert any("Slot 'my_slot' has no title" in m for m in messages)


def test_slot_empty_title_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - slot_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_enum_empty_title_forbidden():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 1
    assert any("Enum 'MyEnum' has no title" in m for m in messages)


def test_enum_empty_title_allowed():
    config = yaml.safe_load(
        """
rules:
  no_empty_title:
    level: error
    exclude_type:
      - enum_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


# todo PVs are not checked for titles yet


def test_class_missing_recommendeds_forbidden():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 1
    assert any("'MyClass' does not have recommended slot 'description'" in m for m in messages)


def test_class_missing_recommendeds_allowed():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
    exclude_type:
      - class_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_class("MyClass")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_slot_missing_recommendeds_forbidden():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 1
    assert any("Slot 'my_slot' does not have recommended slot 'description'" in m for m in messages)


def test_slot_missing_recommendeds_allowed():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
    exclude_type:
      - slot_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my_slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


def test_enum_missing_recommendeds_forbidden():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 1
    assert any("Enum 'MyEnum' does not have recommended slot 'description'" in m for m in messages)


def test_enum_missing_recommendeds_allowed():
    config = yaml.safe_load(
        """
rules:
  recommended:
    level: error
    exclude_type:
      - enum_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0


# todo PVs are not checked for recommended fields yet


def test_class_default_non_standard_name_forbidden():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_class("my class")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 1
    assert any("Class has name 'my class'" in m for m in messages)


def test_class_default_non_standard_name_allowed():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
    exclude_type:
      - class_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_class("my class")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 0


def test_slot_default_non_standard_name_forbidden():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 1
    assert any("Slot has name 'my slot'" in m for m in messages)


def test_slot_default_non_standard_name_allowed():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
    exclude_type:
      - slot_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_slot("my slot")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 0


def test_enum_default_non_standard_name_forbidden():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("my enum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 1
    assert any("Enum has name 'my enum'" in m for m in messages)


def test_enum_default_non_standard_name_allowed():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
    exclude_type:
      - enum_definition
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("my enum")

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    print("\n")
    for m in messages:
        print(m)

    assert len(messages) == 0


def test_pv_default_non_standard_name_forbidden():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum", permissible_values=["pv 1"])

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 1
    assert any("Permissible value of Enum 'MyEnum' has name 'pv 1'" in m for m in messages)


def test_pv_default_non_standard_name_allowed():
    config = yaml.safe_load(
        """
rules:
  standard_naming:
    level: error
    exclude_type:
      - permissible_value
"""
    )

    builder = SchemaBuilder()
    builder.add_enum("MyEnum", permissible_values=["pv 1"])

    linter = Linter(config)
    report = list(linter.lint(builder.schema))

    messages = [p.message for p in report]

    assert len(messages) == 0
