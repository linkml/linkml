# LinkML-runtime test harness
A description of the existing LinkML testing system as envisioned by
Harold Solbrig and Dazhi Ziao

__Note:__ The description below was written in the context of 
[linkml-runtime](https://github.com/linkml/linkml-runtime).  Many (most?) of
the actual testing is performed in [linkml](https://github.com/linkml/linkml)
proper.  This document needs to become a single text that covers _both_ of 
these test envirnoments.  See: [duplicate testing code issue](https://github.com/linkml/linkml-runtime/issues/125)
for followup.

## Philosophy
The intent of the test harness is to verify that every intentional
feature of LinkML exists and behaves correctly.  If there isn't a
test for a particular behavior or feature, developers should feel
free to alter or remove it as long as doing so doesn't break any
existing system test.

Corollary - any code that isn't covered by the test suite should
either:
a) Be removed as an artifact of a development branch that is no
used or
b) Have a test added for it

## Basics 
All unit tests must be in the `tests` directory
Tests are grouped by general function or purpose through the use 
of python packages.  At the time of this writing, the following
testing packages were in use:

      +tests
        |
        + support -- utilities to support testing.  NOT tested themselves
        |
        + test_enumerations -- collection of tests to validate the enumerations
        |                      package
        + test_issues -- tests to demonstrate failure and fix of issues
        |
        + test_loaders_dumpers -- tests for linkml_runtime.loaders and linkml_runtime.dumpers
        |
        + test_utils -- tests for linkml_runtime.utils
        |
        + __init__.py -- basic code to set up the test harness.
        |
        + environment.py -- code to establish a relative position in the file system
        |
        + Testing.md -- this document
        |
        + test_config.ini.example -- example test configuration file


### Background
Unit tests that validate output tend to follow the following evolutionary path:
1) Developer 1 runs some bit of code that generates output that appears in 
   `print` statement:
    ```python
    import unittest

    class DoItTestCase(unittest.TestCase):
      def test_my_new_function(self):
        print(my_new_function())

    if __name__ == '__main__':
       unittest.main()
    ```
   The developer then looks at the output and determines a) it didn't
   blow up and b) it has what the developer expects.
2) Developer 2 makes a tweak that changes the output of `my_new_function`
   They are unaware that they need to check the output of the `print`
   statement and, in fact, may have no idea what *was* expected.
3) Developer 1 discovers that the code no longer works.  They fix the
   problem and change the unit test to read:
   ```python
   import unittest
   
   expected = '''
      Date: Mon, Feb 7, 2021
      model Foo: expected
   '''

   class DoItTestCase(unittest.TestCase):
   def test_my_new_function(self):
      self.assertEqual(expected, str(my_new_function())

   if __name__ == '__main__':
      unittest.main()
   ```
   After doing a bunch of messing w/ tabs and line feeds, developer 
   1 finally gets this to work (on a Mac), and submits the revision.
   Soon after submission, the test fails because the test was run
   on Tue, Feb 8, so the text no longer matches. Developer 1 updates
   the test to mung the data specific information:
   ```python
   def test_my_new_function(self):
        self.assertEqual(fix_date_string(expected), fix_date_string(my_new_function()))
   ```
4) Developer 3 _enhances_ `my_new_function`, changing "model" to "Model"
   When they run the unit tests, `test_my_new_function` fails, along with
   several other function test cases that now utilize `my_new_function`.
   Developer 3 has to go through _each_ of these failures to a) confirm
   that they failed because of the change and b) editing the test cases 
   to reflect the new output.

   At some point, developer 3 realizes that all these individual edits
   are time consuming and error prone.  They decide to do the following:
   a) Create two directories -- one that has files containing the expected
      output of test cases and a second that has what is actually generated.
   b) Create a mechanism that allows the expected output to be updated to
      reflect changes once they have determined that the change is expected.

   Developer 3 submits their new changes:
   ```python
    def test_my_new_function(self):
        expected = fix_date_string(open('output/doit.txt'))
        actual = my_new_function()
        if expected != fix_date_string(actual):
            if OVERWRITING:
                print("Warning...")
                with open('output/doit.txt', 'w') as f:
                    f.write(actual)
            else:
                self.assertEqual(expected, fix_date_string(actual))
   ```
   and includes the local output directory.
