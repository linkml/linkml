import os
from dataclasses import dataclass
from datetime import date
from typing import Optional, TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (LINKML, ClassDefinition,
                                              Definition, EnumDefinition,
                                              SchemaDefinition, SlotDefinition)

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

DEFAULT_OUTPUT_FILENAME = "sssom.tsv"


@dataclass
class SSSOMGenerator(Generator):
    """
    Generates Simple Standard for Sharing Ontology Mappings (SSSOM) TSVs
    """
    # ClassVats
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["tsv"]
    uses_schemaloader = True

    # TODO: move up
    msdf_columns = [
        "subject_id",
        "subject_label",
        "predicate_id",
        "predicate_modifier",
        "object_id",
        "object_label",
        "match_type",
        "subject_source",
        "object_source",
        "mapping_tool",
        "confidence",
        "subject_match_field",
        "object_match_field",
        "subject_category",
        "object_category",
        "match_string",
        "comment",
    ]
    mapping_type_dict = {
        "related_mappings": "skos:relatedMatch",
        "broad_mappings": "skos:broadMatch",
        "narrow_mappings": "skos:narrowMatch",
        "close_mappings": "skos:closeMatch",
        "exact_mappings": "skos:exactMatch",
    }

    def __post_init__(self):
        super().__post_init__()
        self.sourcefile = self.schema
        self.table_as_list = []
        if self.output:
            self.output_file = self.output
        else:
            self.output_file = DEFAULT_OUTPUT_FILENAME


    def make_msdf_list(self, row_as_dict: dict) -> None:
        list_of_row = []
        for col_name in self.msdf_columns:
            if col_name in row_as_dict.keys():
                list_of_row.append(row_as_dict[col_name])
            else:
                list_of_row.append("")
        self.table_as_list.append(list_of_row)

    def definition_extract_info(self, obj: Definition):
        subject_source = obj.from_schema
        if type(obj) is not EnumDefinition:
            if type(obj) is ClassDefinition:
                obj: ClassDefinition
                if obj.class_uri:
                    subject_id = obj.class_uri

            elif type(obj) is SlotDefinition:
                obj: SlotDefinition
                if obj.slot_uri:
                    subject_id = obj.slot_uri

            if obj.title:
                subject_label = obj.title
            else:
                subject_label = obj.name

            for map_key, map_val in self.mapping_type_dict.items():
                if obj.__dict__[map_key]:
                    predicate_id = map_val
                    match_type = map_val
                    for obj_id in obj.__dict__[map_key]:
                        object_id = obj_id
                        # obj_label = "OBJ_LABEL" # Placeholder for the future
                        row_dict = {}
                        row_dict["subject_id"] = subject_id
                        row_dict["subject_label"] = subject_label
                        row_dict["predicate_id"] = predicate_id
                        row_dict["object_id"] = object_id
                        # row_dict["object_label"] = object_label
                        row_dict["subject_source"] = subject_source
                        if match_type:
                            row_dict["match_type"] = match_type

                        self.make_msdf_list(row_dict)

        elif type(obj) is EnumDefinition:
            if obj.permissible_values:
                obj: EnumDefinition
                subject_category = obj.name.replace(" ", "")
                predicate_id = "skos:exactMatch"
                default_prefix = self.schema_defaults[obj.from_schema]
                for k, v in obj.permissible_values.items():
                    if v["meaning"]:
                        subject_id = (
                            default_prefix
                            + ":"
                            + subject_category
                            + "#"
                            + k.replace(" ", "")
                        )
                        subject_label = k.replace(" ", "")
                        object_id = obj.permissible_values[k]["meaning"]
                        row_dict = {}
                        row_dict["subject_id"] = subject_id
                        row_dict["subject_label"] = subject_label
                        row_dict["predicate_id"] = predicate_id
                        row_dict["object_id"] = object_id
                        # row_dict["object_label"] = object_label
                        row_dict["match_type"] = predicate_id
                        row_dict["subject_source"] = subject_source
                        row_dict["subject_category"] = subject_category

                        self.make_msdf_list(row_dict)
        else:
            raise (
                TypeError(
                    "The object type passed is none of the following:\
                    ['ClassDefinition', 'SlotDefinition', 'EnumDefinition']"
                )
            )

    def visit_class(self, cls: ClassDefinition) -> bool:
        self.definition_extract_info(cls)
        return True

    def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
        self.definition_extract_info(slot)

    def visit_enum(self, enum: EnumDefinition) -> None:
        self.definition_extract_info(enum)

    def end_schema(self, context: str = None, **_) -> None:
        metadata = {}
        schema: SchemaDefinition = self.schema

        metadata["license"] = schema.license
        metadata["mapping_set_id"] = schema.id
        metadata["mapping_tool"] = LINKML
        metadata["creator_id"] = "linkml_user"
        metadata["mapping_date"] = date.today().strftime("%Y-%m-%d")
        metadata["curie_map"] = {
            k: v.prefix_reference for k, v in schema.prefixes.items()
        }
        with open(self.output_file, "w", encoding="UTF-8") as sssom_tsv:
            for k, v in metadata.items():
                if k != "curie_map":
                    sssom_tsv.write("#" + k + ": " + v + "\n")
                else:
                    v: dict
                    sssom_tsv.write("#" + k + ": \n")
                    for pref, uri in v.items():
                        sssom_tsv.write("# " + pref + ": " + uri + "\n")

            # Write column names first
            sssom_tsv.writelines("\t".join(self.msdf_columns) + "\n")
            # Write the msdf next
            sssom_tsv.writelines("\t".join(i) + "\n" for i in self.table_as_list)


@shared_arguments(SSSOMGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate SSSOM TSV to represent a LinkML model"""
    print(SSSOMGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
