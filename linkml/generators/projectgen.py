import os
from pathlib import Path
from typing import Union, Dict, List, Any
from functools import lru_cache
from dataclasses import dataclass, field

import click
import yaml

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, lcamelcase
from linkml.utils.generator import Generator, shared_arguments

from linkml.generators.graphqlgen import GraphqlGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonldgen import JSONLDGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.prefixmapgen import PrefixGenerator
from linkml.generators.protogen import ProtoGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.rdfgen import RDFGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.sqlddlgen import SQLDDLGenerator

GEN_MAP = {
    'graphql': (GraphqlGenerator, 'graphql/{name}.graphql', {}),
    'jsonldcontext': (ContextGenerator, 'jsonld/{name}.context.jsonld', {}),
    'jsonld': (JSONLDGenerator, 'jsonld/{name}.jsonld', {'context': '{parent}/{name}.context.jsonld'}),
    'jsonschema': (JsonSchemaGenerator, 'jsonschema/{name}.schema.json', {}),
    'markdown': (MarkdownGenerator, 'docs/',
                 {'directory': '{parent}',
                  'index_file': '{name}.md'}),
    'owl': (OwlSchemaGenerator, 'owl/{name}.owl.ttl', {}),
    'prefixmap': (PrefixGenerator, 'prefixmap/{name}.yaml', {}),
    'proto': (ProtoGenerator, 'protobuf/{name}.proto', {}),
    'python': (PythonGenerator, '{name}.py', {}),
#    'rdf': (RDFGenerator, 'rdf/{name}.ttl', {}),
#    'rdf': (RDFGenerator, 'rdf/{name}.ttl', {'context': '{parent}/../jsonld/{name}.context.jsonld'}),
    'shex': (ShExGenerator, 'shex/{name}.shexj', {}),
    'sqlddl': (SQLDDLGenerator, 'sqlschema/{name}.sql', {}),
}

@lru_cache()
def get_local_imports(schema_path: str, dir: str):
    print(f'GETTING IMPORTS = {schema_path}')
    all_imports = [schema_path]
    with open(schema_path) as stream:
        with open(schema_path) as stream:
            schema = yaml.safe_load(stream)
            for imp in schema.get('imports', []):
                imp_path = os.path.join(dir, imp) + '.yaml'
                print(f' IMP={imp} //  path={imp_path}')
                if os.path.isfile(imp_path):
                    all_imports += get_local_imports(imp_path, dir)
    return all_imports

@dataclass
class ProjectConfiguration:
    directory: str = 'tmp'
    generator_args: Dict[str, Any] = field(default_factory=lambda: {})

class ProjectGenerator:

    def generate(self, schema_path: str, config: ProjectConfiguration = ProjectConfiguration()):
        Path(config.directory).mkdir(parents=True, exist_ok=True)
        all_schemas = get_local_imports(schema_path, os.path.dirname(schema_path))
        print(f'ALL_SCHEMAS = {all_schemas}')
        for gen_name, (gen_cls, gen_path_fmt, gen_args) in GEN_MAP.items():
            print(f'GEN: {gen_name}')
            for local_path in all_schemas:
                print(f' SCHEMA: {local_path}')
                name = os.path.basename(local_path).replace('.yaml', '')
                gen_path = gen_path_fmt.format(name=name)
                gen_path_full = f'{config.directory}/{gen_path}'
                parts = gen_path_full.split('/')
                parent_dir = '/'.join(parts[0:-1])
                print(f' PARENT={parent_dir}')
                Path(parent_dir).mkdir(parents=True, exist_ok=True)
                gen_path_full = '/'.join(parts)

                gen: Generator
                gen = gen_cls(local_path)
                serialize_args = {'mergeimports': False}
                for k, v in {**gen_args, **config.generator_args.get(gen_name, {})}.items():
                    serialize_args[k] = v.format(name=name, parent=parent_dir)
                print(f' ARGS: {serialize_args}')
                gen_dump = gen.serialize(**serialize_args)
                if parts[-1] != '':
                    # markdowngen does not write to a file
                    print(f'  WRITING TO: {gen_path_full}')
                    with open(gen_path_full, 'w') as stream:
                        stream.write(gen_dump)

@click.command()
@click.option("--dir", "-d",
              help="directory in which to place generated files. E.g. linkml_model, biolink_model")
@click.argument('yamlfile')
def cli(yamlfile, dir, **kwargs):
    """ Generate JSONLD file from biolink schema """
    config = ProjectConfiguration()
    config.directory = dir
    gen = ProjectGenerator()
    gen.generate(yamlfile, config)


if __name__ == '__main__':
    cli()





