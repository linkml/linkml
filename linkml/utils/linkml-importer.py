import click
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView


@click.command()
@click.argument('schema',
                type=click.Path(exists=True),
                help="the path of the existing schema file")
@click.argument('import_schema_name',
                type=click.Path(exists=True),
                help="name of the schema file in the same directory as the existing schema, to import")
@click.argument('output',
                type=click.Path(),
                required=True,
                help="the path of the output schema file")
def import_schema(schema, import_schema_name, output_schema_path):
    """
    This script imports a new LinkML schema into an existing schema and saves the merged schema.
    """
    # Load the existing schema
    existing_schema = SchemaView(yaml_loader.load(schema, target_class=None))
    try:
        plus_import = existing_schema.load_import(import_schema_name)
    except Exception as e:
        raise click.ClickException(f"Error loading import: {e}")

    yaml_dumper.dump(plus_import, output_schema_path, sort_keys=False)
    click.echo(f"Merged schema saved to {output_schema_path}")


if __name__ == "__main__":
    import_schema()
