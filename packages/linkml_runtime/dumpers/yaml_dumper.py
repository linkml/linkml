import yaml

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot


class YAMLDumper(Dumper):

    def dumps(self, element: YAMLRoot, **kwargs) -> str:
        """ Return element formatted as a YAML string """
        return yaml.dump(remove_empty_items(element, hide_protected_keys=True),
                                            Dumper=yaml.SafeDumper, sort_keys=False, **kwargs)
