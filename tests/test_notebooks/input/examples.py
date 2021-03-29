from types import ModuleType

from jsonasobj import as_json, loads
from rdflib import Graph

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.yumlgen import YumlGenerator
from linkml.utils.yamlutils import as_json_object as yaml_to_json

yaml = """
id: http://example.org/sample/example1
name: synopsis2
prefixes:
    foaf: http://xmlns.com/foaf/0.1/
    samp: http://example.org/model/
    xsd: http://www.w3.org/2001/XMLSchema#

default_prefix: samp

default_curi_maps:
    - semweb_context

default_range: string

types:
    string:
        base: str
        uri: xsd:string
    int:
        base: int
        uri: xsd:integer
    boolean:
        base: Bool
        uri: xsd:boolean


classes:
    person:
        description: A person, living or dead
        slots:
            - id
            - first name
            - last name
            - age
            - living
            - knows

    friendly_person:
        description: Any person that knows someone
        is_a: person
        slot_usage:
            knows:
                required: True

slots:
    id:
        description: Unique identifier of a person
        identifier: true

    first name:
        description: The first name of a person
        slot_uri: foaf:firstName
        multivalued: true

    last name:
        description: The last name of a person
        slot_uri: foaf:lastName
        required: true

    living:
        description: Whether the person is alive
        range: boolean
        comments:
            - unspecified means unknown

    age:
        description: The age of a person if living or age of death if not
        range: int
        slot_uri: foaf:age

    knows:
        description: A person known by this person (indicating some level of reciprocated interaction between the parties).
        range: person
        slot_uri: foaf:knows
        multivalued: true
"""
python_src = PythonGenerator(yaml).serialize()
print(python_src)
spec = compile(PythonGenerator(yaml).serialize(), 'test', 'exec')
module = ModuleType('test')
exec(spec, module.__dict__)

print(f'<img src="{YumlGenerator(yaml).serialize()}"/>')
print(f'\n-----\n{YumlGenerator(yaml).serialize()}\n')

cntxt = loads(ContextGenerator(yaml).serialize(base="http://example.org/people/"))
print(as_json(cntxt))

shex = ShExGenerator(yaml).serialize(collections=False)
print(shex)


# Generate a person
joe_smith = module.Person(id="42", last_name="smith", first_name=['Joe', 'Bob'], age=43)
print(joe_smith)

# Add the context and turn it into RDF
jsonld = as_json(yaml_to_json(joe_smith, cntxt))
print(jsonld)
g = Graph()
g.parse(data=jsonld, format="json-ld")
print(g.serialize(format="turtle").decode())

from pyshex.evaluate import evaluate
r = evaluate(g, shex,
             start="http://example.org/sample/example1/Person",
             focus="http://example.org/context/42")
print("Conforms" if r[0] else r[1])
