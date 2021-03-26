import os
import re
import sys

import click


def compare_files(file: str, target: str, comments: str = r'^\s+#.*\n') -> int:
    def filtr(txt: str) -> str:
        return re.sub(comments, '', txt, flags=re.MULTILINE).strip()
    if os.path.exists(target):
        with open(target) as oldfile:
            oldtext = filtr(oldfile.read())
    else:
        oldtext = ""

    with open(file) as newfile:
        newtext = filtr(newfile.read())
    return int(oldtext == newtext)


@click.command()
@click.argument("file1", type=click.Path(exists=True, dir_okay=False))
@click.argument("file2", type=click.Path(dir_okay=False))
@click.option("-c", "--comments", help="Comments regexp", default="^#.*$", show_default=True)
def cli(file1, file2, comments) -> None:
    """ Compare file1 to file2 using a filter """
    sys.exit(compare_files(file1, file2, comments))


if __name__ == '__main__':
    cli(sys.argv[1:])
