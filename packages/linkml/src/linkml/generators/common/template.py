"""
Base classes for jinja template handling classes.

See :mod:`.linkml.generators.pydanticgen.template` for example implementation
"""

from collections.abc import Generator
from copy import copy
from typing import Any, ClassVar, Optional, Union

from jinja2 import Environment
from pydantic import BaseModel, Field, field_validator


class TemplateModel(BaseModel):
    """
    Metaclass to render model results with jinja templates.

    Each subclass needs to declare a :class:`typing.ClassVar` for a
    jinja template within the `templates` directory.

    Templates are written expecting each of the other TemplateModels
    to already be rendered to strings - ie. rather than the ``class.py.jinja``
    template receiving a full :class:`.PydanticAttribute` object or dictionary,
    it receives it having already been rendered to a string. See the :meth:`.render` method.
    """

    template: ClassVar[str]
    _environment: ClassVar[Environment]

    meta_exclude: ClassVar[list[str]] = None

    def render(self, environment: Optional[Environment] = None, **kwargs) -> str:
        """
        Recursively render a template model to a string.

        For each field in the model, recurse through, rendering each :class:`.TemplateModel`
        using the template set in :attr:`.TemplateModel.template` , but preserving the structure
        of lists and dictionaries. Regular :class:`.BaseModel` s are rendered to dictionaries.
        Any other value is passed through unchanged.

        Args:
            environment (:class:`jinja2.Environment`): Template environment - see :meth:`.environment`
        """
        if environment is None:
            environment = type(self).environment()

        fields = {**self.model_fields, **self.model_computed_fields}

        data = {k: _render(getattr(self, k, None), environment) for k in fields}
        template = environment.get_template(self.template)
        rendered = template.render(**data)
        return rendered

    @classmethod
    def environment(cls) -> Environment:
        """
        Default environment for Template models.
        uses a :class:`jinja2.PackageLoader` for the templates directory within this module
        with the ``trim_blocks`` and ``lstrip_blocks`` parameters set to ``True`` so that the
        default templates could be written in a more readable way.
        """
        return copy(cls._environment)

    @classmethod
    def exclude_from_meta(cls: "TemplateModel") -> list[str]:
        """
        Attributes in the source definition to exclude from linkml_meta
        """
        ret = [*cls.model_fields.keys()]
        if cls.meta_exclude is not None:
            ret = ret + cls.meta_exclude
        return ret


class ObjectImport(BaseModel):
    """
    An object to be imported from within a module.

    See :class:`.Import` for examples
    """

    name: str
    alias: Optional[str] = None


class Import(TemplateModel):
    """
    A module or module and classes to be imported.
    """

    module: str
    alias: Optional[str] = None
    objects: Optional[list[ObjectImport]] = None
    is_schema: bool = False
    """
    Whether or not this ``Import`` is importing another schema imported by the main schema --
    ie. that it is not expected to be provided by the environment, but imported locally from within the package.
    Used primarily in split schema generation, see :func:`.pydanticgen.generate_split` for example usage.
    """

    def merge(self, other: "Import") -> list["Import"]:
        """
        Merge one import with another, see :meth:`.Imports` for an example.

        * If module don't match, return both
        * If one or the other are a :class:`.ConditionalImport`, return both
        * If modules match, neither contain objects, but the other has an alias, return the other
        * If modules match, one contains objects but the other doesn't, return both
        * If modules match, both contain objects, merge the object lists, preferring objects with aliases
        """
        # return both if we are orthogonal
        if self.module != other.module:
            return [self, other]

        # handle conditionals
        if isinstance(self, ConditionalImport) and isinstance(other, ConditionalImport):
            # If our condition is the same, return the newer version
            if self.condition == other.condition:
                return [other]
        if isinstance(self, ConditionalImport) or isinstance(other, ConditionalImport):
            # we don't have a good way of combining conditionals, just return both
            return [self, other]

        # handle module vs. object imports
        elif other.objects is None and self.objects is None:
            # both are modules, return the other only if it updates the alias
            if other.alias:
                return [other]
            else:
                return [self]
        elif other.objects is not None and self.objects is not None:
            # both are object imports, merge and return
            alias = self.alias if other.alias is None else other.alias
            # FIXME: super awkward implementation
            # keep ours if it has an alias and the other doesn't,
            # otherwise take the other's version
            self_objs = {obj.name: obj for obj in self.objects}
            other_objs = {
                obj.name: obj for obj in other.objects if obj.name not in self_objs or self_objs[obj.name].alias is None
            }
            self_objs.update(other_objs)

            return [
                type(self)(
                    module=self.module,
                    alias=alias,
                    objects=list(self_objs.values()),
                    is_schema=self.is_schema or other.is_schema,
                    **{
                        k: getattr(other, k)
                        for k in other.model_fields
                        if k not in ("module", "alias", "objects", "is_schema")
                    },
                )
            ]
        else:
            # one is a module, the other imports objects, keep both
            return [self, other]

    def sort(self) -> None:
        """
        Sort imported objects

        * First by whether the first letter is capitalized or not,
        * Then alphabetically (by object name rather than alias)
        """
        if self.objects:
            self.objects = sorted(self.objects, key=lambda obj: (obj.name[0].islower(), obj.name))


