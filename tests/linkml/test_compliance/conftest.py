import logging

import tests.linkml
from tests.linkml.test_compliance.helper import report

logger = logging.getLogger(__name__)


def pytest_sessionfinish(session, exitstatus) -> None:
    logger.info(f"finishing session: {session} {exitstatus} {tests.linkml.WITH_OUTPUT}")
    if exitstatus == 0 and tests.linkml.WITH_OUTPUT:
        report()
