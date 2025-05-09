import logging

import tests
from tests.test_compliance.helper import report

logger = logging.getLogger(__name__)


def pytest_sessionfinish(session, exitstatus) -> None:
    logger.info(f"finishing session: {session} {exitstatus} {tests.WITH_OUTPUT}")
    if exitstatus == 0 and tests.WITH_OUTPUT:
        report()
