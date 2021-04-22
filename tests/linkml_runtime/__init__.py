import logging
import configparser
# Global testing control variables
import os

from tests.support.test_environment import MismatchAction

# ---------------------------------------------------------------
#                DO NOT change this file.
# To change the default test harness settings:
#  > cd tests
#  > cp test_config.ini.example test_config.ini
#
#  Make your edits in test_config.ini.  Note that it is in .gitignore and will not be submitted
# ----------------------------------------------------------------

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'test_config.ini'))
if 'test.settings' not in config.sections():
    config['test.settings'] = {}  # initialize a blank setting if file doesn't exist
test_settings = config['test.settings']


# Action on mismatch.  One of 'Ignore', 'Report' or 'Fail'
#  If 'Fail', the expected file will be saved in the appropriate temp directory
#  NOTE: Before setting this back to Report or Ignore, you need to run cleartemp.sh in this directory
DEFAULT_MISMATCH_ACTION = eval(test_settings.get('DEFAULT_MISMATCH_ACTION', 'MismatchAction.Report'))

# Use local import map.  If True, tests/input/local_import_map.json is used to create the test files.  Note that this
#  will result in local path names being recorded in jsonld files.  This should always be set to False before generating
#  the final output
USE_LOCAL_IMPORT_MAP = test_settings.getboolean('USE_LOCAL_IMPORT_MAP', False)


# There are lots of warnings emitted by the generators. Default logging level
DEFAULT_LOG_LEVEL = eval(test_settings.get('DEFAULT_LOG_LEVEL', 'logging.ERROR'))
DEFAULT_LOG_LEVEL_TEXT = test_settings.get('DEFAULT_LOG_LEVEL_TEXT', 'ERROR')


# Skip RDF comparison, as it takes a lot of time
SKIP_RDF_COMPARE = test_settings.getboolean('SKIP_RDF_COMPARE', False)
SKIP_RDF_COMPARE_REASON = test_settings.get('SKIP_RDF_COMPARE_REASON', 'tests/__init__.py RDF output not checked SKIP_RDF_COMPARE is True')

# Exception for use in script testing.  Global to prevent redefinition
class CLIExitException(Exception):
    def __init__(self, code: int) -> None:
        self.code = code
        super().__init__(self)
