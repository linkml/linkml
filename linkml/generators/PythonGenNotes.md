# Notes on the python generator
## Code generation for LinkML slots
The generation of slot entries in class definitions is split into two parts:
1) The declaration of the slot type
2) The `__post_init__` processing transforms several allowable input forms into single, consistent internal representation.

The elements that control the python for slot generation include
* Whether `range` references an instance of a LinkML `type` or a LinkML `class`
* If the slot range is a `class`:
    * Whether the class has a key (`key: <type>`), an identifier (`identifier: <type>`), or neither
    * _If_ the class has a `key` or `identifier`, whether the instances are inlined as a dictionary (`inlined: true`), 
    inlined as a list (`inlined_as_list: true`) or are referenced elsewhere in the model (Default).
* Whether the slot is or concrete (`abstract: false`) or abstract (`abstract: true` or `mixin: true`) (Default: `false`)
* Whether a slot is required (`required: true`) or optional (`required: false`) (Default: `false`)
* Whether a slot is single-valued (`multivalued: false`) or multi-valued  (`multivalued: true`) (Default: `false`)
* The `ifabsent` attribute  (not covered in this document)
* The `default` value (not covered in this document)

These various situations are described more detail below:
### 1) Slot range is a LinkML `type` definition
LinkML type definitions can take one of three forms:
1) Builtin python type
    ```yaml
    types:
       <type>:
          base: <builtin python type> (e.g. 'str', 'int', 'float', etc)
          ...
    ```
2) Defined type
    ```yaml
    types:
       <type>:
          base: <type defined in linkml/linkml_runtime/utils/metamodelcore.py> (e.g. URIorCURIE, Date, NCName, etc)
          ...
    ```

3) Inherited type
    ```yaml
    types:
       <type>:
          typeof: <parent type>
    ```
Each of these are outlined below
#### 1) Python generation for basic python Type.  For this example, we show basic permutations on the python `int` type as a base
YAML:
```yaml
types:
  integer:
    uri: xsd:integer
    base: int
    description: An integer

classes:
    Integers:
      description: various permutations of the integer type
      attributes:
        opt_integer:
          range: integer
        mand_integer:
          range: integer
          required: true
        opt_multi_integer:
          range: integer
          multivalued: true
        mand_multi_integer:
          range: integer
          multivalued: true
          required: true
```
Generated Python:
```python
...

class Integer(int):
    """ An integer """
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "integer"
    type_model_uri = METATYPE.Integer

@dataclass
class Integers(YAMLRoot):
    """
    various permutations of the integer type
    """
    ...

    mand_integer: int = None
    mand_multi_integer: Union[int, List[int]] = None
    opt_integer: Optional[int] = None
    opt_multi_integer: Optional[Union[int, List[int]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.mand_integer is None:
            raise ValueError("mand_integer must be supplied")
        if not isinstance(self.mand_integer, int):
            self.mand_integer = int(self.mand_integer)

        if self.mand_multi_integer is None:
            raise ValueError("mand_multi_integer must be supplied")
        elif not isinstance(self.mand_multi_integer, list):
            self.mand_multi_integer = [self.mand_multi_integer]
        elif len(self.mand_multi_integer) == 0:
            raise ValueError(f"mand_multi_integer must be a non-empty list")
        self.mand_multi_integer = [v if isinstance(v, int) else int(v) for v in self.mand_multi_integer]

        if self.opt_integer is not None and not isinstance(self.opt_integer, int):
            self.opt_integer = int(self.opt_integer)

        if self.opt_multi_integer is None:
            self.opt_multi_integer = []
        if not isinstance(self.opt_multi_integer, list):
            self.opt_multi_integer = [self.opt_multi_integer]
        self.opt_multi_integer = [v if isinstance(v, int) else int(v) for v in self.opt_multi_integer]

        super().__post_init__(**kwargs)
```
The python first emits a class declaration for the base class -- in this case, the class `Integer` which derives from
the builtin type `int`.  Four class variables are included in the generation:
* `type_class_uri` - the URIRef for the type itself
* `type_class_curie` - the string CURIE representation of the type
* `type_name` - the non-mangled name assigned to the type in the original definition
* `type_model_uri` - the URIRef of the type definition in the default LinkML namespace

The python then emits a class definition for the `Integers` classe, where we have defined four slot type permutations:

1) `mand_integer` - a single valued required type:

    * The type, `int`, is from the `base` attribute. The python generator does make use of strictly positional parameters,
    so all type declarations will have an appropriate default, which is `None` in this case:
    
        `mand_integer: int = None`
    
    * Check for the presence of the value itself:
        ``` 
        if self.mand_integer is None:
            raise ValueError("mand_integer must be supplied")
        ```
    * Coerce the input value to `int` if it isn't one already:
        ```
        if not isinstance(self.mand_integer, int):
            self.mand_integer = int(self.mand_integer)
        ```

