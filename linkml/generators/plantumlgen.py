"""Generate plantuml

https://plantuml.com/

"""

import base64
import os
import zlib
from dataclasses import dataclass
from typing import Callable, List, Optional, Set, cast

import click
import requests
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    SlotDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, underscore

from linkml import REQUESTS_TIMEOUT
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

plantuml_is_a = "^--"
plantuml_uses = ("--", " : uses")
plantuml_injected = ("--", " : inject")
plantuml_inline = "*--"
plantuml_inline_rev = "--*"
plantuml_ref = "--"


@dataclass
class PlantumlGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["puml", "plantuml", "png", "pdf", "jpg", "json", "svg"]
    visit_all_class_slots = False

    referenced: Optional[Set[ClassDefinitionName]] = None  # List of classes that have to be emitted
    generated: Optional[Set[ClassDefinitionName]] = None  # List of classes that have been emitted
    class_generated: Optional[Set[ClassDefinitionName]] = None  # Class definitions that have been emitted
    associations_generated: Optional[Set[ClassDefinitionName]] = None  # Classes with associations generated
    focus_classes: Optional[Set[ClassDefinitionName]] = None  # Classes to be completely filled
    gen_classes: Optional[Set[ClassDefinitionName]] = None  # Classes to be generated
    output_file_name: Optional[str] = None  # Location of output file if directory used

    classes: Set[ClassDefinitionName] = None
    directory: Optional[str] = None
    kroki_server: Optional[str] = "https://kroki.io"
    load_image: bool = True
    tooltips_flag: bool = False

    def visit_schema(
        self,
        classes: Set[ClassDefinitionName] = None,
        directory: Optional[str] = None,
        load_image: bool = True,
        **_,
    ) -> Optional[str]:
        if directory:
            os.makedirs(directory, exist_ok=True)
        if classes is not None:
            for cls in classes:
                if cls not in self.schema.classes:
                    raise ValueError(f"Unknown class name: {cls}")
        self.class_generated = set()
        self.associations_generated = set()
        if classes is None:
            self.focus_classes = set()
        else:
            self.focus_classes = set(classes)
        if classes:
            self.gen_classes = self.neighborhood(list(classes)).classrefs.union(classes)
        else:
            self.gen_classes = self.synopsis.roots.classrefs
        self.referenced = self.gen_classes
        self.generated = set()
        plantumlclassdef: List[str] = []
        while self.referenced.difference(self.generated):
            cn = sorted(list(self.referenced.difference(self.generated)), reverse=True)[0]
            self.generated.add(cn)
            assocs = self.class_associations(ClassDefinitionName(cn), cn in self.referenced)
            if assocs:
                plantumlclassdef.extend(assocs)
            else:
                if ClassDefinitionName(cn) not in self.class_generated:
                    plantumlclassdef.append(self.add_class(ClassDefinitionName(cn)))
                    self.add_class(ClassDefinitionName(cn))

        dedup_plantumlclassdef = []
        [dedup_plantumlclassdef.append(x) for x in plantumlclassdef if x not in dedup_plantumlclassdef]

        plantuml_code = "\n".join(dedup_plantumlclassdef)
        b64_diagram = base64.urlsafe_b64encode(zlib.compress(plantuml_code.encode(), 9))

        plantuml_url = self.kroki_server + "/plantuml/svg/" + b64_diagram.decode()
        if directory:
            file_suffix = ".svg" if self.format == "puml" or self.format == "puml" else "." + self.format
            self.output_file_name = os.path.join(
                directory,
                camelcase(sorted(classes)[0] if classes else self.schema.name) + file_suffix,
            )
            if load_image:
                resp = requests.get(plantuml_url, stream=True, timeout=REQUESTS_TIMEOUT)
                if resp.ok:
                    with open(self.output_file_name, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=2048):
                            f.write(chunk)
                else:
                    self.logger.error(f"{resp.reason} accessing {plantuml_url}")
        else:
            out = (
                "@startuml\n"
                "skinparam nodesep 10\n"
                "hide circle\n"
                "hide empty members\n" + "\n".join(dedup_plantumlclassdef) + "\n@enduml\n"
            )
            return out

    def add_class(self, cn: ClassDefinitionName) -> str:
        """Define the class only if
        (a) it hasn't previously been generated and
        (b) it appears in the gen_classes list

        @param cn:
        @return:
        """
        slot_defs: List[str] = []
        if cn not in self.class_generated and (not self.focus_classes or cn in self.focus_classes):
            cls = self.schema.classes[cn]
            for slot in self.filtered_cls_slots(cn, all_slots=True, filtr=lambda s: s.range not in self.schema.classes):
                if True or cn in slot.domain_of:
                    mod = self.prop_modifier(cls, slot)
                    slot_defs.append(
                        "    {field} "
                        + underscore(self.aliased_slot_name(slot))
                        + mod
                        + " : "
                        + underscore(slot.range)
                        + " "
                        + self.cardinality(slot)
                    )
            self.class_generated.add(cn)
        self.referenced.add(cn)
        cls = self.schema.classes[cn]

        tooltip_contents = str(cls.description)
        first_newline_index = tooltip_contents.find("\n")
        tooltip_contents = tooltip_contents if first_newline_index < 0 else tooltip_contents[0:first_newline_index]

        if self.format == "svg" and len(tooltip_contents) > 200:
            tooltip_contents = tooltip_contents[0:197] + " ... "

        tooltip = " [[{" + tooltip_contents + "}]] "
        if cls.abstract:
            class_type = "abstract"
        else:
            class_type = "class"
        return class_type + ' "' + cn + '"' + tooltip + ("{\n" + "\n".join(slot_defs) + "\n}")

    def class_associations(self, cn: ClassDefinitionName, must_render: bool = False) -> str:
        """Emit all associations for a focus class.  If none are specified, all classes are generated

        @param cn: Name of class to be emitted
        @param must_render: True means render even if this is a target (class is specifically requested)
        @return: PLANTUML representation of the association
        """

        classes: List[str] = []
        assocs: List[str] = []
        if cn not in self.associations_generated and (not self.focus_classes or cn in self.focus_classes):
            cls = self.schema.classes[cn]

            # Slots that reference other classes
            for slot in self.filtered_cls_slots(cn, False, lambda s: s.range in self.schema.classes)[::-1]:
                # Swap the two boxes because, in the case of self reference, the last definition wins
                if slot.range not in self.associations_generated and cn in slot.domain_of:
                    if cn not in self.class_generated:
                        classes.append(self.add_class(cn))
                    lhs = cn
                    if cast(ClassDefinitionName, slot.range) not in self.class_generated:
                        classes.append(self.add_class(cast(ClassDefinitionName, slot.range)))
                    rhs = cast(ClassDefinitionName, slot.range)
                    assocs.append(
                        '"'
                        + lhs
                        + '" '
                        + (plantuml_inline if slot.inlined else plantuml_ref)
                        + "> "
                        + self.cardinality(slot, False)
                        + '"'
                        + rhs
                        + '" : '
                        + '"'
                        + self.aliased_slot_name(slot)
                        + '"'
                        + self.prop_modifier(cls, slot)
                    )

            # Slots in other classes that reference this
            for slotname in sorted(self.synopsis.rangerefs.get(cn, [])):
                slot = self.schema.slots[slotname]
                # Don't do self references twice
                # Also, slot must be owned by the class
                if cls.name not in slot.domain_of and cls.name not in self.associations_generated:
                    for dom in [self.schema.classes[dof] for dof in slot.domain_of]:
                        if dom.name not in self.class_generated:
                            classes.append(self.add_class(dom.name))
                        if cn not in self.class_generated:
                            classes.append(self.add_class(cn))
                        assocs.append(
                            '"'
                            + dom.name
                            + '" '
                            + (plantuml_inline if slot.inlined else plantuml_ref)
                            + "> "
                            + self.cardinality(slot, False)
                            + '"'
                            + cn
                            + '" : '
                            + '"'
                            + self.aliased_slot_name(slot)
                            + '"'
                            + self.prop_modifier(dom, slot)
                        )

            # Mixins used in the class
            for mixin in cls.mixins:
                if cn not in self.class_generated:
                    classes.append(self.add_class(cn))
                if mixin not in self.class_generated:
                    classes.append(self.add_class(mixin))
                assocs.append('"' + cn + '" ' + plantuml_uses[0] + ' "' + mixin + '" ' + plantuml_uses[1])

            # Classes that use the class as a mixin
            if cls.name in self.synopsis.mixinrefs:
                for mixin in sorted(self.synopsis.mixinrefs[cls.name].classrefs, reverse=True):
                    if ClassDefinitionName(mixin) not in self.class_generated:
                        classes.append(self.add_class(ClassDefinitionName(mixin)))
                    if cn not in self.class_generated:
                        classes.append(self.add_class(cn))
                    assocs.append(
                        '"' + ClassDefinitionName(mixin) + '" ' + plantuml_uses[0] + ' "' + cn + '" ' + plantuml_uses[1]
                    )

            # Classes that inject information
            if cn in self.synopsis.applytos.classrefs:
                for injector in sorted(self.synopsis.applytorefs[cn].classrefs, reverse=True):
                    if cn not in self.class_generated:
                        classes.append(self.add_class(cn))
                    if ClassDefinitionName(injector) not in self.class_generated:
                        classes.append(self.add_class(ClassDefinitionName(injector)))
                    assocs.append(cn + plantuml_injected[0] + ClassDefinitionName(injector) + plantuml_injected[1])
            self.associations_generated.add(cn)

            # Children
            if cn in self.synopsis.isarefs:
                for is_a_cls in sorted(self.synopsis.isarefs[cn].classrefs, reverse=True):
                    if cn not in self.class_generated:
                        classes.append(self.add_class(cn))
                    if ClassDefinitionName(is_a_cls) not in self.class_generated:
                        classes.append(self.add_class(ClassDefinitionName(is_a_cls)))
                    assocs.append('"' + cn + '" ' + plantuml_is_a + ' "' + ClassDefinitionName(is_a_cls) + '"')

            # Parent
            if cls.is_a and cls.is_a not in self.associations_generated:
                if cls.is_a not in self.class_generated:
                    classes.append(self.add_class(cls.is_a))
                if cn not in self.class_generated:
                    classes.append(self.add_class(cn))
                assocs.append('"' + cls.is_a + '" ' + plantuml_is_a + ' "' + cn + '"')
        entries: List[str] = []
        entries.extend(classes)
        entries.extend(assocs)
        return entries

    @staticmethod
    def cardinality(slot: SlotDefinition, is_attribute: bool = True) -> str:
        if is_attribute:
            if slot.multivalued:
                return " [1..*]" if slot.required else " [0..*]"
            else:
                return " "
        else:
            if slot.multivalued:
                return '"1..*" ' if slot.required else '"0..*" '
            else:
                return '"1" ' if slot.required else '"0..1" '

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

            def filtr(x):
                return True

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
        mixin = inherited and slot.name in [mslot.name for mslot in [self.schema.classes[m] for m in cls.mixins]]
        injected = cls.name in self.synopsis.applytos.classrefs and slot.name in [
            aslot.name
            for aslot in [self.schema.classes[a] for a in sorted(self.synopsis.applytorefs[cls.name].classrefs)]
        ]
        return pk + ("(a)" if injected else "(m)" if mixin else "(i)" if inherited else "")


@shared_arguments(PlantumlGenerator)
@click.command()
@click.option("--classes", "-c", multiple=True, help="Class(es) to emit")
@click.option(
    "--directory",
    "-d",
    help="Output directory - if supplied, PlantUML rendering will be saved in file",
)
@click.option(
    "--kroki-server",
    "-k",
    help="URL of the Kroki server to use for diagram drawing",
    default="https://kroki.io",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate a UML representation of a LinkML model"""
    print(PlantumlGenerator(yamlfile, **args).serialize(**args), end="")


if __name__ == "__main__":
    cli()
