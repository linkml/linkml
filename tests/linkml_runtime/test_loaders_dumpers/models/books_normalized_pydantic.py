from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel as BaseModel, Field

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel):
    __signature__ = {
        "validate_assignment": True,
        "validate_all": True,
        "underscore_attrs_are_private": True,
        "extra": 'forbid',
        "arbitrary_types_allowed": True,
        "use_enum_values": True
    }


class GenreEnum(str, Enum):
    
    scifi = "scifi"
    fantasy = "fantasy"
    western = "western"
    romance = "romance"
    modern = "modern"
    
    

class CreativeWork(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    genres: Optional[list[GenreEnum]] = Field(default_factory=list)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[list[Review]] = Field(default_factory=list)
    


class Book(CreativeWork):
    
    price: Optional[float] = Field(None)
    inStock: Optional[str] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    genres: Optional[list[GenreEnum]] = Field(default_factory=list)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[list[Review]] = Field(default_factory=list)
    


class BookSeries(CreativeWork):
    
    books: Optional[list[Book]] = Field(default_factory=list)
    genres: Optional[list[GenreEnum]] = Field(default_factory=list)
    price: Optional[float] = Field(None)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    creator: Optional[Author] = Field(None)
    summary: Optional[str] = Field(None)
    reviews: Optional[list[Review]] = Field(default_factory=list)
    


class Author(ConfiguredBaseModel):
    
    name: Optional[str] = Field(None)
    genres: Optional[list[GenreEnum]] = Field(default_factory=list)
    from_country: Optional[str] = Field(None)
    


class Shop(ConfiguredBaseModel):
    
    all_book_series: Optional[list[BookSeries]] = Field(default_factory=list)
    


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

