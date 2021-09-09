# String Template proposal
The `string_template` attribute allows a Python [format string](https://docs.python.org/3/library/string.html#formatstrings)
to be associated with a LinkML model `Element`.  

## Syntax
```yaml
classes:
   person:
     attributes:
        name:
          range: string
          required: true
        age:
          range: integer
        gender:
          range string
     ...
     string_template: "{name} - a {age} year old {gender}"
```

The python emitted for a class with a `string_template` looks like:

```python
@dataclass
class FirstClass(YAMLRoot):
    ...
    string_template: ClassVar[str] = "{name} - a {age} year old {gender}"

    name: str = None
    age: Optional[int] = None
    gender: Optional[str] = None
    
    ...

    def __str__(self):
        return FirstClass.string_template.format(**{k: '' if v is None else v for k, v in self.__dict__.items()})

    @classmethod
    def parse(cls, text: str) -> "FirstClass":
        v = parse.parse(FirstClass.string_template, text)
        return FirstClass(*v.fixed, **v.named)
```

## Sample uses
```python

# Construct a class instance
inst = FirstClass("Sam Sneed", 42, "Male")
print(str(inst))
> "Sam Sneed - a 42 year old Male"

# Parse a string into a class image
inst2 = FirstClass.parse("Jillian Johnson - a 93 year old female")
print(str(inst2))
> 'Jillian Johnson - a 93 year old female'

# repr gives you the non-templated 
print(repr(inst2))
> "FirstClass(name='Jillian Johnson', age=93, gender='female')"

# Load an instance from a yaml file
with open('jones.yaml') as yf:
    inst3 = from_yaml(yf, FirstClass)
print(str(inst3))
> 'Freddy Buster Jones - a 11 year old Undetermined'
```

The input YAML file:
```yaml
name: Freddy Buster Jones
age: 11
gender: Undetermined
```

