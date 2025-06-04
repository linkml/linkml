ShEx
======

Example Output
--------------

`personinfo.shex <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/shex/personinfo.shex>`_

Overview
--------

`ShEx <http://shex.io/shex-semantics/index.html>`__, short for Shape
Expressions Language is a modeling language for RDF files. This
generator can be used to create ShEx shapefiles, which can then be
used to validate RDF data.

ShEx provides similar functionality to SHACL, which has its own validator

To run:

.. code:: bash

   gen-shex personinfo.yaml > personinfo.shex

Translation
^^^^^^^^^^^

An example of translating the personinfo schema is shown below.

.. code-block:: shex

    <NamedThing>  (
        CLOSED {
           (  $<NamedThing_tes> (  schema:name @linkml:String ? ;
                 schema:description @linkml:String ? ;
                 schema:image @linkml:String ?
              ) ;
              rdf:type [ <NamedThing> ]
           )
        } OR @<Concept> OR @<Organization> OR @<Person>
    )
    <Person> CLOSED {
        (  $<Person_tes> (  &<NamedThing_tes> ;
              rdf:type [ <NamedThing> ] ? ;
              &<HasAliases_tes> ;
              rdf:type [ <HasAliases> ] ? ;
              <primary_email> @linkml:String ? ;
              schema:birthDate @linkml:String ? ;
              <age_in_years> @linkml:Integer ? ;
              schema:gender @<GenderType> ? ;
              <current_address> @<Address> ? ;
              <has_employment_history> @<EmploymentEvent> * ;
              <has_familial_relationships> @<FamilialRelationship> * ;
              <has_medical_history> @<MedicalEvent> * ;
              <aliases> @linkml:String *
           ) ;
           rdf:type [ schema:Person ]
        )
    }

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.shexgen

.. click:: linkml.generators.shexgen:cli
    :prog: gen-shex
    :nested: short

Code
^^^^


.. autoclass:: ShExGenerator
    :members: serialize
