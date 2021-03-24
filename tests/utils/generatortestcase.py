import os
import re
from typing import Optional, Callable

from rdflib import Graph, Namespace, OWL

from linkml import METAMODEL_NAMESPACE
from linkml.utils.generator import Generator
from tests import DEFAULT_LOG_LEVEL
from tests.utils.test_environment import TestEnvironment, TestEnvironmentTestCase

BIOLINK_NS = Namespace("https://w3id.org/biolink/vocab/")


class GeneratorTestCase(TestEnvironmentTestCase):
    model_name: str = None              # yaml name (sans '.yaml')

    @staticmethod
    def _print_triples(g: Graph):
        """ Pretty print the contents of g, removing the prefix declarations """
        g.bind('BIOLINK', BIOLINK_NS)
        g.bind('meta', METAMODEL_NAMESPACE)
        g.bind('owl', OWL)
        g_text = re.sub(r'@prefix.*\n', '', g.serialize(format="turtle").decode())
        print(g_text)

    def single_file_generator(self,
                              suffix: str,
                              gen: type(Generator), *,
                              subdir: Optional[str] = None,
                              format: Optional[str] = None,
                              generator_args: Optional[dict] = None,
                              serialize_args: Optional[dict] = None,
                              filtr: Optional[Callable[[str], str]] = None,
                              comparator: Callable[[str, str], str] = None,
                              output_name: Optional[str] = None,
                              yaml_file: Optional[str] = None) -> None:
        """ Invoke generator specified in gen

        :param env: Input environment
        :param suffix: File suffix (without '.')
        :param gen: Generator to invoke
        :param format: Generator format argument
        :param subdir: subdirectory within output directory (for includes processing)
        :param generator_args: Additional arguments to the generator
        :param serialize_args: Arguments to serializer.
        :param filtr: Filter to remove metadata specific info from the output.  Default: identity
        :param comparator: Comparison method to use.  Default: GeneratorTestCase._default_comparator
        :param output_name: If present, output base is output name instead of model_name.
        :param yaml_file: File to use for input instead of env.input_path
        """
        if serialize_args is None:
            serialize_args = {}
        if generator_args is None:
            generator_args = {}
        if format:
            generator_args["format"] = format
        if self.env.import_map is not None and 'importmap' not in generator_args:
            generator_args['importmap'] = self.env.import_map
        generator_args['log_level'] = DEFAULT_LOG_LEVEL
        yaml_file = yaml_file or self.env.input_path(subdir or '', self.model_name + '.yaml')

        self.env.generate_single_file([subdir or '', (output_name or self.model_name) + '.' + suffix],
                                      lambda: gen(yaml_file, **generator_args).serialize(**serialize_args),
                                      filtr=filtr, comparator=comparator, value_is_returned=True)

    def directory_generator(self,
                            dirname: str,
                            gen: type(Generator), *,
                            subdir: Optional[str] = None,
                            generator_args: Optional[dict] = None,
                            serialize_args: Optional[dict] = None,
                            input_file: Optional[str] = None) -> None:
        """
        Generate an output directory using the appropriate command and then compare the target with the source
        :param dirname: name of output directory (e.g. gengraphviz)
        :param gen: generator to use
        :param subdir: subdirectory within output directory (for includes processing)
        :param generator_args: arguments to the generator constructor
        :param serialize_args: arguments to the generator serializer
        :param input_file: File to use instead of self.model_name if present
        """
        if serialize_args is None:
            serialize_args = {}
        else:
            serialize_args = dict(serialize_args)
        if generator_args is None:
            generator_args = {}
        else:
            generator_args = dict(generator_args)           # Make a copy so we don't damage the original
        if self.env.import_map is not None and 'importmap' not in generator_args:
            generator_args['importmap'] = self.env.import_map
        generator_args['log_level'] = DEFAULT_LOG_LEVEL
        yaml_file = input_file or self.env.input_path(subdir, self.model_name + '.yaml')

        def call_generator(outdir: str) -> None:
            generator_args['directory'] = outdir
            serialize_args['directory'] = outdir
            gen(yaml_file, **generator_args).serialize(**serialize_args)

        self.env.generate_directory(dirname, lambda outdir: call_generator(outdir))
