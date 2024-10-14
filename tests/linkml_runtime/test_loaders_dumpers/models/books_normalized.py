# Auto generated from books_normalized.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-09-10 16:59
# Schema: example
#
# id: https://w3id.org/example
# description: example
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from jsonasobj2 import as_dict
from typing import Optional, Union, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace

metamodel_version = "1.7.0"

# Namespaces
EXAMPLE = CurieNamespace('example', 'https://w3id.org/example')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EXAMPLE


# Types

# Class references
class CreativeWorkId(extended_str):
    pass


class BookId(CreativeWorkId):
    pass


class BookSeriesId(CreativeWorkId):
    pass


class CountryName(extended_str):
    pass


@dataclass
class CreativeWork(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.CreativeWork
    class_class_curie: ClassVar[str] = "example:CreativeWork"
    class_name: ClassVar[str] = "creative work"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.CreativeWork

    id: Union[str, CreativeWorkId] = None
    name: Optional[str] = None
    genres: Optional[Union[Union[str, "GenreEnum"], list[Union[str, "GenreEnum"]]]] = empty_list()
    creator: Optional[Union[dict, "Author"]] = None
    summary: Optional[str] = None
    reviews: Optional[Union[Union[dict, "Review"], list[Union[dict, "Review"]]]] = empty_list()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CreativeWorkId):
            self.id = CreativeWorkId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.genres, list):
            self.genres = [self.genres] if self.genres is not None else []
        self.genres = [v if isinstance(v, GenreEnum) else GenreEnum(v) for v in self.genres]

        if self.creator is not None and not isinstance(self.creator, Author):
            self.creator = Author(**as_dict(self.creator))

        if not isinstance(self.genres, list):
            self.genres = [self.genres] if self.genres is not None else []
        self.genres = [v if isinstance(v, GenreEnum) else GenreEnum(v) for v in self.genres]

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        if not isinstance(self.reviews, list):
            self.reviews = [self.reviews] if self.reviews is not None else []
        self.reviews = [v if isinstance(v, Review) else Review(**as_dict(v)) for v in self.reviews]

        super().__post_init__(**kwargs)


@dataclass
class Book(CreativeWork):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.Book
    class_class_curie: ClassVar[str] = "example:Book"
    class_name: ClassVar[str] = "book"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.Book

    id: Union[str, BookId] = None
    price: Optional[float] = None
    inStock: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookId):
            self.id = BookId(self.id)

        if self.price is not None and not isinstance(self.price, float):
            self.price = float(self.price)

        if self.inStock is not None and not isinstance(self.inStock, str):
            self.inStock = str(self.inStock)

        super().__post_init__(**kwargs)


@dataclass
class BookSeries(CreativeWork):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.BookSeries
    class_class_curie: ClassVar[str] = "example:BookSeries"
    class_name: ClassVar[str] = "book series"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.BookSeries

    id: Union[str, BookSeriesId] = None
    books: Optional[Union[dict[Union[str, BookId], Union[dict, Book]], list[Union[dict, Book]]]] = empty_dict()
    genres: Optional[Union[Union[str, "GenreEnum"], list[Union[str, "GenreEnum"]]]] = empty_list()
    price: Optional[float] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookSeriesId):
            self.id = BookSeriesId(self.id)

        self._normalize_inlined_as_list(slot_name="books", slot_type=Book, key_name="id", keyed=True)

        if not isinstance(self.genres, list):
            self.genres = [self.genres] if self.genres is not None else []
        self.genres = [v if isinstance(v, GenreEnum) else GenreEnum(v) for v in self.genres]

        if self.price is not None and not isinstance(self.price, float):
            self.price = float(self.price)

        super().__post_init__(**kwargs)


@dataclass
class Author(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.Author
    class_class_curie: ClassVar[str] = "example:Author"
    class_name: ClassVar[str] = "author"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.Author

    name: Optional[str] = None
    genres: Optional[Union[Union[str, "GenreEnum"], list[Union[str, "GenreEnum"]]]] = empty_list()
    from_country: Optional[Union[str, CountryName]] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.genres, list):
            self.genres = [self.genres] if self.genres is not None else []
        self.genres = [v if isinstance(v, GenreEnum) else GenreEnum(v) for v in self.genres]

        if self.from_country is not None and not isinstance(self.from_country, CountryName):
            self.from_country = CountryName(self.from_country)

        super().__post_init__(**kwargs)


