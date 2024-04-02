import logging

from tests import WITH_OUTPUT
from tests.test_compliance.helper import report


def pytest_sessionfinish(session, exitstatus) -> None:
    logging.info(f"finishing session: {session} {exitstatus}")
    if exitstatus == 0 and WITH_OUTPUT:
        report()
