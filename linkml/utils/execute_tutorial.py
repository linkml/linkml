import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import List

import click

from linkml._version import __version__

re_decl = re.compile("^(\\S+):$")
re_start_yaml = re.compile("^```(\w+)$")
re_end_yaml = re.compile("^```$")
re_html_comment = re.compile("^<!-- (.+) -->")


@dataclass
class Block:
    category: str = None  ## yaml, bash, python, ...
    title: str = None
    content: str = None
    output: str = None
    error: str = None
    expected_fail: bool = None
    prior_lines: List[str] = None
    annotations: List[str] = None

    def is_file_block(self) -> bool:
        return self.title and "." in self.title

    def is_stdout(self) -> bool:
        return self.title and "output" in self.title.lower()

    def is_bash(self) -> bool:
        return self.category == "bash"


def execute_blocks(directory: str, blocks: List[Block]) -> List[str]:
    """
    Execute the code blocks embedded in a tutorial

    :param directory:
    :param blocks:
    :return: errors
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    logging.info(f"Executing in: {directory}")
    last_block = None
    errs = []

    def err(e):
        errs.append(e)
        logging.error(e)

    for block in blocks:
        write_lines(block.prior_lines)
        logging.info(f"# Block: {block.category} {block.title}")
        if block.is_file_block():
            path = PurePath(directory, block.title)
            with open(path, "w", encoding="UTF-8") as stream:
                stream.write(block.content)
        elif block.is_bash():
            if "no_execute" in block.annotations:
                continue
            cmd = block.content.strip().split()
            if ">" in cmd:
                # redirects not support in subprocess.run
                pos = cmd.index(">")
                outpath = cmd[pos + 1 :]
                cmd = cmd[0:pos]
                if len(outpath) > 1:
                    raise Exception(
                        f"Maximim 1 token after > in {block.content}. Got: {outpath}"
                    )
                outpath = str(Path(directory, *outpath))
                logging.info(f"OUTPATH = {outpath}")
            else:
                outpath = None
            logging.info(f"Executing: {cmd}")
            r = subprocess.run(cmd, cwd=directory, capture_output=True)
            block.output = r.stdout.decode("utf-8")
            if outpath:
                with open(outpath, "w", encoding="UTF-8") as stream:
                    logging.info(f"WRITING {len(block.output)} TO = {outpath}")
                    stream.write(block.output)
            block.error = r.stderr.decode("utf-8")
            logging.info(f"OUT [sample] = {block.output[0:30]}")
            if block.expected_fail:
                if r.returncode == 0:
                    err(f"Command unexpectedly succeeded: {cmd}")
                else:
                    logging.info(f"Failed as expected")
                if block.error:
                    logging.info(f"ERR [sample] = ...{block.error[-200:]}")
            else:
                if block.error:
                    logging.info(f"ERR = {block.error}")
                if r.returncode != 0:
                    err(f"Command failed: {cmd}")
                else:
                    logging.info(f"Success!")
        elif block.is_stdout():
            if "compare_rdf" in block.annotations:
                logging.warning(
                    "SKIPPING RDF COMPARISON. TODO: https://github.com/linkml/linkml/issues/427"
                )
            elif last_block.output:
                if last_block.output.strip() != block.content.strip():
                    err(f"Mismatch: {str(last_block.output)} != {block.content}")
                else:
                    logging.info(f"Hurray! Contents match!")
            else:
                logging.info("No comparison performed")
        else:
            logging.warning(f"Ignoring block: {block}")
        last_block = block
    return errs


def write_lines(lines: List[str]) -> None:
    for line in lines:
        print(f"+++ {line}")


def parse_file_to_blocks(input) -> List[Block]:
    """
    Parses a markdown tutorial file to code blacks to be executed

    :param input:
    :return:
    """
    with open(input) as stream:
        lines = stream.readlines()
    curr_block = None
    blocks = []
    fn = None
    prior_lines = []
    anns = []
    expected_fail = False
    while lines:
        line = lines[0].rstrip()
        lines = lines[1:]

        if curr_block is None:
            if line.lower().startswith("<!-- fail"):
                expected_fail = True
            m = re_html_comment.match(line)
            if m:
                anns.append(m.group(1).strip().lower())
                continue
            m = re_decl.match(line)
            if m:
                fn = m.group(1)
                print(f"FILE={fn}")
            else:
                m = re_start_yaml.match(line)
                if m:
                    curr_block = Block(
                        category=m.group(1),
                        title=fn,
                        expected_fail=expected_fail,
                        content="",
                        annotations=anns,
                        prior_lines=prior_lines,
                    )
                    prior_lines = []
                    anns = []
                else:
                    prior_lines += [line]
        else:
            # in block
            fn = None
            expected_fail = False
            m = re_end_yaml.match(line)
            if m:
                blocks.append(curr_block)
                curr_block = None
            else:
                curr_block.content += f"{line}\n"
    return blocks


@click.command()
@click.option(
    "--directory",
    "-d",
    required=True,
    help="path to directory to execute tutorial example on",
)
@click.argument("inputs", nargs=-1)
@click.version_option(__version__, "-V", "--version")
def cli(inputs, directory):
    """

    Example:

        export PYTHONPATH=`pwd`
        python -m linkml.utils.execute_tutorial -d /tmp/tutorial/ sphinx/intro/tutorial01.md

    """
    logging.basicConfig(level=logging.INFO)
    errs = []
    for input in inputs:
        logging.info(f"INPUT={input}")
        blocks = parse_file_to_blocks(input)
        print(f"## {len(blocks)} Blocks")
        localdir = Path(input).stem
        subdir = PurePath(directory, localdir)
        input_errs = execute_blocks(str(subdir), blocks)
        if len(input_errs) > 0:
            logging.error(f"TUTORIAL {input} FAILURES: {len(input_errs)}")
        errs += input_errs
    logging.info(f"Errors = {len(errs)}")
    if len(errs) > 0:
        logging.error(f"Encountered {len(errs)} Errors")
        for err in errs:
            logging.error(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    cli(sys.argv[1:])
