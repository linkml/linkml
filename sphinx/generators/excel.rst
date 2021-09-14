Excel Spreadsheet
=================

This feature is still in development.

Example Output
--------------

Using the Person LinkML `schema <https://github.com/linkml/linkml/blob/main/examples/PersonSchema/personinfo.yaml>`_ as
input, the generated Excel spreadsheet looks as follows: `personinfo.xlsx <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/excel/personinfo.xlsx>`_

Overview
--------

You can create an Excel template of a LinkML schema as follows:

.. code:: bash

   gen-excel ~/path/to/personinfo.yaml --output ~/path/to/personinfo.xlsx


Currently, in the generated Excel workbook there can be one or more associated worksheets, each corresponding to classes
from the LinkML schema.

Note that this works best for "flat" or denormalized schemas

Support to be added:

* If the range of a slot is an enum, the possible values for a field will be constrained through a dropdown
* Color schemes to indicate whether a field is required or recommended
* Constraints based on the range of a slot, e.g. constraining int fields to be numbers
* Tooltip notes describing what each field indicates

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.excelgen:cli
    :prog: gen-excel
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.excelgen
