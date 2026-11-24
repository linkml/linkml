"""SchemaView method caches must not keep views alive.

https://github.com/linkml/linkml/issues/3735

The SchemaView methods were cached with ``functools.lru_cache``, whose cache is shared by
all instances and holds ``self`` in every key: each view a cached method was called on
stayed in memory for the rest of the process. Each view now has its own caches, freed with
it. These tests check that views are freed, and that the caching behaviour is unchanged
(results reused, dropped by ``set_modified()``, ``cache_clear()`` available, copies
independent).
"""

import gc
import weakref
from copy import copy, deepcopy

import pytest

from linkml_runtime.linkml_model.meta import ClassDefinition
from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.utils.schemaview import SchemaView


def make_view() -> SchemaView:
    """Return a view of a small schema: a Person class with id and name slots."""
    builder = SchemaBuilder(id="https://example.org/issue_3735", name="issue_3735")
    builder.add_class("Person", slots=["id", "name"])
    builder.add_defaults()
    return SchemaView(builder.schema)


@pytest.mark.parametrize(
    ("method_name", "arguments"),
    [
        ("class_induced_slots", ("Person",)),  # the call from the issue report
        ("induced_slot", ("name", "Person")),
        ("all_classes", ()),
        ("namespaces", ()),
        ("get_elements_applicable_by_prefix", ("ex",)),  # bounded cache (CACHE_SIZE)
        ("all_class", ()),  # deprecated method: @deprecated wraps the cached method
    ],
)
def test_view_is_freed_after_cached_call(method_name: str, arguments: tuple) -> None:
    """A view a cached method was called on is garbage collected once it is no longer used."""
    view = make_view()
    getattr(view, method_name)(*arguments)
    view_reference = weakref.ref(view)
    del view
    gc.collect()
    assert view_reference() is None


def test_many_views_are_freed() -> None:
    """The loop from the issue report: no view is left once the loop is done."""
    view_references = []
    for _ in range(20):
        view = make_view()
        view.class_induced_slots("Person")
        view_references.append(weakref.ref(view))
    del view
    gc.collect()
    assert [reference() for reference in view_references] == [None] * 20


def test_results_are_cached_per_view() -> None:
    """A second call returns the cached object; another view has its own result."""
    view = make_view()
    other_view = make_view()
    assert view.all_classes() is view.all_classes()
    assert view.induced_slot("name", "Person") is view.induced_slot("name", "Person")
    assert view.all_classes() is not other_view.all_classes()


def test_set_modified_drops_cached_results() -> None:
    """A change made through the view (which calls set_modified) shows in later calls."""
    view = make_view()
    assert "Organization" not in view.all_classes()
    view.add_class(ClassDefinition("Organization"))
    assert "Organization" in view.all_classes()


def test_cache_clear_on_view_and_on_class() -> None:
    """cache_clear() still works on a view's method and, for every view, on the class."""
    view = make_view()
    first_result = view.all_classes()
    view.all_classes.cache_clear()
    second_result = view.all_classes()
    assert second_result is not first_result
    SchemaView.all_classes.cache_clear()
    assert view.all_classes() is not second_result


def test_call_through_the_class() -> None:
    """SchemaView.method(view, ...) works as it did with lru_cache."""
    view = make_view()
    assert SchemaView.all_classes(view) is view.all_classes()


def test_deepcopy_has_its_own_caches() -> None:
    """A deep copy answers about itself, not from the caches of the view it was copied from."""
    view = make_view()
    assert "Organization" not in view.all_classes()
    view_copy = deepcopy(view)
    view_copy.add_class(ClassDefinition("Organization"))
    assert "Organization" in view_copy.all_classes()
    assert "Organization" not in view.all_classes()


def test_copy_has_its_own_caches() -> None:
    """A shallow copy shares the schema but not the caches of the view it was copied from."""
    view = make_view()
    cached_result = view.all_classes()
    view_copy = copy(view)
    assert view_copy.all_classes() is not cached_result  # computed again, for the copy
    view_copy.set_modified()
    assert view.all_classes() is cached_result  # the original's cache is untouched


def test_subclass_override_is_kept() -> None:
    """A subclass overriding a cached method is still called after the cache is created."""

    class CountingView(SchemaView):
        """SchemaView counting the calls to all_classes."""

        calls = 0

        def all_classes(self, *args, **kwargs):  # noqa: ANN002, ANN003, ANN201
            CountingView.calls += 1
            return super().all_classes(*args, **kwargs)

    view = CountingView(make_view().schema)
    first_result = view.all_classes()
    assert view.all_classes() is first_result  # cached by the parent method
    assert CountingView.calls == 2  # but the override ran both times
