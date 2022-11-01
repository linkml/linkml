"""
Generate dotfiles
"""
import os
from dataclasses import dataclass
from typing import List, Optional, TextIO, Union

import click
from deprecated.classic import deprecated
from graphviz import FORMATS, Digraph
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import underscore

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

valid_formats = sorted(list(FORMATS))


@deprecated("Replaced by yuml/mermaid")
@dataclass
class DotGenerator(Generator):
    """
    Generates dotfiles

    No longer in use: use mermaid generator instead
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    directory_output = True
    valid_formats = ["png"] + valid_formats
    visit_all_class_slots = True
    uses_schemaloader = True

    # ObjectVars
    classnames: Optional[List[str]] = None
    filename: Optional[str] = None
    dirname: Optional[str] = None
    filedot: Optional[Digraph] = None
    classdot: Optional[Digraph] = None
    cls_subj: Optional[SlotDefinition] = None
    cls_obj: Optional[SlotDefinition] = None
    classname: Optional[List[str]] = None
    directory: Optional[str] = None

    def visit_schema(
        self,
        classname: Optional[List[str]] = None,
        directory: Optional[str] = None,
        filename: Optional[str] = None,
        **_,
    ) -> None:
        self.classnames = [] if classname is None else list(classname)
        for classname in self.classnames:
            if classname not in self.schema.classes:
                raise ValueError(f"Unknown class name: {classname}")
        self.filename = filename
        self.dirname = directory
        if filename:
            self.filedot = Digraph(comment=self.schema.name)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def end_schema(self, **_) -> None:
        if self.filedot:
            self.filedot.render(
                self.filename,
                self.dirname,
                view=False,
                cleanup=True,
                format=self.format,
            )

    def visit_class(self, cls: ClassDefinition) -> bool:
        if self.classnames and cls.name not in self.classnames:
            return False
        if self.dirname:
            self.classdot = Digraph(comment=self.schema.name)
        self.node(cls.name, cls.name)
        if cls.is_a:
            self.edge(cls.name, cls.is_a, label="is_a")
        for mixin in cls.mixins:
            self.edge(cls.name, mixin, label="uses")
        self.cls_subj = self.cls_obj = None
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        if self.cls_subj and self.cls_obj:
            rnode = "relation"
            self.edge(
                self.aliased_slot_name(self.cls_subj),
                self.aliased_slot_name(self.cls_obj),
                label=rnode,
            )
            self.edge(self.aliased_slot_name(self.cls_subj), rnode, style="dotted")
            self.edge(self.aliased_slot_name(self.cls_obj), rnode, style="dotted")
        if self.classdot:
            self.classdot.render(
                underscore(cls.name),
                self.dirname,
                view=False,
                cleanup=True,
                format=self.format,
            )

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ):
        if aliased_slot_name == "subject":
            self.cls_subj = slot
        elif aliased_slot_name == "object":
            self.cls_obj = slot
        color = "blue" if slot.name in cls.slots else "black"
        style = "dashed" if slot.alias in cls.slots else "solid"
        self.edge(
            cls.name,
            aliased_slot_name,
            label=aliased_slot_name,
            color=color,
            style=style,
        )
        srange = slot.range if slot.range else "Thing"
        self.node(slot.name, srange, color=color)

    def node(self, *args, **kwargs) -> None:
        if self.classdot:
            self.classdot.node(*args, **kwargs)
        if self.filedot:
            self.filedot.node(*args, **kwargs)

    def edge(self, *args, **kwargs) -> None:
        if self.classdot:
            self.classdot.edge(*args, **kwargs)
        if self.filedot:
            self.filedot.edge(*args, **kwargs)


@shared_arguments(DotGenerator)
@click.command()
@click.option(
    "--directory",
    "-d",
    help="Output directory - if supplied, a graph per class will be generated",
)
@click.option(
    "--out", "-o", help="Target file -- if supplied, one large graph will be generated"
)
@click.option("--classname", "-c", multiple=True, help="Class(es) to transform")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, out, **args):
    """Generate graphviz representations of the LinkML model"""
    DotGenerator(yamlfile, **args).serialize(filename=out, **args)


if __name__ == "__main__":
    cli()
