import os
import shlex
import unittest
from typing import Union, List, Optional, Callable
from warnings import warn

from tests.support.dirutils import make_and_clear_directory
from tests.support.compare_rdf import compare_rdf
from tests.support.test_environment import TestEnvironmentTestCase, TestEnvironment


class ClickTestCase(TestEnvironmentTestCase):
    """ Common tools for testing command line functions """
    env: TestEnvironment = None

    # The variables below must be set by the inheriting class
    testdir: str = None     # subdirectory within outdir
    click_ep = None         # entry point for particular function
    prog_name: str = None   # executable name

    test_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
    temp_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp'))

    def source_file_path(self, *path: str) -> str:
        """ Return the full file name of path in the input directory """
        return self.env.input_path(*path)

    def expected_file_path(self, *path: str) -> str:
        """ Return the fill file path of the script subdirectory in the output directory """
        return self.env.expected_path(self.testdir, *path)

    def temp_file_path(self, *path: str, is_dir: bool = False) -> str:
        """ Create subdirectory in the temp directory to hold path """
        full_path = self.env.temp_file_path(self.testdir, *path)
        self.env.make_testing_directory(full_path if is_dir else os.path.dirname(full_path))
        return full_path

    @staticmethod
    def jsonld_comparator(expected_data: str, actual_data: str) -> str:
        """ Compare expected data in json-ld format to actual data in json-ld format """
        return compare_rdf(expected_data, actual_data, "json-ld")

    @staticmethod
    def n3_comparator(expected_data: str, actual_data: str) -> str:
        """ compare expected_data in n3 format to actual_data in n3 format """
        return compare_rdf(expected_data, actual_data, "n3")

    @staticmethod
    def rdf_comparator(expected_data: str, actual_data: str, fmt: Optional[str] = 'turtle') -> str:
        """ compare expected_data to actual_data using basic RDF comparator method """
        return compare_rdf(expected_data, actual_data, fmt=fmt)

    @staticmethod
    def always_pass_comparator(expected_data: str, new_data: str) -> Optional[str]:
        """
        No-op comparator -- everyone passes!

        :param expected_data:
        :param new_data:
        :return:
        """
        return None

    @staticmethod
    def closein_comparison(expected_txt: str, actual_txt: str) -> None:
        """ Assist with testing comparison -- zero in on the first difference in a big string

        @param expected_txt:
        @param actual_txt:
        """
        window = 30
        view = 120

        nw = nt = actual_txt.strip()
        ow = ot = expected_txt.strip()
        if ot != nt:
            offset = 0
            while nt and ot and nt[:window] == ot[:window]:
                offset += window
                nt = nt[window:]
                ot = ot[window:]
            offset = max(offset-view, 0)
            print("   - - EXPECTED - -")
            print(ow[offset:offset+view+view])
            print("\n   - - ACTUAL - -")
            print(nw[offset:offset+view+view])

    def do_test(self,
                args: Union[str, List[str]],
                testFileOrDirectory: Optional[str] = None,
                *,
                expected_error: type(Exception) = None,
                filtr: Optional[Callable[[str], str]] = None,
                is_directory: bool = False,
                add_yaml: bool = True,
                comparator: Callable[[type(unittest.TestCase), str, str, str], str] = None, ) -> None:
        """ Execute a command test

        @param args: Argument string or list to command.  'meta.yaml' is always supplied
        @param testFileOrDirectory: name of file or directory to record output in
        @param expected_error: If present, we expect this error
        @param filtr: Filter to remove date and app specific information from text. Only used for single file generation
        @param is_directory: True means output is to a directory
        @param add_yaml: True means add the default meta.yaml file.  False means both yaml and importmap
        are pre-supplied
        @param comparator: If present, use this method for comparison
        """
        assert testFileOrDirectory
        arg_list = shlex.split(args) if isinstance(args, str) else args

        if is_directory and (filtr or comparator):
            warn("filtr and comparator parameters aren't implemented for directory generation")

        if add_yaml and (not arg_list or arg_list[0] != '--help'):
            raise NotImplementedError("This is an artifact from elsewhere")
            # arg_list.insert(0, self.env.meta_yaml)
            # arg_list += ["--importmap", self.env.import_map, "--log_level", DEFAULT_LOG_LEVEL_TEXT]

        target = os.path.join(self.testdir, testFileOrDirectory)
        self.temp_file_path(self.testdir, is_dir=True)

        def do_gen():
            if is_directory:
                self.env.generate_directory(target,
                                            lambda target_dir: self.click_ep(arg_list + ["-d", target_dir],
                                                                             prog_name=self.prog_name,
                                                                             standalone_mode=False))
            else:
                self.env.generate_single_file(target,
                                              lambda: self.click_ep(arg_list, prog_name=self.prog_name,
                                                                    standalone_mode=False), filtr=filtr,
                                              comparator=comparator)

        if expected_error:
            with self.assertRaises(expected_error):
                do_gen()
            return
        else:
            do_gen()

    @classmethod
    def temp_directory(cls, base: str) -> str:
        """
        Create a temporary directory and return the path

        :param base:
        :return: directory
        """
        cls.env.make_testing_directory(cls.env.tempdir, clear=True)
        new_directory = os.path.join(cls.temp_base_dir, base)
        make_and_clear_directory(new_directory)
        return new_directory


if __name__ == '__main__':
    unittest.main()
