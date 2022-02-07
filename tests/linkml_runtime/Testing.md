# LinkML-runtime test harness
A description of the existing LinkML testing system as envisioned by
Harold Solbrig and Dazhi Ziao

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

### `eval_single_file` signature
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
  endings (TODO: Should this be a filter function?) and emit a short message if they aren't the same