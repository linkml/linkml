[![Pyversions](https://img.shields.io/pypi/pyversions/linkml.svg)](https://pypi.python.org/pypi/linkml)
![](https://github.com/linkml/linkml/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/linkml.svg)](https://pypi.python.org/pypi/linkml)

## [Binder Link](https://mybinder.org/v2/gh/linkml/linkml/main?filepath=notebooks)

# LinkML - Linked data Modeling Language

LinkML is a general purpose modeling language following object-oriented and ontological principles. LinkML models can be specified in YAML, JSON or RDF.

A variety of artefacts can be generated from the model:
- ShEx
- JSON Schema
- OWL
- Python dataclasses
- UML diagrams
- Markdown pages (for deployment in a GitHub pages site)

...and more.

The documentation can also be viewed on the [LinkML documentation](https://linkml.io/linkml/).

You can browse the metamodel component documentation [here](https://linkml.github.io/linkml-model/docs). LinkML is self-describing, but a few important vocabulary terms to keep in mind are:
- [ClassDefinition](https://linkml.github.io/linkml-model/docs/ClassDefinition): Component for defining Classes
- [SlotDefinition](https://linkml.github.io/linkml-model/docs/SlotDefinition): Component for defining Class Properties (or _Slots_)
- [TypeDefinition](https://linkml.github.io/linkml-model/docs/TypeDefinition): Component for defining Data Types
- [SchemaDefinition](https://linkml.github.io/linkml-model/docs/SchemaDefinition): Component for defining Schemas (combination of subset, type, slot, class)

Further details about the general design of LinkML can be found in the LinkML Modeling Language [Specification](SPECIFICATION.md).

As an example, LinkML has been used for the development of the [BioLink Model](https://biolink.github.io/biolink-model/), but the framework itself is general purpose and can be used for any kind of modeling. 
For an example Biolink metamodel, see this [Jupyter Notebook](https://github.com/linkml/linkml/blob/main/notebooks/examples.ipynb).

## Installation

This project uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) for installation. Some IDE's like PyCharm also have direct [support](https://www.jetbrains.com/help/pycharm/pipenv.html) for pipenv.

```bash
> pipenv install linkml
```

## Language Features

- Polymorphism/Inheritance, see [is_a](https://linkml.github.io/linkml-model/docs/is_a)
- [Abstract](https://linkml.github.io/linkml-model/docs/abstract) and [Mixin](https://linkml.github.io/linkml-model/docs/mixin) classes 
- Control JSON-LD mappings to URIs via [prefix](https://linkml.github.io/linkml-model/docs/prefixes) declarations 
- Ability to refine the meaning of a _slot_ in the context of a particular class via [slot usage](https://linkml.github.io/linkml-model/docs/slot_usage)

## Examples

LinkML can be used as a modeling language in its own right, or it can be compiled to other schema/modeling languages.

We will use the following simple schema for illustrative purposes:

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

Note that this schema does not illustrate the more advanced datamodel features like in [Biolink Model](https://biolink.github.io/biolink-model/docs/).

## Generators

### JSON Schema

[JSON Schema](https://json-schema.org/) is a schema language for JSON documents.

With the example `organization` [LinkML schema](https://github.com/linkml/linkml/blob/main/examples/organization.yaml) schema, we can illustrate the autogeneration of a
JSON Schema [output](https://github.com/linkml/linkml/blob/main/examples/organization.schema.json). You can run:

```bash
pipenv run gen-json-schema examples/organization.yaml
```

Note that any JSON that conforms to the derived JSON Schema can be converted to RDF using the derived JSON-LD context.

### JSON-LD Context

[JSON-LD context](https://www.w3.org/TR/json-ld/#the-context) provides mapping from JSON to RDF.

With the example `organization` [LinkML schema](examples/organization.yaml) schema, we can illustrate the autogeneration of a
JSON-LD context [output](examples/organization.context.jsonld). You can run:

```bash
pipenv run gen-jsonld-context examples/organization.yaml
```

You can control the output via [prefixes](https://linkml.io/linkml-model/docs/prefixes.html) declarations and [default_curi_maps](https://linkml.io/linkml-model/docs/default_curi_maps.html).

Any JSON that conforms to the derived JSON Schema (see above) can be converted to RDF using this context.

You can also combine a JSON instance file with a JSON-LD context using simple code or a tool like [jq](https://stackoverflow.com/questions/19529688/how-to-merge-2-json-objects-from-2-files-using-jq):

```bash
jq -s '.[0] * .[1]' examples/organization-data.json examples/organization.context.jsonld > examples/organization-data.jsonld
```

The above generated [JSON-LD](examples/organization-data.jsonld) file can be converted to other RDF serialization formats such as [N-Triples](examples/organization-data.nt). For example 
we can use [Apache Jena](https://jena.apache.org/documentation/io/) as follows:

```bash
riot examples/organization-data.jsonld > examples/organization-data.nt
```

### Python Dataclasses

With the example `organization` [LinkML schema](examples/organization.yaml) schema, we can illustrate the autogeneration of a
Python Dataclass [output](examples/organization.py). You can run:

```bash
pipenv run gen-py-classes examples/organization.yaml > examples/organization.py
```

<details>
<summary>Python Dataclass for `organization` schema</summary>
   
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
</details>

For more details see [PythonGenNotes](linkml/generators/PythonGenNotes.md).

The python object can be directly serialized as RDF.

### ShEx

[ShEx](http://shex.io/shex-semantics/index.html), short for Shape Expressions Language is a modeling language for RDF files.

With the example `organization` [LinkML schema](examples/organization.yaml) schema, we can illustrate the autogeneration of a
ShEx [output](examples/organization.shex). You can run:

```bash
pipenv run gen-shex examples/organization.yaml > examples/organization.shex
```

<details>
<summary>ShEx output for `organization` schema</summary>

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
</details>

### OWL

Web Ontology Language [OWL](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) is modeling language used to author ontologies.

With the example `organization` [LinkML schema](examples/organization.yaml) schema, we can illustrate the autogeneration of a
ShEx [output](examples/organization.owl.ttl). You can run:

```bash
pipenv run gen-owl examples/organization.yaml > examples/organization.owl.ttl
```

<details>
<summary>OWL output for `organization` schema</summary>

```turtle
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
</details>

## Generating Markdown documentation

The below command will generate a Markdown document for every class and slot in the model which can be used in a static site for ex., GitHub pages.

```bash
pipenv run gen-markdown examples/organization.yaml -d examples/organization-docs/
```

## Specification

See [specification](https://linkml.github.io/linkml/SPECIFICATION). Also see the [semantics](semantics) folder for an experimental specification in terms of FOL.

## FAQ

### Why not use X as the modeling framework?

Why invent our own yaml and not use JSON-Schema, SQL, UML, ProtoBuf, OWL, etc.?

Each of these is tied to a particular formalism. JSON Schema to
trees. OWL to open world logic. There are various impedance mismatches
in converting between these. The goal was to develop something simple
and more general that is not tied to any one serialization format or
set of assumptions.

There are other projects with similar goals for ex., [schema_salad](https://github.com/common-workflow-language/schema_salad). It may be possible to align with these.

### Why not use X as the datamodel?

Here X may be bioschemas, some upper ontology (BioTop), UMLS metathesaurus, bio*, and various other attempts to model all of biology in
an object model.

Currently, as far as we know there is no existing reference datamodel
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

### Release to PyPI

A Github action is set up to automatically release the package to PyPI. When it is ready
for a new release, create a [Github release](https://github.com/linkml/releases). The version
should be in the vX.X.X format following [the semantic versioning specification](https://semver.org/).

After the release is created, the GitHub action will be triggered to publish to Pypi. The release version will be used to create the Pypi package.

If the Pypi release failed, make fixes, [delete the GitHub release](https://help.github.com/en/enterprise/2.16/user/github/administering-a-repository/editing-and-deleting-releases#:~:text=Deleting%20a%20release,-Tip%3A%20You%20must&text=Under%20your%20repository%20name%2C%20click%20Releases.,of%20the%20page%2C%20click%20Delete.), and recreate a release with the same version again.

## Additional Documentation

[LinkML for environmental and omics metadata](https://docs.google.com/presentation/d/1xK__vZdv0jHtOu0eOTzGUJeDt9YMVOGR1jxIXTtdXDM/edit?usp=sharing)

## History

This framework used to be called BiolinkML. LinkML replaces BiolinkML. For assistance in migration, see [Migration.md](Migration.md).

## Example Projects

Note: this list will be replaced by the [linkml registry](https://github.com/linkml/linkml-registry)

- [Biolink Model](https://github.com/biolink/biolink-model) _the original LinkML project_
- [National Microbiome Data Collaborative](https://github.com/microbiomedata/nmdc-metadata)
- [Sequencing Metadata Alignment Project](https://github.com/microbiomedata/metadata_converter)
- [SSSOM Schema](https://sssom-py.readthedocs.io/)
- [Knowledge Graph Change Language](https://cmungall.github.io/ontology-change-language/)
- [Collections Attribution Model](https://github.com/diatomsRcool/collections-attribution-model)
- [dasher](https://github.com/cmungall/dasher/tree/master/src/schema)
- [Cancer Research Data Commons - Harmonized Model](https://cancerdhc.github.io/ccdhmodel/), developed by the NIH [Center for Cancer Data Harmonization](https://harmonization.datacommons.cancer.gov/)
- [HOT Ecocystem termCI model](https://github.com/HOT-Ecosystem/TermCI-model)