5) We now have multiple potential problems:
   1) Unit tests don't always run in the same relative spot.  When run
      in batch, the working directory may be `tests`, its parent or
      some other directory entirely.  The relative paths above won't work
   2) If two developers both submit changes that impact the output of
      the test files, the second one to issue a pull request may get a
      bolus of merge failures as two different sets of changes to the same
      output files occur.
   3) The comparison failures occur in a single log stream.  Determining
      what changed and where becomes a labor intensive effort.

## Current state of affairs
The current test harness attempts to address the above scenario as well
with a number of related issues not discussed.  It has the following:

### Relative file paths and consistent naming
Every package (i.e. subdirectory) in the `tests` directory should
have the following file named `environment.py`:
```python
from tests.support.test_environment import TestEnvironment

env = TestEnvironment(__file__)
```
This creates a set of testing utilities and variables anchored
in the directory that contains `environment.py`.  Tests run in the
`test_issues` directory will use `tests/test_issues/input` for inputs
to tests, `tests/test_issues/output` for expected output, and
`tests/test_issues/temp` for writing to when testing functions that
write to disk.

__Note that these directories are _local_ to the test space.  `test_issues`
has a different output directory than `test_loaders_dumpers`__

### `TestEnvironment` constants:
* `self.cwd` - directory that contains the input, output and test files
* `self.indir` - directory containing function inputs, such as a yaml file to be parsed
* `self.outdir` - directory containing `expected` function outputs
* `self.tempdir` - directory for saving `actual` function outputs

* `self.import_map` - Location of the import map (if any).  This map is used to allow import statements
  to be overridden so that you can test changes to dependencies.  See: TBD for more details
* `self.mismatch_action` - what to do if expected doesn't match output:
  * `Ignore` - be silent.  Say nothing about errors
  * `Report` - issue a warning whenever there is a mismatch (Default)
  * `Fail` - take the UnitTest.fail action when the first mismatch occurs
  * `FailOnce` - take the UnitTest.fail action AFTER running all tests if one or more failed.  `FailOnce`
    issues report warnings along the way
* `self.root_input_path` - testing root input path.  Used for inputs such as "meta.yaml" that are
   used across many testing nodes
* `self.root_expected_path` = testing root expected 
* `self.root_temp_file_path` = testing root temp
* `self._log` - logger for logging errors.  Same across all tests, defined in `tests/support/mismatchlog.py`

### `TestEnvironment` functions:
* `clear_log() -> None` - throw away the current output log and open a new copy
* `input_path(*path: str) -> str` - return a relative path anchored on `self.indir`, where each
   `path` element is a directory
* `expected_path(*path: str) -> str` - return a relative path anchored on `self.outdir`
* `actual_path(*path: str, is_dir: bool = False) -> str` - _create_ `path` if it doesn't already
   exist. If `is_dir` is `True`, directories are created all the way down.  If `False`, the last
   element in `path` is treated as a non-directory and is not created.
* `temp_file_path(*path: str, is_dir: bool = False` - Same as actual path, except for scratch files
   Note: In the current implementation, actual and temp share the same directory.  This may not always
   be the case.
* `log(file_or_directory: str, message: Optional[str] = None) -> None` - record an "error", acting 
  according to the setting of `self.mismatch_action`.  `file_or_directory` names the file associated
  with the error and `message` an optional identification of what was wrong.  

  The current `log` behavior is to create an ordered list of error messages, which, depending upon
  the `mismatch_action`, get printed at the end of the run.  Other, more complex behaviors are possible.

  Note that `MismatchLog` does some cleaning up on the stack trace to focus in on the actual cause
  of the problem.  

