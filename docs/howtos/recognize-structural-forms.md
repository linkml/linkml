(structural-forms)=
# How to recognize and work with different structural forms

## Introduction

### Purpose of the Guide

This how-to guide is intended to allow schema designers
and data modelers recognize the broadly different *shapes* or *srtructural forms* data can take, including flat tables, trees,
normalized relations, and ontology graphs.

Being able to recognize these, and understanding
the strengths and benefits of each can help you build
schemas that are more fit for purpose, and have a more
predictable and consistent form.

__NOTE__ In this guide we use the term *structural form* to
indicate a broad pattern to which the data conforms. These
are sometimes called data *shapes* but we avoid this term
where it could be confused with [RDF Shape Languages](https://www.w3.org/TR/shacl/).


### The Main Schema Structural Forms

This guide covers four distinct "shapes" of data, each catering to different data modeling requirements:

1. **Tabular Structural Form**: Exemplified by spreadsheets and statistical data frames. Ideal for straightforward, row-and-column data structures,. It is best suited for datasets where complexity and interrelationships are minimal, or have been "flattened" into a table form.

2. **Tree Structural Form**: Focuses on nested data structures, exemplified by JSON/YAML. This style is beneficial for data with nested relationships and hierarchical organization.

3. **Relational Structural Form**: Centers on the normalized relational model used in SQL databases. Typically used for datasets with complex interrelationships between entities.

4. **Ontological/Knowledge Graph Schema Style**: Pertains to modeling data as a network of interconnected entities. This style is vital for datasets requiring rich semantic relationships and is conducive to advanced querying and inference.

5. **Mulidimensional Structural Form**: Guidelines in progress

### Choosing the Right Schema Style
Selecting the appropriate schema style depends on various factors, such as the complexity of the data, the nature of relationships within the data, and the intended use of the data model. It also
might depend on technical requirements, such as suitability for
use with particular database systems, or query performance need.

It is important to note that this guide is not intended to be
prescriptive, nor is it intended to suggest that all schemas
should solely conform to a single form. Where appropriate, we
note cases where it can be useful to blend these forms together.

This guide aims to provide clarity on the strengths and use cases of each style, assisting you in making an informed decision for your data modeling needs.

## Structural Forms

### Tabular Structural Form

#### Overview

The tabular or data frame style organizes data in a familiar row-and-column format, similar to spreadsheets. It's effective for datasets where each row signifies a unique observation or data item and each column denotes a specific attribute of that observation or data item.

#### Tabular Data Example

Imagine we have a table of books:

| Title                           | Author                | Genre       | Year | Price Paperback | Price Hardback | Rating |
|---------------------------------|-----------------------|-------------|------|-----------------|----------------|--------|
| 20,000 Leagues Under the Sea with Walruses | Jules Verne-Inspired   | Sci-Fi      | 2018 | 13.50           | 22.00          | 5      |
| The Great Walrus Gatsby         | F. Scott Fitztusk     | Classic     | 2020 | 14.99           | 23.50          | 4      |
| The Tusk of Physics             | Stephen Hawtusk       | Science     | 2019 | 12.00           | 20.00          | 5      |
| Walruses of Waterloo            | Natasha Rostova       | History     | 2017 | 15.00           | 24.00          | 3      |
| A Tale of Two Walruses          | Charles Tuskens       | Adventure   | 2021 | 16.25           | 26.25          | 4      |

A characteristic of tabular data is that each table can typically be modeled with a single class, i.e schemas are simple **data dictionaries** explaining the meaning of each column.

A minimal schema for the above tabular data might be:

```yaml
classes:
  Book:
    description: "A record representing a book"
    attributes:
      title:
        description: "Title of the book, creatively alluding to classic titles or historic events"
        range: string
      author:
        description: "Author of the book, with names inspired by famous authors"
        range: string
      genre:
        description: "Genre of the book"
        range: GenreEnum
      year:
        description: "Year of publication"
        range: integer
      price_paperback:
        description: "Price of the book in paperback format"
        range: float
      price_hardback:
        description: "Price of the book in hardback format"
        range: float
      rating:
        description: "Rating of the book"
        range: integer
        minimum_value: 1
        maximum_value: 5

enums:
  GenreEnum:
    permissible_values:
      Sci-Fi: {}
      Classic: {}
      Science: {}
      History: {}
      Adventure: {}
```


#### Key Characteristics
- **Row-Oriented Layout**: Each row is an individual observation or data item
- **Columnar Attributes**: Columns represent distinct attributes. The number of columns can potentially be large.
- **Simple Design**: Best suited for datasets without complex hierarchies or nested structures.

#### Usage Scenarios
- **Data Analysis and Reporting**: This format is easily manipulated for statistical analysis, reporting, and data science applications
- **Simple Data Storage and Entry**: Ideal for basic data storage and entry needs, where complexity is minimal. Suited for spreadsheet tools like Excel.
- **Efficient processing**: The simplicity lends itself to efficient processing using data science frameworks like Pandas, Dask, as well as columnar data stores such as BigTable.
- **Data Dictionaries**: Schemas can be simple data dictionaries, focusing on the meaning of each column, without worrying about modeling relationships or hierarchical classification.

#### Serialization Formats and Databases
- **CSVs/TSVs**
- **Excel**
- Efficient data science formats, **Arrow**, **Parquet**

For database systems for efficient querying, columnar stores
such as BigTable can be a good match, but really any kind of system
can be easily used.

#### Key Metamodel Elements and Concepts

- tables correspond to *classes* (typically one per schema)
- `attributes`
- `types`
- `enums` (for categorical data)

#### Relationship to other forms

- **Tabular/Tree**: It's common to combine tabular style with lightweight nesting or additional structure on each attribute. This can be achieve through the use of *inlining*. Note this makes use of simple CSVs or Excel more difficult, and formats such as jsonl or Parquet may be more appropriate
- **Tabular/Relational**: Sometimes it can be useful to break things out into multiple tables, with a primary key and foreign key structure. In some cases it may not make sense to have a crisp distinction between tabular and relational forms.

#### Best Practice: Tidy Data Modeling

[Tidy data modeling](https://vita.had.co.nz/papers/tidy-data.pdf), as proposed by Hadley Wickham, emphasizes a streamlined and consistent approach to organizing data sets. The core principle of this methodology is to structure data in a way that facilitates analysis and visualization, making it easily interpretable and manageable. In a tidy data set, each variable forms a column, each observation forms a row, and each type of observational unit forms a table. This structure significantly simplifies the majority of data manipulation tasks since each variable is isolated in its column, allowing for more intuitive and straightforward data handling. The approach aligns with principles of data normalization, minimizing redundancy and ensuring clarity in data representation. By adhering to these practices, data sets become more orderly, aligned, and accessible for analysis, providing a robust foundation for statistical analysis and data-driven decision-making. Tidy data modeling not only enhances data quality but also streamlines the process of data transformation, visualization, and analysis, making it an essential practice in modern data science.



#### Conclusion
The tabular/tidy schema style, coupled with LinkML, offers a clear, structured format for simple datasets. It's particularly useful where the main focus is on basic data storage, entry, and straightforward analysis, avoiding the complexities of hierarchical or relational data structures.

### Tree Structural Forms

#### Overview
The tree form is designed for data structures where data is organized in a nested manner. This style is suitable for datasets where attributes are composite or compound objects.

#### Example

To illustrate this style we will modify the above example and advantage of nesting to organize the data more efficiently. The prices for paperback and hardback can be collapsed into a nested `prices` array, each with details like amount, currency, and format. Here's how the dataset would look in JSON:

```json
{"books":
    [
        {
            "title": "20,000 Leagues Under the Sea with Walruses",
            "author": "Jules Verne-Inspired",
            "genre": "Sci-Fi",
            "year": 2018,
            "rating": 5,
            "prices": [
                {"amount": 13.50, "currency": "$", "format": "Paperback"},
                {"amount": 22.00, "currency": "$", "format": "Hardback"}
            ]
        },
        {
            "title": "The Great Walrus Gatsby",
            "author": "F. Scott Fitztusk",
            "genre": "Classic",
            "year": 2020,
            "rating": 4,
            "prices": [
                {"amount": 14.99, "currency": "$", "format": "Paperback"},
                {"amount": 23.50, "currency": "$", "format": "Hardback"}
            ]
        },
        {
            "title": "The Tusk of Physics",
            "author": "Stephen Hawtusk",
            "genre": "Science",
            "year": 2019,
            "rating": 5,
            "prices": [
                {"amount": 12.00, "currency": "$", "format": "Paperback"},
                {"amount": 20.00, "currency": "$", "format": "Hardback"}
            ]
        },
        {
            "title": "Walruses of Waterloo",
            "author": "Natasha Rostova",
            "genre": "History",
            "year": 2017,
            "rating": 3,
            "prices": [
                {"amount": 15.00, "currency": "$", "format": "Paperback"},
                {"amount": 24.00, "currency": "$", "format": "Hardback"}
            ]
        },
        {
            "title": "A Tale of Two Walruses",
            "author": "Charles Tuskens",
            "genre": "Adventure",
            "year": 2021,
            "rating": 4,
            "prices": [
                {"amount": 16.25, "currency": "$", "format": "Paperback"},
                {"amount": 26.25, "currency": "$", "format": "Hardback"}
            ]
        }
    ]
}
```

In the above:

- Each book is represented as an *object* within an array.
- Nested `prices` arrays allow for a more compact representation of different formats and their respective prices.
- Other attributes like `title`, `author`, `genre`, `year`, and `rating` remain at the top level of each book object.
- We have introduced a **Container** object that has one attribute, `books`

This JSON representation demonstrates how nested structures can efficiently manage complex data, making it more readable and scalable, especially for attributes with multiple components like book pricing.

To adapt the original LinkML schema to accommodate the modified JSON structure for the books dataset, the main change involves the representation of book prices. Here's the revised part of the LinkML schema reflecting this change:

#### Modified schema to allow for nesting

```yaml
classes:
  Book:
    description: "..."
    attributes:
      ...
      prices:
        description: "List of different format prices for the book"
        multivalued: true
        range: Price

  Price:
    description: "Price details of a book format"
    attributes:
      amount:
        description: "Amount of the book price"
        range: float
      currency:
        description: "Currency of the book price"
        range: CurrencyEnum
      format:
        description: "Format of the book (Paperback or Hardback)"
        range: FormatEnum
```

In this modification:

- **Prices as a Nested Structure**: The `prices` attribute in the `Book` class is now a list (multivalued), each item of which is an instance of a new class `Price`.
- **Price Class**: A new `Price` class is introduced to encapsulate the details of the book's price, including the amount, currency, and format.
- **Enumeration for Format**: The `format` attribute in the `Price` class uses an enumeration to restrict the value to either "Paperback" or "Hardback".


Note that the prices are *inlined* in the JSON - we don't need
an explicit `inlined: true` assignment, because inlining happens
automatically if there is no identifier.

These changes reflect the nested structure of the book prices in the JSON representation, showcasing the flexibility of LinkML in adapting to different data structuring needs.

#### Key Characteristics
- **Nested Data Representation**: Data is structured in a tree-like format, with a composition-style hierarchy
- **Complex Data Structures**: Ideal for representing complex, interrelated data elements that are not easily captured in a flat structure.
- **Flexible and Scalable**: Accommodates varying levels of detail and complexity, allowing for scalability.

#### Usage Scenarios
- **Configurations and Settings**: For data involving settings or configurations where hierarchical groupings are necessary.
- **Complex Data Models**: Suitable for representing complex entities, such as organizational structures or product catalogs.

#### Serialization Formats and Databases
- **JSON/YAML**
- **XML** (not typically used in modern environments)
- **Protobuf, Avro**

Object stores such as Mongo can be a good choice for data following
this shape. In general, other database systems should work, but
may introduce mild impedance mismatches or the need for lightweight
structural transformations.

#### Key Metamodel Elements and Concepts

In addition to the core elements and concepts used for flat
tabular data:

- `range` that is a *class*
- `inlined` declarations

#### Hierarchical Composition

This form also includes the ability to represent
hierarchical structures, for example:

  ```yaml
  classes:
    Department:
      description: "A department in an organization"
      attributes:
        name:
          description: "Name of the department"
          type: string
        manager:
          description: "Manager of the department"
          type: string
        subdepartments:
          description: "Subdepartments within the department"
          type: Department
  ```



#### Conclusion
The Tree Structural Form, when implemented with LinkML, offers an effective way to model complex and hierarchical data structures. This approach is particularly beneficial for datasets where relationships and nested groupings play a crucial role, allowing for a more natural and intuitive representation of the data. With careful planning and implementation, this style can greatly enhance the organization and accessibility of complex datasets.


### Relational Structural Form

#### Overview
The relational or SQL schema style is centered around the relational model, commonly used in SQL databases. In particular, where
the schema has been fully or partially *normalized* (otherwise
it becomes indistinguishable from the Tabular Structural Form).

This style is characterized by data organized into tables (aka records, *relations*), with relationships between these tables managed through keys. It's ideal for datasets with complex interrelationships between different entities.

#### Key Characteristics
- **Table-oriented Data Organization**: Data is structured in tables, where each table represents a different entity type.
- **Relationships Through Keys**: Relationships between tables are defined using primary and foreign keys.
- **Use of Joins in querying**: This style facilitates complex queries, joining data from multiple tables.

#### Usage Scenarios
- **Complex Interrelated Datasets**: Suitable for datasets with intricate relationships between various entities.
- **Scalable Data Models**: Effective for models that require scalability and flexibility in defining inter-table relationships.

### Example JSON, following Relational Structural Form

To transform the JSON representation into a more relational model, we'll create separate collections for authors, books, and prices. Each `Book` will reference an `Author` through an identifier, instead of inlining the author details.

#### Collections in JSON Format:

1. **Authors Collection**:

```json
[
    {"author_id": 1, "name": "Jules Verne-Inspired"},
    {"author_id": 2, "name": "F. Scott Fitztusk"},
    {"author_id": 3, "name": "Stephen Hawtusk"},
    {"author_id": 4, "name": "Natasha Rostova"},
    {"author_id": 5, "name": "Charles Tuskens"}
]
```

2. **Books Collection**:

```json
[
    {"book_id": 101, "title": "20,000 Leagues Under the Sea with Walruses", "author_id": 1, "genre": "Sci-Fi", "year": 2018, "rating": 5},
    {"book_id": 102, "title": "The Great Walrus Gatsby", "author_id": 2, "genre": "Classic", "year": 2020, "rating": 4},
    {"book_id": 103, "title": "The Tusk of Physics", "author_id": 3, "genre": "Science", "year": 2019, "rating": 5},
    {"book_id": 104, "title": "Walruses of Waterloo", "author_id": 4, "genre": "History", "year": 2017, "rating": 3},
    {"book_id": 105, "title": "A Tale of Two Walruses", "author_id": 5, "genre": "Adventure", "year": 2021, "rating": 4}
]
```

3. **Prices Collection**:

```json
[
    {"book_id": 101, "format": "Paperback", "amount": 13.50, "currency": "$"},
    {"book_id": 101, "format": "Hardback", "amount": 22.00, "currency": "$"},
    "...",
    {"book_id": 105, "format": "Paperback", "amount": 16.25, "currency": "$"},
    {"book_id": 105, "format": "Hardback", "amount": 26.25, "currency": "$"}
]
```

#### Explanation:

- **Authors Collection**: Contains details of authors, each with a unique identifier (`author_id`).
- **Books Collection**: Each book has its own identifier (`book_id`), and references an author through `author_id`. Other details like title, genre, year, and rating are also included.
- **Prices Collection**: Lists the prices for each book format (Paperback, Hardback), referenced by `book_id`.

This relational JSON structure separates the entities into distinct collections, allowing for a more modular and scalable data model. The use of identifiers and references creates relationships between the different entities, akin to a relational database.

To model the more relational JSON structure with separate collections for authors, books, and prices in LinkML, we'll define distinct classes for each entity type and establish references between them using identifiers. Here's the relevant part of the LinkML schema:

### LinkML Schema for the Relational Model

#### Author Class

```yaml
classes:
  Author:
    description: "An author of books"
    attributes:
      author_id:
        description: "Unique identifier for the author"
        identifier: true
        range: string
      name:
        description: "Name of the author"
        range: string

```

#### Book Class

```yaml
    Book:
    description: "A record representing a book"
    attributes:
      book_id:
        description: "Unique identifier for the book"
        identifier: true
        range: string
      title:
        description: "Title of the book"
        range: string
      author_id:
        description: "Identifier of the author of the book"
        range: Author
      genre:
        description: "Genre of the book"
        range: string
      year:
        description: "Year of publication"
        range: integer
      rating:
        description: "Rating of the book"
        range: integer
        minimum_value: 1
        maximum_value: 5

```

#### Price Class

```yaml
  Price:
    description: "Price details of a book format"
    attributes:
      book_id:
        description: "Identifier of the book"
        range: Book
      format:
        description: "Format of the book (Paperback or Hardback)"
        range: FormatEnum
      amount:
        description: "Amount of the book price"
        range: float
      currency:
        description: "Currency of the book price"
        range: CurrencyEnum

```

In this schema:

- **Author Class**: Represents authors with a unique identifier (`author_id`) and their name.
- **Book Class**: Represents books, each with a unique identifier (`book_id`). The `author_id` attribute references the `Author` class.
- **Price Class**: Contains pricing details for each book, referenced by `book_id`, and includes the format, amount, and currency.

This schema effectively models the relational structure of the data, with separate entities for authors, books, and prices, and uses identifiers to establish relationships between these entities. It exemplifies how LinkML can be used to represent a relational data model, similar to traditional SQL database designs.

#### Serialization Formats and Databases
- **CSVs/TSVs**
- **RDF** (in particular for fully normalized data)
- **Graph serializations**

The typical database solution for this shape of data is a relational/SQL database, but RDF or Graph databases can be a
good choice, in particular when the data is heavily normalized.
In practice any system can be used, but systems that don't
have first class support for joins/traversal may be suboptimal.

#### Key Metamodel Elements and Concepts

In addition to the core elements and concepts used for flat
tabular data:

- Typically one *class* per SQL Table
- `identifier` to indicate primary key
- non-`inlined` ranges that reference another class

Note in a pure relational model, `multivalued` would never be used.
However, it's typical to include multivalued slots even when
following the Relational Form in LinkML schemas, and to let the
automated translation to SQL translate multivalued columns to join
tables.

#### Best Practices
- **Normalization Principles**: Apply normalization principles to minimize redundancy and dependency, enhancing data integrity.
- **Clear Relationship Mapping**: Clearly define and document relationships between classes, ensuring that the relational model is easy to understand and maintain.


### Ontological Structural Form

#### Overview

The ontological or knowledge graph schema style in LinkML focuses on
hierarchical classification of entities within a domain, and the use of inheritance to propagate down attributes.

__NOTE__ this form is somewhat orthogonal to the others, and as such me may later choose to separate this into its own document.

This form can often be easily intermingled with the other forms in this document

#### Example Ontology

**Base Class**

```yaml
classes:
  CreativeWork:
    description: "A base class representing any form of creative work"
    attributes:
      title:
        description: "Title of the creative work"
        range: string
      creator:
        description: "Creator of the work (individual or organization)"
        range: string
      creation_date:
        description: "Date when the work was created or published"
        range: date
      description:
        description: "A brief description of the work"
        range: string
      language:
        description: "Language of the work"
        range: Language
      license:
        description: "License under which the work is distributed"
        range: LicenseType

```

**SubClasses**

```yaml
  Book:
    is_a: CreativeWork
    description: "Written works, primarily textual in nature"
    attributes:
      isbn:
        description: "International Standard Book Number"
        range: string
      publisher:
        description: "Publisher of the book"
        range: string
      number_of_pages:
        description: "Total number of pages"
        range: integer
      genre:
        description: "Genre of the book"
        range: BookGenre
      format:
        description: "Format of the book (e.g., Hardcover, Paperback, Ebook)"
        range: BookFormat

  Album:
    is_a: CreativeWork
    description: "Musical works released in a collection (album)"
    attributes:
      release_date:
        description: "Release date of the album"
        range: date
      record_label:
        description: "Record label that released the album"
        range: string
      genre:
        description: "Musical genre of the album"
        range: MusicGenre
      tracklist:
        description: "List of tracks in the album"
        range: string

  Art:
    is_a: CreativeWork
    description: "Works of visual art, including paintings, sculptures, and digital art"
    attributes:
      medium:
        description: "Medium used in the artwork (e.g., oil, watercolor, digital)"
        range: ArtMedium
      dimensions:
        description: "Dimensions of the artwork"
        range: string
      style:
        description: "Artistic style of the artwork (e.g., abstract, realism)"
        range: ArtStyle
      gallery:
        description: "Gallery where the artwork is displayed or housed"
        range: string

  Film:
    is_a: CreativeWork
    description: "Motion picture works, including movies and short films"
    attributes:
      director:
        description: "Director of the film"
        range: string
      release_date:
        description: "Release date of the film"
        range: date
      cast:
        description: "Cast members of the film"
        range: string
      genre:
        description: "Genre of the film"
        range: FilmGenre
      running_time:
        description: "Total running time of the film"
        range: string

  Software:
    is_a: CreativeWork
    description: "Computer software and applications"
    attributes:
      developer:
        description: "Developer of the software"
        range: string
      release_date:
        description: "Release date of the software"
        range: date
      version:
        description: "Version of the software"
        range: string
      platform:
        description: "Platform for which the software is developed"
        range: SoftwarePlatform

```

#### Key Characteristics
- **Entity-Relationship Framework**: Models data as entities (nodes) and relationships (edges) in a graph.
- **Semantic Depth**: Emphasizes the meaning and nuances of relationships between entities.
- **Inferential Capabilities**: Facilitates advanced querying and inference for knowledge extraction.

#### Usage Scenarios
- **Complex Semantic Models**: Ideal for complex systems with significant relational depth.
- **Data Integration**: Suited for scenarios requiring the merging of various data sources or adherence to standard ontologies.
- **Defining Entities and Relationships**: Entities are modeled as classes, with relationships represented as attributes or links between classes.

  Example:
  ```yaml
  classes:
    Person:
      description: "An individual"
      attributes:
        knows:
          description: "Another person known by this person"
          type: Person
  ```

#### Serialization Formats and Databases
- **OWL**
- **RDFS**
- Graph-oriented formats like KGX

RDF databases and Graph databases can be a good choice for this
form of data.

#### Key Metamodel Elements and Concepts

- `is_a` and `mixins` for inheritance hierarchies
- `slot_usage` to refine the use of existing properties

#### Property Graph vs. RDF/S Style
- **Property Graph (Biolink Model)**:
  - Focuses on entities as nodes and relationships as edges, with properties attached directly to nodes and edges.
  - Well-suited for detailed, attribute-rich models.
- **RDF/S Style (e.g., Schema.org)**:
  - Emphasizes semantic relationships using RDF standards.
  - More aligned with web semantics and linked data principles.

#### Best Practices
- **Semantic Clarity**: Ensure each entity and relationship is semantically well-defined.
- **Scalable and Adaptable Ontologies**: Design ontologies to be flexible and scalable, accommodating evolving knowledge.
- **Utilize LinkML's Semantic Capabilities**: Leverage LinkML features for semantic web integration and ontology modeling.

#### Conclusion
The ontological/knowledge graph schema style, when utilized with LinkML, offers a sophisticated means to model data with complex semantic relationships. This style is invaluable for creating detailed knowledge graphs that require a deep understanding of the data and its interconnections. By effectively employing class hierarchies and understanding the nuances between property graph and RDF/S styles, one can develop comprehensive, semantically rich models that serve a wide range of advanced data analysis and integration purposes.

### Multidimensional Structural Form

Documentation on this form forthcoming, for now see the how-to section on [multidimensional arrays](https://linkml.io/linkml/howtos/multidimensional-arrays.html)
