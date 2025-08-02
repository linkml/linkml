import json
from pathlib import Path


class CompareJsonldContext:
    @staticmethod
    def compare_with_snapshot(jsonld_context: str, snapshot: Path):
        with open(snapshot) as snapshot:
            actual = json.loads(jsonld_context)
            expected = json.loads(snapshot.read())

            if "comments" in actual:
                del actual["comments"]["generation_date"]
            if "comments" in expected:
                del expected["comments"]["generation_date"]

            assert actual == expected
