def remove_duplicates(lst):
    """Remove duplicate tuples from a list of tuples."""
    return [t for t in (set(tuple(i) for i in lst))]

def write_to_file(file_path, data, mode="w"):
    """Write string data to a file."""
    with open(file_path, mode) as f:
        f.write(data)
