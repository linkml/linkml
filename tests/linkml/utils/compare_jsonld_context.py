import json
from pathlib import Path


class CompareJsonldContext:
    @staticmethod
    def compare_with_snapshot(jsonld_context: str, snapshot: Path):
        with open(snapshot) as snapshot:
            actual = json.loads(jsonld_context)
            expected = json.loads(snapshot.read())

            del actual["comments"]["generation_date"]
            del expected["comments"]["generation_date"]

            assert actual == expected
