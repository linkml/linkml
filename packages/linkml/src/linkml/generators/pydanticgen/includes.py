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
def _coerce_keyed_collection(value: Any, key_name: str, value_name: str | None = None) -> Any:
    """
    Normalize the input forms of a multivalued, inlined-as-dict slot to a dict
    of dicts, injecting the dict key into each value's key/identifier slot
    (``key_name``). A scalar entry value is assigned to ``value_name`` when
    given (the positional second-slot semantics of the dataclass metamodel,
    e.g. ``annotations: {tag: v}`` or ``prefixes: {pfx: url}``). Mirrors the
    normalization YAMLRoot performs for the equivalent dataclass models.
    """
    if isinstance(value, str):
        return {value: {key_name: value}}
    if isinstance(value, dict):
        if key_name in value and isinstance(value[key_name], (str, int, float)) and not isinstance(value[key_name], bool):
            # flat single-object form, e.g. annotations: {tag: t, value: v} --
            # only when the key field holds a scalar (a None/dict body means an
            # entry whose dict key happens to equal the key slot's name)
            return {value[key_name]: dict(value)}
        out = {}
        for key, item in value.items():
            if not isinstance(key, str):
                key = str(key)
            if item is None:
                out[key] = {key_name: key}
            elif isinstance(item, dict):
                if key_name not in item:
                    out[key] = {key_name: key, **item}
                elif item[key_name] != key:
                    raise ValueError(f"{key_name} mismatch: dict key {key!r} != {item[key_name]!r}")
                else:
                    out[key] = item
            elif value_name is not None and isinstance(item, (str, int, float, bool)):
                # simple form: dict key + scalar value, e.g. prefixes: {pfx: url}
                out[key] = {key_name: key, value_name: item}
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

InlinedListCoercion = '''
def _coerce_inlined_list(value: Any, key_name: str) -> Any:
    """
    Normalize the input forms of a multivalued slot inlined as a list of
    objects: a dict keyed by ``key_name`` (the identifier/key slot of the
    range class, or its first required slot) becomes a list with the keys
    injected, and a single object is wrapped into a singleton list. Mirrors
    the normalization YAMLRoot performs for the equivalent dataclass models.
    """
    if value is None or isinstance(value, list):
        return value
    if isinstance(value, dict):
        if key_name in value and isinstance(value[key_name], (str, int, float)) and not isinstance(value[key_name], bool):
            # flat single-object form, e.g. structured_aliases: {literal_form: x, ...}
            return [value]
        out = []
        for key, item in value.items():
            if item is None:
                out.append({key_name: key})
            elif isinstance(item, dict) and key_name not in item:
                out.append({key_name: key, **item})
            else:
                out.append(item)
        return out
    return [value]

'''
