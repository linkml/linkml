Java
======

Overview
--------

The Java Generator produces java class files from a linkml model,
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

Additional Notes
----------------

The Java generator's default template uses Project Lombok's `@Data <https://projectlombok.org/features/Data>`__ annotation, which provides getters, setters, equals and hashcode functionality.


Biolink Example
---------------

Begin by downloading the Biolink Model YAML and adding a virtual environment and installing linkml.

.. code-block:: bash

    curl -OJ https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml
    python3 -m venv venv
    source venv/bin/activate
    pip install linkml

Now generate the classes using the `gen-java` command

.. code-block:: bash

    gen-java --package org.biolink.model --output_directory org/biolink/model biolink-model.yaml

Finally, fetch the Lombok jar, build the java classes and package into a jar file

.. code-block:: bash

    curl -OJ https://repo1.maven.org/maven2/org/projectlombok/lombok/1.18.20/lombok-1.18.20.jar
    javac org/biolink/model/*.java -cp lombok-1.18.20.jar
    jar -cf biolink-model.jar org


Alternate Template Example
--------------------------


Here is an alternate template using Hibernate JPA annotations, named `example_template.java.jinja2`

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

The alternate template for the generator can be specified with the `--template_file` option

.. code-block::

   gen-java --package org.biolink.model --output_directory org/biolink/model \
            --template_file example_template.java.jinja2 biolink-model.yaml