2) `mand_multi_integer` - a mandatory list of integers

    * Accept _either_ a list of integers or a single integer, which will be converted to a list:
    
        `mand_multi_integer: Union[int, List[int]] = None` 
    
    * Check that the value is present.  _Note:_ LinkML treats an empty list as the same as an absent value.
     
        ```
            if self.mand_multi_integer is None:
                raise ValueError("mand_multi_integer must be supplied")
        ```
    * Convert a non-list value into a list.  This allows constructors to be lazy when it comes to single valued entries.
    Note, however, that this _does_ require that list-of-list constructs to be explicitly declared because, while the 
    code treats `x = C(1)` as the same as `x = C([1])` in the multivalued case, it does _not_ attempt to differentiate
    `x = C([1])` and `x = C([[1]])`. This could be done if there is a compelling reason to, however:
    
        ```        
        elif not isinstance(self.mand_multi_integer, list):
            self.mand_multi_integer = [self.mand_multi_integer]
        ```
    *  Check that the mandatory list has at least one element (our definition of `mandatory list`:
        ```        
        elif len(self.mand_multi_integer) == 0:
            raise ValueError(f"mand_multi_integer must be a non-empty list")
        ```
    * Coerce all of the member of the list into the target type (`int`):
    
        `self.mand_multi_integer = [v if isinstance(v, int) else int(v) for v in self.mand_multi_integer]`
            
3) `opt_integer` - Optional non-list.
    * Accept either an `int` or `None`, the latter being entailed in the `Optional` type:
        `opt_integer: Optional[int] = None`
        
    * Coerce to an integer if the value is present, otherwise let it be:
        ```        
        if self.opt_integer is not None and not isinstance(self.opt_integer, int):
            self.opt_integer = int(self.opt_integer)
        ```
    * Type is `Optional[<type>]`
    * `__post_init__` adds type coercion if necessary
    
4) `opt_multi_integer`: list:
    * Accept one of `None`, `int`, list of `int`, or anything that can be coerced into `List[int]`:
    
        `opt_multi_integer: Optional[Union[int, List[int]]] = empty_list()`
        
    * The absence of a list property is always represented as an emtpy list:
        ```        
        if self.opt_multi_integer is None:
            self.opt_multi_integer = []
        ```
      
    * Coerce any other non-list into a list:
        ```        
        if not isinstance(self.opt_multi_integer, list):
            self.opt_multi_integer = [self.opt_multi_integer]
        ```
      
    * Coerce all the members of the list into the range type
        ```        
        self.opt_multi_integer = [v if isinstance(v, int) else int(v) for v in self.opt_multi_integer]
        ```

    
### 2) Python generation for a Type defined in `metamodelcore.py` -- `XSDDate` in this example
YAML:
```yaml
types:
  date:
    uri: xsd:date
    base: XSDDate
    repr: str
    description: a date (year, month and day) in an idealized calendar

classes:
  Dates:
    description: various permutations of the date type
    attributes:
      opt_date:
        range: date
      mand_date:
        range: date
        required: true
      opt_multi_date:
        range: date
        multivalued: true
      mand_multi_date:
        range: date
        multivalued: true
        required: true

```
python:
```python
class Date(XSDDate):
    """ a date (year, month and day) in an idealized calendar """
    type_class_uri = XSD.date
    type_class_curie = "xsd:date"
    type_name = "date"
    type_model_uri = METATYPE.Date

@dataclass
class Dates(YAMLRoot):
    """
    various permutations of the date type
    """
    ...

    mand_date: Union[str, XSDDate] = None
    mand_multi_date: Union[Union[str, XSDDate], List[Union[str, XSDDate]]] = None
    opt_date: Optional[Union[str, XSDDate]] = None
    opt_multi_date: Optional[Union[Union[str, XSDDate], List[Union[str, XSDDate]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.mand_date is None:
            raise ValueError("mand_date must be supplied")
        if not isinstance(self.mand_date, XSDDate):
            self.mand_date = XSDDate(self.mand_date)

        if self.mand_multi_date is None:
            raise ValueError("mand_multi_date must be supplied")
        elif not isinstance(self.mand_multi_date, list):
            self.mand_multi_date = [self.mand_multi_date]
        elif len(self.mand_multi_date) == 0:
            raise ValueError(f"mand_multi_date must be a non-empty list")
        self.mand_multi_date = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.mand_multi_date]

        if self.opt_date is not None and not isinstance(self.opt_date, XSDDate):
            self.opt_date = XSDDate(self.opt_date)

        if self.opt_multi_date is None:
            self.opt_multi_date = []
        if not isinstance(self.opt_multi_date, list):
            self.opt_multi_date = [self.opt_multi_date]
        self.opt_multi_date = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.opt_multi_date]

        super().__post_init__(**kwargs)
```
The generated python for this type is identical to that of the builtin type with the exception that type declarations
are the `Union` of the class representing the element and the `repr` element (e.g. `XSDDate` and `str`):

`int` type:

        mand_multi_integer: Union[int, List[int]] = None
        
`XSDDate` type:

        mand_multi_date: Union[Union[str, XSDDate], List[Union[str, XSDDate]]] = None

#### 3) Python generation for an inherited Type

