import re


def remove_duplicates(lst):
    """Remove duplicate tuples from a list of tuples."""
    return [t for t in (set(tuple(i) for i in lst))]


def write_to_file(file_path, data, mode="w", encoding="utf-8"):
    with open(file_path, mode, encoding=encoding) as f:
        f.write(data)


def convert_to_snake_case(str):
    str = re.sub(r"(?<=[a-z])(?=[A-Z])|[^a-zA-Z]", " ", str).strip().replace(" ", "_")
    return "".join(str.lower())
