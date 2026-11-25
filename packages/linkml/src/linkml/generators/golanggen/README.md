# Golang Generator (`golanggen`)

Generates idiomatic Go code from LinkML schemas. Supports custom templates
via the `--template-dir` CLI option.

## JSON tag preservation

By default a field's JSON tag is the snake-cased slot name (`underscore(slot.alias or slot.name)`).
Some pipelines need CURIE keys instead (for example a JSON-LD CURIE such as
`demo:id`, which contains a colon). The tag is resolved with the following
precedence:

1. **Slot CURIE** -- with `--use-curies` (or `use_curies=True`), each
   non-identifier slot uses its CURIE, resolved with `SchemaView.get_curie`.
   This is the same resolution used by the JSON-LD Context
   generator and the JSON Schema generator under their `--use-curies` flags, so
   Go JSON tags agree with their keys for non-identifier slots. Identifier slots
   retain their ordinary alias/name, matching those generators' identifier-key
   behavior. For non-identifier slots, a declared `slot_uri` is compacted to its
   CURIE (e.g. `demo:id`); a slot without a declared URI is synthesized as
   `<default_prefix>:<name>` (e.g. `ex:name`) and compacted.
2. **Automatic fallback** -- when `--use-curies` is not set and snake-casing
   changes the key (e.g. an alias containing `-` or whitespace), the original
   `slot_alias` is used as the JSON tag. This mirrors the Pydantic generator's
   `Field(alias=...)` behavior.
3. **Default** -- the snake-cased slot alias (unchanged legacy behavior).

The CURIE mode is opt-in: output is unchanged when it is not enabled. Only the
JSON tag is affected; `go_name` is still derived from `camelcase(slot_alias)` so
the exported Go field identifier stays valid (colons never leak into the field
name). The negative CLI form is `--not-use-curies`, matching the sibling
generators.

