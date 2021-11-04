from datetime import date
import os
from typing import Optional, TextIO, Union

import click
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    LINKML,
    ClassDefinition,
    SchemaDefinition,
)
import pandas as pd


class SSSOMGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["tsv"]
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
    final_df = pd.DataFrame(columns=msdf_columns)

    def __init__(
        self,
        schema: Union[str, TextIO, SchemaDefinition],
        format: str = valid_formats[0],
        output: Optional[str] = None,
        **kwargs
    ) -> None:

        self.sourcefile = schema
        if output:
            self.output_file = output
        else:
            self.output_file = "sssom.tsv"

        if format is None:
            format = self.valid_formats[0]
        super().__init__(schema, **kwargs)

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.class_uri:
            subject_id = cls.class_uri
            if cls.title:
                subject_label = cls.title
            else:
                subject_label = cls.name

            if cls.exact_mappings:
                predicate_id = "skos:exactMatch"
                match_type = "skos:exactMatch"
                for obj in cls.exact_mappings:
                    object_id = obj

                    # object_label is a TODO for the future.
                    object_label = obj  # temporary placeholder
                    # Create a pandas DataFrame to eventually export s TSV
                    row_dict = {}
                    row_dict["subject_id"] = subject_id
                    row_dict["subject_label"] = subject_label
                    row_dict["predicate_id"] = predicate_id
                    row_dict["object_id"] = object_id
                    row_dict["object_label"] = object_label
                    row_dict["match_type"] = match_type
                    tmp_df = pd.DataFrame(row_dict, index=[0])
                    tmp_df = tmp_df.reindex(
                        columns=self.msdf_columns, fill_value=""
                    )
                    self.final_df = pd.concat(
                        [self.final_df, tmp_df], ignore_index=True
                    )

            return True
        else:
            return False

    # def visit_slot(self, aliased_slot_name: str, slot: SlotDefinition) -> None:
    #     slot_as_dict = slot._as_dict
    #     print(slot_as_dict)

    # def visit_type(self, typ: TypeDefinition) -> None:
    #     type_as_dict = typ._as_dict
    #     print(type_as_dict)

    # def visit_enum(self, enum: EnumDefinition) -> None:
    #     enum_as_dict = enum._as_dict
    #     print(enum_as_dict)

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

        with open(self.output_file, "w") as sssom_tsv:
            for k, v in metadata.items():
                if k != "curie_map":
                    sssom_tsv.write("#" + k + ": " + v + "\n")
                else:
                    v: dict
                    sssom_tsv.write("#" + k + ": \n")
                    for pref, uri in v.items():
                        sssom_tsv.write("# " + pref + ": " + uri + "\n")
        self.final_df.to_csv(self.output_file, sep="\t", index=None, mode="a")


@shared_arguments(SSSOMGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
def cli(yamlfile, **kwargs):
    """Generate SSSOM TSV to represent a LinkML model"""
    print(SSSOMGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
