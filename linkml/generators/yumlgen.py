"""Generate yuml

https://yuml.me/diagram/scruffy/class/samples

"""
import logging
import os
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Set, TextIO, Union, cast

import click
import requests
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              ClassDefinitionName,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import camelcase, underscore
from rdflib import Namespace

from linkml.utils.generator import Generator, shared_arguments

yuml_is_a = "^-"
yuml_uses = "uses -.->"
yuml_injected = "< -.- inject"
yuml_slot_type = ":"
yuml_inline = "++- "
yuml_inline_rev = "-++"
yuml_ref = "- "

yuml_base = "https://yuml.me/diagram/nofunky"
yuml_scale = ""  # ';scale:180' ';scale:80' for small
yuml_dir = ";dir:TB"  # '
yuml_class = "/class/"
YUML = Namespace(yuml_base + yuml_scale + yuml_dir + yuml_class)


@dataclass
class YumlGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["yuml", "png", "pdf", "jpg", "json", "svg"]
    visit_all_class_slots = False

    referenced: Optional[
        Set[ClassDefinitionName]
    ] = None  # List of classes that have to be emitted
    generated: Optional[
        Set[ClassDefinitionName]
    ] = None  # List of classes that have been emitted
    box_generated: Optional[
        Set[ClassDefinitionName]
    ] = None  # Class boxes that have been emitted
    associations_generated: Optional[
        Set[ClassDefinitionName]
    ] = None  # Classes with associations generated
    focus_classes: Optional[
        Set[ClassDefinitionName]
    ] = None  # Classes to be completely filled
    gen_classes: Optional[
        Set[ClassDefinitionName]
    ] = None  # Classes to be generated
    output_file_name: Optional[
        str
    ] = None  # Location of output file if directory used

    classes: Set[ClassDefinitionName] = None
    directory: Optional[str] = None
    load_image: bool = field(default_factory=lambda: True)


    def visit_schema(
        self,
        classes: Set[ClassDefinitionName] = None,
        directory: Optional[str] = None,
        load_image: bool = True,
        **_,
    ) -> None:
        if directory:
            os.makedirs(directory, exist_ok=True)
        if classes is not None:
            for cls in classes:
                if cls not in self.schema.classes:
                    raise ValueError(f"Unknown class name: {cls}")
        self.box_generated = set()
        self.associations_generated = set()
        self.focus_classes = classes
        if classes:
            self.gen_classes = self.neighborhood(list(classes)).classrefs.union(classes)
        else:
            self.gen_classes = self.synopsis.roots.classrefs
        self.referenced = self.gen_classes
        self.generated = set()
        yumlclassdef: List[str] = []
        while self.referenced.difference(self.generated):
            cn = sorted(list(self.referenced.difference(self.generated)), reverse=True)[
                0
            ]
            self.generated.add(cn)
            assocs = self.class_associations(
                ClassDefinitionName(cn), cn in self.referenced
            )
            if assocs:
                yumlclassdef.append(assocs)
            else:
                yumlclassdef.append(self.class_box(ClassDefinitionName(cn)))

        yuml_url = (
            str(YUML)
            + ",".join(yumlclassdef)
            + (("." + self.format) if self.format not in ("yuml", "svg") else "")
        )
        file_suffix = ".svg" if self.format == "yuml" else "." + self.format
        if directory:
            self.output_file_name = os.path.join(
                directory,
                camelcase(sorted(classes)[0] if classes else self.schema.name)
                + file_suffix,
            )
            if load_image:
                resp = requests.get(yuml_url, stream=True)
                if resp.ok:
                    with open(self.output_file_name, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=2048):
                            f.write(chunk)
                else:
                    self.logger.error(f"{resp.reason} accessing {yuml_url}")
        else:
            print(str(YUML) + ",".join(yumlclassdef), end="")

    def class_box(self, cn: ClassDefinitionName) -> str:
        """Generate a box for the class.  Populate its interior only if (a) it hasn't previously been generated and
        (b) it appears in the gen_classes list

        @param cn:
        @return:
        """
        slot_defs: List[str] = []
        if cn not in self.box_generated and (
            not self.focus_classes or cn in self.focus_classes
        ):
            cls = self.schema.classes[cn]
            for slot in self.filtered_cls_slots(
                cn, all_slots=True, filtr=lambda s: s.range not in self.schema.classes
            ):
                if True or cn in slot.domain_of:
                    mod = self.prop_modifier(cls, slot)
                    slot_defs.append(
                        underscore(self.aliased_slot_name(slot))
                        + mod
                        + ":"
                        + underscore(slot.range)
                        + self.cardinality(slot)
                    )
            self.box_generated.add(cn)
        self.referenced.add(cn)
        return (
            "[" + camelcase(cn) + ("|" + ";".join(slot_defs) if slot_defs else "") + "]"
        )

    def class_associations(
        self, cn: ClassDefinitionName, must_render: bool = False
    ) -> str:
        """Emit all associations for a focus class.  If none are specified, all classes are generated

        @param cn: Name of class to be emitted
        @param must_render: True means render even if this is a target (class is specifically requested)
        @return: YUML representation of the association
        """

        # NOTE: YUML diagrams draw in the opposite order in which they are created, so we work from bottom to top and
        # from right to left
        assocs: List[str] = []
        if cn not in self.associations_generated and (
            not self.focus_classes or cn in self.focus_classes
        ):
            cls = self.schema.classes[cn]

            # Slots that reference other classes
            for slot in self.filtered_cls_slots(
                cn, False, lambda s: s.range in self.schema.classes
            )[::-1]:
                # Swap the two boxes because, in the case of self reference, the last definition wins
                if (
                    not slot.range in self.associations_generated
                    and cn in slot.domain_of
                ):
                    rhs = self.class_box(cn)
                    lhs = self.class_box(cast(ClassDefinitionName, slot.range))
                    assocs.append(
                        lhs
                        + "<"
                        + self.aliased_slot_name(slot)
                        + self.prop_modifier(cls, slot)
                        + self.cardinality(slot, False)
                        + (yuml_inline_rev if slot.inlined else yuml_ref)
                        + rhs
                    )

            # Slots in other classes that reference this
            for slotname in sorted(self.synopsis.rangerefs.get(cn, [])):
                slot = self.schema.slots[slotname]
                # Don't do self references twice
                # Also, slot must be owned by the class
                if (
                    cls.name not in slot.domain_of
                    and cls.name not in self.associations_generated
                ):
                    for dom in [self.schema.classes[dof] for dof in slot.domain_of]:
                        assocs.append(
                            self.class_box(dom.name)
                            + (yuml_inline if slot.inlined else yuml_ref)
                            + self.aliased_slot_name(slot)
                            + self.prop_modifier(dom, slot)
                            + self.cardinality(slot, False)
                            + ">"
                            + self.class_box(cn)
                        )

            # Mixins used in the class
            for mixin in cls.mixins:
                assocs.append(self.class_box(cn) + yuml_uses + self.class_box(mixin))

            # Classes that use the class as a mixin
            if cls.name in self.synopsis.mixinrefs:
                for mixin in sorted(
                    self.synopsis.mixinrefs[cls.name].classrefs, reverse=True
                ):
                    assocs.append(
                        self.class_box(ClassDefinitionName(mixin))
                        + yuml_uses
                        + self.class_box(cn)
                    )

            # Classes that inject information
            if cn in self.synopsis.applytos.classrefs:
                for injector in sorted(
                    self.synopsis.applytorefs[cn].classrefs, reverse=True
                ):
                    assocs.append(
                        self.class_box(cn)
                        + yuml_injected
                        + self.class_box(ClassDefinitionName(injector))
                    )
            self.associations_generated.add(cn)

            # Children
            if cn in self.synopsis.isarefs:
                for is_a_cls in sorted(
                    self.synopsis.isarefs[cn].classrefs, reverse=True
                ):
                    assocs.append(
                        self.class_box(cn)
                        + yuml_is_a
                        + self.class_box(ClassDefinitionName(is_a_cls))
                    )

            # Parent
            if cls.is_a and cls.is_a not in self.associations_generated:
                assocs.append(self.class_box(cls.is_a) + yuml_is_a + self.class_box(cn))
        return ",".join(assocs)

    @staticmethod
    def cardinality(slot: SlotDefinition, is_attribute: bool = True) -> str:
        if is_attribute:
            if slot.multivalued:
                return " %2B" if slot.required else " *"
            else:
                return "" if slot.required else " %3F"
        else:
            if slot.multivalued:
                return " 1..*" if slot.required else " 0..*"
            else:
                return " 1..1" if slot.required else " 0..1"

    def filtered_cls_slots(
        self,
        cn: ClassDefinitionName,
        all_slots: bool = True,
        filtr: Callable[[SlotDefinition], bool] = None,
    ) -> List[SlotDefinition]:
        """Return the set of slots associated with the class that meet the filter criteria.  Slots will be returned
        in defining order, with class slots returned last

        @param cn: name of class to filter
        @param all_slots: True means include attributes
        @param filtr: Slot filter predicate
        @return: List of slot definitions
        """
        if filtr is None:
            filtr = lambda x: True

        rval = []
        cls = self.schema.classes[cn]
        cls_slots = self.all_slots(cls, cls_slots_first=True)
        for slot in cls_slots:
            if (all_slots or slot.range in self.schema.classes) and filtr(slot):
                rval.append(slot)

        return rval

    def prop_modifier(self, cls: ClassDefinition, slot: SlotDefinition) -> str:
        """Return the modifiers for the slot:
            (i) - inherited
            (m) - inherited through mixin
            (a) - injected
            (pk) - primary ckey

        @param cls:
        @param slot:
        @return:
        """
        pk = "(pk)" if slot.key else ""
        inherited = slot.name not in self.own_slot_names(cls)
        mixin = inherited and slot.name in [
            mslot.name for mslot in [self.schema.classes[m] for m in cls.mixins]
        ]
        injected = cls.name in self.synopsis.applytos.classrefs and slot.name in [
            aslot.name
            for aslot in [
                self.schema.classes[a]
                for a in sorted(self.synopsis.applytorefs[cls.name].classrefs)
            ]
        ]
        return pk + (
            "(a)" if injected else "(m)" if mixin else "(i)" if inherited else ""
        )


@shared_arguments(YumlGenerator)
@click.command()
@click.option("--classes", "-c", multiple=True, help="Class(es) to emit")
@click.option(
    "--directory",
    "-d",
    help="Output directory - if supplied, YUML rendering will be saved in file",
)
def cli(yamlfile, **args):
    """Generate a UML representation of a LinkML model"""
    print(YumlGenerator(yamlfile, **args).serialize(**args), end="")


if __name__ == "__main__":
    cli()
