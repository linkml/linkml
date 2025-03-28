CSV
========
This generator outputs the classes of the LinkML schema in CSV form. Each row contains the identifier, mappings and description of each class in the schema.

This generator does not output a CSV that is configured based on the template (e.g. where each sheet is a class and column headers are slots), but rather it transforms the template itself into a CSV. It cannot be used to generate templates for inputting data.  

Auto-generated docs
----

Code
^^^^
.. automodule:: linkml.generators.csvgen
    :members:
    :undoc-members:

Command Line
^^^^^^^^^^^^
*Note: The output from this command needs to be piped in order to create a CSV file.*

.. click:: linkml.generators.csvgen:cli
    :prog: gen-csv
