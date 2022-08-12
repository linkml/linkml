def remove_duplicates(lst):
    """Remove duplicate tuples from a list of tuples."""
    return [t for t in (set(tuple(i) for i in lst))]


def write_to_file(file_path, data, mode="w", encoding="utf-8"):
    with open(file_path, mode, encoding=encoding) as f:
        f.write(data)
