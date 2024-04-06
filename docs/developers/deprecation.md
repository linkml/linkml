(deprecation-guide)=
```{index} Deprecation; Guide
```
# Deprecations

```{currentmodule} linkml.utils.deprecation
```

## Guidelines

### What to Deprecate

All of the following should be given deprecation warnings that give
downstream packages enough time to adapt.

#### Breaking changes
 
All breaking changes to public classes and functions.
"Public" is not strictly defined in `linkml`, but in general these are things
made available via CLI, or things that are given their own packages/modules.

Breaking changes include (but are not limited to)
- Removal of features, classes, functions, and parameters
- Changes to defaults
- Refactoring that changes import location

#### Dependencies

Changes to dependencies typically do not need a deprecation warning, but
for updates that exclude a commonly used version with substantial differences
with the newer version, a warning should be emitted. As an example, the
{mod}`~linkml.utils.deprecation` module was initially motivated by 
the need to warn about deprecating support for Pydantic v1.

#### Supported Python Version

All changes to the minimum supported python versions should be deprecated
with at least a patch version of notice.

### Duration of Deprecation

The amount of time (or, the number of versions between when a feature is 
marked as deprecated and when it is removed) depends on the size of the change
and the complexity of adapting to it, but typically they should coincide with a 
minor or major version.

## Process

There are two phases to a deprecation:
- **Deprecation** - A feature is deprecated when it is marked for removal. 
  No new code should use that feature, and its usage should emit a warning.
- **Removal** - A previously deprecated feature is removed from the package.

All deprecations use the tools in the {mod}`~linkml.utils.deprecation` module.

### Declare the Deprecation

To declare a deprecation, create a new {class}`Deprecation` class and add it to the
{class}`DEPRECATIONS` tuple in {mod}`linkml.utils.deprecation` . The ``Deprecation``
object contains 

- the information about what is being deprecated, 
- after which version it is considered deprecated
- (Optional) which version it will be removed in
- (Optional) what should be done instead
- (Optional) an issue that contains further information.

For example, if we are deprecating a feature for rendering a linkml schema to 
[semaphore](https://en.wikipedia.org/wiki/Flag_semaphore), we might create an object like this:

`deprecation.py`
```python
DEPRECATIONS = (
  Deprecation(
    name = "semaphore",
    message = (
      "Flag-based semaphore schemas were considered to not have a high "
      "enough information capacity to usefully represent a linkml schema"),
    recommendation = "Update to a digital schema representation or morse code",
    deprecated_in = SemVer.from_str("1.7.5"),
    removed_in = SemVer.from_str("1.8.0"),
    issue = -1
  ),
)
```

Declaring the deprecation will add it to the [Deprecation Log](../code/deprecation.rst).

### Mark the Deprecation

Everywhere the deprecated feature would be used, add a {func}`deprecation_warning` call
that uses the `name` of the `Deprecation` object.

This will emit a {class}`DeprecationWarning` that looks like this:

```python
>>> deprecation_warning('semaphore')
[semaphore] DEPRECATED
Flag-based semaphore schemas were considered to not have a high enough information capacity to usefully represent a linkml schema
Deprecated In: 1.7.0
Removed In: 1.8.0
Recommendation: Update to a digital schema representation or morse code
See: https://github.com/linkml/linkml/issues/-1
```

This looks different depending on what is being deprecated, see [this guide](https://dev.to/hckjck/python-deprecation-2mof)
for further examples of how to deprecate various python language constructs.

Some examples:

#### Module

`semaphore.py`
```python
from linkml.utils import deprecation_warning
deprecation_warning('semaphore')
```

#### Function

```python
def render_semaphore(schema):
    deprecation_warning('semaphore')
```

#### Class

```python
class MyClass:
    def __init__(self):
        deprecation_warning('semaphore')
```

#### Dependency Version

eg. if we were deprecating all versions of `pysemaphore<2.0.0`, in every place it is imported:

```python
import pysemaphore
from linkml.utils.deprecation import SemVer

if SemVer.from_package('pysemaphore').major < 2:
  deprecation_warning('semaphore')
```

#### Python Version

In `linkml/__init__.py`
```python
import sys

if sys.version_info.minor <= 8:
  deprecation_warning('semaphore')
```

#### Default Value

If we are changing a default value that is `None` in the function signature
and filled in the function body:

```python
def my_function(arg:Optional[str] = None):
    if arg is None:
        deprecation_warning('semaphore')
        arg = 'old_default'
```

Or if we are dropping support for calling a function with a `str` in favor of a `Path`

```python
def my_function(arg: Union[Path, str]):
    if isinstance(arg, str):
        deprecation_warning('semaphore')
        arg = Path(str)
```

It's inelegant to check whether a python is called explicitly with a parameter or whether
it is using the default, but it is possible:

```python
import inspect
def my_function(arg = 'default'):
    frame = inspect.currentframe()
    outer = inspect.getouterframes(frame, 1)[1]
    if arg not in outer.code_context[0]:
        deprecation_warning('semaphore')
    
```

### Removal

LinkML's deprecation warnings are tested: when the version where a deprecation is 
marked to be removed is reached, the tests will fail (specifically 
`tests/test_utils/test_deprecation.py::test_removed_are_removed`). 

Remove all deprecated functionality and the calls to {func}`deprecation_warning`, but 
leave the {class}`Deprecation` class declaration in place as a record.

## API

```{eval-rst}
.. automodule:: linkml.utils.deprecation
    :members: 
    :undoc-members:
```

## See Also

- [Deprecation Log](../code/deprecation.rst)