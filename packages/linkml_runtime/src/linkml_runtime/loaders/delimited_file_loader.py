import json
from abc import ABC, abstractmethod
from typing import Union

from json_flattener import GlobalConfig, KeyConfig, unflatten_from_csv
from pydantic import BaseModel

from linkml_runtime.linkml_model.meta import SchemaDefinition, SlotDefinitionName
from linkml_runtime.loaders.json_loader import JSONLoader
from linkml_runtime.loaders.loader_root import Loader
from linkml_runtime.utils.csvutils import get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot


def _get_list_config_from_annotations(
    schemaview: SchemaView,
    index_slot: SlotDefinitionName = None,
) -> tuple[tuple[str, str], str, bool]:
    """
    Read list_syntax, list_delimiter, and list_strip_whitespace from schema-level annotations.

    These annotations control how multivalued fields are serialized in CSV/TSV:
    - list_syntax: "python" (default) uses brackets [a|b|c], "plaintext" has no brackets
    - list_delimiter: character between list items (default "|")
    - list_strip_whitespace: strip whitespace around delimiter (default true)

    Note: These are schema-level only because json-flattener's GlobalConfig
    applies the same markers/delimiter to ALL columns in the CSV/TSV.

    Returns:
        Tuple of (csv_list_markers, csv_inner_delimiter, strip_whitespace) for GlobalConfig.
        - csv_list_markers: ('[', ']') for python style, ('', '') for plaintext
        - csv_inner_delimiter: the delimiter between list items (default '|')
        - strip_whitespace: whether to strip whitespace from list items (default True)
    """
    # Default values matching json-flattener defaults
    list_markers = ("[", "]")
    inner_delimiter = "|"
    strip_whitespace = True  # Default to stripping whitespace

    if not schemaview or not schemaview.schema:
        return list_markers, inner_delimiter, strip_whitespace

    # Check schema-level annotations
    if schemaview.schema.annotations:
        annotations = schemaview.schema.annotations
        if "list_syntax" in annotations:
            syntax = annotations["list_syntax"].value
            if syntax == "plaintext":
                list_markers = ("", "")
        if "list_delimiter" in annotations:
            inner_delimiter = annotations["list_delimiter"].value
        if "list_strip_whitespace" in annotations:
            value = annotations["list_strip_whitespace"].value
            # Handle string "false" or boolean False
            strip_whitespace = str(value).lower() not in ("false", "no", "0")

    return list_markers, inner_delimiter, strip_whitespace


