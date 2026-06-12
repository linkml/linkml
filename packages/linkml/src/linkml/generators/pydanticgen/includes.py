"""
Classes to inject in generated pydantic models
"""

LinkMLMeta = """
class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root

"""

KeyedCollectionCoercion = '''
def _coerce_keyed_collection(value: Any, key_name: str) -> Any:
    """
    Normalize the input forms of a multivalued, inlined-as-dict slot to a dict
    of dicts, injecting the dict key into each value's key/identifier slot
    (``key_name``). Mirrors the normalization YAMLRoot performs for the
    equivalent dataclass models.
    """
    if isinstance(value, str):
        return {value: {key_name: value}}
    if isinstance(value, dict):
        if key_name in value and not isinstance(value[key_name], (dict, list)):
            # flat single-object form, e.g. annotations: {tag: t, value: v}
            return {value[key_name]: dict(value)}
        out = {}
        for key, item in value.items():
            if item is None:
                out[key] = {key_name: key}
            elif isinstance(item, dict):
                if key_name not in item:
                    out[key] = {key_name: key, **item}
                elif item[key_name] != key:
                    raise ValueError(f"{key_name} mismatch: dict key {key!r} != {item[key_name]!r}")
                else:
                    out[key] = item
            else:
                out[key] = item
        return out
    if isinstance(value, list):
        out = {}
        for item in value:
            if isinstance(item, dict):
                if key_name not in item:
                    raise ValueError(f"Missing {key_name} in list item {item!r}")
                out[item[key_name]] = item
            elif isinstance(item, (str, int, float)):
                out[item] = {key_name: item}
            elif hasattr(item, key_name):
                out[getattr(item, key_name)] = item
            else:
                raise ValueError(f"Cannot key list item {item!r} by {key_name}")
        return out
    return value

'''
