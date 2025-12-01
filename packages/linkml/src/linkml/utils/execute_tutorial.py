"""
This module executes and evaluates code blocks in tutorial markdown files.
Command line usage example: `python -m linkml.utils.execute_tutorial -d /tmp/tutorial/ docs/intro/tutorial01.md`

It requires that the code blocks have the following format:
- A code block containing file contents that should be written to a file for testing should be preceded by a line
whose text is the file name (no spaces) and a colon.
- A code block containing expected output should be preceded by a line whose text is a single word containing the
text "output" (case insensitive) and a colon.
- A code block containing a command that is expected to fail should be preceded by a line that starts with
"<!-- fail" (case insensitive).
- A code block containing commands that should not be executed should be preceded by a line that starts with
"<!-- no_execute" (case insensitive).
- The code block starts with a line containing three backticks. It can then contain either the language name
(e.g., `bash`, `python`, etc.) or `{literalinclude}` followed by a file path. If using `{literalinclude}`,
the next line should contain the language tag (e.g., `:language: python`).
- The code block ends with a line containing three backticks.
"""

import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePath

import click

from linkml._version import __version__

logger = logging.getLogger(__name__)

re_decl = re.compile(r"^(\S+):$")
re_start_code_block = re.compile(r"^```(\w+)$")  # does not include literalinclude blocks
re_literalinclude = re.compile(r"^```\{literalinclude\} (.+)$")
re_end_code_block = re.compile(r"^```$")
re_html_comment = re.compile(r"^<!-- (.+) -->")


@dataclass
class Block:
    category: str = None  # yaml, bash, python, ...
    title: str = None
    content: str = None
    output: str = None
    error: str = None
    expected_fail: bool = None
    prior_lines: list[str] = None
    annotations: list[str] = None

    def is_file_block(self) -> bool:
        return self.title and "." in self.title

    def is_stdout(self) -> bool:
        return self.title and "output" in self.title.lower()

    def is_bash(self) -> bool:
        return self.category == "bash"


def execute_blocks(directory: str, blocks: list[Block]) -> list[str]:
    """
    Execute the code blocks embedded in a tutorial

    :param directory:
    :param blocks:
    :return: errors
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    logger.info(f"Executing in: {directory}")
    last_block = None
    errs = []

    def err(e):
        errs.append(e)
        logger.error(e)

    for block in blocks:
        write_lines(block.prior_lines)
        logger.info(f"# Block: {block.category} {block.title}")
        if block.is_file_block() and not block.is_bash():
            path = PurePath(directory, block.title)
            logger.info(f"Writing to: {path}")
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
                    raise Exception(f"Maximum 1 token after > in {block.content}. Got: {outpath}")
                outpath = str(Path(directory, *outpath))
                logger.info(f"OUTPATH = {outpath}")
            else:
                outpath = None
            logger.info(f"Executing: {cmd}")
            r = subprocess.run(cmd, cwd=directory, capture_output=True)
            block.output = r.stdout.decode("utf-8")
            if outpath:
                with open(outpath, "w", encoding="UTF-8") as stream:
                    logger.info(f"WRITING {len(block.output)} CHARS TO = {outpath}")
                    stream.write(block.output)
            block.error = r.stderr.decode("utf-8")
            logger.info(f"OUT [sample] = {block.output[0:30]}")
            if block.expected_fail:
                if r.returncode == 0:
                    err(f"Command unexpectedly succeeded: {cmd}")
                else:
                    logger.info("Failed as expected")
                if block.error:
                    logger.info(f"ERR [sample] = ...{block.error[-200:]}")
            else:
                if block.error:
                    logger.info(f"ERR = {block.error}")
                if r.returncode != 0:
                    err(f"Command failed: {cmd}")
                else:
                    logger.info("Success!")
        elif block.is_stdout():
            if "compare_rdf" in block.annotations:
                logger.warning("SKIPPING RDF COMPARISON. TODO: https://github.com/linkml/linkml/issues/427")
            elif last_block.output:
                if last_block.output.strip() != block.content.strip():
                    err(f"Mismatch: {str(last_block.output)} != {block.content}")
                else:
                    logger.info("Hurray! Contents match!")
            else:
                logger.info("No comparison performed")
        else:
            logger.warning(f"Ignoring block: {block}")
        last_block = block
    return errs


def write_lines(lines: list[str]) -> None:
    for line in lines:
        print(f"+++ {line}")


def parse_file_to_blocks(input) -> list[Block]:
    """
    Parses a markdown tutorial file to code blocks to be executed

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
                print(f"TITLE={fn}")
            else:
                m = re_start_code_block.match(line)
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
                    m = re_literalinclude.match(line)
                    if m and fn:
                        # Handle literalinclude directive
                        file_path = m.group(1).strip()
                        # Look ahead and extract language from the language tag
                        language = "yaml"  # Default to yaml if no language tag is found
                        if lines and lines[0].strip().startswith(":language:"):
                            language_line = lines[0].strip()
                            language = language_line.split(":language:")[1].strip()
                            lines = lines[1:]
                        # Skip end of code block
                        if lines and lines[0].strip() == "```":
                            lines = lines[1:]
                        else:
                            logger.warning(
                                f"Expected end of code block after literalinclude, but found: {lines[0].strip()}"
                            )

                        # Convert relative path to absolute path
                        input_dir = Path(input).parent
                        abs_path = input_dir / file_path

                        try:
                            with open(abs_path) as f:
                                file_content = f.read()

                            # Create a block for this file
                            file_block = Block(
                                category=language,  # Use the extracted language
                                title=fn,
                                expected_fail=expected_fail,
                                content=file_content,
                                annotations=anns,
                                prior_lines=prior_lines,
                            )
                            blocks.append(file_block)
                            prior_lines = []
                            anns = []
                        except Exception as e:
                            logger.error(f"Failed to read included file {abs_path}: {e}")
                    else:
                        prior_lines += [line]
        else:
            # in block
            fn = None
            expected_fail = False
            m = re_end_code_block.match(line)
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
    Execute a tutorial markdown file (eg. those in the /docs/intro/ directory) and
    save the outputs in the given directory

    Example:

        export PYTHONPATH=`pwd`
        python -m linkml.utils.execute_tutorial -d /tmp/tutorial/ docs/intro/tutorial01.md

    """
    logging.basicConfig(level=logging.INFO)
    errs = []
    for input in inputs:
        logger.info(f"INPUT={input}")
        blocks = parse_file_to_blocks(input)
        print(f"## {len(blocks)} Blocks")
        localdir = Path(input).stem
        subdir = PurePath(directory, localdir)
        input_errs = execute_blocks(str(subdir), blocks)
        if len(input_errs) > 0:
            logger.error(f"TUTORIAL {input} FAILURES: {len(input_errs)}")
        errs += input_errs
    logger.info(f"Errors = {len(errs)}")
    if len(errs) > 0:
        logger.error(f"Encountered {len(errs)} Errors")
        for err in errs:
            logger.error(f"Error: {err}")
        sys.exit(1)


if __name__ == "__main__":
    cli(sys.argv[1:])