Example (`ex` is the schema's `default_prefix`):

```yaml
prefixes:
  ex: https://example.org/
  demo: https://example.org/demo/
default_prefix: ex

classes:
  Entity:
    slots:
      - id
      - demo_id

slots:
  id:
    range: string
    required: true
    identifier: true
  demo_id:
    range: string
    slot_uri: demo:id
```

with `--use-curies` generates:

```go
type Entity struct {
 Id     string  `json:"ex:id"`
 DemoId *string `json:"demo:id,omitempty"`
}
```

## Custom Templates

Pass `--template-dir <dir>` to override any built-in template. Place a file
with the same name as the default template in your directory; the generator
will pick it up automatically and fall back to the built-in version for any
template not present in your directory.

### Overridable templates

| Template                  | Description                                       |
| ------------------------- | ------------------------------------------------- |
| `module.go.jinja`         | Top-level package file (entry point)              |
| `struct.go.jinja`         | Individual struct definition                      |
| `field.go.jinja`          | Single struct field                               |
| `enum.go.jinja`           | Const block for enum-like values                  |
| `imports.go.jinja`        | Import statements                                 |
| `jsonld_wrapper.go.jinja` | JSON-LD wrapper struct (used via `{% include %}`) |

## Template Variables Reference

### `module.go.jinja`

Top-level template rendered once per schema.

| Variable            | Type             | Description                                                                                       |
| ------------------- | ---------------- | ------------------------------------------------------------------------------------------------- |
| `package_name`      | `str`            | Go package name (from `--package`, else derived from schema name)                                 |
| `imports`           | `str`            | Rendered import block (from `imports.go.jinja`)                                                   |
| `enums`             | `dict[str, str]` | Rendered enum blocks keyed by enum name                                                           |
| `structs`           | `dict[str, str]` | Rendered struct blocks keyed by struct name                                                       |
| `struct_names`      | `list[str]`      | Names of all non-alias structs                                                                    |
| `root_struct_names` | `list[str]`      | Names of structs **not** used as a field type in any other struct (i.e. top-level / root classes) |

### `struct.go.jinja`

Rendered once per class.

| Variable           | Type                     | Description                                              |
| ------------------ | ------------------------ | -------------------------------------------------------- |
| `name`             | `str`                    | CamelCase struct name                                    |
| `description`      | `str \| None`            | Class description (rendered as `//` comment)             |
| `embedded_structs` | `list[str] \| None`      | Parent/mixin struct names for Go embedding (inheritance) |
| `fields`           | `dict[str, str] \| None` | Rendered field strings keyed by field name               |
| `is_type_alias`    | `bool`                   | `True` when the struct is a simple type alias            |
| `type_alias_value` | `str \| None`            | Target type for aliases (e.g. `string`)                  |

### `field.go.jinja`

Rendered once per slot/field.

| Variable      | Type          | Description                                                                            |
| ------------- | ------------- | -------------------------------------------------------------------------------------- |
| `go_name`     | `str`         | CamelCase field name for Go                                                            |
| `json_name`   | `str`         | Name used in the JSON struct tag (see [JSON tag preservation](#json-tag-preservation)) |
| `type`        | `str`         | Go type string (e.g. `string`, `int`, `[]Person`, `*Address`)                          |
| `required`    | `bool`        | Whether the field is required                                                          |
| `identifier`  | `bool`        | Whether the field is the identifier slot                                               |
| `key`         | `bool`        | Whether the field is a key slot                                                        |
| `description` | `str \| None` | Field description (rendered as `//` comment)                                           |
| `pattern`     | `str \| None` | Regex pattern constraint                                                               |
| `omitempty`   | `bool`        | Whether to add `,omitempty` to the JSON tag (default `True`)                           |

### `enum.go.jinja`

Rendered once per enum.

| Variable      | Type                        | Description                                 |
| ------------- | --------------------------- | ------------------------------------------- |
| `name`        | `str`                       | CamelCase enum type name                    |
| `type`        | `str`                       | Underlying Go type (default `string`)       |
| `description` | `str \| None`               | Enum description (rendered as `//` comment) |
| `values`      | `dict[str, GolangConstant]` | Constants keyed by permissible value name   |

Each `GolangConstant` in `values` has:

| Field         | Type          | Description                                              |
| ------------- | ------------- | -------------------------------------------------------- |
| `name`        | `str`         | Constant name (e.g. `FamilialRelationshipTypeSIBLINGOF`) |
| `value`       | `str \| None` | Literal value                                            |
| `description` | `str \| None` | Constant description                                     |

### `imports.go.jinja`

Rendered in two contexts:

**Single import** (`Import` model):

| Variable | Type          | Description                                         |
| -------- | ------------- | --------------------------------------------------- |
| `module` | `str`         | Import path (e.g. `time`, `github.com/example/pkg`) |
| `alias`  | `str \| None` | Optional import alias                               |

**Import block** (`Imports` model):

| Variable  | Type        | Description                         |
| --------- | ----------- | ----------------------------------- |
| `imports` | `list[str]` | List of rendered individual imports |

## Pro tip: Include extra manifests

You can include extra manifests with following trick:

First create in your directory structure a new jinja template file.

Example: `jsonld_wrapper.go.jinja`

```jinja
// JsonLD{{ name }} is a JSON-LD wrapper for {{ name }}
type JsonLD{{ name }} struct {
    Context     map[string]interface{} `json:"@context"`
    PayloadType string                 `json:"@type"`
    Payload     {{ name }}             `json:",inline"`
}
```

Then update the `module.go.jinja`

```jinja
// Code generated by linkml-golanggen. DO NOT EDIT.
package {{ package_name }}

import (
{% if imports and imports.strip() %}
{{ imports | replace("import (", "") | replace(")", "") }}
{% endif %}
    "encoding/json"
    "reflect"
)
{% if enums %}
{% for e in enums.values() %}
{{ e }}
{% endfor %}
{% endif %}
{% for s in structs.values() %}
{{ s }}
{% endfor %}
{% for name in root_struct_names %}
{% include "jsonld_wrapper.go.jinja" %}
{% endfor %}
```

Finally run the command with option `--template-dir <dir>` where `<dir>` is the directory containing your custom templates
