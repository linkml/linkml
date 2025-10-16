import pytest

from linkml.generators.panderagen.dependency_sorter import DependencySorter


def assert_sorted_order(sorted_list: list[str], dependency_dict: dict[str, list[str]]):
    """
    Assert that each dependency appears before its dependent in the sorted list.

    Args:
        sorted_list: The sorted list of nodes.
        dependency_dict: The dictionary mapping nodes to their dependencies.
    """
    for node, dependencies in dependency_dict.items():
        for dep in dependencies:
            if sorted_list.index(dep) > sorted_list.index(node):
                pytest.fail(f"Dependency '{dep}' should appear before its dependent '{node}'")


def test_sort_dependencies():
    ds = DependencySorter({"A": ["B", "C"], "B": [], "C": ["D"], "D": ["E"], "E": []})
    result = ds.sort_dependencies()
    # assert result == ['B', 'C', 'D', 'E', 'A']
    assert_sorted_order(result, ds.dependency_dict)


def test_cyclic_dependency():
    ds = DependencySorter({"A": ["B"], "B": ["A"]})
    with pytest.raises(ValueError) as cm:
        ds.sort_dependencies()
    assert "Cyclic dependency detected" in str(cm.value)


def test_add_dependency():
    ds = DependencySorter()
    ds.add_dependency("A", "B")
    ds.add_dependency("B", "C")
    result = ds.sort_dependencies()
    # assert result == ['C', 'B', 'A']
    assert_sorted_order(result, ds.dependency_dict)
