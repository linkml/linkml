import yaml

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.yamlutils import YAMLRoot


class YAMLDumper(Dumper):

    def dumps(self, element: YAMLRoot, **kwargs) -> str:
        """ Return element formatted as a YAML string """
        return yaml.dump(element, Dumper=yaml.SafeDumper, sort_keys=False, **kwargs)
