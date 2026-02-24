"""Generate plantuml

https://plantuml.com/

"""

import base64
import os
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

import click
import requests

from linkml import REQUESTS_TIMEOUT
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    SlotDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, underscore

plantuml_is_a = "^--"
plantuml_uses = ("--", " : uses")
plantuml_injected = ("--", " : inject")
plantuml_inline = "*--"
plantuml_inline_rev = "--*"
plantuml_ref = "--"

_TEXT_FORMATS: frozenset[str] = frozenset({"puml", "plantuml"})
"""Formats that produce PlantUML source text rather than a rendered image."""
_BINARY_FORMATS: frozenset[str] = frozenset({"png", "pdf", "jpg"})
"""Rendered formats whose output is binary and cannot be written to stdout."""


@dataclass
class PlantumlGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["puml", "plantuml", "png", "pdf", "jpg", "json", "svg"]
    visit_all_class_slots = False
    preserve_names: bool = False

    referenced: set[ClassDefinitionName] | None = None  # List of classes that have to be emitted
    generated: set[ClassDefinitionName] | None = None  # List of classes that have been emitted
    class_generated: set[ClassDefinitionName] | None = None  # Class definitions that have been emitted
    associations_generated: set[ClassDefinitionName] | None = None  # Classes with associations generated
    focus_classes: set[ClassDefinitionName] | None = None  # Classes to be completely filled
    gen_classes: set[ClassDefinitionName] | None = None  # Classes to be generated
    output_file_name: str | None = None  # Location of output file if directory used

    classes: set[ClassDefinitionName] = None
    directory: str | None = None
    kroki_server: str | None = "https://kroki.io"
    tooltips_flag: bool = False
    dry_run: bool = False
    include_enums: bool = False
    """If True, render enumeration definitions as PlantUML ``enum`` blocks and add
    association arrows from classes to their enum-typed slots."""
    include_all: bool = False
    """If True, include all classes and enumerations from the schema, regardless of
    which classes are selected. Implies ``include_enums`` for the enum selection
    strategy: all enumerations are rendered rather than only those referenced by
    selected classes."""
    mark_mixins: bool = False
    """If True, mixin classes are annotated with a ``<<(M,orchid) mixin>>`` PlantUML
    spot stereotype so they are visually distinguishable from regular classes."""

    def _referenced_enum_names(self) -> set[str]:
        """Return the names of all enumerations referenced by slots in the generated classes."""
        all_enum_names = set(self.schema.enums.keys())
        referenced: set[str] = set()
        for cn in self.generated or set():
            if cn in self.schema.classes:
                for slot in self.all_slots(self.schema.classes[cn], cls_slots_first=True):
                    if slot.range in all_enum_names:
                        referenced.add(slot.range)
        return referenced

    def _all_enum_names(self) -> set[str]:
        """Return the names of all enumerations defined in the schema."""
        return set(self.schema.enums.keys())

    def _generate_enum_defs(self, enum_names: set[str]) -> list[str]:
        """Return PlantUML ``enum`` block definitions for each name in *enum_names*.

        Each permissible value is listed as a member.  When the value has a
        ``meaning`` URI it is appended in brackets, e.g. ``FIRE [bizcodes:002]``.
        """
        defs: list[str] = []
        for enum_name in sorted(enum_names):
            enum_def = self.schema.enums[enum_name]
            members: list[str] = []
            for pv_name, pv in (enum_def.permissible_values or {}).items():
                label = pv_name
                if pv.meaning:
                    label += f" [{pv.meaning}]"
                members.append(f"    {label}")
            block = f'enum "{enum_name}" {{\n' + "\n".join(members) + "\n}"
            defs.append(block)
        return defs

    def _generate_enum_inherits(self, enum_names: set[str]) -> list[str]:
        """Return PlantUML generalisation arrows for enum ``inherits`` relationships.

        Only arrows where both parent and child are in *enum_names* are emitted.
        """
        arrows: list[str] = []
        for enum_name in sorted(enum_names):
            enum_def = self.schema.enums[enum_name]
            for parent in enum_def.inherits or []:
                if parent in enum_names:
                    arrows.append(f'"{parent}" <|-- "{enum_name}"')
        return arrows

    def _generate_enum_assocs(self, enum_names: set[str]) -> list[str]:
        """Return PlantUML association arrows from classes to their enum-typed slots.

        Only slots that are directly defined on the class (via ``domain_of``) are
        included to avoid duplicating inherited associations.
        """
        assocs: list[str] = []
        for cn in sorted(self.generated or set()):
            if cn not in self.schema.classes:
                continue
            cls = self.schema.classes[cn]
            for slot in self.all_slots(cls, cls_slots_first=True):
                if slot.range not in enum_names:
                    continue
                if cn not in slot.domain_of:
                    continue
                slot_name = self.aliased_slot_name(slot)
                assocs.append(f'"{cn}" --> "{slot.range}" : "{slot_name}"')
        return assocs

    def visit_schema(
        self,
        classes: set[ClassDefinitionName] = None,
        directory: str | None = None,
        **_,
    ) -> str | None:
        if self.include_all:
            classes = set(self.schema.classes.keys())
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
        plantumlclassdef: list[str] = []
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

        if self.include_enums or self.include_all:
            enum_names = self._all_enum_names() if self.include_all else self._referenced_enum_names()
            plantumlclassdef.extend(self._generate_enum_defs(enum_names))
            plantumlclassdef.extend(self._generate_enum_inherits(enum_names))
            plantumlclassdef.extend(self._generate_enum_assocs(enum_names))

        dedup_plantumlclassdef = []
        [dedup_plantumlclassdef.append(x) for x in plantumlclassdef if x not in dedup_plantumlclassdef]

        plantuml_code = "\n".join(dedup_plantumlclassdef)
        b64_diagram = base64.urlsafe_b64encode(zlib.compress(plantuml_code.encode(), 9))

        kroki_format = "svg" if self.format in _TEXT_FORMATS else self.format
        plantuml_url = self.kroki_server + f"/plantuml/{kroki_format}/" + b64_diagram.decode()
        if self.dry_run:
            return plantuml_url
        if directory:
            file_suffix = ".svg" if self.format in _TEXT_FORMATS else "." + self.format
            schema_name = sorted(classes)[0] if classes else self.schema.name
            filename = schema_name if self.preserve_names else camelcase(schema_name)
            self.output_file_name = os.path.join(directory, filename + file_suffix)
            resp = requests.get(plantuml_url, stream=True, timeout=REQUESTS_TIMEOUT)
            if resp.ok:
                with open(self.output_file_name, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=2048):
                        f.write(chunk)
            else:
                self.logger.error(f"{resp.reason} accessing {plantuml_url}")
        else:
            if self.format in _TEXT_FORMATS:
                return (
                    "@startuml\n"
                    "skinparam nodesep 10\n"
                    "hide circle\n"
                    "hide empty members\n" + "\n".join(dedup_plantumlclassdef) + "\n@enduml\n"
                )
            if self.format in _BINARY_FORMATS:
                raise ValueError(f"Binary format {self.format!r} cannot be written to stdout; use --directory instead.")
            resp = requests.get(plantuml_url, timeout=REQUESTS_TIMEOUT)
            if resp.ok:
                return resp.text
            self.logger.error(f"{resp.reason} accessing {plantuml_url}")
            return None

    def add_class(self, cn: ClassDefinitionName) -> str:
        """Define the class only if
        (a) it hasn't previously been generated and
        (b) it appears in the gen_classes list

        @param cn:
        @return:
        """
        slot_defs: list[str] = []
        if cn not in self.class_generated and (not self.focus_classes or cn in self.focus_classes):
            cls = self.schema.classes[cn]
            for slot in self.filtered_cls_slots(cn, all_slots=True, filtr=lambda s: s.range not in self.schema.classes):
                if True or cn in slot.domain_of:
                    mod = self.prop_modifier(cls, slot)
                    slot_name = (
                        self.aliased_slot_name(slot)
                        if self.preserve_names
                        else underscore(self.aliased_slot_name(slot))
                    )
                    range_name = slot.range if self.preserve_names else underscore(slot.range)
                    slot_defs.append(
                        "    {field} " + slot_name + mod + " : " + range_name + " " + self.cardinality(slot)
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
        stereotype = " <<(M,orchid) mixin>>" if self.mark_mixins and cls.mixin else ""
        return class_type + ' "' + cn + '"' + stereotype + tooltip + ("{\n" + "\n".join(slot_defs) + "\n}")

    def class_associations(self, cn: ClassDefinitionName, must_render: bool = False) -> str:
        """Emit all associations for a focus class.  If none are specified, all classes are generated

        @param cn: Name of class to be emitted
        @param must_render: True means render even if this is a target (class is specifically requested)
        @return: PLANTUML representation of the association
        """

        classes: list[str] = []
        assocs: list[str] = []
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
        entries: list[str] = []
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
    ) -> list[SlotDefinition]:
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
@click.command(name="plantuml")
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
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    show_default=True,
    help="Print out Kroki URL calls instead of sending the real requests",
)
@click.option(
    "--preserve-names/--normalize-names",
    default=False,
    show_default=True,
    help="Preserve original LinkML names in PlantUML diagram output (e.g., for class names, slot names, file names).",
)
@click.option(
    "--include-enums/--no-include-enums",
    default=False,
    show_default=True,
    help=(
        "If true, render enumerations referenced by the selected classes as PlantUML enum blocks "
        "and add association arrows from classes to their enum-typed slots."
    ),
)
@click.option(
    "--mark-mixins/--no-mark-mixins",
    default=False,
    show_default=True,
    help=(
        "If true, annotate mixin classes with a <<(M,orchid) mixin>> PlantUML spot stereotype "
        "so they are visually distinguishable from regular classes."
    ),
)
@click.option(
    "--all",
    "-a",
    "include_all",
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        "Include all classes and enumerations from the schema. "
        "Overrides --classes and implies all enumerations are rendered."
    ),
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate a UML representation of a LinkML model"""
    print(PlantumlGenerator(yamlfile, **args).serialize(**args), end="")


if __name__ == "__main__":
    cli()
