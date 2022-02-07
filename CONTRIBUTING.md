## Contribution Guidelines

### How to Author a Unit Test for an Issue

The following section has instructions on how to write a unit test specific to an issue that you are encountering.

* There are a number of repos under the linkml [organization](https://github.com/linkml) banner. Such as the main [linkml](https://github.com/linkml/linkml) library, [linkml-runtime](https://github.com/linkml/linkml-runtime), [linkml-owl](https://github.com/linkml/linkml-owl), etc. Make sure you are creating the test in the appropriate repo. For ex., if there is a bug that you have noticed with respect to one of the generators, then you want to be creating the test in the main linkml library repo.
* The location where all the issue specific unit tests are created, is in this location: [linkml/tests/test-issues](https://github.com/linkml/linkml/tree/main/tests/test_issues).
* You can create a new test called `test_linkml_issue_NNN.py`. It is perhaps easiest to just copy over a test from an existing issue and modify it.

Note: You will see a number of issues which are named `test_issue_NNN.py`. The numbers and convention for those issues are with reference to the old biolinkml issue numbering convention.

* All tests within this repo are Python [unittest](https://docs.python.org/3/library/unittest.html) tests. The unittest module is bundled natively with the latest versions of Python. The tests can be run using either the unittest module, or using the [pytest](https://docs.pytest.org/en/6.2.x/) library.

To run your test using unittest:

```python
python -m unittest tests/test_issues/test_linkml_issue_NNN.py
```

To run your test using pytest:

```python
pytest tests/test_issues/test_linkml_issue_NNN.py
```

* Most tests will use a schema, and sometimes a datafile as input. One pattern is that you include in the Python file as docstrings. Another pattern is to include them as separate YAML files. If you include separate YAML files, then they must be added to the following location: [tests/test_issues/input](https://github.com/linkml/linkml/tree/main/tests/test_issues/input), and follow the same naming convention as the test_issue itself, i.e., `linkml_issue_NNN.yaml`.

### How to Author a Unit Test for New Functionality

The following section has instructions on how to write a unit test for new functionality that you are requesting.

Follow the same procedure as above, but add this test to the appropriate folder. For example, if you are requesting a new LinkML generator, then the test must be added to this location: [tests/test_generators](https://github.com/linkml/linkml/tree/main/tests/test_generators).

### General Tips

* Always make sure to use `assert` statements to compare the expected value with the actual value, rather than simply printing or logging the expected and actual values.
* Avoid using `print` statements for logging purposes. Use the `logging` module natively provided by Python approporiately with it's various logging levels like `DEBUG`, `INFO`, `ERROR`, etc.
* You can create a config file by copying the [test_config.ini.example](https://github.com/linkml/linkml/blob/main/tests/test_config.ini.example) to a `test_config.ini` file and making changes, for example, to the logging levels:

```
[test.settings]
DEFAULT_LOG_LEVEL: logging.ERROR
DEFAULT_LOG_LEVEL_TEXT: ERROR
```

* Never hardcode any file paths. Always use import variables such as `INPUT_DIR`, `OUTPUT_DIR` and use `os.path.join()` to make file paths. This ensures that the tests will run independent of the OS they are running on.

### Running Tests Locally

PyCharm, IntelliJ:

To run a single test:
* Open to Run/Debug
* `+` to add test
* Choose Python "tests > unittests"
* In dialog:
  * Target: Select Script path, browse to test script
  * Choose Python interpreter
  * Click ‘OK’ to save
* Run or debug the test from the configurations menu

To run all tests:
* Open to Run/Debug
* `+` to add test
* Choose “Python tests > unittests”

### Release to PyPI

A Github action is set up to automatically release the package to PyPI. When it is ready for a new release, create a [Github release](https://github.com/linkml/releases). The version should be in the vX.X.X format following [the semantic versioning specification](https://semver.org/).

After the release is created, the GitHub action will be triggered to publish to PyPI. The release version will be used to create the PyPI package.

If the PyPI release failed, make fixes, [delete](https://docs.github.com/en/enterprise/2.16/user/github/administering-a-repository/editing-and-deleting-releases#deleting-a-release) the GitHub release, and recreate a release with the same version again.
