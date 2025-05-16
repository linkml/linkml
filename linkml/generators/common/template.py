"""
Base classes for jinja template handling classes.

See :mod:`.linkml.generators.pydanticgen.template` for example implementation
"""

from copy import copy
from typing import Any, ClassVar, Optional, Union

from jinja2 import Environment
from pydantic import BaseModel


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
            environment = TemplateModel.environment()

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
        fields = item.model_fields
        return {k: _render(getattr(item, k, None), environment) for k in fields.keys()}
    else:
        return item