The following YAML shows three inherited types - one that inherits from a builtin type, a second from a metamodelcore
type and a third from a the inherited type.
```yaml
types:
  InheritedType:
    typeof: integer

  InheritedType2:
    typeof: uriorcurie

  InheritedType3:
    typeof: InheritedType2
```
Python:
```python
# Types
class InheritedType(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "InheritedType"
    type_model_uri = PTYPES.InheritedType


class InheritedType2(Uriorcurie):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "InheritedType2"
    type_model_uri = PTYPES.InheritedType2


class InheritedType3(InheritedType2):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "InheritedType3"
    type_model_uri = PTYPES.InheritedType3

     ...

@dataclass
class InheritedTypes(YAMLRoot):
    """
    various permutations of a typeof referencing a builtin
    """
    ...

    mand_InheritedType: Union[int, InheritedType] = None
    mand_multi_InheritedType: Union[Union[int, InheritedType], List[Union[int, InheritedType]]] = None
    opt_InheritedType: Optional[Union[int, InheritedType]] = None
    opt_multi_InheritedType: Optional[Union[Union[int, InheritedType], List[Union[int, InheritedType]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.mand_InheritedType is None:
            raise ValueError("mand_InheritedType must be supplied")
        if not isinstance(self.mand_InheritedType, InheritedType):
            self.mand_InheritedType = InheritedType(self.mand_InheritedType)

        if self.mand_multi_InheritedType is None:
            raise ValueError("mand_multi_InheritedType must be supplied")
        elif not isinstance(self.mand_multi_InheritedType, list):
            self.mand_multi_InheritedType = [self.mand_multi_InheritedType]
        elif len(self.mand_multi_InheritedType) == 0:
            raise ValueError(f"mand_multi_InheritedType must be a non-empty list")
        self.mand_multi_InheritedType = [v if isinstance(v, InheritedType) else InheritedType(v) for v in self.mand_multi_InheritedType]

        if self.opt_InheritedType is not None and not isinstance(self.opt_InheritedType, InheritedType):
            self.opt_InheritedType = InheritedType(self.opt_InheritedType)

        if self.opt_multi_InheritedType is None:
            self.opt_multi_InheritedType = []
        if not isinstance(self.opt_multi_InheritedType, list):
            self.opt_multi_InheritedType = [self.opt_multi_InheritedType]
        self.opt_multi_InheritedType = [v if isinstance(v, InheritedType) else InheritedType(v) for v in self.opt_multi_InheritedType]

        super().__post_init__(**kwargs)
```
The Python patterns for each of the inherited types (Inherited from basic (e.g. `int`), inherited from metamodelcore.py
(e.g. `uriorcurie`) or from another type are identical to those generated above for `XSDDate`

### 2) Slot range is a LinkML `class` definition
The previous section described the Python that was generated for slot ranges that reference LinkML **Type** definitions.
This section addresses the second use case, where the slot range references another LinkML **Class**.  Classes are
a more complex example, because, as opposed to types, classes can either be represented by _value_ or, if they have been 
declared to have unique identifiers, by _reference_.  In addition, classes that are represented by value can either be
represented as lists of values or dictionaries. 

The following attributes control how the python is generated for a LinkML `class` definition:
* The slot `abstract` setting
* The slot `required` setting
* The slot `multivalued` setting
* Whether a class includes a slot identified as a "key" (`"key": true`), an "identifier" (`"identifier": true`) or 
neither.  Note that at the moment, a class may have at most one key or identifier slot.  Two keys, two identifiers or
a key and an identifier are all considered errors.  It is anticipated that a future version of LinkML will allow
multiple key slots, directly implementing the notion of a "compound key".
* The slot `inlined` and `inlined_as_list` properties
* The slot `ifabsent` attribute
* The slot `default` value

Various permutations of these cases are described below:

#### 1) Non-keyed, non-identified classes
Classes without keys or identifiers cannot only be realized inline.  The following code shows examples of various
permutations of this type of class:

```yaml
classes:
  OptionalOneElementRange:
    description: Range is a optional class that contains one non-key/non-identifier element
    attributes:
      v1:
        range: OneElementClass

  RequiredOneElementRange:
    description: Range is a required class that contains one non-key/non-identifier element
    is_a: OptionalOneElementRange
    attributes:
      v1:
        range: OneElementClass
        required: true

  OptionalOneElementRangeList:
    description: Range is a optional list of a class that contain one non-key/non-identifier element
    attributes:
      v1:
        range: OneElementClass
        multivalued: true

  RequiredThreeElementRangeList:
    description: Range is a required list of a class that contain one non-key/non-identifier element
    attributes:
      v1:
        range: ThreeElementClass
        multivalued: true
        required: true
```

An optional, single element class generates the following code:

```python
@dataclass
    class OptionalOneElementRange(YAMLRoot):
        """
        Range is a optional class that contains one non-key/non-identifier element
        """
        ...
    
        v1: Optional[Union[dict, OneElementClass]] = None
    
        def __post_init__(self, **kwargs: Dict[str, Any]):
            if self.v1 is not None and not isinstance(self.v1, OneElementClass):
                self.v1 = OneElementClass(**self.v1)
    
            super().__post_init__(**kwargs)
```
`v1` can be one of: 
* `None` - as in indicated by the `Optional` type
* any python `dict`, which is the type that underlies all class representations
* an instance of `OneElementClass`

The only additional initialization code coerces the input to a OneElementClass if it exists (is not `None`) and it isn't
already an instance.

Switching from optional to required produces:

```python
@dataclass
class RequiredOneElementRange(YAMLRoot):
    """
    Range is a required class that contains one non-key/non-identifier element
    """
    ...

    v1: Union[dict, OneElementClass] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, OneElementClass):
            self.v1 = OneElementClass(**self.v1)

        super().__post_init__(**kwargs)
```
Which is the same as the previous example, with the exception that the value, `v1` _must_ be supplied.

The third example, an optional list of `OneElementClass` instances:

```python
@dataclass
class OptionalOneElementRangeList(YAMLRoot):
    """
    Range is a optional list of a class that contain one non-key/non-identifier element
    """
    ...

    v1: Optional[Union[Union[dict, OneElementClass], List[Union[dict, OneElementClass]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, list):
            self.v1 = [self.v1]
        self.v1 = [v if isinstance(v, OneElementClass) else OneElementClass(**v) for v in self.v1]

        super().__post_init__(**kwargs)
```
Accepts any of:
* `None` - the list is not present
* An empty list (`[]`) - same semantics as `None`
* A dictionary
* An instance of `OneElementClass`
* A list of dictionaries and/or `OneElementClass` instances

The code:
1) translates the `None` value into the equivalent empty list
2) converts a naked dict or `OneElementClass` instance into a single element list
3) coerces the list of zero or more items into a list of `OneElementClass` instances

