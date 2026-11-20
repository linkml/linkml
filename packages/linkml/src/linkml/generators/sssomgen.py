"""Generate a SSSOM mapping set from the mappings a LinkML schema declares."""

import os
import re
from dataclasses import dataclass
from datetime import date
from typing import ClassVar
from urllib.parse import quote

import click
import yaml

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    Element,
    EnumDefinition,
    SlotDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore

DEFAULT_OUTPUT_FILENAME = "sssom.tsv"

# The terms that SSSOM 1.x admits in ``mapping_justification``, as the pattern on that slot
# in sssom_schema 1.1 lists them. A mapping that an author writes into a schema is curated by
# hand, so ManualMappingCuration is the default.
MAPPING_JUSTIFICATIONS = (
    "semapv:ManualMappingCuration",
    "semapv:MappingReview",
    "semapv:LogicalReasoning",
    "semapv:LexicalMatching",
    "semapv:CompositeMatching",
    "semapv:UnspecifiedMatching",
    "semapv:SemanticSimilarityThresholdMatching",
    "semapv:LexicalSimilarityThresholdMatching",
    "semapv:MappingChaining",
    "semapv:MappingInversion",
    "semapv:StructuralMatching",
    "semapv:InstanceBasedMatching",
    "semapv:BackgroundKnowledgeBasedMatching",
)
DEFAULT_MAPPING_JUSTIFICATION = "semapv:ManualMappingCuration"

# SSSOM's own value for a mapping set whose licence is not known.
UNSPECIFIED_LICENSE = "https://w3id.org/sssom/license/unspecified"

# The prefixes that every output uses. The curie_map declares them even when the schema does not.
SSSOM_PREFIXES = {
    "semapv": "https://w3id.org/semapv/vocab/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
}

# SPDX identifiers that LinkML schemas often carry as ``license``, each with the licence URL
# that SSSOM expects. The keys are in upper case, because the generator compares the schema's
# value in upper case.
SPDX_LICENSE_URLS = {
    "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/",
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
    "CC-BY-NC-4.0": "https://creativecommons.org/licenses/by-nc/4.0/",
    "CC-BY-NC-SA-4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "CC-BY-ND-4.0": "https://creativecommons.org/licenses/by-nd/4.0/",
    "CC-BY-NC-ND-4.0": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
    "CC-BY-3.0": "https://creativecommons.org/licenses/by/3.0/",
    "CC-BY-SA-3.0": "https://creativecommons.org/licenses/by-sa/3.0/",
    "MIT": "https://spdx.org/licenses/MIT.html",
    "APACHE-2.0": "https://spdx.org/licenses/Apache-2.0.html",
    "BSD-2-CLAUSE": "https://spdx.org/licenses/BSD-2-Clause.html",
    "BSD-3-CLAUSE": "https://spdx.org/licenses/BSD-3-Clause.html",
    "GPL-3.0-ONLY": "https://spdx.org/licenses/GPL-3.0-only.html",
    "GPL-3.0-OR-LATER": "https://spdx.org/licenses/GPL-3.0-or-later.html",
    "LGPL-3.0-ONLY": "https://spdx.org/licenses/LGPL-3.0-only.html",
    "MPL-2.0": "https://spdx.org/licenses/MPL-2.0.html",
}


def tsv_cell(value: str) -> str:
    r"""Return ``value`` as one SSSOM/TSV cell, with each tab or line break turned into a space.

    A tab would end the cell, and a line break would end the row.

    >>> tsv_cell("A person\twith\na title")
    'A person with a title'
    """
    return re.sub(r"[\t\r\n]+", " ", str(value)).strip()


# The columns that every output carries, whether or not a row fills them.
REQUIRED_COLUMNS = ("subject_id", "subject_label", "predicate_id", "object_id", "mapping_justification")