class ConditionalImport(Import):
    """
    Import that depends on some condition in the environment, common when
    using backported features or straddling dependency versions.

    Make sure that everything that is needed to evaluate the condition is imported
    before this is added to the injected imports!
    """

    condition: str
    alternative: Import

    def sort(self) -> None:
        """
        :meth:`.Import.sort` called for self and :attr:`.alternative`
        """
        super().sort()
        self.alternative.sort()


class Imports(TemplateModel):
    """
    Container class for imports that can handle merging!

    See :class:`.Import` and :class:`.ConditionalImport` for examples of declaring individual imports

    Useful for generation, because each build stage will potentially generate
    overlapping imports. This ensures that we can keep a collection of imports
    without having many duplicates.

    Defines methods for adding, iterating, and indexing from within the :attr:`Imports.imports` list.
    """

    imports: list[Union[Import, ConditionalImport]] = Field(default_factory=list)
    render_sorted: bool = True
    """When rendering, render in sorted groups"""

    @classmethod
    def _merge(
        cls, imports: list[Union[Import, ConditionalImport]], other: Union[Import, "Imports", list[Import]]
    ) -> list[Union[Import, ConditionalImport]]:
        """
        Add a new import to an existing imports list, handling deduplication and flattening.

        Mutates and returns ``imports``

        Generally will prefer the imports in ``other`` , updating those in ``imports``.
        If ``other`` ...
        - doesn't match any ``module`` in ``imports``, add it!
        - matches a single ``module`` in imports, :meth:`.Import.merge` the object imports
        - matches multiple ``module``s in imports, then there must have been another
            :class:`.ConditionalImport` already present, so we :meth:`.Import.merge` the existing
            :class:`.Import` if it is one, and if it's a :class:`.ConditionalImport` just YOLO
            and append it since there isn't a principled way to merge them from strings.
        - is :class:`.Imports`  or a list of :class:`.Import` s, call this recursively for each
          item.

        Since imports can be merged in an undefined order depending on the generator configuration,
        default behavior for imports with matching ``module`` is to remove them and append to the
        end of the imports list (rather than keeping it in the position of the existing
        :class:`.Import` ). :class:`.ConditionalImports` make it possible to have namespace
        conflicts, so in imperative import style we assume the most recently added :class:`.Import`
        is the one that should prevail.
        """
        #
        if isinstance(other, cls) or (isinstance(other, list) and all([isinstance(i, Import) for i in other])):
            for i in other:
                imports = cls._merge(imports, i)
            return imports

        existing = [i for i in imports if i.module == other.module]

        # if we have nothing importing from this module yet, add it!
        if len(existing) == 0:
            imports.append(other)
        elif len(existing) == 1:
            imports.remove(existing[0])
            imports.extend(existing[0].merge(other))
        else:
            # we have both a conditional and at least one nonconditional already.
            # If this is another conditional, we just add it, otherwise, we merge it
            # with the single nonconditional
            if isinstance(other, ConditionalImport):
                imports.append(other)
            else:
                for e in existing:
                    if isinstance(e, Import):
                        imports.remove(e)
                        merged = e.merge(other)
                        imports.extend(merged)
                        break

        # SPECIAL CASE - __future__ annotations must happen at the top of a file
        # sort here outside of sort method because our imports are invalid without it,
        # where calling ``sort`` should be optional.
        imports = sorted(imports, key=lambda i: i.module == "__future__", reverse=True)
        return imports

    def __add__(self, other: Union[Import, "Imports", list[Import]]) -> "Imports":
        imports = self.imports.copy()
        imports = self._merge(imports, other)
        return type(self).model_construct(
            imports=imports, **{k: getattr(self, k, None) for k in self.model_fields if k != "imports"}
        )

    def __len__(self) -> int:
        return len(self.imports)

    def __iter__(self) -> Generator[Import, None, None]:
        yield from self.imports

    def __getitem__(self, item: Union[int, str]) -> Import:
        if isinstance(item, int):
            return self.imports[item]
        elif isinstance(item, str):
            # the name of the module
            an_import = [i for i in self.imports if i.module == item]
            if len(an_import) == 0:
                raise KeyError(f"No import with module {item} was found.\nWe have: {self.imports}")
            return an_import[0]
        else:
            raise TypeError(f"Can only index with an int or a string as the name of the module,\nGot: {type(item)}")

    def __contains__(self, item: Union[Import, "Imports", list[Import]]) -> bool:
        """
        Check if all the objects are imported from the given module(s)

        If the import is a bare module import (ie its :attr:`~.Import.objects` is ``None`` )
        then we must also have a bare module import in this Imports (because even if
        we import from the module, unless we import it specifically its name won't be
        available in the namespace.

        :attr:`.Import.alias` must always match for the same reason.
        """
        if isinstance(item, Imports):
            return all([i in self for i in item.imports])
        elif isinstance(item, list):
            return all([i in self for i in item])
        elif isinstance(item, Import):
            try:
                an_import = self[item.module]
            except KeyError:
                return False
            if item.objects is None:
                return an_import == item
            else:
                return all([obj in an_import.objects for obj in item.objects])
        else:
            raise TypeError(f"Imports only contains single Import objects or other Imports\nGot: {type(item)}")

    @field_validator("imports", mode="after")
    @classmethod
    def imports_are_merged(
        cls, imports: list[Union[Import, ConditionalImport]]
    ) -> list[Union[Import, ConditionalImport]]:
        """
        When creating from a list of imports, construct model as if we have done so by iteratively
        constructing with __add__ calls
        """
        merged_imports = []
        for i in imports:
            merged_imports = cls._merge(merged_imports, i)
        return merged_imports

    def sort(self) -> None:
        """
        Sort imports recursively, mimicking isort:

        * First by :attr:`.Import.group` according to :attr:`.Imports.group_order`
        * Then by whether the :class:`.Import` has any objects
          (``import module`` comes before ``from module import name``)
        * Then alphabetically by module name
        """

        def _sort_key(i: Import) -> tuple[int, str]:
            return (int(i.objects is not None), i.module)

        imports = sorted(self.imports, key=_sort_key)
        for i in imports:
            i.sort()
        self.imports = imports

    def render(self, environment: Optional[Environment] = None, black: bool = False) -> str:
        if self.render_sorted:
            self.sort()
        rendered = super().render(environment=environment, black=black)
        return rendered


def _render(
    item: Union[TemplateModel, Any, list[Union[Any, TemplateModel]], dict[str, Union[Any, TemplateModel]]],
    environment: Environment,
) -> Union[str, list[str], dict[str, str]]:
    if isinstance(item, TemplateModel):
        return item.render(environment)
    elif isinstance(item, list):
        return [_render(i, environment) for i in item]
    elif isinstance(item, dict):
        return {k: _render(v, environment) for k, v in item.items()}
    elif isinstance(item, BaseModel):
        fields = {**item.model_fields, **getattr(item, "model_computed_fields", {})}
        return {k: _render(getattr(item, k, None), environment) for k in fields.keys()}
    else:
        return item
