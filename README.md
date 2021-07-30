[![Pyversions](https://img.shields.io/pypi/pyversions/linkml.svg)](https://pypi.python.org/pypi/linkml)
![](https://github.com/linkml/linkml/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/linkml.svg)](https://pypi.python.org/pypi/linkml)


## [Binder Link](https://mybinder.org/v2/gh/linkml/linkml/main?filepath=notebooks)

# LinkML - <u>Link</u>ed data <u>M</u>odeling <u>L</u>anguage

LinkML is a general purpose modeling language following object-oriented and ontological principles. Models can be created in YAML, JSON or RDF. A variety of artefacts can be generated from the model, including ShEx, JSON-Schema, OWL, Python dataclasses, UML diagrams, Markdown pages for deployment in a GitHub pages site, and more.

LinkML is used for development of the [BioLink Model](https://linkml.github.io/biolink-model), but the framework is general purpose and can be used for any kind of modeling.

This documentation is best seen via the [linkml site](https://linkml.github.io/linkml-model/) but can also be viewed via the GitHub repository

Quickstart docs:

 * Browse the model (linkml is self-describing): [https://linkml.github.io/linkml-model/docs](https://linkml.github.io/linkml-model/docs)
    * [class definition](https://linkml.github.io/linkml-model/docs/ClassDefinition) Class definitions
    * [slot definition](https://linkml.github.io/linkml-model/docs/SlotDefinition) Class properties
    * [type definition](https://linkml.github.io/linkml-model/docs/TypeDefinition) Data types
    * [schema definition](https://linkml.github.io/linkml-model/docs/SchemaDefinition) Schema definition

Further details about the general design of LinkML are in the [LinkML Modeling Language Specification](SPECIFICATION.md).

For an example, see the [Jupyter notebook example](https://nbviewer.jupyter.org/github/linkml-model/blob/main/notebooks/examples.ipynb)


## Installation

This project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to install. Some IDE's like [PyCharms also have direct support for pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html). Once pipenv is running, the project may be installed:

```bash
> pipenv install linkml
```

## Language Features

 * polymorphism/inheritance, see [is_a](https://linkml.github.io/linkml-model/docs/is_a)
 * [abstract](https://linkml.github.io/linkml-model/docs/abstract) and [mixin](https://linkml.github.io/linkml-model/docs/mixin) classes
 * control JSON-LD mappings to URIs via [prefixes](https://linkml.github.io/linkml-model/docs/prefixes) declarations
 * ability to refine meaning of a slot in the context of a particular class via [slot usage](https://linkml.github.io/linkml-model/docs/slot_usage)


## Examples

linkml can be used as a modeling language in its own right, or it can be
compiled to other schema/modeling languages

We use a basic schema for illustrative purposes:

```yaml
id: http://example.org/sample/organization
name: organization

types:
  yearCount:
    base: int
    uri: xsd:int
  string:
    base: str
    uri: xsd:string

classes:

  organization:
    slots:
      - id
      - name
      - has boss

  employee:
    description: A person
    slots:
      - id
      - first name
      - last name
      - aliases
      - age in years
    slot_usage:
      last name :
        required: true

  manager:
    description: An employee who manages others
    is_a: employee
    slots:
      - has employees

slots:
  id:
    description: Unique identifier of a person
    identifier: true

  name:
    description: human readable name
    range: string

  aliases:
    is_a: name
    description: An alternative name
    multivalued: true

  first name:
    is_a: name
    description: The first name of a person

  last name:
    is_a: name
    description: The last name of a person

  age in years:
    description: The age of a person if living or age of death if not
    range: yearCount

  has employees:
    range: employee
    multivalued: true
    inlined: true

  has boss:
    range: manager
    inlined: true
```

Note this schema does not illustrate the more advanced features of blml

## Generators

See [](linkml/generators/)

### JSON Schema

[JSON Schema](https://json-schema.org/) is a schema language for JSON documents

JSON schema can be derived from a linkml schema, for example:

`pipenv run gen-json-schema examples/organization.yaml`

Output: [examples/organization.schema.json](examples/organization.schema.json)

Note that any JSON that conforms to the derived JSON-Schema can be converted to RDF using the derived JSON-LD context.

### JSON-LD Context

[JSON-LD contexts](https://www.w3.org/TR/json-ld/#the-context) provide a mapping from JSON to RDF

A JSON-LD context can be derived from a linkml schema, for example:

`pipenv run gen-jsonld-context examples/organization.yaml`

Output: [examples/organization.context.jsonld](examples/organization.context.jsonld)

You can control this via [prefixes](https://w3id.org/linkml/meta/prefixes) declarations and [default_curi_maps](https://w3id.org/linkml/meta/default_curi_maps).

Any JSON that conforms to the derived JSON-Schema (see above) can be converted to RDF using this context. See the [Jupyter notebook example]() for an example.

You can also combine a JSON instance file with a JSON-LD context using simple code or a tool like [jq](https://stackoverflow.com/questions/19529688/how-to-merge-2-json-objects-from-2-files-using-jq)

```bash
jq -s '.[0] * .[1]' examples/organization-data.json examples/organization.context.jsonld > examples/organization-data.jsonld
```

You can then use a standard JSON-LD conversion file to make other RDF syntaxes, e.g.

```bash
riot examples/organization-data.jsonld > examples/organization-data.nt
```

See [examples/organization-data.nt](examples/organization-data.nt)


### Python DataClasses

`pipenv run gen-py-classes examples/organization.yaml > examples/organization.py`

See [examples/organization.py](examples/organization.py)

For example:

```python
@dataclass
class Organization(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Organization")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "organization"
    class_model_uri: ClassVar[URIRef] = URIRef("http://example.org/sample/organization/Organization")

    id: Union[str, OrganizationId]
    name: Optional[str] = None
    has_boss: Optional[Union[dict, "Manager"]] = None

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.id is None:
            raise ValueError(f"id must be supplied")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)
        if self.has_boss is not None and not isinstance(self.has_boss, Manager):
            self.has_boss = Manager(self.has_boss)
        super().__post_init__(**kwargs)

```

For more details see [PythonGenNotes](linkml/generators/)

The python object can be direcly serialized as RDF. See the [Jupyter notebook example](https://nbviewer.jupyter.org/github/linkml/blob/master/notebooks/examples.ipynb) for an example.


### ShEx

 [ShEx](http://shex.io/shex-semantics/index.html) - Shape Expressions Langauge

`pipenv run gen-shex examples/organization.yaml > examples/organization.shex`

```
BASE <http://example.org/sample/organization/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd1: <http://example.org/UNKNOWN/xsd/>


<YearCount> xsd1:int

<String> xsd1:string

<Employee>  (
    CLOSED {
       (  $<Employee_tes> (  <first_name> @<String> ? ;
             <last_name> @<String> ;
             <aliases> @<String> * ;
             <age_in_years> @<YearCount> ?
          ) ;
          rdf:type [ <Employee> ]
       )
    } OR @<Manager>
)

<Manager> CLOSED {
    (  $<Manager_tes> (  &<Employee_tes> ;
          rdf:type [ <Employee> ] ? ;
          <has_employees> @<Employee> *
       ) ;
       rdf:type [ <Manager> ]
    )
}

<Organization> CLOSED {
    (  $<Organization_tes> (  <name> @<String> ? ;
          <has_boss> @<Manager> ?
       ) ;
       rdf:type [ <Organization> ]
    )
}
```

See [examples/organization.shex](examples/organization.shex) for full output

### OWL

Web Ontology Language [OWL](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/)

`pipenv run gen-owl examples/organization.yaml > examples/organization.owl.ttl`

```turtle
...
<http://example.org/sample/organization/Organization> a owl:Class,
        meta:ClassDefinition ;
    rdfs:label "organization" ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onClass <http://example.org/sample/organization/String> ;
            owl:onProperty <http://example.org/sample/organization/id> ;
            owl:qualifiedCardinality 1 ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass <http://example.org/sample/organization/String> ;
            owl:onProperty <http://example.org/sample/organization/name> ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality 1 ;
            owl:onClass <http://example.org/sample/organization/Manager> ;
            owl:onProperty <http://example.org/sample/organization/has_boss> ] .
```

See [examples/organization.owl.ttl](examples/organization.owl.ttl) for full output

## Generating Markdown documentation

`pipenv run gen-markdown examples/organization.yaml -d examples/organization-docs/`

This will generate a markdown document for every class and slot in the
model. These can be used in a static site, e.g. via GitHub pages.

### Others

* [YUML](https://yuml.me/) - UML diagram drawing tool
* Class and interface definitions for [GraphQL](https://graphql.org/)
* Graphviz -- fairly basic representation of hierarchies
* Protobuf
* [JSON](https://json.org/) and [JSON-LD](https://json-ld.org/)
* [Markdown](https://daringfireball.net/projects/markdown/) - markup language used by github and others
* [RDF](https://www.w3.org/2001/sw/wiki/RDF) - Resource Description Format


## Specification

See the [specification](https://linkml.github.io/linkml/SPECIFICATION).

Also see the [semantics](semantics) folder for an experimental specification in terms of FOL.

## FAQ

### Why not use X as the modeling framework?

Why invent our own yaml and not use JSON-Schema, SQL, UML, ProtoBuf,
OWL, ...

each of these is tied to a particular formalisms. E.g. JSON-Schema to
trees. OWL to open world logic. There are various impedance mismatches
in converting between these. The goal was to develop something simple
and more general that is not tied to any one serialization format or
set of assumptions.

There are other projects with similar goals, e.g
https://github.com/common-workflow-language/schema_salad

It may be possible to align with these.

### Why not use X as the datamodel

Here X may be bioschemas, some upper ontology (BioTop), UMLS
metathesaurus, bio*, various other attempts to model all of biology in
an object model.

Currently as far as we know there is no existing reference datamodel
that is flexible enough to be used here.


## Biolink Modeling Language

### Type Definitions

```
typeof:
    domain: type definition
    range: type definition
    description: supertype

  base:
    domain: type definition
    description: python base type that implements this type definition
    inherited: true

  type uri:
    domain: type definition
    range: uri
    alias: uri
    description: the URI to be used for the type in semantic web mappings

  repr:
    domain: type definition
    range: string
    description: the python representation of this type if different than the base type
    inherited: true
```


### Slot Definitions


## Developers Notes

### Release to Pypi

[A Github action] is set up to automatically release the Pypi package. When it is ready
for a new release, create a [Github release](https://github.com/linkml/releases). The version
should be in the vX.X.X format following [the semantic versioning specification](https://semver.org/).

After the release is created, the GitHub action will be triggered to publish to Pypi. The release version will be used to create the Pypi package.

If the Pypi release failed, make fixes, [delete the GitHub release](https://help.github.com/en/enterprise/2.16/user/github/administering-a-repository/editing-and-deleting-releases#:~:text=Deleting%20a%20release,-Tip%3A%20You%20must&text=Under%20your%20repository%20name%2C%20click%20Releases.,of%20the%20page%2C%20click%20Delete.), and recreate a release with the same version again.

## Additional Documentation

 * [LinkML for environmental and omics metadata](https://docs.google.com/presentation/d/1xK__vZdv0jHtOu0eOTzGUJeDt9YMVOGR1jxIXTtdXDM/edit?usp=sharing)

## History

This framework used to be called BiolinkML. LinkML replaces BiolinkML.

For assistance in migration, see [Migration.md](Migration.md)

## Example Projects

Note: this list will be replaced by the [linkml registry](https://github.com/linkml/linkml-registry)

 * [Biolink Model](https://github.com/biolink/biolink-model) -- this was the original linkml project
 * [National Microbiome Data Collaborative](https://github.com/microbiomedata/nmdc-metadata)
 * [Sequencing Metadata Alignment Project](https://github.com/microbiomedata/metadata_converter)
 * [SSSOM Schema](https://sssom-py.readthedocs.io/)
 * [Knowledge Graph Change Language](https://cmungall.github.io/ontology-change-language/)
 * https://github.com/diatomsRcool/collections-attribution-model
 * https://github.com/cmungall/dasher/tree/master/src/schema
 * [Cancer Research Data Commons - Harmonized Model](https://cancerdhc.github.io/ccdhmodel/), developed by the NIH [Center for Cancer Data Harmonization](https://harmonization.datacommons.cancer.gov/)
 * [HOT Ecocystem termCI model](https://github.com/HOT-Ecosystem/TermCI-model)
