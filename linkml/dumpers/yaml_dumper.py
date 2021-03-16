import yaml
from linkml.utils.yamlutils import YAMLRoot


def dump(element: YAMLRoot, to_file: str) -> None:
    """ Emit element to to_file """
    with open(to_file, 'w') as outf:
        outf.write(dumps(element))


def dumps(element: YAMLRoot) -> str:
    """ Return element formatted as a YAML string """
    return yaml.dump(element, Dumper=yaml.SafeDumper, sort_keys=False)