@dataclass
class Shop(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.Shop
    class_class_curie: ClassVar[str] = "example:Shop"
    class_name: ClassVar[str] = "shop"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.Shop

    all_book_series: Optional[Union[dict[Union[str, BookSeriesId], Union[dict, BookSeries]], list[Union[dict, BookSeries]]]] = empty_dict()

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="all_book_series", slot_type=BookSeries, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Country(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.Country
    class_class_curie: ClassVar[str] = "example:Country"
    class_name: ClassVar[str] = "country"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.Country

    name: Union[str, CountryName] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, CountryName):
            self.name = CountryName(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Review(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EXAMPLE.Review
    class_class_curie: ClassVar[str] = "example:Review"
    class_name: ClassVar[str] = "review"
    class_model_uri: ClassVar[URIRef] = EXAMPLE.Review

    creator: Optional[Union[dict, Author]] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None

    def __post_init__(self, *_: list[str], **kwargs: dict[str, Any]):
        if self.creator is not None and not isinstance(self.creator, Author):
            self.creator = Author(**as_dict(self.creator))

        if self.rating is not None and not isinstance(self.rating, int):
            self.rating = int(self.rating)

        if self.review_text is not None and not isinstance(self.review_text, str):
            self.review_text = str(self.review_text)

        super().__post_init__(**kwargs)


# Enumerations
class GenreEnum(EnumDefinitionImpl):

    scifi = PermissibleValue(text="scifi")
    fantasy = PermissibleValue(text="fantasy")
    western = PermissibleValue(text="western")
    romance = PermissibleValue(text="romance")
    modern = PermissibleValue(text="modern")

    _defn = EnumDefinition(
        name="GenreEnum",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=EXAMPLE.id, name="id", curie=EXAMPLE.curie('id'),
                   model_uri=EXAMPLE.id, domain=None, range=URIRef)

slots.book_category = Slot(uri=EXAMPLE.book_category, name="book_category", curie=EXAMPLE.curie('book_category'),
                   model_uri=EXAMPLE.book_category, domain=None, range=Optional[Union[str, list[str]]])

slots.name = Slot(uri=EXAMPLE.name, name="name", curie=EXAMPLE.curie('name'),
                   model_uri=EXAMPLE.name, domain=None, range=Optional[str])

slots.price = Slot(uri=EXAMPLE.price, name="price", curie=EXAMPLE.curie('price'),
                   model_uri=EXAMPLE.price, domain=None, range=Optional[float])

slots.inStock = Slot(uri=EXAMPLE.inStock, name="inStock", curie=EXAMPLE.curie('inStock'),
                   model_uri=EXAMPLE.inStock, domain=None, range=Optional[str])

slots.creator = Slot(uri=EXAMPLE.creator, name="creator", curie=EXAMPLE.curie('creator'),
                   model_uri=EXAMPLE.creator, domain=None, range=Optional[Union[dict, Author]])

slots.genres = Slot(uri=EXAMPLE.genres, name="genres", curie=EXAMPLE.curie('genres'),
                   model_uri=EXAMPLE.genres, domain=None, range=Optional[Union[Union[str, "GenreEnum"], list[Union[str, "GenreEnum"]]]])

slots.from_country = Slot(uri=EXAMPLE.from_country, name="from_country", curie=EXAMPLE.curie('from_country'),
                   model_uri=EXAMPLE.from_country, domain=None, range=Optional[Union[str, CountryName]])

slots.books = Slot(uri=EXAMPLE.books, name="books", curie=EXAMPLE.curie('books'),
                   model_uri=EXAMPLE.books, domain=None, range=Optional[Union[dict[Union[str, BookId], Union[dict, Book]], list[Union[dict, Book]]]])

slots.all_book_series = Slot(uri=EXAMPLE.all_book_series, name="all_book_series", curie=EXAMPLE.curie('all_book_series'),
                   model_uri=EXAMPLE.all_book_series, domain=None, range=Optional[Union[dict[Union[str, BookSeriesId], Union[dict, BookSeries]], list[Union[dict, BookSeries]]]])

slots.summary = Slot(uri=EXAMPLE.summary, name="summary", curie=EXAMPLE.curie('summary'),
                   model_uri=EXAMPLE.summary, domain=None, range=Optional[str])

slots.reviews = Slot(uri=EXAMPLE.reviews, name="reviews", curie=EXAMPLE.curie('reviews'),
                   model_uri=EXAMPLE.reviews, domain=None, range=Optional[Union[Union[dict, Review], list[Union[dict, Review]]]])

slots.rating = Slot(uri=EXAMPLE.rating, name="rating", curie=EXAMPLE.curie('rating'),
                   model_uri=EXAMPLE.rating, domain=None, range=Optional[int])

slots.review_text = Slot(uri=EXAMPLE.review_text, name="review_text", curie=EXAMPLE.curie('review_text'),
                   model_uri=EXAMPLE.review_text, domain=None, range=Optional[str])

slots.country_name = Slot(uri=EXAMPLE.name, name="country_name", curie=EXAMPLE.curie('name'),
                   model_uri=EXAMPLE.country_name, domain=Country, range=Union[str, CountryName])
