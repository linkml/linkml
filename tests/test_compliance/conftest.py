import logging

from tests.test_compliance.helper import copy_report, report


def pytest_sessionfinish(session, exitstatus) -> None:
    logging.info(f"finishing session: {session} {exitstatus}")
    report()
    if exitstatus == 0:
        copy_report()