def _strip_whitespace_from_lists(obj: Union[dict, list]) -> Union[dict, list]:
    """
    Recursively strip whitespace from string items in lists.

    This post-processes the unflattened data to strip leading/trailing
    whitespace from list items, handling cases like "a | b | c" being
    parsed as ['a ', ' b ', ' c'].

    Args:
        obj: A dict or list from json-flattener unflatten

    Returns:
        The same structure with whitespace stripped from list string items
    """
    if isinstance(obj, dict):
        return {k: _strip_whitespace_from_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        result = []
        for item in obj:
            if isinstance(item, str):
                result.append(item.strip())
            elif isinstance(item, (dict, list)):
                result.append(_strip_whitespace_from_lists(item))
            else:
                result.append(item)
        return result
    else:
        return obj


def _enhance_configmap_for_multivalued_primitives(
    schemaview: SchemaView,
    index_slot: SlotDefinitionName,
    configmap: dict,
    plaintext_mode: bool = False,
) -> dict:
    """
    Enhance configmap with KeyConfig entries for multivalued primitive slots.

    The base get_configmap() only creates KeyConfig for class-ranged inlined slots.
    This function adds KeyConfig(is_list=True) for multivalued primitive slots
    (like aliases: string*) so json-flattener knows to split/join on delimiter.

    Note: KeyConfig(is_list=True) is only added in plaintext mode because:
    - In python mode ([a|b|c]), json-flattener already parses brackets correctly
    - In plaintext mode (a|b|c), we need KeyConfig to tell json-flattener to split

    Args:
        schemaview: The schema view
        index_slot: The slot that indexes the top-level objects
        configmap: The existing configmap from get_configmap()
        plaintext_mode: If True, add KeyConfig for plaintext list parsing

    Returns:
        Enhanced configmap with entries for multivalued primitive slots
    """
    # Only enhance in plaintext mode - python mode works without KeyConfig
    if not plaintext_mode:
        return configmap

    if schemaview is None or index_slot is None:
        return configmap

    slot = schemaview.get_slot(index_slot)
    if slot is None or slot.range is None:
        return configmap

    # Get the class that the index slot points to
    target_class = slot.range
    if target_class not in schemaview.all_classes():
        return configmap

    # Get all classes for type checking
    all_classes = schemaview.all_classes()

    # Check each slot in the target class for multivalued slots
    for slot_name in schemaview.class_slots(target_class):
        # Skip if already in configmap (handled by get_configmap)
        if slot_name in configmap:
            continue

        induced_slot = schemaview.induced_slot(slot_name, target_class)
        if induced_slot.multivalued:
            slot_range = induced_slot.range
            # Add KeyConfig for any non-class range (primitives AND enums)
            # In plaintext mode, all multivalued fields need explicit parsing
            if slot_range not in all_classes:
                configmap[slot_name] = KeyConfig(is_list=True)

    return configmap


class DelimitedFileLoader(Loader, ABC):
    @property
    @abstractmethod
    def delimiter(self):
        pass

    def load_as_dict(
        self,
        source: str,
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> Union[dict, list[dict]]:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().load_as_dict(json_str)

    def load_any(self, *args, **kwargs) -> Union[YAMLRoot, list[YAMLRoot]]:
        return self.load(*args, **kwargs)

    def loads(
        self,
        input,
        target_class: type[Union[BaseModel, YAMLRoot]],
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> str:
        json_str = self._get_json_str_to_load(input, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def load(
        self,
        source: str,
        target_class: type[Union[BaseModel, YAMLRoot]],
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        **kwargs,
    ) -> str:
        json_str = self._get_json_str_to_load(source, index_slot, schema, schemaview, **kwargs)
        return JSONLoader().loads(json_str, target_class=target_class)

    def _get_json_str_to_load(
        self,
        input,
        index_slot: SlotDefinitionName = None,
        schema: SchemaDefinition = None,
        schemaview: SchemaView = None,
        list_syntax: str = None,
        list_delimiter: str = None,
        list_strip_whitespace: bool = None,
        **kwargs,
    ):
        if schemaview is None:
            schemaview = SchemaView(schema)

        # Read list configuration from schema annotations
        list_markers, inner_delimiter, strip_whitespace = _get_list_config_from_annotations(schemaview, index_slot)

        # CLI options override schema annotations
        if list_syntax is not None:
            list_markers = ("", "") if list_syntax == "plaintext" else ("[", "]")
        if list_delimiter is not None:
            inner_delimiter = list_delimiter
        if list_strip_whitespace is not None:
            strip_whitespace = list_strip_whitespace

        # Plaintext mode means no brackets around lists (e.g., a|b|c instead of [a|b|c])
        plaintext_mode = list_markers == ("", "")

        # Get base configmap and enhance with multivalued primitive slots
        configmap = get_configmap(schemaview, index_slot)
        configmap = _enhance_configmap_for_multivalued_primitives(
            schemaview, index_slot, configmap, plaintext_mode=plaintext_mode
        )

        config = GlobalConfig(
            key_configs=configmap,
            csv_delimiter=self.delimiter,
            csv_list_markers=list_markers,
            csv_inner_delimiter=inner_delimiter,
        )
        objs = unflatten_from_csv(input, config=config, **kwargs)

        # Strip whitespace from list items if enabled (default)
        if strip_whitespace:
            objs = [_strip_whitespace_from_lists(obj) for obj in objs]

        return json.dumps({index_slot: objs})
