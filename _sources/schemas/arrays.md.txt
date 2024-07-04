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
```{role} feature
```


(arrays)=
# Arrays

```{versionadded} 1.8.0
from Jonny Saunders, Ryan Ly, and Chris Mungall [`#1887`](https://github.com/linkml/linkml/pull/1887), [`linkml-model#181`](https://github.com/linkml/linkml-model/pull/181)
```

---

We can divide data types into a few [abstract forms](https://en.wikipedia.org/wiki/Abstract_data_type)
(see ["Recognizing Structural Forms"](structural-forms)). Linked data tools regularly handle scalars, lists,
tables, graphs, and trees, but less commonly handle multidimensional arrays. The LinkML metamodel has first-class support 
to specify them, and its generators are growing first-class support to make those specifications work with
array formats and libraries that people actually use. 

## Types

There are two types of array specification in LinkML:

- [**NDArrays**](#ndarrays) - "regular" dense multidimensional arrays with shape and dtype constraints 
- {feature}`Coming Soon` **Labeled Arrays** - arrays that use additional arrays as their indices (eg. a set of temperature measurements indexed by latitude and longitude).

## NDArrays

```{code-cell}
---
tags: [hide-cell]
---
from linkml.generators import PydanticGenerator
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.dumpers.yaml_dumper import YAMLDumper
from IPython.display import display, Markdown
from pathlib import Path
import numpy as np
from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from rich.color import Color

theme = Theme({
    "repr.call": Style(color=Color.from_rgb(110,191,38), bold=True),
    "repr.attrib_name": Style(color="slate_blue1"),
    "repr.number": Style(color="deep_sky_blue1"),
    
})
console = Console(theme=theme)

schemas = Path('.').resolve().parent / '_includes' / 'arrays'

COMPARISON = """
:::::{{tab-set}}
::::{{tab-item}} LinkML
:::{{code-block}} yaml
{linkml}
:::
::::
::::{{tab-item}} pydantic - LoL
:::{{code-block}} python
{pydantic_lol}
:::
::::
::::{{tab-item}} numpydantic
:::{{admonition}} Coming Soon
Direct support for array libraries like numpy, hdf5, dask, zarr, and xarray with pydantic validation <3
::: 
::::
:::::
"""

def render_module(path):
    generator = PydanticGenerator(str(path), array_representations=['list'])
    module = generator.render()
    return module
    
def compile_module(path):
    generator = PydanticGenerator(str(path), array_representations=['list'])
    module = generator.compile_module()
    return module

def render_class(path, cls) -> str:
    module = render_module(path)
    cls = module.classes[cls]
    code = cls.render(black=True)
    return code

def render_comparison(path, cls, string=False) -> str:
    if not isinstance(cls, list):
        cls = [cls]
        
    path = str(path)
    sch = YAMLLoader().load_as_dict(path)
    class_strs = []
    pydantic_strs = []
    
    for a_cls in cls:
        class_def = sch['classes'][a_cls]
        class_def = {a_cls: class_def}
        class_strs.append(YAMLDumper().dumps(class_def))
        pydantic_strs.append(render_class(path, a_cls))
        
    class_str = "\n".join(class_strs)
    pydantic_str = "\n".join(pydantic_strs)
    md = COMPARISON.format(linkml=class_str, pydantic_lol=pydantic_str)
    if string:
        return md
    else:
        display(Markdown(md))
    
``` 
 
NDArrays are a *slot-level* feature - they augment the usual [slot `range`](slots.md#ranges) syntax with an `array` property.

For example, A class with a `data` slot which consists of array of integers between 2 and 5 dimensions and its 
{class}`~linkml.generators.pydanticgen.PydanticGenerator` {mod}`~linkml.generators.pydanticgen.array` representations look like:

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'example.yaml'
render_comparison(sch, 'MyClass')
example_mod = compile_module(sch)
MyClass = getattr(example_mod, 'MyClass')
```

The generated pydantic model can validate all the constraints of the array, serialize it to JSON,
and everything else that you'd expect from a pydantic model.

This model correctly validates:
```{code-cell}

model = MyClass(data=np.ones((5,4,3), dtype=int))
console.print(model)
```

But an array with the wrong shape doesn't:
```{code-cell}
---
tags: ['hide-output']
---
try:
    MyClass(data=np.ones((1,)))
except Exception as e:
    console.print(e)
```

Nor does an array with the wrong type