In the final case, we've attempted to show both a) what a required inline list looks like and b) show that the target
type is irrelevant as long as it is a LinkML `Class` and has no `key` or `identifier` slots
 

```python
@dataclass
class RequiredThreeElementRangeList(YAMLRoot):
    """
    Range is a required list of a class that contain two non-key/non-identifier elements
    """
    ...

    v1: Union[Union[dict, ThreeElementClass], List[Union[dict, ThreeElementClass]]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        elif not isinstance(self.v1, list):
            self.v1 = [self.v1]
        elif len(self.v1) == 0:
            raise ValueError(f"v1 must be a non-empty list")
        self.v1 = [v if isinstance(v, ThreeElementClass) else ThreeElementClass(**v) for v in self.v1]

        super().__post_init__(**kwargs)
```
The structural differences between the above class and its predecessor are:
1) The `v1` signature does not include `None` as an option (i.e. does not begin with `Optional[]`)
2) A `None` value is flagged as an error rather than converted to an empty list
3) An empty list is flagged as an error.


### Keyed or Identified Classes
When the range of a slot is a LinkML class that has a `key` or an `identifier`, additional options 
present themselves:
1) Should elements be represented inline or as references?
2) If inline, should the elements be represented as lists or as dictionaries, whose key is the `key` or `identifier`
value.

We discuss each of these options below

#### Key or identified class _references_

Using the following classes as building blocks

```yaml
  KeyedThreeElementClass:
    description: A keyed class with an additional integer and date
    attributes:
      name:
        range: string
        key: true
      value:
        range: integer
      modifier:
        range: date

  IdentifiedThreeElementClass:
    description: A identified class with an additional integer and date
    attributes:
      name:
        range: string
        identifier: true
      value:
        range: integer
      modifier:
        range: date
```
Python:
```python
class KeyedThreeElementClassName(extended_str):
    pass

class IdentifiedThreeElementClassName(extended_str):
    pass

@dataclass
class KeyedThreeElementClass(YAMLRoot):
    """
    A keyed class with an additional integer and date
    """
    ...

    name: Union[str, KeyedThreeElementClassName] = None
    value: Optional[int] = None
    modifier: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, KeyedThreeElementClassName):
            self.name = KeyedThreeElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        if self.modifier is not None and not isinstance(self.modifier, XSDDate):
            self.modifier = XSDDate(self.modifier)

        super().__post_init__(**kwargs)

@dataclass
class IdentifiedThreeElementClass(YAMLRoot):
    """
    A identified class with an additional integer and date
    """
    ...

    name: Union[str, IdentifiedThreeElementClassName] = None
    value: Optional[int] = None
    modifier: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.name is None:
            raise ValueError("name must be supplied")
        if not isinstance(self.name, IdentifiedThreeElementClassName):
            self.name = IdentifiedThreeElementClassName(self.name)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        if self.modifier is not None and not isinstance(self.modifier, XSDDate):
            self.modifier = XSDDate(self.modifier)

        super().__post_init__(**kwargs)
```

We can now begin with the following LinkML class definitions:
```yaml
  OptionalKeyedThreeElementRange:
    description: Range is a optional class that contains one key and two regular elements
    attributes:
      v1:
        range: KeyedThreeElementClass

  OptionalKeyedThreeElementRangeList:
    description: Range is a optional list of a class that contains one key and two regular elements
    attributes:
      v1:
        range: KeyedThreeElementClass
        multivalued: true

  RequiredIdentifiedThreeElementRange:
    description: Range is a required class that contains one identifier and two regular elements
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        required: true

  RequiredIdentifiedThreeElementRangeList:
    description: Range is a optional list of a class that contains one identifier and two regular elements
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        multivalued: true
        required: true
```
Python equivalents
```python
@dataclass
class OptionalKeyedThreeElementRange(YAMLRoot):
    """
    Range is a optional class that contains one key and two regular elements
    """
    ...

    v1: Optional[Union[str, KeyedThreeElementClassName]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is not None and not isinstance(self.v1, KeyedThreeElementClassName):
            self.v1 = KeyedThreeElementClassName(self.v1)

        super().__post_init__(**kwargs)
```
In the above example, `v1` is a single, optional reference to a `KeyedThreeElementClass` instance.  The constructor can
take one of:
1) `None` - because the link is optional
2) `str` - the type of the key to the `KeyedThreeElementClass`
3) `ThreeElementClassName` - an instance of the actual key.
4) Any python object that can be _coerced_ into a `KeyedThreeElementClassName`

The key is recorded in the class.  Note that the Python code, as it exists today, does NOT check that there actually
`exists` an instance of `KeyedThreeElementClass` with the name in `v1` and, as such, there is _currently_ no way to
get directly from an instance of the class, `OptionalKeyedThreeElementRange` to an instance of `KeyedThreeElementClass`.
This check and capability may be added to a later version of the LinkML tooling. The second example, below, shows
an optional _list_

