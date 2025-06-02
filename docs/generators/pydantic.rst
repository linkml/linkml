:tocdepth: 3

.. _pydanticgen:

Pydantic
========

Example Output
--------------

`personinfo_pydantic.py <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo_pydantic.py>`_

Overview
--------

The Pydantic Generator produces Pydantic flavored python dataclasses from a linkml model,
with optional support for user-supplied jinja2 templates to generate alternate classes.


Example
^^^^^^^

Given a definition of a Person class:

.. code-block:: yaml


    Person:
      is_a: NamedThing
      description: >-
        A person (alive, dead, undead, or fictional).
      class_uri: schema:Person
      mixins:
        - HasAliases
      slots:
        - primary_email
        - birth_date
        - age_in_years
        - gender
        - current_address
        - has_employment_history
        - has_familial_relationships
        - has_medical_history

(some details omitted for brevity, including slot definitions and
parent classes)

The generate python looks like this:

.. code-block:: python


    class Person(NamedThing):
        """
        A person (alive, dead, undead, or fictional).
        """
        primary_email: Optional[str] = Field(None)
        birth_date: Optional[str] = Field(None)
        age_in_years: Optional[int] = Field(None, ge=0, le=999)
        gender: Optional[GenderType] = Field(None)
        current_address: Optional[Address] = Field(None, description="""The address at which a person currently lives""")
        has_employment_history: Optional[List[EmploymentEvent]] = Field(None)
        has_familial_relationships: Optional[List[FamilialRelationship]] = Field(None)
        has_medical_history: Optional[List[MedicalEvent]] = Field(None)
        aliases: Optional[List[str]] = Field(None)
        id: Optional[str] = Field(None)
        name: Optional[str] = Field(None)
        description: Optional[str] = Field(None)
        image: Optional[str] = Field(None)


Command Line
------------

.. currentmodule:: linkml.generators.pydanticgen

.. click:: linkml.generators.pydanticgen:cli
    :prog: gen-pydantic
    :nested: short

Generator
---------


.. autoclass:: PydanticGenerator
    :members:

Split Generation
----------------

Pydantic models can also be generated in a "split" mode where rather than
rolling down all classes into a single file, schemas are kept as their own
pydantic modules that import from one another.

See:

* :attr:`.PydanticGenerator.split`
* :attr:`.PydanticGenerator.split_pattern`
* :attr:`.PydanticGenerator.split_context`
* :meth:`.PydanticGenerator.generate_split`

The implementation of ``split`` mode in the Generator itself still generates
a single module, except for importing classes from other modules rather than
including them directly. This is wrapped by :meth:`.PydanticGenerator.generate_split` which
can be used to generate the module files directly


Templates
---------

The pydanticgen module has a templating system that allows each part of a
schema to be generated independently and customized. See the documentation
for the individual classes, but in short - each part of the output pydantic
domain has a model with a corresponding template. At render time, each model
is recursively rendered.

The :class:`.PydanticGenerator` then serves as a translation layer between
the source models from :mod:`linkml_runtime` and the target models in
:mod:`.pydanticgen.template` , making clear what is needed to generate
pydantic code as well as what parts of the linkml metamodel are supported.

Usage example:

Imports:

.. code-block:: python

    imports = (Imports() +
        Import(module="sys") +
        Import(module="pydantic", objects=[{"name": "BaseModel"}, {"name": "Field"}])
    )

renders to:

.. code-block:: python

    import sys
    from pydantic import (
        BaseModel,
        Field
    )

Attributes:

.. code-block:: python

    attr = PydanticAttribute(
        name="my_field",
        annotations={"python_range": {"value": "str"}},
        title="My Field!",
        description="A Field that is mine!",
        pattern="my_.*",
    )

By itself, renders to:

.. code-block:: python

    my_field: str = Field(None, title="My Field!", description="""A Field that is mine!""")

Classes:

.. code-block:: python

    cls = PydanticClass(
        name="MyClass",
        bases="BaseModel",
        description="A Class I Made!",
        attributes={"my_field": attr},
    )

Renders to (along with the validator for the attribute):

.. code-block:: python

    class MyClass(BaseModel):
        my_field: str = Field(None, title="My Field!", description="""A Field that is mine!""")

        @validator('my_field', allow_reuse=True)
        def pattern_my_field(cls, v):
            pattern=re.compile(r"my_.*")
            if isinstance(v,list):
                for element in v:
                    if not pattern.match(element):
                        raise ValueError(f"Invalid my_field format: {element}")
            elif isinstance(v,str):
                if not pattern.match(v):
                    raise ValueError(f"Invalid my_field format: {v}")
            return v

Modules:

.. code-block:: python

    module = PydanticModule(imports=imports, classes={cls.name: cls})

Combine all the pieces:

.. code-block:: python

    import sys
    from pydantic import (
        BaseModel,
        Field
    )

    metamodel_version = "None"
    version = "None"

    class WeakRefShimBaseModel(BaseModel):
        __slots__ = '__weakref__'


    class ConfiguredBaseModel(WeakRefShimBaseModel,
                    validate_assignment = True,
                    validate_all = True,
                    underscore_attrs_are_private = True,
                    extra = "forbid",
                    arbitrary_types_allowed = True,
                    use_enum_values = True):
        pass


    class MyClass(BaseModel):
        my_field: str = Field(None, title="My Field!", description="""A Field that is mine!""")

        @validator('my_field', allow_reuse=True)
        def pattern_my_field(cls, v):
            pattern=re.compile(r"my_.*")
            if isinstance(v,list):
                for element in v:
                    if not pattern.match(element):
                        raise ValueError(f"Invalid my_field format: {element}")
            elif isinstance(v,str):
                if not pattern.match(v):
                    raise ValueError(f"Invalid my_field format: {v}")
            return v


    # Update forward refs
    # see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
    MyClass.update_forward_refs()


.. automodule:: linkml.generators.pydanticgen.template
    :members:
    :undoc-members:
    :member-order: bysource

Arrays
-------

.. admonition:: TODO

    Narrative documentation for pydantic LoL Arrays. Subsection this by different array reps

See `Schemas/Arrays <arrays>`_

.. automodule:: linkml.generators.pydanticgen.array
    :members:
    :member-order: bysource

Additional Notes
----------------
LinkML contains two Python generators. The Pydantic dataclass generator is specifically
useful for FastAPI, but is newer and less full featured than the standard
:doc:`Python generator </generators/python>`.


Biolink Example
---------------

Begin by downloading the Biolink Model YAML and adding a virtual environment and installing linkml.

.. code-block:: bash

    curl -OJ https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml
    python3 -m venv venv
    source venv/bin/activate
    pip install linkml

Now generate the classes using the `gen-pydantic` command

.. code-block:: bash

    gen-pydantic biolink-model.yaml > biolink-model.py