## Using the testing environment
### Test class setup
The first example below implements the example we described above using the test harness:
```python
from tests.support.test_environment import TestEnvironmentTestCase

from tests.test_issues.environment import env

from linkml_runtime.utils import my_function


class MyFunctionTestCase(TestEnvironmentTestCase):
    env = env
 
    def test_single_file(self):
        """ Test that my function behaves correctly with a single output file """
        output_text = my_function(env.input_path('input.txt'))
        self.env.eval_single_file('input.mod', output_text)
```
The above test will invoke `my_function` with the path `tests\test_dir\input\input.txt`.  It
will then compare the output with `tests\test_dir\output\input.mod` with the following results
* if `input.mod` matches `output_text` _or_ `self.mismatch_action == Ignore`, nothing happens
* `output_text` will be written to `tests\test_dir\temp\input.mod`.  Based on the `self.mismatch_action` setting:
  * `Fail` - a notice of mismatch will be given and `self.assertFail` will be invoked
  * `Report` or `FailOnce` - the notice will be recorded in `self.log`

At the _end_ of `MyFunctionTestCase` execution, `self.log` will be printed as output and, if `FailOnce`,
`self.assertFail` will be raised.

### eval_single_file 
`eval_single_file(expected_file_path: str, actual_text: str, filtr: Callable[[str], str] = None, comparator: Callable[[str, str], str] = None) -> bool:`

* `expected_file_path` - path to expected output in `output` directory
* `actual` - text of the actual file
* `filtr` - filter that is applied to _both_ the contents of `expected_file_path` and `actual` to
  remove context dependent things such as dates, etc.  The default `filtr` is the identity function
  (no filter).  Note that there is a library of filters in `tests/support/filters.py`, including:
  * ldcontext_metadata_filter - for JSON-LD context files output
  * json_metadata_filter - for JSON output
  * metadata_filter - for output that uses '#' as comments and includes metadata
  * yaml_filter - for LinkML output yaml files
  * nb_filter - for Jupyter notebooks
* `comparator` - takes two strings as input (`expected` and `actual`), tweaks the unix/dos line
  endings (TODO: Should this be a filter function?) and emit a short message if they aren't the same.
  Several pre-existing comparators can be found in `tests/support/clicktestcase.py`, including:
  * ClickTestCase.jsonld_comparator - compare json ld output
  * ClickTestCase.n3_comparator - compare n3 format output
  * ClickTestCase.rdf_comparator - compare RDF in any format (3 args, expected, actual, format)
  * ClickTestCase.always_pass_comparator - always true. (Note: doesn't appear to be used at the moment)

Note that, if the expected output file does not exist, eval_single_file creates the missing file and
then logs it as a mismatch.  If the `mismatch_action` is `Ignore` or `Report`, any missing or 
mismatched files will be updated.

## Unit tests for LinkML generators
Quite frequently, one wants to test test a LinkML generator (e.g. Markdowngen, pythongen, etc.).  While
the actual generator code now resides in the [linkml](https://github.com/linkml/linkml) project, the
test code managed to end up in [linkml-runtime](https://github.com/linkml/linkml-runtime) in the
code split.

LinkML generators can have one of several behaviors:
1) Generate output to stdout (e.g. pythongen)
2) Generate output to a single file
3) Generate multiple outputs to a directory

`TestEnvironment.generate_single_file` covers the first two cases and `TestEnvironment.generate_directory`
covers the third.  Both are described below.

## generate_single_file
`def generate_single_file(self, filename: Union[str, List[str]], generator: Callable[[Optional[str]], Optional[str]],
value_is_returned: bool = False, filtr: Callable[[str], str] = None,
comparator: Callable[[str, str], str] = None, use_testing_root: bool = False) -> str`

* `filename` - the path of the input file(s) relative to `self.indir`.  This is almost always a
   LinkML schema (yaml) file.
* `generator` -

