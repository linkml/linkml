import click
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.utils.schemaview import SchemaView


@click.command()
@click.option('--schema',
              help="the path of the existing schema file")
@click.option('--import_schema_name',
              help="name of the schema file in the same directory as the existing schema, to import")
@click.option('--output',
              type=click.Path(),
              required=True,
              help="the path of the output schema file")
def cli(schema, import_schema_name, output_schema_path):
    """
    This script imports a new LinkML schema into an existing schema and saves the merged schema.
    """
    # Load the existing schema
    click.echo("can you see this?")
    click.echo(output_schema_path)
    existing_schema = SchemaView(yaml_loader.load(schema, target_class=None))
    plus_import = existing_schema.load_import(import_schema_name)

    yaml_dumper.dump(plus_import, output_schema_path, sort_keys=False)
    click.echo(f"Merged schema saved to {output_schema_path}")


if __name__ == "__main__":
    cli()
