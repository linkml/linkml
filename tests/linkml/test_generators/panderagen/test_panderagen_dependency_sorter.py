"""Tests for ``DependencySorter`` — the topological sort used by panderagen.

Covers all common cycle topologies and ensures behavior is locked down so
future regressions are caught immediately. The LinkML metamodel imports
exercise nearly every pattern below in practice (self-references, parent/child
cycles, peer cycles between mutually-recursive classes, leaf nodes reachable
from cycles), so each one has explicit unit coverage here in addition to the
end-to-end metamodel test in ``test_import_compliance.py``.
"""

import pytest

from linkml.generators.panderagen.dependency_sorter import DependencySorter


def assert_sorted_order(sorted_list: list[str], dependency_dict: dict[str, list[str]]):
    """Assert each non-self dependency appears before its dependent in the sorted list.

    Self-references are skipped — a node can never come "before itself" and the
    sorter is documented to silently ignore them.
    """
    for node, dependencies in dependency_dict.items():
        for dep in dependencies:
            if dep == node:
                continue
            if sorted_list.index(dep) > sorted_list.index(node):
                pytest.fail(f"Dependency '{dep}' should appear before its dependent '{node}'")


def _all_nodes(deps: dict[str, list[str]]) -> set[str]:
    """Return every node mentioned anywhere in the graph (keys and values)."""
    return set(deps) | {d for ds in deps.values() for d in ds}


# ---------------------------------------------------------------------------
# Acyclic baseline
# ---------------------------------------------------------------------------


def test_sort_dependencies_simple_dag():
    ds = DependencySorter({"A": ["B", "C"], "B": [], "C": ["D"], "D": ["E"], "E": []})
    result = ds.sort_dependencies()
    assert_sorted_order(result, ds.dependency_dict)


def test_add_dependency_builds_graph():
    ds = DependencySorter()
    ds.add_dependency("A", "B")
    ds.add_dependency("B", "C")
    result = ds.sort_dependencies()
    assert_sorted_order(result, ds.dependency_dict)


# ---------------------------------------------------------------------------
# Self-references: silently skipped regardless of allow_cycles
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("allow_cycles", [False, True])
def test_pure_self_reference_does_not_raise(allow_cycles):
    """A node referencing only itself is harmless: no ordering constraint at all.

    LinkML example: ``extension`` whose only association is to ``extension``
    (nested extensions inside an extension).
    """
    ds = DependencySorter({"A": ["A"]}, allow_cycles=allow_cycles)
    assert ds.sort_dependencies() == ["A"]


@pytest.mark.parametrize("allow_cycles", [False, True])
def test_self_reference_alongside_real_dep(allow_cycles):
    """Self-loops don't disturb the ordering of legitimate dependencies."""
    ds = DependencySorter({"A": ["A", "B"], "B": []}, allow_cycles=allow_cycles)
    result = ds.sort_dependencies()
    assert set(result) == {"A", "B"}
    assert result.index("B") < result.index("A")


# ---------------------------------------------------------------------------
# Default (raise) behaviour across cycle topologies
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "deps",
    [
        # 2-node cycle (the classic mutual recursion)
        {"A": ["B"], "B": ["A"]},
        # 3-node cycle
        {"A": ["B"], "B": ["C"], "C": ["A"]},
        # 4-node cycle (longer chain returning to start)
        {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]},
        # Two independent cycles in the same graph
        {"A": ["B"], "B": ["A"], "X": ["Y"], "Y": ["X"]},
        # Cycle reachable from an outside node
        {"Top": ["A"], "A": ["B"], "B": ["A"]},
        # Node with self-loop AND participation in a multi-node cycle
        {"A": ["A", "B"], "B": ["A"]},
    ],
    ids=[
        "2-node-cycle",
        "3-node-cycle",
        "4-node-cycle",
        "two-parallel-cycles",
        "cycle-with-incoming-edge",
        "self-loop-plus-multi-node-cycle",
    ],
)
def test_default_raises_on_multi_node_cycles(deps):
    """With ``allow_cycles=False`` (the default), any cycle between distinct
    nodes must raise. This locks down the existing contract so existing callers
    of the sorter aren't silently changed."""
    ds = DependencySorter(deps)
    with pytest.raises(ValueError, match="Cyclic dependency detected"):
        ds.sort_dependencies()


