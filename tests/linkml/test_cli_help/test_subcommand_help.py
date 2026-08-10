"""Every ``linkml`` subcommand should describe itself in its parent's help listing.

Click builds the one-line entry in a group's ``Commands:`` block from the command
callback's docstring, taking everything up to the first period. A command with no
docstring gets a blank entry, and a docstring whose first sentence contains an
internal period (``eg.``, ``i.e.``, ``e.g.``) gets cut mid-phrase.

See https://github.com/linkml/linkml/issues/2635. The same truncate-at-the-first-period
habit bites docgen's ``enshorten`` filter, tracked separately in
https://github.com/linkml/linkml/issues/3732.
"""

import re

import click
import pytest

from linkml.cli.main import linkml as linkml_cli


def _groups() -> list[tuple[str, click.Group]]:
    """Return every ``click.Group`` reachable from the top-level entry point."""
    found: list[tuple[str, click.Group]] = []
    stack: list[tuple[str, click.Command]] = [("linkml", linkml_cli)]
    while stack:
        path, command = stack.pop()
        if isinstance(command, click.Group):
            found.append((path, command))
            for name, sub in command.commands.items():
                stack.append((f"{path} {name}", sub))
    return found


def _subcommands() -> list[tuple[str, click.Command]]:
    """Return ``(invocation path, command)`` for every subcommand of every group."""
    return [(f"{group_path} {name}", sub) for group_path, group in _groups() for name, sub in group.commands.items()]


@pytest.mark.parametrize(
    "path,command",
    _subcommands(),
    ids=[path for path, _ in _subcommands()],
)
def test_subcommand_has_short_help(path: str, command: click.Command) -> None:
    """Each subcommand renders a non-empty one-line description."""
    assert command.get_short_help_str().strip(), (
        f"`{path}` has no short help, so it appears as a blank entry in its group's "
        f"Commands listing. Give its callback a docstring."
    )


@pytest.mark.parametrize(
    "path,command",
    _subcommands(),
    ids=[path for path, _ in _subcommands()],
)
def test_short_help_is_not_cut_at_an_abbreviation(path: str, command: click.Command) -> None:
    """The one-line description does not end inside an abbreviation.

    Click truncates at the first period, so a first sentence containing ``eg.`` or
    ``e.g.`` produces a fragment such as ``Execute a tutorial markdown file (eg.``
    """
    short_help = command.get_short_help_str(limit=200).strip()
    # Take the final token and drop surrounding punctuation, so that a fragment such
    # as "(eg." is compared as "eg".
    trailing_fragment = re.sub(r"[^\w.]", "", short_help.rsplit(" ", 1)[-1]).rstrip(".").lower()
    assert trailing_fragment not in {"eg", "e.g", "i.e", "ie", "cf", "etc", "vs"}, (
        f"`{path}` short help ends at an abbreviation: {short_help!r}. Click cuts at "
        f"the first period, so keep abbreviations out of the opening sentence."
    )
