from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from typing_extensions import Literal
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


class GenreEnum(str, Enum):
    
    scifi = "scifi"
    fantasy = "fantasy"
    western = "western"
    romance = "romance"
    modern = "modern"
    
    

class CreativeWork(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    genres: Optional[List[GenreEnum]] = Field(default_factory=list)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[List[Review]] = Field(default_factory=list)
    


class Book(CreativeWork):
    
    price: Optional[float] = Field(None)
    inStock: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    genres: Optional[List[GenreEnum]] = Field(default_factory=list)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[List[Review]] = Field(default_factory=list)
    


class BookSeries(CreativeWork):
    
    books: Optional[List[Book]] = Field(default_factory=list)
    genres: Optional[List[GenreEnum]] = Field(default_factory=list)
    price: Optional[float] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[List[Review]] = Field(default_factory=list)
    


class Author(ConfiguredBaseModel):
    
    name: Optional[str] = Field(None)
    genres: Optional[List[GenreEnum]] = Field(default_factory=list)
    from_country: Optional[str] = Field(None)
    


class Shop(ConfiguredBaseModel):
    
    all_book_series: Optional[List[BookSeries]] = Field(default_factory=list)
    


class Country(ConfiguredBaseModel):
    
    name: Optional[str] = Field(None)
    


class Review(ConfiguredBaseModel):
    
    creator: Optional[Author] = Field(None)
    rating: Optional[int] = Field(None)
    review_text: Optional[str] = Field(None)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
CreativeWork.update_forward_refs()
Book.update_forward_refs()
BookSeries.update_forward_refs()
Author.update_forward_refs()
Shop.update_forward_refs()
Country.update_forward_refs()
Review.update_forward_refs()

