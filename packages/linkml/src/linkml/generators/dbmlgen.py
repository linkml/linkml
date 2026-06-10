import logging

import click

from linkml.utils.generator import Generator
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView


def _map_range_to_dbml_type(range_name: str) -> str:
    """
    Map LinkML range types to DBML types.

    :param range_name: LinkML range name
    :return: Corresponding DBML type
    """
    type_mapping = {
        "string": "varchar",
        "integer": "int",
        "float": "float",
        "boolean": "boolean",
        "date": "date",
        "datetime": "datetime",
    }
    return type_mapping.get(range_name, "varchar")  # Default to varchar


class DBMLGenerator(Generator):
    """
    A generator for converting a LinkML schema into DBML (Database Markup Language).
    """

    generatorname = "dbmlgen"
    generatorversion = "0.2.0"
    valid_formats = ["dbml"]

    def __post_init__(self) -> None:
        super().__post_init__()
        self.logger = logging.getLogger(__name__)
        # ``SchemaLoader.resolve()`` strips ``schema.source_file`` to a basename,
        # so a fresh ``SchemaView(self.schema)`` would later (during lazy
        # ``load_import``) fall back to ``os.getcwd()`` when resolving sibling-
        # relative imports. Build the view from the original schema location
        # (preserved on ``self.schema_location``) when it's available so
        # ``SchemaView`` sees a real path and can resolve imports correctly.
        if self.schema_location:
            self.schemaview = SchemaView(self.schema_location, base_dir=self.base_dir, importmap=self.importmap)
        else:
            self.schemaview = SchemaView(self.schema, base_dir=self.base_dir, importmap=self.importmap)

    def serialize(self) -> str:
        """
        Generate DBML representation of the LinkML schema.

        :return: DBML as a string
        """
        dbml_lines = [
            "// DBML generated from LinkML schema\n",
            f"Project {{\n  name: '{self.schemaview.schema.name}'\n}}\n",
        ]

        for class_name, class_def in self.schemaview.all_classes().items():
            dbml_lines.append(self._generate_table(class_name, class_def))

        # Generate relationships if applicable
        relationships = self._generate_relationships()
        if relationships:
            dbml_lines.append(relationships)

        return "\n".join(dbml_lines)

    def _generate_table(self, class_name: str, class_def) -> str:
        """
        Generate the DBML for a single class (table).

        :param class_name: Name of the class
        :param class_def: ClassDefinition object
        :return: DBML representation of the class
        """
        dbml = [f"Table {camelcase(class_name)} {{"]

        # ``class_induced_slots`` already returns slot definitions with
        # inherited and inferred metadata applied (e.g. ``identifier=True``
        # implies ``required=True``). Use the induced slot directly rather than
        # re-fetching the raw slot via ``get_slot`` — that fetch would discard
        # the inferred attributes the column generator depends on.
        for induced_slot in self.schemaview.class_induced_slots(class_name):
            dbml.append(self._generate_column(induced_slot))

        dbml.append("}\n")
        return "\n".join(dbml)

    def _generate_column(self, slot) -> str:
        """
        Generate the DBML for a single slot (column).

        :param slot: SlotDefinition object
        :return: DBML representation of the column
        """
        column_name = slot.name
        data_type = _map_range_to_dbml_type(slot.range or "string")
        constraints = []
        constraints_str = ""

        if slot.required:
            constraints.append("not null")
        if slot.identifier:
            constraints.append("primary key")

        if constraints:
            constraints_str = f"{', '.join(constraints)}"
            constraints_str = "[" + constraints_str + "]"

        return f"  {underscore(column_name)} {data_type} {constraints_str}".strip()

    def _generate_relationships(self) -> str:
        """
        Generate DBML relationships based on slot ranges referencing other classes.

        :return: DBML representation of relationships
        """
        relationships = []
        for class_name, class_def in self.schemaview.all_classes().items():
            # Use induced slots directly so inferred attributes (e.g. range)
            # are honored; see ``_generate_table`` for the same reasoning.
            for slot in self.schemaview.class_induced_slots(class_name):
                # Check if the slot references another class
                if slot.range in self.schemaview.all_classes():
                    # Find the identifier slot of the referenced class
                    identifier_slot_name = next(
                        (
                            target_slot.name
                            for target_slot in self.schemaview.class_induced_slots(slot.range)
                            if target_slot.identifier
                        ),
                        None,
                    )

                    if identifier_slot_name is None:
                        # Inlined / embedded references — where the referenced
                        # class has no identifier — are a legitimate LinkML
                        # pattern. DBML supports them: the foreign-key column
                        # simply has no ``Ref:`` line. Skip rather than raise.
                        self.logger.debug(
                            "Skipping DBML relationship for %s.%s -> %s: referenced class has no identifier slot.",
                            class_name,
                            slot.name,
                            slot.range,
                        )
                        continue

                    # Generate the DBML relationship
                    relationships.append(
                        f"Ref: {camelcase(class_name)}.{underscore(slot.name)} > "
                        f"{camelcase(slot.range)}.{underscore(identifier_slot_name)}"
                    )
        return "\n".join(relationships)


# CLI Definition
@click.command()
@click.option(
    "--schema",
    "-s",
    required=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="Path to the LinkML schema YAML file",
)
@click.option(
    "--output",
    "-o",
    required=False,
    type=click.Path(dir_okay=False, writable=True),
    help="Path to save the generated DBML file. If not specified, DBML will be printed to stdout.",
)
def cli(schema, output):
    """
    CLI for LinkML to DBML generator.
    """
    generator = DBMLGenerator(schema)

    # Generate the DBML
    dbml_output = generator.serialize()

    # Save to file or print to stdout
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(dbml_output)
        click.echo(f"DBML has been saved to {output}")
    else:
        click.echo(dbml_output)


if __name__ == "__main__":
    cli()
