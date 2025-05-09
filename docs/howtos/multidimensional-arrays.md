(howto-arrays)=
# Multidimensional Arrays

```{important}
With the release of LinkML 1.7.0. 
[The LinkML metamodel has first-class N-dimensional array 
support](https://github.com/linkml/linkml-model/releases/tag/v1.7.0) -- this guide
will be updated as support is built into tooling.
This page is a historical reference for considerations made during the
development of the specification, and will be integrated elsewhere in the docs.

See [Schema/arrays](arrays) for more information on specifying arrays
```


## Background

Multidimensional arrays (Also: N-dimensional arrays, or here just
"Arrays") are essential for scientific computing - yet many modeling
languages lack first class support for arrays.

Consider for example measurements taken from x and y coordinates, with an additional time axis:

![img](https://user-images.githubusercontent.com/50745/183749279-806a3ae9-e279-40eb-8a41-27f83ccc24eb.png)

__FIGURE__: example 4 x 4 x 3 array (taken from NetCDF documentation)


The natural representation for this in scientific computing is a 3D
array indexed by three coordinates. For example, to access the
measurement for `x=2, y=3, time=1` we would conventionally write this using notation such as `[2][3][1]`, yielding the value `231`.

(the values in this example are of course not real, we just use these values for illustration)

Many modeling frameworks such as SQL and LinkML lack the concepts of N-dimensional arrays as first-class entities. Of course, the same information can be modeled directly by representing each measurement using some kind of measurement class/object/table/record.

This can be thought of as a *narrow table* representation

|x|y|time|value|
|---|---|---|---|
|1|1|1|111|
|1|1|2|112|
|...|...|...|...|
|4|4|3|443|

In SQL elements may be accessed using syntax like

```sql
SELECT value FROM measurement WHERE x=2 and y=3 and time=1
```


when serialized in JSON this may look like a list of objects:

```json
[
  {
    "x":1,
    "y":1,
    "time":1,
    "value":111,
  },
]
```

This has the value of having an unambiguous representation (provided the keys are sufficiently defined), and being amenable to standard json operations.

And in RDF, as a collection of nodes (possibly blank) with properties for each axis:

```turtle
[:x 1, :y 1, :time 1, :value 111],
...
```

We use properties like `:x` for illustration, these could be taken from vocabularies such as wgs84, which provides additional semantics to the representation.

However, these representations are not natural for scientific
computing purposes, where it is more conventional to have some kind of
first class array representation, which is often preferable both for
data science and efficiency reasons.

## Alternatives: Wide table representation

For scientific computing purposes, we may choose to implement a different JSON serialization, such as a list of lists of lists (LoLoLs):

```json
[
   [
       [111, 211, 311, 411],
       [121, 221, 321, 421],
       "..."
   ],
   "...",
   [
       "...",
       [143, 243, 343, 443]
   ]
]
```

This can be thought of as an N-dimensional generalization of a "wide
table", in contrast to the "narrow table" representation above. Note
that for 2D arrays, a direct wide array representation in SQL would be
*possible* (with column names corresponding to axis values like
1,2,3,4), this would be highly non-idiomatic.

This representation is quite convenient for scientific computing. The underlying data typically maps to
an N-dimensional (nested lists) in many languages:

```python
>>> measurements = yaml.safe_load(open("lolol.yaml"))
>>> measurements[0][0][0]
111
```

However, this relies on out of band information to interpret the list of lists.

We can get around this by embedding the LoLoLol in an object with additional metadata, as in the netCDF example above. Here we will switch to YAML for compactness:

```yaml
dimensions:
  x: 4
  y: 4
  time:  ## unlimited
variables:
  x: float
  y: float
  time: float
  value: float
axes:
  x: [10, 20, 30, 40]
  y: [110, 120, 130, 140]
  time: [31, 59, 90]
values:
  [[[111,211,311,411],...],....,[...,[143,243,343,443]]]
```

(note that it is valid to represent yaml lists using `[...]` notation. Using `-` notation is more common, but gets awkward for LoLoLs)

This is better but it still relies on conventions, e.g. that `axes` `values` and so on have a particular *interpretation*.

Note that there is currently no way to schematize the direct LoLoLol representation in LinkML

We may alternatively choose to represent as a single linearized list, as in the netCDF example above:

```yaml
values: [111, 211, ..., 343, 443]
```

This example uses a generalization of [column-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order)

![img](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Row_and_column_major_order.svg/280px-Row_and_column_major_order.svg.png)

This has certain compactness advantages, but it too relies on certain
conventions - in fact additional conventions, such as whether row or
column ordering is used.

This is also slightly less convenient for direct computation, as we have to compute the mapping between the index tuple and the linearization index. We might write a subroutine for this:

```python
def lookup(data, x, y, time) -> float:
  return data[(x-1) + (y-1)*4 + (z-1)*4*4]
```

(generalizing this to any array or use the offsets is left as an exercise for the reader)

This is suboptimal for many broader uses.

The philosophy of LinkML is one of *pluralism*, we like to give people
the abstractions that make most sense for their applications.

Here we give our current recommendations for representing
N-dimensional arrays for scientific computing. Note these are
preliminary, and may change in future!

## N-Dimensional Arrays in LinkML


To illustrate this, we will start with some example YAML data, similar to the above:

```yaml
x:
  values: [10, 20, 30, 40]
y:
  values: [110, 120, 130, 140]
time:
  values: [31, 59, 90]
temperatures: [111, 211, ..., 343, 443]
```

Note that this uses the *linearized* representation of array values,
which we said was suboptimal: without any further context the above
data is highly ambiguous when removed from its original context.

We solve this by providing sufficient metadata in the schema:

```yaml
id: https://example.org/arrays
name: arrays-example
prefixes:
  linkml: https://w3id.org/linkml/
  wgs84: http://www.w3.org/2003/01/geo/wgs84_pos#
  example: https://example.org/
default_prefix: example
imports:
  - linkml:types

classes:
  TemperatureMatrix:
    implements:
      - linkml:ThreeDimensionalArray
      - linkml:ColumnOrderedArray
    attributes:
      x:
        implements:
          - linkml:axis0
        range: LatitudeSeries
      y:
        implements:
          - linkml:axis1
        range: LongitudeSeries
      time:
        implements:
          - linkml:axis2
        range: DaySeries
      temperatures:
        implements:
          - linkml:elements
        multivalued: true
        range: float
        required: true
        unit:
          ucum_code: K

  LatitudeSeries:
    description: A series whose values represent latitude
    implements:
      - linkml:OneDimensionalSeries
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        unit:
          ucum_code: deg
          
  LongitudeSeries:
    description: A series whose values represent longitude
    implements:
      - linkml:OneDimensionalSeries
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        unit:
          ucum_code: deg
          
  DaySeries:
    description: A series whose values represent the days since the start of the measurement period
    implements:
      - linkml:OneDimensionalSeries
    attributes:
      values:
        range: float
        multivalued: true
        implements:
          - linkml:elements
        unit:
          ucum_code: a
```

This relies on a feature implemented in LinkML 1.5,
[implements](https://w3id.org/linkml/implements). This provides
information for tools to *interpret* the axes and elements.

In particular:

 - our `TemperatureMatrix` class *implements* `linkml:ThreeDimensionalArray`
 - the 3 axes class *implements* `linkml:OneDimensionalSeries`
 - the values *implements* `linkml:elements`

The classes and slots that are referenced bia *implements* can be thought of as *templates*.

Currently this only serves *documentative* purposes; default LinkML
tooling will use the *direct* linearized representation.

This means we can't use standard tuple access notation:

```python
>>> from my_model import TemperatureMatrix
>>> mm = TemperatureMatrix(**yaml.safe_load(open("data.yaml")))
>>> print(mm.temperatures[0][0][0])
TypeError: 'float' object is not subscriptable
```

However, we at least have an unambiguous interpretation of the elements

### JSON and YAML serialization

The *direct* linear sequence serialization is currently default.

In future, the LinkML will allow for conversion between a nested list representation and the linearized sequence via the LinkML *normalizer*.

See:

 - https://w3id.org/linkml/docs/specification/06mapping

### Serialization to HDF5, Zarr, and other matrix formats

We exploring how this work can be used in the context of other formats and standards:

- [Zarr](https://zarr.readthedocs.io/en/stable/) Zarr is a file storage format for chunked, compressed, N-dimensional arrays based on an open-source specification.
- [HDF5](https://www.hdfgroup.org/solutions/hdf5/) supports n-dimensional datasets and each element in the dataset may itself be a complex object.
- [the The Hierarchical Data Modeling Framework¶](https://hdmf.readthedocs.io/en/stable/) (HDMF) is a Python package for working with standardizing, reading, and writing hierarchical object data (such as HDF5 or Zarr)
- [Network Common Data Form](https://www.unidata.ucar.edu/software/netcdf/) (netCDF) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. It is also a community standard for sharing scientific data
- [CORAL](https://github.com/jmchandonia/CORAL) is a framework developed at Berkeley Lab for rigorous self-validated data modeling and integrative, reproducible data analysis.

Currently LinkML does not have a defined serialization to
matrix-oriented formats like HDF5 or Zarr. The LinkML N-Dimensional
Array working group
[@ndarray-wg](https://github.com/orgs/linkml/teams/ndarray-wg) is
exploring options for a native serialization that would leverage the
Array templates, potentially integrating with HDMF and/or CORAL.

### Enhanced python serializations

One option we are exploring is an alternative python/pydantic
generation where there are convenient methods/properties for accessing
elements using array index tuples.

We are also exploring ways in which we can drop in plugins to libraries such as `xarray` or `numpy`

## Further discussion

Feel free to open an issue and tag [@ndarray-wg](https://github.com/orgs/linkml/teams/ndarray-wg)
