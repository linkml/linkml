"""
Classes to inject in generated pydantic models
"""

from pydantic.version import VERSION

PYDANTIC_VERSION = int(VERSION[0])


LinkMLMeta_v1 = """
class LinkMLMeta(BaseModel):
    __root__: Dict[str, Any] = {}
    
    def __getattr__(self, key:str):
        return getattr(self.__root__, key)
        
    def __getitem__(self, key:str):
        return self.__root__[key]
    
    def __setitem__(self, key:str, value):
        self.__root__[key] = value
        
    def __contains__(self, key:str) -> bool:
        return key in self.__root__
   
    class Config:
        allow_mutation = False
"""

LinkMLMeta_v2 = """
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

# if PYDANTIC_VERSION >= 2:
#     LinkMLMeta = eval(LinkMLMeta_v2)
# else:
#     LinkMLMeta = eval(LinkMLMeta_v1)
