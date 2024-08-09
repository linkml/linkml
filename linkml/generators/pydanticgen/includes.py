"""
Classes to inject in generated pydantic models
"""

from linkml.generators.pydanticgen.template import Import, ObjectImport

LinkMLMeta = """
class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
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


unnest_identifier = """    @field_validator("*", mode="before")
    @classmethod
    def _unnest_identifier(cls, val: Any, info: ValidationInfo):
        \"\"\"
        If a slot is inlined as a dict/simple dict, and is being passed to us with without the value
        of that slot set, fill it in from the key (field name)
    
        eg if we have a field like
    
        ``field_name: Dict[str, IDClass]``
    
        and are given
    
        ``{'id_value': {'some_other_value': 'who_knows'}}``
    
        and there is some required identifier/key slot ``id_slot``, we return
    
        ``{'id_value': {'id_slot': 'id_value', 'some_other_value': 'who_knows'}}``
        \"\"\"
        if (
                identifier_slot := getattr(cls.model_fields[info.field_name], "json_schema_extra")
                        .get("linkml_meta", {})
                        .get("identifier_slot", None)
        ) is not None:
            if isinstance(val, dict):
                for key, inner_val in val.items():
                    if not isinstance(inner_val, dict):
                        continue
                    if identifier_slot not in inner_val:
                        inner_val[identifier_slot] = key
        return val
"""
unnest_identifier_imports = [Import(module="pydantic", objects=[ObjectImport(name="ValidationInfo")])]