```python
@dataclass
class OptionalKeyedThreeElementRangeList(YAMLRoot):
    """
    Range is a optional list of a class that contains one key and two regular elements
    """
    ...

    v1: Optional[Union[Union[str, KeyedThreeElementClassName], List[Union[str, KeyedThreeElementClassName]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
        self.v1 = [v if isinstance(v, KeyedThreeElementClassName) else KeyedThreeElementClassName(v) for v in self.v1]

        super().__post_init__(**kwargs)
```
The above signature is a bit confusing.  It allows:
1) `None` - no list has been supplied
2) `str` - the type of the key to a _single_ `KeyedThreeElementClass`
3) `ThreeElementClassName` - an instance of an actual key
4) Any python object that can be _coerced_ into a `KeyedThreeElementClass` (not explicit in the signature)
4) A list consisting of any combination of `str`, `ThreeElementClassNames`, or other objects that can be coerced into
`KeyedThreeElementClassName`

The remaining two non-line examples are similar enough to the above that they are included below without comment. Note,
in particular, that there is no difference between keyed and identified class representation.
```python
@dataclass
class RequiredIdentifiedThreeElementRange(YAMLRoot):
    """
    Range is a required class that contains one identifier and two regular elements
    """
    ...

    v1: Union[str, IdentifiedThreeElementClassName] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, IdentifiedThreeElementClassName):
            self.v1 = IdentifiedThreeElementClassName(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class RequiredIdentifiedThreeElementRangeList(YAMLRoot):
    """
    Range is a optional list of a class that contains one identifier and two regular elements
    """
    ...

    v1: Union[Union[str, IdentifiedThreeElementClassName], List[Union[str, IdentifiedThreeElementClassName]]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        elif not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
        if len(self.v1) == 0:
            raise ValueError(f"v1 must be a non-empty list dictionary or class")
        self.v1 = [v if isinstance(v, IdentifiedThreeElementClassName) else IdentifiedThreeElementClassName(v) for v in self.v1]

        super().__post_init__(**kwargs)
```

### Python generation options for single-value (non-list) slots
The table below describes the various python generation options for single-valued slots (`"multivalued": false`)

| case # | multivalued | inlined | inlined_as_list | range class has key or identifier | result |
| ---: | ------- | ----------------| :------------: | :------: | ----- |
| 1.1 | false (default) | - | - | N | slot value in of containing class (i.e. inline) |
| 1.2 | false | N | N | Y | slot key or identifier is in containing class |
| 1.3 | false | Y | - | Y | slot value in of containing class (i.e. inline) |
| 1.4 | false | - | Y | Y | slot value in of containing class (i.e. inline) |

The YAML examples below the above options for both optional and required slots.
 
 ```yaml
  OptionalThreeElementRange:
    description: Case 1.1(o) -- single values optional slot - range has no keys or identifiers
    attributes:
      v1:
        range: ThreeElementClass

  RequiredThreeElementRange:
    description: Case 1.1(r) -- single values optional slot - range has no keys or identifiers
    attributes:
      v1:
        range: ThreeElementClass
        required: true

  OptionalIdentifiedThreeElementRange:
    description: Case 1.2(o) -- single values optional slot - range has an identifier
    attributes:
      v1:
        range: IdentifiedThreeElementClass

  RequiredKeyedThreeElementRange:
    description: Case 1.2(r) -- single values optional slot - range has a key
    attributes:
      v1:
        range: KeyedThreeElementClass
        required: true

  OptionalInlinedKeyedThreeElementRange:
    description: Case 1.3(o) -- single values optional slot - range has an identifier
    attributes:
      v1:
        range: KeyedThreeElementClass
        inlined: true

  RequiredInlinedIdentifiedThreeElementRange:
    description: Case 1.3(r) -- single values optional slot - range has a key
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        required: true
        inlined: true

  OptionalInlinedAsListKeyedThreeElementRange:
    description: Case 1.4(o) -- single values optional slot - range has an identifier
    attributes:
      v1:
        range: KeyedThreeElementClass
        inlined_as_list: true

  RequiredInlinedAsListIdentifiedThreeElementRange:
    description: Case 1.4(r) -- single values optional slot - range has a key
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        required: true
        inlined_as_list: true
```
The emitted python is as described for types with the exception of case 1.2 -- non-inlined keyed or identified class,
where the identifier or key of the class is the range of the `v1` slot in Python:

