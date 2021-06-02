import contextlib
import filecmp
import logging
import os
import shutil
import sys
import unittest
from enum import Enum
from importlib import import_module
from io import StringIO
from pathlib import Path
from typing import Optional, Callable, Union, List

from linkml_runtime.linkml_model import linkml_files
from linkml_runtime.linkml_model.linkml_files import Source, Format

from linkml import LOCAL_METAMODEL_YAML_FILE, LOCAL_TYPES_YAML_FILE, LOCAL_MAPPINGS_YAML_FILE
from tests.utils.dirutils import are_dir_trees_equal
from tests.utils.mismatchlog import MismatchLog


def no_click_exit(_self, code=0):
    from tests import CLIExitException
    raise CLIExitException(code)


# This import has to occur here
import click
click.core.Context.exit = no_click_exit


class MismatchAction(Enum):
    Ignore = 0
    Report = 1
    Fail = 2
    FailOnce = 3                    # Run all tests and then fail if there are any mismatches


class TestEnvironment:
    import_map_warning_emitted: bool = False

    """ Testing environment """
    def __init__(self, filedir: str) -> None:
        self.cwd = os.path.dirname(filedir)                     # base directory for indir, outdir and tempdir
        self.indir = os.path.join(self.cwd, 'input')            # Input files
        self.outdir = os.path.join(self.cwd, 'output')          # Expected/actual output files
        self.tempdir = os.path.join(self.cwd, 'temp')           # Scratch directory for temporary work

        # Get the parent's directory name.  If it is a test directory, borrow from its environment
        parent = Path(self.cwd).parts[-2]
        if parent.startswith('test'):
            parent_env = import_module('..environment', __package__)
            self.meta_yaml = linkml_files.LOCAL_PATH_FOR(Source.META, Format.YAML)
            self.types_yaml = linkml_files.LOCAL_PATH_FOR(Source.TYPES, Format.YAML)
            self.mapping_yaml = linkml_files.LOCAL_PATH_FOR(Source.MAPPINGS, Format.YAML)
            self.import_map = parent_env.env.import_map
            self.mismatch_action = parent_env.env.mismatch_action
            self.root_input_path = parent_env.env.root_input_path
            self.root_expected_path = parent_env.env.root_expected_path
            self.root_temp_file_path = parent_env.env.root_temp_file_path
            self._log = parent_env.env._log
        else:
            self.meta_yaml = LOCAL_METAMODEL_YAML_FILE
            self.types_yaml = LOCAL_TYPES_YAML_FILE
            self.mapping_yaml = LOCAL_MAPPINGS_YAML_FILE

            from tests import USE_LOCAL_IMPORT_MAP
            self.import_map = self.input_path('local_import_map.json') if USE_LOCAL_IMPORT_MAP else None
            from tests import DEFAULT_MISMATCH_ACTION
            self.mismatch_action = DEFAULT_MISMATCH_ACTION
            self.root_input_path = self.input_path
            self.root_expected_path = self.expected_path
            self.root_temp_file_path = self.temp_file_path
            self._log = MismatchLog()

    @staticmethod
    def _check_changed(test_file: str, runtime_file: str) -> None:
        if not filecmp.cmp(test_file, runtime_file):
            print(
                f"WARNING: Test file {test_file} does not match {runtime_file}.  "
                f"You may want to update the test version and rerun")
        from tests import USE_LOCAL_IMPORT_MAP
        if USE_LOCAL_IMPORT_MAP and not TestEnvironment.import_map_warning_emitted:
            print(
                f"WARNING: USE_LOCAL_IMPORT_MAP must be reset to False before completing submission."
            )
            TestEnvironment.import_map_warning_emitted = True

    def clear_log(self) -> None:
        """ Clear the output log """
        self._log = MismatchLog()

    def input_path(self, *path: str) -> str:
        """ Create a file path in the local input directory """
        return os.path.join(self.indir, *[p for p in path if p])

    def expected_path(self, *path: str) -> str:
        """ Create a file path in the local output directory """
        return os.path.join(self.outdir, *[p for p in path if p])

    def actual_path(self, *path: str, is_dir: bool = False) -> str:
        """ Return the full path to the path fragments in path """
        dir_path = [p for p in (path if is_dir else path[:-1]) if p]
        self.make_temp_dir(*dir_path, clear=False)
        return os.path.join(self.tempdir, *[p for p in path if p])

    def temp_file_path(self, *path: str, is_dir: bool = False) -> str:
        """ Create the directories down to the path fragments in path.  If is_dir is True, create and clear the
         innermost directory
        """
        return self.actual_path(*path, is_dir=is_dir)

    def log(self, file_or_directory: str, message: Optional[str] = None) -> None:
        self._log.log(file_or_directory, message)

    @property
    def verb(self) -> str:
        return 'will be' if self.fail_on_error else 'was'

    @property
    def fail_on_error(self) -> bool:
        return self.mismatch_action == MismatchAction.Fail

    @property
    def report_errors(self) -> bool:
        return self.mismatch_action != MismatchAction.Ignore

    def __str__(self):
        """ Return the current state of the log file """
        return '\n\n'.join([str(e) for e in self._log.entries])

    def make_temp_dir(self, *paths: str, clear: bool = True) -> str:
        """ Create and initialize a list of paths """
        full_path = self.tempdir
        TestEnvironment.make_testing_directory(full_path)
        if len(paths):
            for i in range(len(paths)):
                full_path = os.path.join(full_path, paths[i])
                TestEnvironment.make_testing_directory(full_path, clear=clear and i == len(paths) - 1)
        return full_path

    def string_comparator(self, expected: str, actual: str) -> Optional[str]:
        """
        Compare two strings w/ embedded line feeds.  Return a simple match/nomatch output message
        :param expected: expected string
        :param actual: actual string
        :return: Error message if mismatch else None
        """
        if expected.replace('\r\n', '\n').strip() != actual.replace('\r\n', '\n').strip():
            return f"Output {self.verb} changed."

    @staticmethod
    def remove_testing_directory(directory: str) -> None:
        shutil.rmtree(directory, ignore_errors=True)

    @staticmethod
    def make_testing_directory(directory: str, clear: bool = False) -> None:
        """
        Create directory if necessary and clear it if requested
        :param directory: Directory to create
        :param clear: True means remove everything there
        """
        if clear or not os.path.exists(directory):
            safety_file = os.path.join(directory, "generated")
            if os.path.exists(directory):
                if not os.path.exists(safety_file):
                    raise FileNotFoundError(f"'generated' guard file not found in {directory}")
                shutil.rmtree(directory)
            os.makedirs(directory, exist_ok=True)
            with open(safety_file, "w") as f:
                f.write("Generated for safety.  Directory will not be cleared if this file is not present")

    def generate_directory(self, dirname: Union[str, List[str]], generator: Callable[[str], None]) -> None:
        """
        Invoke the generator and compare the output in a temp directory to the output directory.  Report the results
        and then update the output directory
        :param dirname: relative directory name (e.g. gengolr/meta)
        :param generator: function to create the output. First argument is the target directory
        """
        dirname = dirname if isinstance(dirname, List) else [dirname]
        temp_output_directory = self.make_temp_dir(*dirname)
        expected_output_directory = self.expected_path(*dirname)
        self.make_testing_directory(expected_output_directory)

        generator(temp_output_directory)

        diffs = are_dir_trees_equal(expected_output_directory, temp_output_directory)
        if diffs:
            self.log(expected_output_directory, diffs)
            if not self.fail_on_error:
                shutil.rmtree(expected_output_directory)
                os.rename(temp_output_directory, expected_output_directory)
        else:
            shutil.rmtree(temp_output_directory)

    def generate_single_file(self, filename: Union[str, List[str]], generator: Callable[[Optional[str]], Optional[str]],
                             value_is_returned: bool = False, filtr: Callable[[str], str] = None,
                             comparator: Callable[[str, str], str] = None, use_testing_root: bool = False) -> str:
        """
        Invoke the generator and compare the actual results to the expected.
        :param filename: relative file name(s) (no path)
        :param generator: output generator. Either produces a string or creates a file
        :param value_is_returned: True means that generator returns output directly
        :param filtr: Optional filter to remove non-compare information (e.g. dates, specific paths, etc.)
        :param comparator: Optional output comparison function.
        :param use_testing_root: True means output directory is in test root instead of local directory
        :return: the generator output
        """
        # If no filter, default to identity function
        if not filtr:
            filtr = lambda s: s
        filename = filename if isinstance(filename, List) else [filename]
        actual_file = self.root_temp_file_path(*filename) if use_testing_root else self.actual_path(*filename)
        expected_file = self.root_expected_path(*filename) if use_testing_root else self.expected_path(*filename)

        if value_is_returned:
            actual = generator()
        else:
            outf = StringIO()
            from tests import CLIExitException
            with contextlib.redirect_stdout(outf):
                try:
                    generator()
                except CLIExitException:
                    pass
            actual = outf.getvalue()

        if not self.eval_single_file(expected_file, actual, filtr, comparator):
            if self.fail_on_error:
                self.make_temp_dir(os.path.dirname(actual_file), clear=False)
                with open(actual_file, 'w') as actualf:
                    actualf.write(actual)
        return actual

    def eval_single_file(self, expected_file_path: str, actual_text: str, filtr: Callable[[str], str] = None,
                         comparator: Callable[[str, str], str] = None) -> bool:
        """ Compare actual_text to the contents of the expected file.  Log a message if there is a mismatch and
            overwrite the expected file if we're not in the fail on error mode
        """
        if filtr is None:
            filtr = lambda s: s
        if comparator is None:
            comparator = self.string_comparator
        if os.path.exists(expected_file_path):
            with open(expected_file_path) as expf:
                expected_text = filtr(expf.read())
            msg = comparator(expected_text, filtr(actual_text))
        else:
            msg = f"New file {self.verb} created"
            cmsg = comparator(actual_text, actual_text)
            if cmsg:
                msg = msg + '\n' + cmsg
        if msg:
            self.log(expected_file_path, msg)
        if msg and not self.fail_on_error:
            self.make_temp_dir(os.path.dirname(expected_file_path), clear=False)
            with open(expected_file_path, 'w') as outf:
                outf.write(actual_text)
        return not msg


class TestEnvironmentTestCase(unittest.TestCase):
    """
    A unit test TextCase with an environment inside.  env has to be initialized in situ, as it needs to reference the
    input, output and temp directories within the context of the particular set of tests.  To initialize
    this environment:

    class InheritedTestCase(TestEnvironmentTestCase):
        env = TestEnvironment(__file__)
        ...
    """
    env: TestEnvironment = None

    @classmethod
    def setUpClass(cls) -> None:
        if cls.env:
            cls.env.make_testing_directory(cls.env.tempdir, clear=True)

    def tearDown(self) -> None:
        if self.env.fail_on_error:
            msg = str(self.env)
            if msg:
                self.env.clear_log()
                self.fail(msg)

    @classmethod
    def tearDownClass(cls) -> None:
        msg = str(cls.env)
        cls.env.clear_log()
        if msg and cls.env.report_errors:
            print(msg, file=sys.stderr)

    @contextlib.contextmanager
    def redirect_logstream(self):
        logstream = StringIO()
        logging.basicConfig()
        logger = logging.getLogger(self.__class__.__name__)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(logging.StreamHandler(logstream))
        logger.setLevel(logging.INFO)
        try:
            yield logger
        finally:
            logger.result = logstream.getvalue()
