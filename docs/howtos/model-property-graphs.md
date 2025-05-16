# How to make a property graph schema

LinkML is intended to be a flexible, general purpose "[polyglot](https://github.com/json-ld/yaml-ld/issues/19)" data modeling framework. You can use it with JSON documents and document databases like MongoDB, with tables and data frames, or with graph or RDF databases, and more. See [How to recognize and work with different structural forms](recognize-structural-forms.md) for more details.

A lot of the LinkML documentation uses JSON/YAML as examples, as these are flexible commonly used syntaxes for exchanging data, but many of the original use cases for LinkML came from [graph modeling](https://biolink.github.io/biolink-model/), and this continues to be a driving use case.

This how-to guide walks through the steps for making a schema for a [Property Graph](https://en.wikipedia.org/wiki/Property_graph) (PG), such as what might be found in a graph database like [Neo4J](https://neo4j.com/), or also in an RDF database that supports [RDF-star](https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/), such as GraphDB.

We focus here on PGs, because there are some specific design considerations that don't come up when thinking about simple RDF-style subject-property-object graphs (see [working with RDF](https://linkml.io/linkml/data/rdf.html) for more on this topic).

## What is a property graph?

A property graph (PG) is a graph data model that allows for properties to be associated with both edges (relationships) and nodes (vertices). This allows for more expressive queries and data modeling than a simple graph.

The Neo4J documentation on [graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) shows an example of a PG for representing relationships of persons to Movies:

![example graph](https://neo4j.com/docs/getting-started/_images/graph_simple-arr.svg)

As can be seen, the graph in this example has two edges:

- a simple edge between `Person` and `Movie`, with an edge label `DIRECTED`
- a more complex edge between `Person` and `Movie`, with an edge label `ACTED_IN` and an edge property `roles`

Let's explore how this could be modeled in LinkML. Our first attempt will be a simple projection of the PG where each edge is a *slot*, but this has some limitations. Then we will explore an alternative way of doing this.

## First attempt: A simple graph projection

If we ignore the edge property `roles`, then coming up with a schema for this graph is quite easy:

```yaml
id: https://example.org/person-movie
name: Person-Movie
description: Illustration of simple RDF graph model
prefixes:
  neo4j: https://neo4j.com/
  schema: https://schema.org/
  example: https://example.org/

imports:
  - linkml:types
  
default_prefix: example
default_range: string
  
classes:

  Person:
    attributes:
      name:
      born:
      profession:
      acted_in:
        range: Movie
        multivalued: true
      directed:
        range: Movie
        multivalued: true
   Movie:
     attributes:
      title:
        identifier: true
      released:
```

Each edge type in the graph corresponds to a slot/attribute, whose range is a class.

Here we choose to make the `acted_in` and `directed` attributes as owned by Person, but we could equally have flipped this around and made `actors` and `directors` attributes of Movie. While this doesn't make any semantic difference, the choice of direction can have practical implications on YAML/JSON and Object Oriented representations.

We have also chosen to model the profession as a simple string, for simplicity for now.

We can also think of this as a *graph projection*:

| Graph Element           | LinkML                       |
|-------------------------|------------------------------|
| Node                    | instance of a Class          |
| Edge                    | Attribute-Value Assignment   |
| Predicate (Edge Label)  | Attribute                    |
| Node Property           | Attribute-Value Assignment   |
| Edge Property           | *not represented*            |

Note that in this simple graph projection, we don't have any way of representing the `roles` edge property in the original Neo4J example.

### Schemasheets representation of direct simple graphs

The above schema can easily be represented in a tabular form using [SchemaSheets](https://linkml.io/schemasheets/):

Main tab:

| Class  | Attribute  | Type      | Multivalued | Identifier |
|--------|------------|-----------|-------------|------------|
| Person | name       | string    |             |            |
| Person | born       | string    |             |            |
| Person | profession | string    |             |            |
| Person | acted_in   | Movie     | true        |            |
| Person | directed   | Movie     | true        |            |
| Movie  | title      | string    |             | true       |
| Movie  | released   | string    |             |            |

### Example data

Let's examine some example data instances, using the simple projection schema. We'll show these first as YAML:

Persons:

```yaml
- name: Tom Hanks
  profession: Actor
  born: 1956
  acted_in: Forrest Gump
- name: Robert Zemeckis
  profession: Director
  born: 1951
  directed: Forrest Gump
```

Movies:

```yaml
- title: Forrest Gump
  released: 1994
```

We are using references rather than [inlining](https://linkml.io/linkml/schemas/inlining.html) here, so although the YAML looks "flat" it is semantically a graph.

These have a natural representation as RDF graphs, with persons and movies being nodes, and the edges being the triples connecting them: 

```turtle
# node-to-node edges
:Tom_Hanks :acted_in :Forrest_Gump .
:Robert_Zemeckis :directed :Forrest_Gump .

# node-to-literal edges
:Tom_Hanks :born "1956" .
:Robert_Zemeckis :born "1951" .
:Tom_Hanks :profession "Actor" .
:Forest_Gump :title "Forrest Gump" .
:Forest_Gump :released "1994" .
```

In RDF, we also have "literal edges" as triples, so the relationship between a person and the string literal representing the year they were born are also represented as triples,

When working with the default python or pydantic models for this, we can iterate over all movies a person has participated in:

```python
# assume we have two lists, movies and persons
movies_ix = {movie.title: movie for movie in movies}
for person in persons:
    print(f"Person: {person.name}")
    for movie_id in person.acted_in:
        movie = movies_ix[movie_id]
        print(f"{person.name} acted in {movie.title}, released in {movie.released}")
    for movie_id in person.directed:
        movie = movies_ix[movie_id]
        print(f"{person.name} directed {movie.title}, released in {movie.released}")
```

Note that when we try and traverse from movie to persons directly, this won't work as associations are directional in OO models. Note also the awkward need to lookup non-inlined references.

### Limitations of simple graphs

This all works well for simple graphs, but what happens if we want to represent the *role* of the actor in the movie, e.g. the name of the character that Tom Hanks plays in the movie Forest Gump is... "Forrest Gump"?

![example graph](https://neo4j.com/docs/getting-started/_images/graph_simple-arr.svg)

There are a number of different design patterns here, and from an RDF modeling perspective these have all been collected in an influential W3C note on [n-ary relations](https://www.w3.org/TR/swbp-n-aryRelations/). More recently, the RDF-star extension to RDF has been proposed to allow for properties on edges. The Ontotext site has good up to date documentation contrasting the different design patterns for representing PGs in RDF, and their relationship to RDF-star: [What is rdf-star?](https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/)

In RDF-star, we can represent the role of the actor in the movie as a property on the edge between the person and the movie:

```
:Tom_Hanks :acted_in :Forrest_Gump   {| :role "Forrest Gump" |} .
:Robert_Zemeckis :directed :Forrest_Gump .
```

This uses [annotation syntax](https://w3c.github.io/rdf-star/cg-spec/editors_draft.html#annotation-syntax), which is a shorthand for both asserting the triple, and the reification.

However, there is as yet not agreed upon standard for schematizing RDF-star (see [w3c/shacl#23](https://github.com/w3c/shacl/issues/23) for discussion on combining RDF-star and SHACL), and no agreed upon standard for schematizing PGs more generally.

## Second attempt: Standard PG Pattern: Node and Edge classes

A standard pattern for modeling PGs is to have two sets of classes: classes for nodes, and classes for edges. These could either be generic, or they could be abstract base classes intended to be subclassed.

```yaml
classes:
  Node:
    abstract: true
    attributes:
      id:
        identifier: true
        range: uriorcurie
      name:
        slot_uri: rdfs:label
      category:
        slot_uri: rdf:type
        range: string
        designates_type: true
      types:
        name:
        range: string
        multivalued: true
  Edge:
    abstract: true
    attributes:
      class_uri: rdf:Statement
      subject:
        slot_uri: rdf:subject
        range: Node
      predicate:
        range: uriorcurie
        slot_uri: rdf:predicate
        designates_type: true
      object:
        slot_uri: rdf:object
        range: Node
  Graphs:
    attributes:
      nodes:
        range: Node
        multivalued: true
        inlined_as_list: true
      edges:
        range: Edge
        multivalued: true
        inlined_as_list: true
```

The *graph projection* for this schema is

| Graph Element           | LinkML                                      |
|-------------------------|---------------------------------------------|
| Node                    | instance of a (Node) Class                  |
| Edge                    | instance of an (Edge) Class                 |
| Predicate (Edge Label)  | (Edge) Class                                | 
| Node Property           | Attribute-Value Assignment on Node instance |
| Edge Property           | Attribute-Value Assignment on Edge instance |

We made a few design decisions here, but these are not set in stone. For different use cases, you may want to
model differently.

- identifiers
   - nodes have identifiers, and references to nodes from edges are not inlined. Data providers are expected to mint these. 
   - edges do not have identifiers. This makes it harder for an edge to reference another edge.
- vocabulary
   - we use the RDF reification vocabulary for URIs, but we could use anything here.
   - we use `name` for a human-readable name, and map this to `rdfs:label` (not to be confused with neo4j [labels](https://neo4j.com/news/labels-and-schema-indexes-in-neo4j/))
- extensibility
   - both `Node` and `Edge` are declared abstract, so they are intended to be subclassed
   - `Node` uses a `category` as a [type designator](https://linkml.io/linkml/schemas/type-designators.html)
   - `Edge` uses a `predicate` as a type designator (we will see the consequences of this later)
   - We also allow any number of types to be associated with a node (akin to "labels" in neo4j)
- containers
   - We include a `Graphs` class that can hold a list of nodes and a list of edges.
   - Graphs are treated as different from nodes and edges, but we could have made graphs a subtype of node, allowing them to be referenced as if they were nodes.

The above module could be reused across multiple different domains. Let's extend it for the movie domain:

```yaml
classes:
  Person:
    is_a: Node
    attributes:
      born:
      profession:
  Movie:
    is_a: Node
    attributes:
      title:
        identifier: true
      released:
  ActedIn:
    is_a: Edge
    attributes:
      role:
  Directed:
    is_a: Edge
```

Note that unlike the previous schema, edges are "first-class", and nodes no longer "own" the edges. From a graph database perspective, there is no such distinction, but this has implications for e.g. Pydantic and JSON representations.

As before, we can easily represent this in SchemaSheets:

Nodes tab:

| Node Class | Attribute  | Type     | Multivalued | Identifier |
|------------|------------|----------|-------------|------------|
| Person     | name       | string   |             |            |
| Person     | born       | string   |             |            |
| Person     | profession | string   |             |            |
| Movie      | title      | string   |             | true       |
| Movie      | released   | string   |             |            |

Edges tab:

| Predicate | Subject | Object | Attribute | Type   | Multivalued |
|-----------|---------|--------|-----------|--------|-------------|
| ActedIn   | Person  | Movie  | role      | string |             |
| Directed  | Person  | Movie  |           |        |             |

Data in YAML might look like this:

```yaml
nodes:
- id: PERSON:TH
  name: Tom Hanks
  profession: Actor
  born: 1956
  category: my:Person
- id: PERSON:RZ
  name: Robert Zemeckis
  profession: Director
  born: 1951
  category: my:Person
- id: MOVIE:FG
  title: Forrest Gump
  released: 1994
  category: my:Movie
edges:
- subject: PERSON:TH
  predicate: my:ActedIn
  object: MOVIE:FG
  role: Forrest Gump
- subject: PERSON:RZ
  predicate: my:Directed
  object: MOVIE:FG
```  

Our decision to use classes to represent edge types (which for now we conflate with predicates) has the advantage of allowing fine-grained control over the properties of edges. For example, if we had an edge:

```
- subject: PERSON:RZ
  predicate: my:Directed
  object: MOVIE:FG
  role: Director
```

This would be flagged as invalid.

### Direct RDF mapping of example data

If we were to serialize the above data as RDF using the schema above, this would result in triples such as:

```
PERSON:TH a my:Person ;
  rdfs:label "Tom Hanks" ;
  born 1956 ;
  profession "Actor" .
PERSON:RZ a my:Person ;
  rdfs:label "Robert Zemeckis" ;
  born 1951 ;
  profession "Director" .
MOVIE:FG a my:Movie ;
  rdfs:label "Forrest Gump" ;
  released 1994 .
[ a rdf:Statement ;
  rdf:subject PERSON:TH ;
  rdf:predicate my:ActedIn ;
  rdf:object MOVIE:FG ;
  my:role "Forrest Gump" ] .
[ a rdf:Statement ;
  rdf:subject PERSON:RZ ;
  rdf:predicate my:Directed ;
  rdf:object MOVIE:FG ] .
```

This is perhaps slightly unusual from an RDF perspective, as we are using the reification vocabulary, but we are only "quoting" the edge and not asserting it. This means that a query:

```sparql
SELECT ?person WHERE {?person my:ActedIn MOVIE:FG}
```

Would not return any results; it's necessary to query the reified edge:

```sparql
SELECT ?person WHERE {?s rdf:subject ?person ; rdf:predicate my:ActedIn ; rdf:object MOVIE:FG}
```

In RDF-star the edge statements can be represented using quotation syntactic sugar:

```
<< Tom_Hanks :acted_in :Forrest_Gump >> :role "Forrest Gump" .
<< :Robert_Zemeckis :directed :Forrest_Gump >> .
```

### Edge types

In the above example, we equate the RDF predicate with the edge type. This has the advantage of simplicity.

In some cases we might want to make edge types more granular than predicates. For example, consider a schema that uses a `HasPart` predicate. This is a very general predicate that could be used for:

- protein complex to sub-complexes to proteins (to amino acids...)
- anatomical structures such as organisms relating to organisms to organs to tissues to cells to molecules...
- engineered structures such as a car to parts to sub-parts to materials...

In this case, we might want to have a more granular set of edge types, such as `AnatomicalHasPart`, `ProteinHasPart`, in order to enforce constraints. However, we might still want the rdf predicate to map to the more general `HasPart`.

We might do this by modifying the `Edge` class to have a distinct `type` attribute, and then subclassing `Edge`:

```
classes:
  Edge:
    abstract: true
    attributes:
      class_uri: rdf:Statement
      subject:
        slot_uri: rdf:subject
        range: Node
      predicate:
        range: uriorcurie
        slot_uri: rdf:predicate
        designates_type: true
      object:
        slot_uri: rdf:object
        range: Node
      type:
        slot_uri: rdf:type
        range: uriorcurie
        designates_type: true
  HasPart:
    is_a: Edge
    slot_usage:
      predicate:
        equals_string: "BFO:0000051"
    attributes:
      quantity:
      range: integer
  AnatomicalHasPart:
    is_a: HasPart
    slot_usages:
      subject: AnatomicalEntity
      object: AnatomicalEntity
  VehicleHasPart:
    is_a: HasPart
    ...    
```

Our YAML/JSON objects might look like:

```
edges:
- subject: Heart
  predicate: BFO:0000051
  object: Ventricle
  type: my:AnatomicalHasPart
  quantity: 2
```

This provides a bit more flexibility, but with some additional complexity.

### Assertions vs Quotes

As noted above, when using the standard PG modeling pattern, edge types (predicates) are classes. We do not have slots `acted_in` and `directed`. Instead we have `ActedIn` and `Directed` classes, and generic n-ary relation properties to relate edge instances to nodes.

This is in contrast to the simple representation, where we have explicit slots for each predicate, but we can't represent directly the edge properties.

We are currently exploring options for allow features such as auto-asserting PG style models when mapping to RDF-star.


## See Also

- [What is RDF-star](https://www.ontotext.com/knowledgehub/fundamentals/what-is-rdf-star/) from GraphDB docs
- [Property Graphs with LinkML store](https://linkml.io/linkml-store/how-to/Use-Neo4j.html)

