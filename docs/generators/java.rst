Java
======

Overview
--------

The Java generator produces java class files from a LinkML model,
with optional support for user-supplied jinja2 templates to generate
classes with alternate annotations or additional documentation.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.javagen

.. click:: linkml.generators.javagen:cli
    :prog: gen-java
    :nested: short

Code
^^^^


.. autoclass:: JavaGenerator
    :members: serialize

Configurable Behaviors
----------------------

Rendering of Enumerations
^^^^^^^^^^^^^^^^^^^^^^^^^

LinkML enumerations can be rendered in two ways:

* as plain `String` objects: that is, the enumeration themselves are
  *not* rendered at all, and slots whose range is set to an enumeration
  are rendered as `String`-typed fields;
* as standard Java ``enum`` objects.

For backwards compatibility reasons, the default behavior is to render
enumerations as `String` objects. Use the ``--true-enums`` option
(from the command line) or the ``true_enums`` named parameter (in the
`JavaGenerator` constructor) to render LinkML enumerations as standard
Java ``enum`` objects. Of note, this settings applies to all enumerations
defined in the LinkML schema – it is not possible to render some
enumerations as `String` objects and others as standard ``enum``
objects.

Use of Slot Aliases
^^^^^^^^^^^^^^^^^^^

Slots in a LinkML schema can optionally have an
`alias <https://linkml.io/linkml-model/latest/docs/alias/>`__, which, if
present, is intended to be “used instead of the actual slot name”.

By default, the Java generator always derives the name of a field in a
class from the actual name of the slot, *not* from its alias. Use the
``--use-aliases`` option (from the command line) or the ``use_aliases``
named parameter (in the `JavaGenerator` constructor) to force the
generator to honor the presence of a slot alias.

For example, given the definition of the ``slot_definitions`` slot in
LinkML’s own metamodel:

.. code-block:: yaml

  slot_definitions:
    domain: schema_definition
    multivalued: true
    range: slot_definition
    inlined: true
    alias: slots

the generator will, by default, render this slot as a field named
``slotDefinitions`` (derived from the actual slot name, ignoring the
``slots`` alias):

.. code-block:: java

  private List<SlotDefinition> slotDefinitions;

With ``--use-aliases``, that slot will instead be rendered as:

.. code-block:: java

  private List<SlotDefinition> slots;

Of note, when using the ``org.incenp.linkml`` template variant, the slot
alias, when present, is always used to determine how the slot is
expected to be serialised in the JSON or YAML serialisations; the
``--use-aliases`` option only affects the symbol used to represent the
slot in the Java code.

Package Configuration
---------------------
The generated Java ``package`` statement is driven by the following precedence:

1. ``--package`` command-line option (or ``package=...`` when using ``JavaGenerator`` programmatically)
2. ``generator_args.java.package`` set via ``--config-file``/``-C`` (see :ref:`java-configuration-file` below)
3. Fallback default: ``example``

NOTE:
    The package name is *not* configurable via schema-level annotations: LinkML
    classes, slots, and enums live in a single global namespace regardless of
    which (sub-)schema declares them - the package is a global configuration for
    the generator, not a property of the model.


The package applies to every generated class and enum: ``gen-java`` emits one file per
class into a single flat output directory, and cross-class references rely on all
generated types sharing one package.

.. _java-configuration-file:

Configuration File
-------------------

As an alternative to the ``--package`` argument, ``gen-java`` accepts a
``--config-file``/``-C`` YAML file -- the **same format** used by
``gen-project``'s own ``--config-file`` (see :doc:`project-generator`), so a single
project-wide ``config.yaml`` can be shared between ``gen-project`` and a
standalone ``gen-java`` run. ``package`` lives under ``generator_args.java``,
since that file is structured to configure every generator at once:

.. code-block:: yaml

    # config.yaml
    generator_args:
      java:
        package: org.example.model

``gen-java`` only ever reads ``generator_args.java.package`` out of this file --
every other key (``directory``, ``excludes``, other generators' ``generator_args``
entries, etc.) is ignored, so a full multi-generator project ``config.yaml`` can be
passed as-is without modification.

An explicit ``--package`` command-line option always overrides a value set via
``--config-file``.

The same configuration-file mechanism is supported by ``gen-golang`` (see
:doc:`golang`), which reads ``generator_args.golang.package`` from the same file.


Generating Visitor Patterns
---------------------------

The Java generator includes a built-in feature to easily implement a
`visitor pattern <https://en.wikipedia.org/wiki/Visitor_pattern>`__ over
a class hierarchy defined in a LinkML schema.

Assuming the following schema (simplified excerpt from the
`KGCL Schema <https://w3id.org/kgcl/>`__):

.. code-block:: yaml

  classes:
    Change:
      description: Any change perform on an ontology or knowledge graph.
      slots:
        - id
        - type

    SimpleChange:
      is_a: Change
      description: A change that is about a single ontology element.
      slots:
        - old_value
        - new_value

    ComplexChange:
      is_a: Change
      description: A change that is a composition of other changes.
      slots:
        - change_set

    # Several dozens of other subclasses (direct or indirect) of Change,
    # representing various specialized types of change...

Calling the Java generator with ``--visitor Change`` (on the command
line; ``visitors=["Change"]`` when calling the ``serialize`` method)
will cause the generator to

(a) create a `IChangeVisitor` interface containing a ``visit`` method
for each subclass of `Change` (and for `Change` itself):

.. code-block:: java

  public interface IChangeVisitor {
      public void visit(Change visited);
      public void visit(SimpleChange visited);
      public void visit(ComplexChange visited);
      /* and so on for all other subclasses... */
  }

(b) add a ``accept(IChangeVisitor)`` method to the `Change` class and to
all its subclasses, e.g. in ``SimpleChange.java``:

.. code-block:: java

  public class SimpleChange extends Change {

      /* Normal code generated for the SimpleChange class... */

      public void accept(IChangeVisitor visitor) {
          visitor.visit(this);
      }
  }

Template Variants
-----------------

The Java generator offers different templates allowing to generate
different “flavors” of Java code to represent the same LinkML schema.

A set of template (hereafter called a “template variant”) is selected on
the command line by the ``--template-variant`` option, or in Python code
by the ``template_variant`` named parameter to the ``serialize`` method.

LinkML currently provides three Java template variants:

* the default variant;
* the `records` variant;
* and the `org.incenp.linkml` variant.

Default Variant
^^^^^^^^^^^^^^^

The default template variant (which is used when no other variant is
explicitly requested) generates Java classes that use Project Lombok’s
`@Data <https://projectlombok.org/>`__ annotations to provide getters,
setters, equals and hashcode functionality.

Records Variant
^^^^^^^^^^^^^^^

The `records` variant represents LinkML classes as Java
`Record classes <https://openjdk.org/jeps/359>`__, which are intended to
hold *immutable data*.

Note that Record classes are only available since Java 14 as a feature
preview, and as an official feature since Java 16.

Also note that a Record class cannot extend another class. If a class
`Bar` is defined in a LinkML schema as extending a class `Foo`, the
`records` variant will generate a Java `Bar` class that will contain all
the slots from the `Foo` class but that will *not* be a subclass of
`Foo` (meaning for example that it will not be possible to assign an
instance of `Bar` to a `Foo`-typed slot). This makes the `records`
variant unlikely to be suitable for schemas that have complex class
hierarchies.

org.incenp.linkml Variant
^^^^^^^^^^^^^^^^^^^^^^^^^

The `org.incenp.linkml` variant generates Java code that is suitable for
use with the `LinkML-Java <https://incenp.org/dvlpt/linkml-java/>`__
runtime library – that is, code that meets the requirements set forth in
the `runtime documentation <https://incenp.org/dvlpt/linkml-java/linkml-core/codegen.html>`__.

This allows to use said runtime to easily load data (conformant to the
LinkML schema from which the code was generated) from files into the
Java in-memory representation, and conversely to dump data from the
Java representation into files.

Template Selection Logic
------------------------

The template selection logic used by the Java generator allows to
fine-tune which template is used for any given class or enum.

When generating the code for a given class *Foo*, and assuming a
template variant *V* has been requested (with ``--template-variant=V``),
the generator will look up for the following template files, using the
first one that it finds:

* ``Foo-V.jinja2`` (the *V* variant template specific for the *Foo*
  class);
* ``class-V.jinja2`` (the generic *V* variant template for all classes);
* ``Foo.jinja2`` (default template specific for the *Foo* class);
* ``class.jinja2`` (generic default template for all classes).

When no variant is explicitly requested, the first two lookups are
skipped, meaning the generator will look up first for ``Foo.jinja2`` and
then for ``class.jinja2``.

When the ``--true-enums`` option is enabled, the same logic will also be
used to find the template file to render an enumeration *Bar*:

* ``Bar-V.jinja2`` (the *V* variant template specific for the *Bar*
  enumeration);
* ``enum-V.jinja2`` (the generic *V* variant template for all
  enumerations);
* ``Bar.jinja2`` (default template specific for the *Bar* enumeration);
* ``enum.jinja2`` (generic default template for all enumerations).

By default, all templates are looked up in the generator’s internal
template directory. Use the ``--template-dir=D`` option to make the
generator look up first in the specified directory *D*; any template
file found in that directory will take precedence over the templates
from the internal directory.

Lastly, use the ``--template-file=F`` option to force the generator to
always use the specified template. This overrides all the logic
described above.

Examples
--------

Biolink Example
^^^^^^^^^^^^^^^

This example illustrates how to generate a Java package containing a
Java representation of the Biolink model, using the default
(Lombok-dependent) templates.

This assumes a working installation of LinkML. Check the
:doc:`Quick Install Guide <../intro/install>` if needed.

Begin by downloading the YAML file containing the Biolink schema:

.. code-block:: bash

    curl -OJ https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml

Now generate the classes using the `generate java` command:

.. code-block:: bash

    linkml generate java --package org.biolink.model \
                         --output-directory org/biolink/model \
                         biolink-model.yaml

Finally, fetch the Lombok jar, build the java classes and package into a
jar file:

.. code-block:: bash

    curl -OJ https://repo1.maven.org/maven2/org/projectlombok/lombok/1.18.20/lombok-1.18.20.jar
    javac org/biolink/model/*.java -cp lombok-1.18.20.jar
    jar -cf biolink-model.jar org

Alternate Template Example
^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an alternate template using Hibernate JPA annotations, named
``example_template.java.jinja2``:

.. code-block::

    package {{ doc.package }};

    import java.util.List;
    import lombok.*;
    import javax.persistence.*;
    import org.hibernate.search.engine.backend.types.*;
    import org.hibernate.envers.Audited;
    import org.hibernate.search.mapper.pojo.mapping.definition.annotation.*;


    @Audited
    @Indexed
    @Entity
    @Data @EqualsAndHashCode(onlyExplicitlyIncluded = true, callSuper = true)
    public class {{ cls.name }} {% if cls.is_a -%} extends {{ cls.is_a }} {%- endif %} {
    {% for f in cls.fields %}
      private {{f.range}} {{ f.name }};
    {%- endfor %}

    }

The alternate template for the generator can be specified with the
``--template-file`` option:

.. code-block::

   linkml generate java --package org.biolink.model \
                        --output-directory org/biolink/model \
                        --template-file example_template.java.jinja2 \
                        biolink-model.yaml