```{code-cell}
---
tags: ['hide-output']
---
try:
    MyClass(data=np.random.rand(5,4,3))
except Exception as e:
    console.print(e)
```

### Specification

NDArrays are defined by an {class}`~linkml_runtime.linkml_model.meta.ArrayExpression` ([metamodel docs](https://linkml.io/linkml-model/latest/docs/ArrayExpression/))

An `ArrayExpression` has many of the default properties other LinkML expressions have -- you can annotate your arrays like the rest of your data.
To define the array, an `ArrayExpression` uses the following unique properties:

```{rubric} Shape
```

Shape can be specified numerically:

```{py:data} maximum_number_dimensions
:type: int | False | None

Maximum (inclusive) number of dimensions. 

When used with `dimensions`, to differentiate with being unset or `None`, needs to be set to ``False`` explicitly to indicate 
an "infinite"[^infinity] number of dimensions (see [Complex Shaped Arrays](ComplexShape))
```

```{py:data} minimum_number_dimensions
:type: int | None

Minimum (inclusive) number of dimensions.
```

```{py:data} exact_number_dimensions
:type: int | None

An exact number of dimensions.

Equivalent to `minimum_number_dimensions` and `maximum_number_dimensions` being equal `int`s
```

```{py:data} dimensions
:type: list[DimensionExpression]

Parameterization of individual dimensions (see below)
```

```{rubric} Dimensions
```

Dimensions can be further parameterized by defining `dimensions` with a list of {class}`.DimensionExpression`s, which accept:

```{py:data} alias
:type: str | None

The name of the dimension
```

```{py:data} maximum_cardinality
:type: int | None

The maximum size of this dimension (inclusive). If `None`, no maximum is set
```

```{py:data} minimum_cardinality
:type: int | None

The minimum size of this dimension (inclusive). If `None`, no minimum is set
```

```{py:data} exact_cardinality
:type: int | None

The exact size of this dimension. Equivalent to `minimum_cardinality` and `maximum_cardinality` being equal `int`s
```

(array-forms)=
### Shape Forms

The combinations of the different {class}`.ArrayExpression` properties imply four NDArray forms:

- [Any Shape](AnyShapeArrays) - Arrays without limits to their shape
- [Bounded Shape](BoundedShape) - Arrays with constraints on the number of dimensions without further parameterization
- [Parameterized Shape](ParameterizedShape) - Arrays with parameterized dimensions
- [Complex Shape](ComplexShape) - Arrays with both constraints on the number of dimensions and parameterized dimensions

(AnyShapeArrays)=
#### Any

An Any shaped array can take any shape. This is the simplest array form, indicating the mere presence of an array.

An any shaped array is specified with an empty `array` dictionary:

:::::{tab-set}
::::{tab-item} LinkML
:::{code-block} yaml
AnyType:
  attributes:
    array:
      range: AnyType
      array: {}

Typed:
  attributes:
    array:
      range: integer
      array: {}
:::
::::
::::{tab-item} pydantic - LoL
:::{code-block} python
class AnyType(ConfiguredBaseModel):
    array: Optional[AnyShapeArray] = Field(None)

class Typed(ConfiguredBaseModel):
    array: Optional[AnyShapeArray[int]] = Field(None)
:::
::::
::::{tab-item} numpydantic
:::{admonition} Coming Soon
Direct support for array libraries like numpy, hdf5, dask, zarr, and xarray with pydantic validation <3
::: 
::::
:::::

The resulting pydantic models use a special {class}`AnyShapeArray` class injected by pydanticgen's 
{mod}`~linkml.generators.pydanticgen.template` system when using the List of List (LoL) representation 
(see [Representations](array-representations)). 


````{note}
In the future, Any shape arrays might also be able to be specified with an explicit `None` value, e.g.:

```yaml
MyClass:
  attributes:
    data:
      range: integer
      array:
```

This is a technical limitation in {class}`.SchemaView` - see [`linkml-model#189`](https://github.com/linkml/linkml-model/pull/189) and [`#1975`](https://github.com/orgs/linkml/discussions/1975)

````

(BoundedShape)=
#### Bounded

We have already seen so-called "Bounded" shaped arrays, which don't add any additional parameterization beyond
the number of their dimensions.

The `maximum_`, `minimum_`, and `exact_number_dimensions` properties can be used in combination to indicate...

A minimum without a maximum, using the {class}`AnyShapeArray` model internally -

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'bounded_shape.yaml'
render_comparison(sch, 'MinDimensions')
```

A maximum without a minimum -

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'bounded_shape.yaml'
render_comparison(sch, 'MaxDimensions')
```

An exact number of dimensions - 

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'bounded_shape.yaml'
render_comparison(sch, 'ExactDimensions')
```

And a range of dimensions -

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'bounded_shape.yaml'
render_comparison(sch, 'RangeDimensions')
```

(ParameterizedShape)=
#### Parameterized

Dimensions can be further parameterized, giving them names and cardinality constraints.

Similarly to bounded arrays, the following demonstrate setting a single-dimensional array with cardinality constraints...

Minimum cardinality:

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'parameterized_shape.yaml'
render_comparison(sch, 'MinCard')
```

Maximum cardinality:

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'parameterized_shape.yaml'
render_comparison(sch, 'MaxCard')
```

Exact cardinality:

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'parameterized_shape.yaml'
render_comparison(sch, 'ExactCard')
```

Cardinality range:

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'parameterized_shape.yaml'
render_comparison(sch, 'RangeCard')
```

And they can be used together, for example one can specify 

> A four dimensional array such that
> 
> - The first dimension has at least two items
> - The second dimension has at most five items
> - The third dimension has between two and five items
> - The fourth dimension has exactly six items

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'parameterized_shape.yaml'
render_comparison(sch, 'ParameterizedArray')
parameterized_mod = compile_module(sch)
ParameterizedArray = getattr(parameterized_mod, 'ParameterizedArray')
```

Which validates each of the constraints separately:

```{code-cell}
array = np.arange(4*1*2*6,dtype=int).reshape((4,1,2,6))
# array = np.ones((4,1,2,6), dtype=int)

console.print(ParameterizedArray(array=array))
```

(ComplexShape)=
#### Complex

Complex NDArrays combine all three of the prior forms.

For example:

> An array with between 5 and 7 dimensions such that...
> 
> - The first dimension has at least two items
> - The second dimension has at most five items
> - The third dimension has between two and five items
> - The fourth dimension has exactly six items

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'complex_shape.yaml'
render_comparison(sch, 'ComplexRangeShapeArray')
```

The only place where the syntax of complex arrays differ is that `minimum` and `maximum_number_dimensions`
are set at the length of the specified `dimensions` list by default. In order to specify an array
with a fixed number of parameterized dimensions with an arbitrary number of additional dimensions,
set `maximum_number_dimensions` to `False` :

```{code-cell}
---
tags: ['hide-input']
---
sch = schemas / 'complex_shape.yaml'
render_comparison(sch, 'ComplexAnyShapeArray')
```

## Generators

### Support

At release, only pydanticgen supports arrays, but arrays will be implemented gradually for the rest of the generators.

| generator                 | representation | anyshape | bounded | parameterized | complex |
|---------------------------|----------------|----------|-----------|---------|-------|
| [pydantic](pydanticgen)   | List of Lists  | Y        | Y         | Y       | Y     |
| [pydantic](pydanticgen)   | Numpydantic    | X        | X         | X       | X     |
| ... (the rest of em)      |                |          |           |         |       |

(array-representations)=
### Representations

Since arrays are unlike other data types in that they usually require some specialized libraries to handle them,
and many formats don't have a single canonical array type, generators may accommodate multiple array
representations.

The pydantic generator currently supports a "List of lists" style array representation to be able to use
arrays without any additional external dependencies beyond pydantic. 

See each [generator](../generators/index.rst)'s documentation page for a summary of the array representations they support.

```{admonition} Numpy And Friends
We are in the process of implementing an additional pydantic array representation that can
directly work with numpy-style arrays, including lazy loading and passthrough array routines for
several major array libraries as a standalone package. See {mod}`numpydantic` 
```

### Implementation Guidance

```{admonition} TODO
Implementation docs for arrays are forthcoming.
 
For now see {class}`~linkml.generators.pydanticgen.array.ArrayRangeGenerator`
and {class}`~linkml.generators.pydanticgen.array.ListOfListsArray` 
as the reference implementation
```

## See Also

- [How-to: Multidimensional arrays](howto-arrays) - discussion about the problems with array specification in linked data
- [Tricky Choices](tricky-choices) - Some further discussions of decisions made in the specification

## References

- [ArrayExpression](https://linkml.io/linkml-model/latest/docs/ArrayExpression/) metamodel specification



[^infinity]: Of course, Python has a recursion limit and every array library only supports a finite number of dimensions. 
    Infinite in this case just means that the abstract specification sets no limit, and the implementations try and meet that as best they can.