```python
@dataclass
class OptionalThreeElementRange(YAMLRoot):
    """
    Case 1.1(o) -- single values optional slot - range has no keys or identifiers
    """
    ...
    v1: Optional[Union[dict, ThreeElementClass]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is not None and not isinstance(self.v1, ThreeElementClass):
            self.v1 = ThreeElementClass(**self.v1)

        super().__post_init__(**kwargs)


@dataclass
class RequiredThreeElementRange(YAMLRoot):
    """
    Case 1.1(r) -- single values optional slot - range has no keys or identifiers
    """
    ...
    v1: Union[dict, ThreeElementClass] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, ThreeElementClass):
            self.v1 = ThreeElementClass(**self.v1)

        super().__post_init__(**kwargs)


@dataclass
class OptionalIdentifiedThreeElementRange(YAMLRoot):
    """
    Case 1.2(o) -- single values optional slot - range has an identifier
    """
    ...
    v1: Optional[Union[str, IdentifiedThreeElementClassName]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is not None and not isinstance(self.v1, IdentifiedThreeElementClassName):
            self.v1 = IdentifiedThreeElementClassName(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class RequiredKeyedThreeElementRange(YAMLRoot):
    """
    Case 1.2(r) -- single values optional slot - range has a key
    """
    ...
    v1: Union[str, KeyedThreeElementClassName] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, KeyedThreeElementClassName):
            self.v1 = KeyedThreeElementClassName(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class OptionalInlinedKeyedThreeElementRange(YAMLRoot):
    """
    Case 1.3(o) -- single values optional slot - range has an identifier
    """
    ...
    v1: Optional[Union[dict, KeyedThreeElementClass]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is not None and not isinstance(self.v1, KeyedThreeElementClass):
            self.v1 = KeyedThreeElementClass(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class RequiredInlinedIdentifiedThreeElementRange(YAMLRoot):
    """
    Case 1.3(r) -- single values optional slot - range has a key
    """
    ...
    v1: Union[dict, IdentifiedThreeElementClass] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, IdentifiedThreeElementClass):
            self.v1 = IdentifiedThreeElementClass(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class OptionalInlinedAsListKeyedThreeElementRange(YAMLRoot):
    """
    Case 1.4(o) -- single values optional slot - range has an identifier
    """
    ...
    v1: Optional[Union[dict, KeyedThreeElementClass]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is not None and not isinstance(self.v1, KeyedThreeElementClass):
            self.v1 = KeyedThreeElementClass(self.v1)

        super().__post_init__(**kwargs)


@dataclass
class RequiredInlinedAsListIdentifiedThreeElementRange(YAMLRoot):
    """
    Case 1.4(r) -- single values optional slot - range has a key
    """
    ...
    v1: Union[dict, IdentifiedThreeElementClass] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        if not isinstance(self.v1, IdentifiedThreeElementClass):
            self.v1 = IdentifiedThreeElementClass(self.v1)

        super().__post_init__(**kwargs)
```

### Python generation options for multivalued slots

The python generated for multivalued slots is a more interesting situation.

| case # | multivalued | inlined | inlined_as_list | range class has key or identifier | result |
| ---: | ------- | ----------------| :------------: | :------: | ----- |
| 2.1 | true  | - | - |     N | Slot is inlined as a list |
| 2.2 | true | false (default) | false (default) | Y | Slot is a list of range keys or identifiers |
| 2.3 | true | - | true | - | Slot is inlined as a list |
| 2.4 | true | true | false | Y | Slot is inlined as a dictionary, keyed by the slot key or identifier |

The first two cases (2.1) and (2.2) do not differ significantly from what was described earlier
```yaml
OptionalMultivaluedThreeElementRange:
    description: Case 2.1(o) -- multivalued optional slot - range has no key or identifier
    attributes:
      v1:
        range: ThreeElementClass
        multivalued: true

  RequiredMultivaluedThreeElementRange:
    description: Case 2.1(r) -- multivalued optional slot - range has no key or identifier
    attributes:
      v1:
        range: ThreeElementClass
        multivalued: true
        required: true

  OptionalMultivaluedKeyedThreeElementRange:
    description: Case 2.2(o) -- multivalued optional slot - range has a key
    attributes:
      v1:
        range: KeyedThreeElementClass
        multivalued: true

  RequiredMultivaluedIdentifiedThreeElementRange:
    description: Case 2.2(r) -- multivalued optional slot - range has an identifier
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        multivalued: true
        required: true
```

```python
@dataclass
class OptionalMultivaluedThreeElementRange(YAMLRoot):
    """
    Case 2.1(o) -- multivalued optional slot - range has no key or identifier
    """
    ...
    v1: Optional[Union[Union[dict, ThreeElementClass], List[Union[dict, ThreeElementClass]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, list):
            self.v1 = [self.v1]
        self.v1 = [v if isinstance(v, ThreeElementClass) else ThreeElementClass(**v) for v in self.v1]

        super().__post_init__(**kwargs)


@dataclass
class RequiredMultivaluedThreeElementRange(YAMLRoot):
    """
    Case 2.1(r) -- multivalued optional slot - range has no key or identifier
    """
    ...
    v1: Union[Union[dict, ThreeElementClass], List[Union[dict, ThreeElementClass]]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        elif not isinstance(self.v1, list):
            self.v1 = [self.v1]
        elif len(self.v1) == 0:
            raise ValueError(f"v1 must be a non-empty list")
        self.v1 = [v if isinstance(v, ThreeElementClass) else ThreeElementClass(**v) for v in self.v1]

        super().__post_init__(**kwargs)

@dataclass
class OptionalMultivaluedKeyedThreeElementRange(YAMLRoot):
    """
    Case 2.2(o) -- multivalued optional slot - range has a key
    """
    ...
    v1: Optional[Union[Union[str, KeyedThreeElementClassName], List[Union[str, KeyedThreeElementClassName]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, list):
            self.v1 = [self.v1]
        self.v1 = [v if isinstance(v, KeyedThreeElementClassName) else KeyedThreeElementClassName(v) for v in self.v1]

        super().__post_init__(**kwargs)


@dataclass
class RequiredMultivaluedIdentifiedThreeElementRange(YAMLRoot):
    """
    Case 2.2(r) -- multivalued required slot - range has an identifier
    """
    ...
    v1: Union[Union[str, IdentifiedThreeElementClassName], List[Union[str, IdentifiedThreeElementClassName]]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        elif not isinstance(self.v1, list):
            self.v1 = [self.v1]
        elif len(self.v1) == 0:
            raise ValueError(f"v1 must be a non-empty list")
        self.v1 = [v if isinstance(v, IdentifiedThreeElementClassName) else IdentifiedThreeElementClassName(v) for v in self.v1]

        super().__post_init__(**kwargs)
```

