Excel Spreadsheet
=================

This generator allows you to create a spreadsheet template from your
LinkML schema.

.. seealso:: `SchemaSheets <https://github.com/linkml/schemasheets>`_
             for maintaining schemas as spreadsheets


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

The generator also supports validation at the enum level. In that, each slot with a range property
that is of enum type will have associated drop downs for all cells corresponding to that slot in the excel spreadsheet.

Note: It works best for "flat" or denormalized schemas.

Caveat:
One of the features of ``gen-excel`` is that it has the ability to add Data Validation to columns
that have a range of an enumeration type in the form of dropdowns. A caveat within Microsoft Excel
is that the Data Validation list formula is limited to 255 characters, meaning, if the length of
all strings (permissible values) in your enumeration exceed 255 characters (combined, with separators),
then it will result in the creation of a "corrputed" Excel file. You will notice this when you try to
open up the Excel file, and Excel will prompt you with an error message saying: *We found a problem
with some content in 'xyz.xlsx'. Do you want us to try to recover as much as we can?* In order to
avoid any warning pop ups, we are simply turning off dropdown Data Validation for columns constrained
by enumerations with total length > 255 characters.

Additional validation support to be added:

* Color schemes to indicate whether a field is required or recommended
* Constraints based on the range of a slot, e.g. constraining Integer fields to be numbers
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
