# Schema Linter

When authoring a schema -- especially when it is large or there are many authors -- it is important to establish and adhere to best practices. For example, while [providing a description](./metadata.md#providing-descriptions) for each schema element is not required, descriptions can help reduce miscommunication between schema authors. LinkML provides a configurable [linter](https://en.wikipedia.org/wiki/Lint_(software)) to identify violations of best practices or error-prone patterns.

## Introduction

The `linkml-lint` command performs checks on a schema which -- while valid -- may not represent best practices or may indicate a likely mistake in the schema. These checks are referred to as [rules](#rules) and without additional [configuration](#configuration) a default set of rules will be used.

To lint a single schema file:
```bash
linkml-lint schema.yaml
```

To recursively lint a directory of schema files:
```bash
linkml-lint schemas
```

## Configuration

The `linkml-lint` command can be configured with a YAML configuration file. The configuration file can be provided using the `--config` command line option:

```bash
linkml-lint --config myconfig.yaml myschema.yaml
```

Alternatively, if there is a file named `.linkmllint.yaml` in the current working directory when you run `linkml-lint` that file will automatically be loaded as the configuration file. If all or most of the schema files in a project can be checked with the same rules, storing the configuration at the root of the project in a `.linkmllint.yaml` file can make it more convenient to check them without having to pass the `--config` option.

Here is an example of a configuration file which includes all the recommended rules and enables an additional rule named `no_empty_title`:

```yaml
# Use all the recommended rules and also enable the no_empty_title rule
extends: recommended
rules:
  no_empty_title:
    level: error
```

The `extends` field of the configuration file allows you to inherit from an existing configuration. Currently the only valid value for this field is `recommended`.

The `rules` field is a dictionary where each key is a rule name and the value is the configuration for that rule. Every rule has at least one configurable property: `level`. Each rule's `level` can be set to `disabled` (the default) meaning the schema will not be checked with that rule, or `level` can be set to `warning` or `error`. If set to `warning` or `error` the schema will be checked with that rule and violations will be reported. The distinction between `warning` and `error` is solely cosmetic and is designed to help you prioritize issues to fix. If you are unsure there is no harm in only using the `error` level. Some rules have additional configuration beyond the `level` property, as described in the [Rules](#rules) section.

To use the recommended configuration set except for one of the rules, manually specify `level: disabled` for that rule:

```yaml
# Use the recommended rule set except for the standard_naming rule
extends: recommended
rules:
  standard_naming:
    level: disabled
```

It is also acceptable to _not_ extend the recommended set. Simply omit the `extends` field from your configuration. In that case, only the rules that your configuration enables are checked:

```yaml
# Only the no_empty_title and standard_naming rules will be checked
rules:
  no_empty_title:
    level: error
  standard_naming:
    level: error
```

## Rules

Rule names denoted with a star ⭐ are part of the `recommended` configuration set.

### canonical_prefixes ⭐

Enforce canonical prefixes by verifying that the mappings defined in the schema's `prefixes` slot agree with those provided by the [prefixmaps](https://github.com/linkml/prefixmaps) package.

**Additional Configuration**
* `prefixmaps_contexts`: The list of context names which will be loaded by the `prefixmaps` library to do the validation. The order of names is meaningful and will be preserved. See also: [prefixmaps documentation](https://github.com/linkml/prefixmaps#usage). Default: `[merged]`

### no_empty_title

Disallow empty titles on schema elements.

### no_invalid_slot_usage ⭐

Disallow `slot_usage` definitions where the name of the slot does not refer to an existing slot of the class.

### no_xsd_int_type ⭐

Disallow use of `uri: xsd:int` in type definitions. In nearly all cases, `xsd:integer` should be used instead.

### permissible_values_format

Enforce consistent formatting of enum permissible values. This rule may conflict with the `standard_naming` rule, but it is more flexible.

**Additional Configuration**
* `format`: The enforced format of enum permissible values. Special values "snake", "uppersnake", "camel", and "kebab" will be recognized, otherwise the value will be interpreted as a regular expression. Default: `uppersnake`.

### recommended ⭐

Require any slot in the [metamodel](./metamodel) with `recommended: true` (e.g. `description`) to be provided.

**Additional Configuration**
* `include`: If specified, only elements with the provided names will be checked. Default: `[]`.
* `exclude`: All elements except the ones with names specified in this list will be checked. Default: `[]`.

### standard_naming ⭐

Enforce standard naming conventions: CamelCase for classes, snake_case for slots, CamelCase for enums, snake_case (default) or UPPER_SNAKE for permissible_values (see `permissible_values_upper_case` option). This rule may conflict with the `permissible_values_format` rule.

**Additional Configuration**
* `permissible_values_upper_case`: If `true`, permissible values will be checked for UPPER_SNAKE, otherwise snake_case. Default: `false`.
* `class_pattern`: If specified, permissible format pattern for classes can be provided either as one of the following pattern `snake`, `uppersnake`, `camel`, `uppercamel`, `kebab` or as regular expression (e.g. `"[a-z][_a-z0-9]+"` for snake case)
* `slot_pattern`: If specified, permissible format pattern for slots can be provided in analogy to `class_pattern`.

### tree_root_class

Require a single class with `tree_root: true` and optionally verify that class's name.

* `validate_existing_class_name`: If `true`, in addition to validating that a `tree_root: true` ClassDefinition exists, the rule will also validate that is has the name provided by the `root_class_name` option. Default: `false`.
* `root_class_name`: The name of the root class. Default: `Container`.

## Reports

By default, if the `linkml-lint` command identifies violations of the configured rules it will print the files and issues to the terminal. This behavior can be changed with the `--format` and `--output` command line options. 

The valid values for `--format` are terminal (the default), markdown, json, and tsv.

If the `--output` option is provided the report will be written to the specified file instead of the terminal.

For example, to generate a markdown report in a file named `linter-results.md`:

```bash
linkml-lint --format markdown --output linter-results.md myschema.yaml
```

## Exit Codes

If the linter does not encounter any rule violations at all it will exit with code `0`. 

If the linter encounters rule violations with `level: error` it will exit with code `2`. This will be the case regardless of whether there are also rule violations with `level: warning`.

By default, if the linter encounters _only_ rule violations with `level: warning` it will exit with code `1`. This behavior can be changed with command line options. In this scenario, if the `--ignore-warnings` flag is provided the exit code will be `0`. If instead the `--max-warnings <int>` option is passed, the exit code will be `1` or `0` depending on whether the number of warning rule violations is greater than the provided number or not. If both `--ignore-warnings` and `--max-warnings` are used `--ignore-warnings` takes precedence. 

## API Docs

```{eval-rst}
.. click:: linkml.linter.cli:main
    :prog: linkml-lint
    :commands:
```