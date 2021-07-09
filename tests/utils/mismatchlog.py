import os
import sys
from dataclasses import dataclass
from typing import Optional, List

base_dir = os.path.abspath(os.path.join( os.path.dirname(__file__), '..', '..'))


class MismatchLog:
    """
    A collection of log entries about output file mismatches.
    file_or_directory - the relative file or directory that didn't match (e.g. tests/test_scripts/output/echoit/help)
    filename - the python file that caused the error
    line_no - the line number in the python file
    difference_text - the details on the difference.  Used for RDF and other non-ascii files
    """
    class MismatchLogEntry:
        @dataclass
        class StackFrame:
            filename: str
            method: str
            line: int

            def __str__(self):
                return f'File "{self.filename}", line {self.line} in {self.method} '

        def __init__(self, file_or_directory: str, msg: Optional[str]) -> None:
            self.file_or_directory = file_or_directory
            self.msg = msg
            self.call_stack = list()
            frame = sys._getframe(2)
            while True:
                self.call_stack.append(MismatchLog.MismatchLogEntry.StackFrame(frame.f_code.co_filename,
                                                                               frame.f_code.co_name, frame.f_lineno))
                if frame.f_code.co_name.startswith("test_"):
                    break
                frame = frame.f_back

        def __str__(self):
            rval = [f'Output mismatch: File "{os.path.relpath(self.file_or_directory, base_dir)}", line 1']
            rval.append("Stack:  " + '\n\t\t'.join([str(e) for e in self.call_stack]))
            if self.msg:
                rval.append(self.msg.rstrip().capitalize())
            return '\n'.join(rval) + '\n'

    def __init__(self) -> None:
        self.entries: List[MismatchLog.MismatchLogEntry] = list()

    def log(self, file_or_directory: str, message: Optional[str] = None) -> None:
        self.entries.append(MismatchLog.MismatchLogEntry(file_or_directory, message))
