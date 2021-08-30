def remove_duplicates(lst):
    """Remove duplicate tuples from a list of tuples."""
    return [t for t in (set(tuple(i) for i in lst))]