Case 2.3 (Inlined as list) shows a new pattern:
```yaml
  OptionalMultivaluedInlinedListIdentifiedThreeElementRange:
    description: 2.3(o) Range is an optional identified three element class that is represented as an inlined list
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        multivalued: true
        inlined_as_list: true


  RequiredMultivaluedInlinedListKeyedThreeElementRangeList:
    description: 2.3(r) Range is a required keyed three element class that is represented as an inlined list
    attributes:
      v1:
        range: KeyedThreeElementClass
        multivalued: true
        inlined_as_list: true
        required: true
```

The Python that is generated from the above entries will require some more description:

```python

@dataclass
class OptionalMultivaluedInlinedListIdentifiedThreeElementRange(YAMLRoot):
    """
    2.3(o) Range is an optional identified three element class that is represented as an inlined list
    """
    ...
    v1: Optional[Union[Dict[Union[str, IdentifiedThreeElementClassName], Union[dict, IdentifiedThreeElementClass]], List[Union[dict, IdentifiedThreeElementClass]]]] = empty_list()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
        self._normalize_inlined_slot(slot_name="v1", slot_type=IdentifiedThreeElementClass, key_name="name", inlined_as_list=True, keyed=True)

        super().__post_init__(**kwargs)

```

Starting with the signature:

`v1: Optional[Union[Dict[Union[str, IdentifiedThreeElementClassName], Union[dict, IdentifiedThreeElementClass]], List[Union[dict, IdentifiedThreeElementClass]]]] = empty_list()`

The outermost declaration: `Optional[...] = empty_list()` reflects:
1) `v1` is not required: `None` is a valid value 
2) the internal storage structure is going to be a list.  Note that None, [] and {} (Missing scalar, empty list and empty dictionary all indicate absence of a value)

Moving inwards, `Union[Dict[...], List[...]]` means that the inputs can either be in the form of a dictionary or a list.

#### Input in the form of a dictionary
If the input is in the form of a dictionary, its signature is "`Dict[Union[str, IdentifiedThreeElementClassName], Union[dict, IdentifiedThreeElementClass]]`", that is
a dictionary whose _keys_ are valid `IdentifiedThreeElementClassNames` and whose _values_ are instances of `IdentifiedThreeElementClass`.  The `str` part of the key
signature and the `dict` component of the value indicate that, raw strings can be substituted for class names and plain dictionaries for class values.

Noting the definition for `KeyedThreeElementClass` is:
```yaml
  KeyedThreeElementClass:
    description: A keyed class with an additional integer and date
    attributes:
      name:
        range: string
        key: true
      value:
        range: integer
      modifier:
        range: date
```

One can represent instances of `OptionalMultivaluedInlinedListIdentifiedThreeElementRange` in YAML as:
```yaml
  element1:
    value: 17
    modifier: 2012-03-11
  element2:
  element3:
    name: element3
    value: 42
```
or in python as:
```python
ktec_examples = OptionalMultivaluedInlinedListIdentifiedThreeElementRange(
    { 
        element1: {value: 17, modifier: "2012-03-11"},
        KeyedThreeElementClassKey('element2'): {},
        element3: {name: 'element3', value: 42}
    }   
)  
```
Note that the following is not valid because, while the `name` attribute (the key) is not required, as it has already
been established by the key, if present it _must_ match the key itself
```yaml
  element3:
    name: test
    value: 42
```
One of the reasons for the explicit key types (e.g. `KeyedThreeElementClassKey`) is to provide some level of checking
for potential link mismatches.  The following code snippet:
```python
itc = IdentifiedThreeElementClass('entry1', 17)
ktec_examples: OptionalMultivaluedInlinedListIdentifiedThreeElementRange = {
    itc.name: {value: 42}
}
```
Would result in an error, as `itc.name` is an instance of `IdentifiedThreeElementClassKey` while `KeyedThreeElementClass` expects a `KeyedThreeElementClassKey`

#### Input in the form of a list
Starting with the skeleton we visited earlier, Moving inwards, `Union[Dict[...], List[...]]` the second option, 
`List[Union[dict, IdentifiedThreeElementClass]]` indicates that the input to the constructor can also be a _list_ of
dictionaries that conform to the `IdentifiedThreeElementClass` model. Referencing the examples that we used above, 
we could also use:
```yaml
    - name: element1
      value: 17
      modifier: 2012-03-11
    - name: element2
    - name: element3
      value: 42
```
And the Python equivalent would be:
```python
ktec_examples = OptionalMultivaluedInlinedListIdentifiedThreeElementRange(
    [ {name: 'element1', value: 17, modifier: "2012-03-11"},
      {name: KeyedThreeElementClassKey('element2')},
      {name: 'element3', value: 42}
    ]  
)  
```
We then move on to the generated code:
```python
    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
```
The first two tests are pretty close to what we saw earlier, with the exception that you can't pass an isolated
dictionary.  You can construct a list of integers with a single value:

```python
    my_entries = ListOfIntegers(17)
```
Which would, if the class `ListOfIntegers`'s first variable was a multivalued slot with a range of intgers, result in
`my_entries.v == [17]`.  When dealing with classes, however, the following:
```python
    my_entries = ListOfClasses(dict(name='element1', value=17))
```
would fail, as it would try to convert this into a list with two `IdentifiedThreeElementClass` entries.

The final line in the `__post_init__` section:
```python
    self._normalize_inlined_slot(slot_name="v1", slot_type=IdentifiedThreeElementClass, key_name="name", inlined_as_list=True, keyed=True)
```
passes the remainder of the post initilization normalization to a function defined in `YAMLRoot`.  


