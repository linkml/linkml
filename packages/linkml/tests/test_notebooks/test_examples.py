import importlib
import logging
import os
import re
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

from tests.test_notebooks import output_directory

logger = logging.getLogger(__name__)


def eval_test(target: str, import_module: str) -> None:
    output = StringIO()
    output_file = Path(os.path.join(output_directory, target))
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with redirect_stdout(output):
        importlib.import_module(import_module)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            re.sub(
                r'Generation date: .*?(["\n])',
                r"Generation date:\1",
                output.getvalue(),
            )
        )
    logger.info(f"Output written to {output_file}")


@pytest.mark.parametrize(
    "test_name, import_module",
    [
        ("examples.txt", "tests.test_notebooks.input.examples"),
        ("inheritance.txt", "tests.test_notebooks.input.inheritance"),
    ],
)
def test_examples(test_name: str, import_module: str) -> None:
    eval_test(test_name, import_module)


@pytest.mark.network
def test_distributed_models() -> None:
    eval_test("distributedmodels.txt", "tests.test_notebooks.input.distributedmodels")
