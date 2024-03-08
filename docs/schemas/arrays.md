---
file_format: mystnb
mystnb:
    output_stderr: remove
    render_text_lexer: python
    render_markdown_format: myst
myst:
    enable_extensions: ["colon_fence"]
---
```{index} Arrays
```
(arrays)=
# Arrays

We can divide data types into a few [abstract forms](https://en.wikipedia.org/wiki/Abstract_data_type)
(see ["Recognizing Structural Forms"](structural-forms)). Linked data tools regularly handle scalars, lists,
tables, graphs, and trees, but less commonly handle multidimensional arrays. Arrays are
ubiquitous in real data, though, and LinkML has first-class support to specify them.

## Specification

### Terms

```{admonition} TODO
Document the terms used in the spec
```

### Forms

```{admonition} TODO
Document the "four forms" (if we want to go with that organization)

- any shape
- anonymous shape
- labeled dimensions
- mixed
```

Example documentation of a single form using the below convenience functions:

```{code-cell}
---
tags: [hide-cell]
---
from linkml.generators import PydanticGenerator
from linkml.generators.pydanticgen.black import format_black
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.dumpers.yaml_dumper import YAMLDumper
from IPython.display import display, Markdown


from pathlib import Path

schemas = Path('.').resolve().parent / '_includes' / 'arrays'

COMPARISON = """
:::::{{tab-set}}
::::{{tab-item}} LinkML
:::{{code-block}} yaml
{linkml}
:::
::::
::::{{tab-item}} pydantic
:::{{code-block}} python
{pydantic}
:::
::::
:::::
"""

def render_class(path, cls) -> str:
    generator = PydanticGenerator(str(path), pydantic_version=2)
    module = generator.render()
    cls = module.classes[cls]
    code = cls.render()
    code = format_black(code)
    return code

def render_comparison(path, cls, string=False) -> str:
    path = str(path)
    sch = YAMLLoader().load_as_dict(path)
    class_def = sch['classes'][cls]
    class_str = YAMLDumper().dumps(class_def)
    pydantic_str = render_class(path, cls)
    md = COMPARISON.format(linkml=class_str, pydantic=pydantic_str)
    if string:
        return md
    else:
        display(Markdown(md))
    
```

```{code-cell}
sch = schemas / 'mixed_shape.yaml'
render_comparison(sch, 'MixedAnyShapeArray')
```

## Generators

### Support

Which generators support what?

| generator               | representation | anyshape | anonymous | labeled | mixed |
|-------------------------|----------------|----------|-----------|---------|-------|
| [pydantic](pydanticgen) | List of Lists  | Y        | Y         | Y       | Y     |
| [pydantic](pydanticgen) | Numpydantic    | X        | X         | X       | X     |
| ... (the rest of em)    |                |          |           |         |       |
| 

### Implementation Guidance

```{admonition} TODO
Document {class`~linkml.generators.pydanticgen.array.ArrayRangeGenerator` and examples
of recursive JSON-schema 
```

## See Also

- [How-to: Multidimensional arrays](howto-arrays) - discussion about the problems with array specification in linked data
- [Tricky Choices](tricky-choices) - Some further discussions of decisions made in the specification

## References



