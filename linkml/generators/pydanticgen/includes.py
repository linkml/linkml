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
