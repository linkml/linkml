# Migrating from BiolinkML to LinkML


## Schema sources
The base URI for LinkML is: https://w3id.org/linkml/

The following entries need to be changed in any LinkML SchemaDefinition source (if present):

prefixes:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;~~meta: https://w3id.org/biolink/biolinkml/meta/~~ <br/>
&nbsp;&nbsp;&nbsp;&nbsp;~~biolinkml: https://w3id.org/biolink/biolinkml/~~ → linkml: https://w3id.org/linkml/

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

default_prefix: ~~meta~~ → linkml

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...


emit_prefixes:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~meta~~  → linkml<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~bilinkml~~  → linkml<br/>
&nbsp;&nbsp;&nbsp;&nbsp;-

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

imports:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~biolinkml:types~~ → linkml:types<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~biolinkml:mappings~~ → linkml:mappings<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~biolinkml:extensions~~ → linkml:extensions<br/>
&nbsp;&nbsp;&nbsp;&nbsp;- ~~biolinkml:annotations~~ → linkml:annotations<br/>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

## Python
Python programs that use LinkML `meta.py`, `types.py`, `mappings.py`, `annotations.py` and/or `extensions.py`
will need to make the following changes:


from ~~biolinkml~~.meta import SchemaDefinition, ...  → from linkml_model.meta import SchemaDefinition ...

You will also need to make the following changes:

~~biolinkml~~ = "&ast;" → linkml = "&ast;"<br/>
linkml_model = "&ast;"


To the Pipfile and/or requirements.txt

Note: All of the model artifacts are now available directly in the `linkml_model` root. The current form:
```python
from linkml_model.meta import SchemaDefinition
from linkml_model.types import Boolean
```
can be replaced with:
```python
from linkml_model import SchemaDefinition, Boolean
```

The above change, however, is strictly optional.  Both forms will work equally well.


