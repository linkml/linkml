def assert_file_contains(filename, text, after=None) -> None:
    """
    Check that a file contains a specific bit of text in a line, and raise an assertion failure if it does not.

    :param filename: the name of the file to be checked
    :param text: the motif that must be present in the file
    :param after: if present, the text to search for must appear after a line containing this
    """
    found = False
    is_after = False
    with open(filename) as stream:
        for line in stream.readlines():
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
            if after is not None and after in line:
                is_after = True
    assert found