@dataclass
class SSSOMGenerator(Generator):
    """
    Generates a Simple Standard for Sharing Ontological Mappings (SSSOM) 1.x mapping set,
    as SSSOM/TSV, from the mappings declared in a schema.

    The generator writes one row for each entry in the ``exact_mappings``, ``close_mappings``,
    ``related_mappings``, ``narrow_mappings`` and ``broad_mappings`` of a class, slot or
    permissible value, with the matching SKOS property as its predicate. Each entry of the
    generic ``mappings`` slot becomes a ``skos:mappingRelation`` row. A ``class_uri`` or
    ``slot_uri`` that differs from the element's own URI is an exact mapping to it. One that
    equals the element's own URI is the element itself, and produces no row. A permissible
    value is identified by its enum's URI, a hash and its text, which is how gen-owl names a
    value without a ``meaning``. A ``meaning`` is written as an exact mapping of the value.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["tsv"]
    uses_schemaloader = True

    mapping_justification: str = DEFAULT_MAPPING_JUSTIFICATION
    """The semapv term written in every row's ``mapping_justification``."""

    mapping_set_id: str | None = None
    """The ``mapping_set_id`` of the output, which defaults to the schema id with ``mappings`` appended."""

    # The SSSOM 1.x columns that this generator fills, in the order the SSSOM schema lists them.
    # A column that no row fills is left out of the output, as sssom-py does when it writes a set.
    msdf_columns: ClassVar[list[str]] = [
        "subject_id",
        "subject_label",
        "subject_category",
        "predicate_id",
        "object_id",
        "mapping_justification",
        "subject_source",
    ]
    mapping_type_dict: ClassVar[dict[str, str]] = {
        "related_mappings": "skos:relatedMatch",
        "broad_mappings": "skos:broadMatch",
        "narrow_mappings": "skos:narrowMatch",
        "close_mappings": "skos:closeMatch",
        "exact_mappings": "skos:exactMatch",
        "mappings": "skos:mappingRelation",
    }

    def __post_init__(self):
        if self.mapping_justification not in MAPPING_JUSTIFICATIONS:
            raise ValueError(
                f"mapping_justification must be one of {', '.join(MAPPING_JUSTIFICATIONS)}; "
                f"got {self.mapping_justification}"
            )
        super().__post_init__()
        self.sourcefile = self.schema
        self.rows: list[dict[str, str]] = []
        self.written: set[tuple[str, str, str]] = set()
        self.related: set[tuple[str, str]] = set()
        self.used_prefixes: set[str] = set()
        if self.output:
            self.output_file = self.output
        else:
            self.output_file = DEFAULT_OUTPUT_FILENAME

    def native_uri(self, element: Element, local_name: str) -> str:
        """Return the URI that an element has in its own schema, as a CURIE when the default prefix is declared."""
        from_schema = element.from_schema or self.schema.id
        default_prefix = self.schema_defaults.get(from_schema, sfx(from_schema))
        return self.namespaces.uri_or_curie_for(default_prefix, local_name)

    def expand(self, uri_or_curie: str) -> str:
        """Return the full URI of a CURIE whose prefix is declared, and any other value unchanged."""
        value = str(uri_or_curie)
        if "://" in value or ":" not in value:
            return value
        prefix, local = value.split(":", 1)
        if prefix not in self.namespaces:
            return value
        return str(self.namespaces[prefix]) + local

    def as_curie(self, uri_or_curie: str) -> str:
        """Return a full URI as a CURIE when a declared prefix covers it, and any other value unchanged.

        SSSOM/TSV writes entity references as CURIEs, while a schema may give a mapping or a
        ``class_uri`` as a full URI. A URI that is exactly a namespace stays a URI, because
        sssom-py does not accept a CURIE with an empty local part.
        """
        value = str(uri_or_curie)
        if "://" not in value:
            return value
        curie = self.namespaces.curie_for(value, default_ok=False)
        if curie is None or curie.endswith(":"):
            return value
        return curie

    def same_entity(self, a: str, b: str) -> bool:
        """Return whether two CURIEs or URIs name the same entity."""
        return self.expand(a) == self.expand(b)

    def note_prefix(self, uri_or_curie: str) -> None:
        """Remember the prefix of a CURIE so that the curie_map can declare it."""
        value = str(uri_or_curie)
        if "://" in value or ":" not in value:
            return
        self.used_prefixes.add(value.split(":", 1)[0])

    def add_row(self, row: dict[str, str]) -> None:
        """Keep a row unless the same mapping is already written, and note the prefixes it uses.

        The schema loader visits a slot that a class refines in ``slot_usage`` again, with the
        same mappings and perhaps another title. The first row for a mapping comes from the
        slot's own declaration, and the generator keeps that row.
        """
        triple = (row["subject_id"], row["predicate_id"], row["object_id"])
        if triple in self.written:
            return
        self.written.add(triple)
        self.related.add((row["subject_id"], row["object_id"]))
        self.rows.append(row)
        for column in ("subject_id", "predicate_id", "object_id", "mapping_justification"):
            self.note_prefix(row[column])

    def add_mapping_rows(
        self,
        element: Element,
        subject_id: str,
        subject_label: str,
        subject_source: str | None,
        extra_exact: list[str] | None = None,
        **extra_columns: str,
    ) -> None:
        """Write one row per mapping the element declares, with ``extra_exact`` as further exact matches."""
        subject_id = self.as_curie(subject_id)
        for metaslot, predicate_id in self.mapping_type_dict.items():
            object_ids = list(getattr(element, metaslot) or [])
            if metaslot == "exact_mappings" and extra_exact:
                object_ids = extra_exact + object_ids
            for object_id in object_ids:
                object_id = self.as_curie(object_id)
                if self.same_entity(subject_id, object_id):
                    # Skip a class_uri or slot_uri equal to the element's own URI, because it
                    # names the element and is not a mapping. The schema loader copies a
                    # class_uri into exact_mappings, and a slot_uri into the generic mappings.
                    continue
                if metaslot == "mappings" and (subject_id, object_id) in self.related:
                    # Skip a generic mapping of a pair that a more specific mapping already
                    # relates, such as a slot_uri that the schema loader has put into the generic
                    # mappings. skos:mappingRelation is the parent of the SKOS match properties,
                    # so it adds nothing to such a pair.
                    continue
                row = {
                    "subject_id": subject_id,
                    "subject_label": subject_label,
                    "predicate_id": predicate_id,
                    "object_id": object_id,
                    "mapping_justification": self.mapping_justification,
                }
                if subject_source:
                    row["subject_source"] = str(subject_source)
                row.update(extra_columns)
                self.add_row(row)

    def visit_class(self, cls: ClassDefinition) -> bool:
        """Write the rows for a class's mappings, and for a class_uri that is not the class's own URI."""
        subject_id = self.native_uri(cls, camelcase(cls.name))
        self.add_mapping_rows(
            cls,
            subject_id,
            cls.title or cls.name,
            cls.from_schema,
            extra_exact=[str(cls.class_uri)] if cls.class_uri else None,
        )
        return False

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        """Write the rows for a slot's mappings, and for a slot_uri that is not the slot's own URI."""
        subject_id = self.native_uri(slot, underscore(aliased_slot_name))
        self.add_mapping_rows(
            slot,
            subject_id,
            slot.title or aliased_slot_name,
            slot.from_schema,
            extra_exact=[str(slot.slot_uri)] if slot.slot_uri else None,
        )

    def visit_enum(self, enum: EnumDefinition) -> None:
        """Write the rows for each permissible value's meaning and mappings, labelled with its title or text.

        Every value is identified the same way, by the URI that gen-owl gives a value without a
        meaning: its enum's URI, a hash and the text. A ``meaning`` names the external term that
        the value stands for, which is a mapping. So the meaning becomes the value's first exact
        match rather than its identifier, and a value with nothing but a meaning still has its row.
        """
        enum_uri = str(enum.enum_uri) if enum.enum_uri else self.native_uri(enum, camelcase(enum.name))
        for pv in enum.permissible_values.values():
            self.add_mapping_rows(
                pv,
                enum_uri + "#" + quote(pv.text.strip(), safe=""),
                pv.title or pv.text,
                enum.from_schema,
                extra_exact=[str(pv.meaning)] if pv.meaning else None,
                subject_category=enum.name,
            )

    def license_url(self) -> tuple[str, str | None]:
        """Return the licence URL for the header and, when the schema's licence cannot be used, a comment saying so."""
        declared = self.schema.license
        if not declared:
            return UNSPECIFIED_LICENSE, "The schema declares no license."
        declared = self.expand(str(declared))
        if "://" in declared:
            return declared, None
        url = SPDX_LICENSE_URLS.get(declared.upper())
        if url:
            return url, None
        return (
            UNSPECIFIED_LICENSE,
            f"The schema's license '{declared}' is neither a URI nor a recognised SPDX identifier, "
            "so the license of this mapping set is left unspecified.",
        )

    def curie_map(self) -> dict[str, str]:
        """Return the schema's prefixes, plus every prefix that a row uses, in prefix order."""
        prefixes = set(self.schema.prefixes) | self.used_prefixes | set(SSSOM_PREFIXES)
        curie_map = {}
        for prefix in sorted(prefixes):
            if prefix in self.schema.prefixes:
                curie_map[prefix] = str(self.schema.prefixes[prefix].prefix_reference)
            elif prefix in self.namespaces:
                curie_map[prefix] = str(self.namespaces[prefix])
            elif prefix in SSSOM_PREFIXES:
                curie_map[prefix] = SSSOM_PREFIXES[prefix]
            else:
                self.logger.warning(
                    f"Prefix '{prefix}' is used by a mapping but declared nowhere; the curie_map leaves it out"
                )
        return curie_map

    def end_schema(self, context: str = None, **_) -> None:
        """Write the mapping set: a YAML header on lines that start with '#', then the rows.

        The table holds only the columns that are in use.
        """
        metadata = {}
        metadata["mapping_set_id"] = self.mapping_set_id or sfx(str(self.schema.id)) + "mappings"
        metadata["license"], comment = self.license_url()
        metadata["mapping_provider"] = str(self.schema.id)
        if self.include_generation_date:
            # Write the day of generation as publication_date, not as mapping_date. SSSOM
            # propagates a mapping_date to each mapping, so it would say that every mapping was
            # asserted that day. The value is a date object, so that the header carries an
            # unquoted YAML date, as SSSOM files do.
            metadata["publication_date"] = date.today()
        if comment:
            metadata["comment"] = comment
        metadata["curie_map"] = self.curie_map()

        columns = [
            column
            for column in self.msdf_columns
            if column in REQUIRED_COLUMNS or any(row.get(column) for row in self.rows)
        ]
        header = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True, width=float("inf"))
        with open(self.output_file, "w", encoding="UTF-8") as sssom_tsv:
            for line in header.rstrip("\n").split("\n"):
                sssom_tsv.write("#" + line + "\n")
            sssom_tsv.write("\t".join(columns) + "\n")
            for row in self.rows:
                sssom_tsv.write("\t".join(tsv_cell(row.get(column, "")) for column in columns) + "\n")


@shared_arguments(SSSOMGenerator)
@click.command(name="sssom")
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--mapping-justification",
    default=DEFAULT_MAPPING_JUSTIFICATION,
    show_default=True,
    type=click.Choice(MAPPING_JUSTIFICATIONS),
    help="The semapv term written in every row's mapping_justification column",
)
@click.option(
    "--mapping-set-id",
    help="The mapping_set_id of the output, which defaults to the schema id with 'mappings' appended",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate a SSSOM 1.x mapping set (SSSOM/TSV) from the mappings declared in a LinkML schema"""
    print(SSSOMGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