The final case, Case 2.4 (Inlined as dictionary) is essentially the same, with the exception that the target type is
a dictionary rather than a list.  
  
```yaml
OptionalMultivaluedInlinedIdentifiedThreeElementRangeList:
    description: 2.4(o) Range is an optional identified three element class that is represented as an inlined dictionary
    attributes:
      v1:
        range: IdentifiedThreeElementClass
        multivalued: true
        inlined: true


  RequiredMultivaluedInlinedKeyedThreeElementRange:
    description: 2.4(r) Range is a required keyed three element class that is represented as an inlined dictionary
    attributes:
      v1:
        range: KeyedThreeElementClass
        multivalued: true
        inlined: true
        required: true
```
```python
@dataclass
class OptionalMultivaluedInlinedIdentifiedThreeElementRangeList(YAMLRoot):
    """
    2.4(o) Range is an optional identified three element class that is represented as an inlined dictionary
    """
    ...
    v1: Optional[Union[Dict[Union[str, IdentifiedThreeElementClassName], Union[dict, IdentifiedThreeElementClass]], List[Union[dict, IdentifiedThreeElementClass]]]] = empty_dict()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            self.v1 = []
        if not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
        self._normalize_inlined_slot(slot_name="v1", slot_type=IdentifiedThreeElementClass, key_name="name", inlined_as_list=None, keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class RequiredMultivaluedInlinedKeyedThreeElementRange(YAMLRoot):
    """
    2.4(r) Range is a required keyed three element class that is represented as an inlined dictionary
    """
    ...
    v1: Union[Dict[Union[str, KeyedThreeElementClassName], Union[dict, KeyedThreeElementClass]], List[Union[dict, KeyedThreeElementClass]]] = empty_dict()

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.v1 is None:
            raise ValueError("v1 must be supplied")
        elif not isinstance(self.v1, (list, dict)):
            self.v1 = [self.v1]
        if len(self.v1) == 0:
            raise ValueError(f"v1 must be a non-empty list, dictionary, or class")
        self._normalize_inlined_slot(slot_name="v1", slot_type=KeyedThreeElementClass, key_name="name", inlined_as_list=None, keyed=True)

        super().__post_init__(**kwargs)
```
The generated code is identical to the previous case (2.3) with the exception that the default initializer is `empty_dict()` instead
of `empty_list()`, and the `_normalized_inlined_slot` function is passed a false `inlined_as_list` value (well, 'None' but...).

As a final note on the `inlined_as_list` vs. just plain `inlined`, while the internal storage structure is different, the
initialization code is exactly the same -- YAML emitted from a list structure can be loaded as a dictionary and visa-versa.

### Slots
One bit that we haven't touched on here is the `slots` section of the emitted Python.

At the moment, the following code is emitted:
```python

# Slots
class slots:
    pass
    
    ...

slots.RequiredInlinedKeyedTwoElementRange_v1 = Slot(uri=LISTS_AND_KEYS.v1, name="RequiredInlinedKeyedTwoElementRange_v1", curie=LISTS_AND_KEYS.curie('v1'),
                   model_uri=LISTS_AND_KEYS.RequiredInlinedKeyedTwoElementRange_v1, domain=RequiredInlinedKeyedTwoElementRange, range=Union[dict, KeyedTwoElementClass])

slots.RequiredInlinedKeyedTwoElementRangeList_v1 = Slot(uri=LISTS_AND_KEYS.v1, name="RequiredInlinedKeyedTwoElementRangeList_v1", curie=LISTS_AND_KEYS.curie('v1'),
                   model_uri=LISTS_AND_KEYS.RequiredInlinedKeyedTwoElementRangeList_v1, domain=RequiredInlinedKeyedTwoElementRangeList, range=Union[Dict[Union[str, KeyedTwoElementClassName], Union[dict, KeyedTwoElementClass]], List[Union[dict, KeyedTwoElementClass]]])

slots.RequiredInlinedKeyedThreeElementRange_v1 = Slot(uri=LISTS_AND_KEYS.v1, name="RequiredInlinedKeyedThreeElementRange_v1", curie=LISTS_AND_KEYS.curie('v1'),
                   model_uri=LISTS_AND_KEYS.RequiredInlinedKeyedThreeElementRange_v1, domain=RequiredInlinedKeyedThreeElementRange, range=Union[dict, KeyedThreeElementClass])

slots.RequiredInlinedKeyedThreeElementRangeList_v1 = Slot(uri=LISTS_AND_KEYS.v1, name="RequiredInlinedKeyedThreeElementRangeList_v1", curie=LISTS_AND_KEYS.curie('v1'),
                   model_uri=LISTS_AND_KEYS.RequiredInlinedKeyedThreeElementRangeList_v1, domain=RequiredInlinedKeyedThreeElementRangeList, range=Union[Dict[Union[str, KeyedThreeElementClassName], Union[dict, KeyedThreeElementClass]], List[Union[dict, KeyedThreeElementClass]]])
```

The `slots` class is here to keep the module namespace from getting too confusing, the idea that, if you want to reference
a slot, you use `slots.RequiredInlinedTwoElementRange_v1` (which is the mangling of the owner class name and the actual slot)

At the _moment_, you have the following elements:

* uri - the SLOT URI
* name - the mangled name 
* curie - the SLOT CURIE
* model_uri - the slot URI where the base is the Model URI vs. one assigned via `slot_uri`
* domain - the slot domain
* range - the range _signature_

Note, however, that the slots area is still being enhanced, so keep an eye on entries like [Issue #272](https://github.com/linkml/issues/272)
