CSV
========
This generator outputs the classes of the LinkML schema in CSV format. Each row contains the identifier, mappings and description of each class in the schema.

This generator does not output a CSV that is configured based on the template. If fillable template spreadsheets are required, consider using [gen-excel](https://linkml.io/linkml/generators/excel.html) or [DataHarmonizer](https://github.com/cidgoh/DataHarmonizer). 

Auto-generated docs
-------------------

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
