import yaml
from typing import Union
from pydantic import BaseModel

from linkml_runtime.dumpers.dumper_root import Dumper
from linkml_runtime.utils.formatutils import remove_empty_items
from linkml_runtime.utils.yamlutils import YAMLRoot

class YAMLDumper(Dumper):

    def dumps(self, element: Union[BaseModel, YAMLRoot], **kwargs) -> str:
        """ Return element formatted as a YAML string """
        # Internal note: remove_empty_items will also convert Decimals to int/float;
        # this is necessary until https://github.com/yaml/pyyaml/pull/372 is merged

        dumper_safe_element = element.model_dump() if isinstance(element, BaseModel) else element
        return yaml.dump(remove_empty_items(dumper_safe_element, hide_protected_keys=True),
                         Dumper=yaml.SafeDumper, sort_keys=False, 
                         allow_unicode=True,
                         **kwargs)
