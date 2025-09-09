import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CompareJsonldContext:
    @staticmethod
    def compare_with_snapshot(jsonld_context: str, snapshot: Path):
        with open(snapshot) as snapshot:
            actual = json.loads(jsonld_context)
            expected = json.loads(snapshot.read())

            del actual["comments"]["generation_date"]
            del expected["comments"]["generation_date"]

            logger.debug("JSON-LD Context comparison against snapshot")
            logger.debug(f"actual: {actual}")
            logger.debug(f"snapshot: {expected}")
            assert actual == expected
