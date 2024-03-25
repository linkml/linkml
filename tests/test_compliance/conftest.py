import logging
import pdb

from tests.test_compliance.helper import report, copy_report


def pytest_sessionfinish(session, exitstatus) -> None:
    logging.info(f"finishing session: {session} {exitstatus}")
    report()
    if exitstatus == 0:
        copy_report()