### Use example
```python
import unittest

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env
from tests.utils.python_comparator import compare_python
from tests.utils.test_environment import TestEnvironmentTestCase


class Issue106TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_106(self):
        env.generate_single_file('issue_106.py',
                                 lambda: PythonGenerator(env.input_path('issue_106.yaml')).serialize(),
                                 comparator=lambda exp, act: compare_python(exp, act, self.env.expected_path('issue_106.py')),
                                 value_is_returned=True)


if __name__ == '__main__':
    unittest.main()
```
The above example calls the PythonGenerator with `issue_106.yaml` from the local `input` directory
as an input.  The python generator returns a string (`value_is_returned == True`), which is then 
compared with `issue_106.py` in the local `output` directory.  The `compare_python` comparator is used,
which compares the generated text with `output/issue_106.py`.  If the files do not match or `output/issue_106.py'
doesn't exist:
* if `self.mismatch_action` is `Fail` or `FailOnce`, the new output will be saved in `temp/issue_106.py`
  and a log message will ge generated.
* if `self.mismatch_action` is `Ignore` or `Report`, the new output will be saved in `output/issue_106.py`.

The general idea behind this is that the developer has a choice.  If mismatches aren't expected, they
can set `self.mismatch_action` to `Fail` (see: [TestEnvironment.md](TestEnvironment.md) for details
on how to do this).  If the test fails, they can compare `temp/issue_106.py` with `output/issue_106.py`
to understand the problem.  On the other hand, if `self.mismatch_action` is `Report` (the default),
they can use `git diff` or local history in PyCharm to determine what the changes were.

### Slightly more complex example
```python
import unittest

from linkml.generators.owlgen import OwlSchemaGenerator
from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDF
from tests.utils.compare_rdf import compare_rdf
from tests.utils.test_environment import TestEnvironmentTestCase

from tests.test_issues.environment import env


# Tests: https://github.com/biolink/biolinkml/issues/163
class IssueOWLNamespaceTestCase(TestEnvironmentTestCase):
    env = env

    def _test_owl(self, name: str) -> Graph:
        self.env.generate_single_file(f'{name}.owl',
                                      lambda: OwlSchemaGenerator(env.input_path(f'{name}.yaml'),
                                                                 importmap=env.import_map).serialize(),
                                      value_is_returned=True, comparator=compare_rdf)
        g = Graph()
        g.parse(env.expected_path(f'{name}.owl'), format="turtle")
        return g

    def test_issue_owl_namespace(self):
        """ Make sure that types are generated as part of the output """
        g = self._test_owl('issue_163')
        A = URIRef('http://example.org/A')
        self.assertIn((A, RDF.type, OWL.Class), g)
        NAME = URIRef('http://example.org/name')
        self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)

    def test_issue_no_default(self):
        """ Make sure that types are generated as part of the output """
        g = self._test_owl('issue_163b')
        
        A = URIRef('http://example.org/sample/example1/A')
        self.assertIn((A, RDF.type, OWL.Class), g)
        NAME = URIRef('http://example.org/sample/example1/name')
        self.assertIn((NAME, RDF.type, OWL.ObjectProperty), g)

    def test_aliases(self):
        """ Make sure aliases work """
        g = self._test_owl('issue_163c')


if __name__ == '__main__':
    unittest.main()

