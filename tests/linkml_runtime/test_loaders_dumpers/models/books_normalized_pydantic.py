from __future__ import annotations

from enum import Enum

from pydantic import BaseModel as BaseModel
from pydantic import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(WeakRefShimBaseModel):
    __signature__ = {
        "validate_assignment": True,
        "validate_all": True,
        "underscore_attrs_are_private": True,
        "extra": "forbid",
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }


class GenreEnum(str, Enum):
    scifi = "scifi"
    fantasy = "fantasy"
    western = "western"
    romance = "romance"
    modern = "modern"


class CreativeWork(ConfiguredBaseModel):
    id: str | None = Field(None)
    name: str | None = Field(None)
    genres: list[GenreEnum] | None = Field(default_factory=list)
    creator: Author | None = Field(None)
    summary: str | None = Field(None)
    reviews: list[Review] | None = Field(default_factory=list)


class Book(CreativeWork):
    price: float | None = Field(None)
    inStock: str | None = Field(None)
    id: str | None = Field(None)
    name: str | None = Field(None)
    genres: list[GenreEnum] | None = Field(default_factory=list)
    creator: Author | None = Field(None)
    summary: str | None = Field(None)
    reviews: list[Review] | None = Field(default_factory=list)


class BookSeries(CreativeWork):
    books: list[Book] | None = Field(default_factory=list)
    genres: list[GenreEnum] | None = Field(default_factory=list)
    price: float | None = Field(None)
    id: str | None = Field(None)
    name: str | None = Field(None)
    creator: Author | None = Field(None)
    summary: str | None = Field(None)
    reviews: list[Review] | None = Field(default_factory=list)


class Author(ConfiguredBaseModel):
    name: str | None = Field(None)
    genres: list[GenreEnum] | None = Field(default_factory=list)
    from_country: str | None = Field(None)


class Shop(ConfiguredBaseModel):
    all_book_series: list[BookSeries] | None = Field(default_factory=list)


class Country(ConfiguredBaseModel):
    name: str | None = Field(None)


class Review(ConfiguredBaseModel):
    creator: Author | None = Field(None)
    rating: int | None = Field(None)
    review_text: str | None = Field(None)


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
CreativeWork.update_forward_refs()
Book.update_forward_refs()
BookSeries.update_forward_refs()
Author.update_forward_refs()
Shop.update_forward_refs()
Country.update_forward_refs()
Review.update_forward_refs()
