import filecmp
import os
from contextlib import redirect_stdout
from io import StringIO
from typing import Optional

from tests.utils.filters import ldcontext_metadata_filter


def make_and_clear_directory(dirbase: str) -> None:
    """ Make dirbase if necessary and then clear generated files """
    import shutil

    safety_file = os.path.join(dirbase, "generated")
    if os.path.exists(dirbase):
        if not os.path.exists(safety_file):
            raise FileNotFoundError("'generated' guard file not found in {}".format(safety_file))
        shutil.rmtree(dirbase)
    os.makedirs(dirbase)
    with open(os.path.join(dirbase, "generated"), "w") as f:
        f.write("Generated for safety.  Directory will not be cleared if this file is not present")


def file_text(txt_or_fname: str) -> str:
    """
    Determine whether text_or_fname is a file name or a string and, if a file name, read it
    :param text_or_fname:
    :return:
    """
    if len(txt_or_fname) > 4 and '\n' not in txt_or_fname:
        with open(txt_or_fname) as ef:
            return ef.read()
    return txt_or_fname


class dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files,
                                 shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp

    filecmp.dircmp.methodmap['same_files'] = phase3
    filecmp.dircmp.methodmap['diff_files'] = phase3
    filecmp.dircmp.methodmap['funny_files'] = phase3


def _do_cmp(f1, f2):
    bufsize = filecmp.BUFSIZE
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if f1.endswith('.context.jsonld'):
                b1 = ldcontext_metadata_filter(b1.decode())
                b2 = ldcontext_metadata_filter(b2.decode())
            if b1 != b2:
                return False
            if not b1:
                return True


filecmp._do_cmp = _do_cmp


def are_dir_trees_equal(dir1: str, dir2: str) -> Optional[str]:
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: None if directories match, else summary of differences
   """
    def has_local_diffs(dc: dircmp) -> bool:
        return dc.diff_files or dc.funny_files or dc.left_only or dc.right_only

    def has_diffs(dc: dircmp) -> bool:
        return has_local_diffs(dc) or any(has_diffs(sd) for sd in dc.subdirs.values())

    dirs_cmp = dircmp(dir1, dir2, ignore=['generated'])
    if has_diffs(dirs_cmp):
        output = StringIO()
        with redirect_stdout(output):
            dirs_cmp.report_full_closure()
        return output.getvalue()
    return None
