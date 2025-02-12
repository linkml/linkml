import logging

from tests import WITH_OUTPUT
from tests.test_compliance.helper import report

logger = logging.getLogger(__name__)


def pytest_sessionfinish(session, exitstatus) -> None:
    logger.info(f"finishing session: {session} {exitstatus}")
    if exitstatus == 0 and WITH_OUTPUT:
        report()