```
The above set of tests use the `OwlSchemaGenerator` to transform input YAML files into OWL turtle
format.  The `_test_owl` method takes an input file name (e.g. `input/issue_163.yaml`) and generates
the OWL turtle output (e.g. `input/issue_163.owl`). Note that in this case, we include `env.input_map`
as an additional parameter (not sure why but...).  It uses the RDF comparator on the output and,
assuming that the `Report` mode is in operation, the output file is updated if necessary.  _Note: We 
may want to consider what to do in `Fail` or `FailOnce` modes_.  This test case then returns the
generated OWL in the form of an RDF graph, which can be used to test for the presence or absence
of individual fields.

### generate_single_file parameters
* `filename` -- the relative path to the output file.  The file itself may be found in the `output`
  directory, the `temp` directory or both.  Example:  `issue_163.owl`.
* `generator` -- a function that converts an optional string into an optional output string.  Replace
  this with a lambda expression to invoke the actual code.  The generator can either return a string
  on stdout or save it to a file
* `value_is_returned` -- `True` means that the output on the generator can be found on stdout.  `False`
  means that the destination file name will be passed as a parameter to the generator function and
  the output will be found in that file
* `filtr` -- Optional filter to remove non-comparable information, normalize format, etc.
* `comparator` -- Optional comaprator that does non-standard (e.g. RDF) comparisons
* `use_testing_root` -- 'True' means that, instead of using the _local_ input, output and temp
  directories, those at the root of the testing package should be used.  This parameter is used
  when one wants to run tests on the standard linkml yaml files.


## generate_directory
`generate_directory(self, dirname: Union[str, List[str]], generator: Callable[[str], None]) -> None`
The `generate_directory` test is used to test generaters that produce multiple files (e.g. markdowngen)
### Parameters
* `dirname` -- the relative path of the output directory.  The directory will be first be created (and cleared)
  in the `temp` subdirectory. If a `list` is passed, each list element is a path element within the
  directory
* `generator` -- a function that takes the full path of the output directory as input and creates
   one or more files in that generator

`generate_directory` then compares all of the files in the `temp` directory with their equivalents
in the `output` directory.  If there are any differences, including files that have been added or
are missing, this is reported and, if the `mismatch_action` is `Ignore` or `Report`, the current
output directory will be removed and replaced with the temp directory.

### Example
```python
import unittest

from linkml.generators.markdowngen import MarkdownGenerator
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue65TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_65(self):
        """ Make sure that types are generated as part of the output """
        env.generate_directory('issue65',
                               lambda d: MarkdownGenerator(env.input_path('issue_65.yaml')).serialize(directory=d))


if __name__ == '__main__':
    unittest.main()
```
The above example:
1) Creates an empty directory named `issue65` in the local `temp` directory
2) Calls `generator` with the full path to `issue65`
3) Compares the contents of `temp/issue65` and `output/issue65` acting accordingly

## Testing the `Click` API
`ClickTestCase` is an extension of the `TestEnvironmentTestCase` that is use for testing the
`Click` interface of various generators.  The primary entry point in `ClickTestCase` is `do_test`:

### Signature
``` def do_test(self,
                args: Union[str, List[str]],
                testFileOrDirectory: Optional[str] = None,
                *,
                expected_error: type(Exception) = None,
                filtr: Optional[Callable[[str], str]] = None,
                is_directory: bool = False,
                add_yaml: bool = True,
                comparator: Callable[[type(unittest.TestCase), str, str, str], str] = None, ) -> None
 ```
* `args` - the command line arguments to the function. This can either be one long string that will
   be parsed (e.g. "-r schema_definition -r slot_definition") or a list of strings (e.g. 
   ["-r", "schema_definition", "-r", sd]). 
* `testFileOrDirectory` - where the output is to be put. _Note:_ this parameter is listed as optional,
   but the first line of code causes a failure if it isn't there.  TBD: change this signature.
* `expected_error` - if the unit test is expected to fail, this is the error that is expected
* `filtr` - filter to remove non-comparable data from the output and expected files
* `is_directory` - `True` means that `testFileOrDirectory` is a directory, not a file
* `add_yaml` - `True` means to to prepend the following string to the arguments:
    "tests/input/meta.yaml --importmap <importmap location> --log_level <DEFAULT LOG LEVEL>"
* `comparator` - file comparator

### ClickTestCase example
The following code tests tha various parameters of the CSV generator:
```python
import unittest
import click

from linkml.generators import csvgen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenCSVTestCase(ClickTestCase):
    testdir = "gencsv"
    click_ep = csvgen.cli
    prog_name = "gen-csv"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta.csv')
        self.do_test('-f tsv', 'meta.tsv')
        self.do_test('-f xsv', 'meta_error', expected_error=click.exceptions.BadParameter)
        self.do_test(["-r", "schema_definition"], 'meta_sd')
        self.do_test(["-r", "schema_definition", "-r", "slot_definition"], 'meta_sd_sd')
        self.do_test(["-r", "nada"], 'meta_sd', expected_error=ValueError)


if __name__ == '__main__':
    unittest.main()
```
The above code tests all (or at least most) of the options for `gencsv`.