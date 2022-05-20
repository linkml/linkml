# Porting LinkML tools to other languages

## Preamble

__ this is an advanced how-to guide that is not expected to be useful for typical LinkML users or developers__.

If you are thinking of porting LinkML please contact us first!

## Introduction

LinkML is a programming language-neutral framework. Using LinkML you
can specify a datamodel for your project, and use LinkML tools for
validating data. These tools are in Python, but they can be executed
during the development cycle of your project, avoiding python
dependencies in non-python code.

For a small but growing set of languages there is support for
[generating data access object
models](https://linkml.io/linkml/generators/index.html) for that
language. For other languages it should be possible to code up
generators using the flexible Jinja2 template based generator
framework.

However, there may still be cases where it is desirable to have full
LinkML support within a language other than python, typically when
writing a generic application that is designed to work with *any*
LinkML model.

Examples of these might be:

1. A generic data editor or visualizer for LinkML models
2. A code generator for a particular language where one wants to take advantage of features of that language

For more on the first use case, see the [tool developer guide](https://linkml.io/linkml/developers/tool-developer-guide.html).

As an example of the second, consider writing a code generator for
Java that creates data access classes with the ability to customize
the generation for various different styles of java annotations
(Jackson, Lombok, Hibernate, ...). While this could be done in Python
and Jinja2 templates, there is an advantage to leveraging existing
tooling in the host language.

It may be tempting to take the "easy" approach and simply write code
that works directly from LinkML yaml files. This is a good approach if
you are targeting one of the simple sub-profiles of LinkML but if you
are aiming for a more powerful library then this has a number of disadvantages.

## Definitions

- LinkML framework: a general purpose programming library for working with LinkML models
- Target Language: the programming language one wishes to write a LinkML framework for
- LinkML metamodel: A schema that describes LinkML itself

# Overview of Python Framework

Currently there are 3 core repos:

- [linkml-model](https://github.com/linkml/linkml-model) This holds the Source of Truth for the *metamodel*
- [linkml-runtime](https://github.com/linkml/linkml-runtime) A runtime library that is depended on by schema-specific generated python dataclass libraries
- [linkml](https://github.com/linkml/linkml) The core tooling, including [generators](https://linkml.io/linkml/generators/index.html)

This guide assumes familiarity with all of the above

Note that there are no runtime dependencies on linkml-model; this
would create a circularity since the metamodel is like any other
schema and depends on the runtime. Instead, linkml-model is synced into linkml-runtime.

# How to Port to your language of choice

## Step 1: Bootstrap metamodel data access classes

Even if you intended to ultimately use the target language for doing
codegen, we strongly recommend you bootstrap by using the existing
generators framework. This may take a little bit of Python coding and some Jinja2 templates.

Consult some of the existing generators to see how this is done. Be
sure to use the newer style SchemaView generators.

for example: https://github.com/linkml/linkml/blob/main/linkml/generators/javagen.py

Definitely make an issue on our repo so you can coordinate with others interested in support for the target language!

When writing the bootstrap generators there are a number of design decisions:

- Should the generated code be standalone, or should there be runtime dependencies?
- If there are runtime dependencies, are these on 3rd party libraries or something you will generate?
- What are the appropriate constructs to map to in the target language?
- How do you intend to handle serialization and parsing to/from JSON?
- What is your strategy for validation within the target language?
- How should imports be handled in a way that comports well with the target lnaguage

There are no right or wrong answers here. A good strategy is to start with the simplest thing that could work and build out from there.

By way of comparison here are some rough descriptions of existing generators and their decisions:

### Case study: pydanticgen

__pydanticgen__: this generates largely standalone python classes, with only a dependency on the 3rd party pydantic framework (all classes ultimately inherit from BaseModel)

### Case study: pythongen

__pythongen__: this builds fully-featured Python classes that follow
the dataclasses framework, which is part of the Python core. These
classes are not standalone however. Let's examine the header of
generated classes:

```python
import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE
```

Many of these are part of Python:

The standard typing library is used for type hints:

```python
from typing import Optional, List, Union, Dict, ClassVar, Any
```

the standard python dataclasses library is used:

```python
import dataclasses
...

@dataclass
class Person(NamedThing):
   ...
```

Others are dependencies on either the linkml-runtime itself or on external libraries

All classes inherit from YAMLRoot which itself inherits from JsonObj in jsonasonj2:

```python
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
...

@dataclass
class NamedThing(YAMLRoot):
   ...
```

The `as_dict` method from jsonasobj2 provides convenient methods for normalizing inputs to initialization routines:

```python
from jsonasobj2 import JsonObj, as_dict
...

@dataclass
class MedicalEvent(Event):
    ...
    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        ...
        if self.diagnosis is not None and not isinstance(self.diagnosis, DiagnosisConcept):
            self.diagnosis = DiagnosisConcept(**as_dict(self.diagnosis))

```


rdflib.URIRef is used to allow for introspection to retrieve the URI of any LinkML class at rumtime:

```python
from rdflib import Namespace, URIRef
...

@dataclass
class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Person
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person
```

Additionally, if parts of the metamodel are imported - such as for `linkml:types` this generates a corresponding python import:


```python
from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDate
...

@dataclass
class Event(YAMLRoot):
    ...
    started_at_time: Optional[Union[str, XSDDate]] = None

```

the python generator will also generate subclasses of builtin Python strings - these are useful for non-inlined references to type the reference slot: 

```python
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int

class NamedThingId(extended_str):
    pass

class PersonId(NamedThingId):
    pass

...
@dataclass
class FamilialRelationship(Relationship):
    ...
    type: Union[str, "FamilialRelationshipType"] = None
    related_to: Union[str, PersonId] = None

```

All of these decisions lead to a very fully featured set of generated data access classes, but these decisions do not need to be replicated when writing a generator for your target language.

### Case study: typescriptgen

In contrast to the python approaches, this targets typescript *Interfaces* as the construct of choice in the target language

Note that interfaces are "compiled away" but are used for static analyis and IDE support

### Case study: javagen

Currently the approaches here are under discussion. There are different choices of target language construct:

- classes
- interfaces
- records (introduced in java 16)

The current pattern for generation roughly follows the pydanticgen approach of generating largely standalone classes (soon: records)

### Implementing for your target language

We recommend starting with a generator for simple standalone classes. These do not need to be as fully featured as pythongen. You can treat things like annotating
model elements with URIs, providing introspection support, and generating JSON as separate concerns -- at least at first.

## Step 2: Generate data access classes for the metamodel

This will give you the equivalent of meta.py, types,py in linkml-runtime.

E.g if your target langauge is C, and you decided on structs as target construct, then you will have structs with names like `ClassDefinition`, `SchemaDefinition`

Depending on the approach you took in Step 1, this may also include an approach to instantiate this target language datamodel from YAML or JSON.

If you have that then you should have the ability to do the equivalent of:

```
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.linkml_model.meta import SchemaDefinition

schema = yaml_loader.load('my-schema.yaml', target=SchemaDefinition)
# now do things with the schema
```

## Step 3: Implement core logic for derived schemas

By this stage you can load and dump schema objects in a type-safe way. It may be tempting to just go off and implement things with this.

However, you will also want to implement the core logic of LinkML as defined in the LinkML specification, under "Derived Schemas". You can do this simply by implementing the spec in your target language,
but a more pragmatic approach is to port the python class SchemaView

SchemaView is a class in linkml-runtime here: https://github.com/linkml/linkml-runtime

Note that you may only need to implement this for a simple profile of linkml before moving to the next step. As an example, see the SchemaView.js class in linkml-runtime.js

This may include:

- basic inheritance methods using is_a and mixins
- induced class slots/attributes

## Step 4 (optional): Jettison the bootstrap approach

Now you have a core framework - perhaps not yet complete - for your target language, you may wish to jettison the original generator you wrote with Python/Jinja2 and implement this in the target language. This culd have advantages such as leveraging code generation frameworks in that target language (this is the case for Java that has a rich codegen framework)

At this stage you may wish to revisit some design decisions in the original generator, and make the generated code more fully featured like pythongen.

# Summary

This guide is by its nature high level, and various decisions will be determined by specific features of the target language or even by developer preference. As we gain more experience and port core linkml utilities to more target languages we will update this guide.

