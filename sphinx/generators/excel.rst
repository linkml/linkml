Excel Spreadsheet
=================

This feature is still in development.

Example Output
--------------

Using the Person LinkML `schema <https://github.com/linkml/linkml/blob/main/examples/PersonSchema/personinfo.yaml>`_ as
input, the generated Excel spreadsheet looks as follows: `personinfo.xlsx <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/excel/personinfo.xlsx>`_

Overview
--------

You can create a rudimentary Excel spreadsheet visualization of the LinkML schema by running the following command:

.. code:: bash

   gen-excel ~/path/to/personinfo.yaml --output ~/path/to/personinfo.xlsx

Currently, in the generated Excel workbook there can be one or more associated worksheets, each corresponding to classes
from the LinkML schema.

Support to be added:

* If the range of a slot is an enum, the possible values for a field will be constrained through a dropdown
* Color schemes to indicate scenarios like, required fields, etc.
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