# ---------------------------------------------------------------------------
# allow_cycles=True: produces a best-effort ordering for every cycle topology
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "deps",
    [
        # Same topologies as the "raises" set above
        {"A": ["B"], "B": ["A"]},
        {"A": ["B"], "B": ["C"], "C": ["A"]},
        {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]},
        {"A": ["B"], "B": ["A"], "X": ["Y"], "Y": ["X"]},
        {"Top": ["A"], "A": ["B"], "B": ["A"]},
        {"A": ["A", "B"], "B": ["A"]},
        # Plus: longer chain into a cycle, and a cycle with a leaf dependency
        {"Top": ["Mid"], "Mid": ["A"], "A": ["B"], "B": ["A"]},
        {"A": ["B", "Leaf"], "B": ["A"], "Leaf": []},
    ],
    ids=[
        "2-node-cycle",
        "3-node-cycle",
        "4-node-cycle",
        "two-parallel-cycles",
        "cycle-with-incoming-edge",
        "self-loop-plus-multi-node-cycle",
        "chain-into-cycle",
        "cycle-with-leaf-dep",
    ],
)
def test_allow_cycles_yields_full_node_set(deps):
    """``allow_cycles=True`` must always return every node exactly once,
    regardless of cycle shape — no crashes, no duplicates, no drops."""
    ds = DependencySorter(deps, allow_cycles=True)
    result = ds.sort_dependencies()
    assert set(result) == _all_nodes(deps)
    assert len(result) == len(set(result)), "no duplicates in output"


# ---------------------------------------------------------------------------
# allow_cycles=True: topological order STILL preserved for non-cyclic edges
# ---------------------------------------------------------------------------


def test_allow_cycles_preserves_topological_order_outside_cycles():
    """Acyclic edges outside the cycle must still be honoured. Only the
    edge that *closes* a cycle gets broken; everything else stays ordered."""
    deps = {
        "Top": ["Mid"],
        "Mid": ["Bottom"],
        "Bottom": [],
        "CycleA": ["CycleB"],
        "CycleB": ["CycleA"],
    }
    ds = DependencySorter(deps, allow_cycles=True)
    result = ds.sort_dependencies()
    assert result.index("Bottom") < result.index("Mid") < result.index("Top")


def test_allow_cycles_leaf_dep_of_cyclic_node_comes_before():
    """A node depended on by a cyclic node — but not itself in the cycle —
    must still come before the cyclic node in the output."""
    deps = {"A": ["B", "Leaf"], "B": ["A"], "Leaf": []}
    ds = DependencySorter(deps, allow_cycles=True)
    result = ds.sort_dependencies()
    assert result.index("Leaf") < result.index("A")


def test_allow_cycles_chain_into_cycle_orders_outside_part():
    """A chain that leads into a cycle: the chain nodes must precede the
    cyclic ones in the output (the chain is acyclic; only the inner cycle
    is broken)."""
    deps = {"X": ["A"], "A": ["B"], "B": ["A"]}
    ds = DependencySorter(deps, allow_cycles=True)
    result = ds.sort_dependencies()
    # A and B are cyclic; X depends on A so A should appear before X.
    assert result.index("A") < result.index("X")
    assert result.index("B") < result.index("X")


# ---------------------------------------------------------------------------
# allow_cycles=True is a no-op when no cycles present
# ---------------------------------------------------------------------------


def test_allow_cycles_no_op_on_acyclic_graph():
    """With no cycles present, allow_cycles=True must produce an identical
    result to the default sorter."""
    deps = {"A": ["B", "C"], "B": [], "C": ["D"], "D": ["E"], "E": []}
    a = DependencySorter(dict(deps)).sort_dependencies()
    b = DependencySorter(dict(deps), allow_cycles=True).sort_dependencies()
    assert a == b


def test_allow_cycles_empty_graph():
    ds = DependencySorter({}, allow_cycles=True)
    assert ds.sort_dependencies() == []


def test_default_empty_graph():
    ds = DependencySorter({})
    assert ds.sort_dependencies() == []


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_sort_is_deterministic_with_cycles():
    """Repeated sort calls on the same input must produce the same output
    even when cycles are present — important so generator output is stable."""
    deps = {
        "A": ["B"],
        "B": ["C"],
        "C": ["A"],
        "Leaf1": [],
        "Leaf2": [],
        "Top": ["A", "Leaf1", "Leaf2"],
    }
    a = DependencySorter(dict(deps), allow_cycles=True).sort_dependencies()
    b = DependencySorter(dict(deps), allow_cycles=True).sort_dependencies()
    assert a == b


# ---------------------------------------------------------------------------
# Backwards-compatibility: the documented exception is preserved
# ---------------------------------------------------------------------------


def test_cycle_error_message_lists_cycle_path():
    """The error message must include the cycle path so authors can debug."""
    ds = DependencySorter({"A": ["B"], "B": ["C"], "C": ["A"]})
    with pytest.raises(ValueError) as excinfo:
        ds.sort_dependencies()
    # Every node in the cycle should be mentioned in the path
    msg = str(excinfo.value)
    assert "A" in msg and "B" in msg and "C" in msg
    assert "->" in msg
