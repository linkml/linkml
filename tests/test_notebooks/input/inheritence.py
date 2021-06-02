from types import ModuleType

from jsonasobj2 import as_json, loads
from rdflib import Graph

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.shexgen import ShExGenerator
from linkml.generators.yumlgen import YumlGenerator
from linkml_runtime.utils.yamlutils import as_json_object as yaml_to_json

yaml = """
id: http://example.org/sample/example2
name: inheritence
prefixes:
    foaf: http://xmlns.com/foaf/0.1/
    ex: http://example.org/model/
    xsd: http://www.w3.org/2001/XMLSchema#

default_prefix: ex

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
    root:
        description: an empty class
        
    children:
        description: an identified class
        is_a: root
        slots:
            - root_id
            
    child_1:
        description: first child
        is_a: children
        
    child_2:
        description: second child
        is_a: children
        slots:
            - description
            
    child_2_1:
        description: grand child with a parent slot
        is_a: child_2
        
    child_2_2:
        description: grand child with parent and own slot
        is_a: child_2
        slots:
            - angry
            
slots:
    root_id:
        description: Unique identifier 
        identifier: true
        
    description:
        description: Text description of class
        required: true
        
    angry:
        description: angry grandchild
        range: boolean
        required: true
"""

print(f'<img src="{YumlGenerator(yaml).serialize()}"/>')
print(f'\n-----\n{YumlGenerator(yaml).serialize()}\n')

shex = ShExGenerator(yaml).serialize(collections=False)
print(shex)

# # Generate a person
# joe_smith = module.Person(id="42", last_name="smith", first_name=['Joe', 'Bob'], age=43)
# print(joe_smith)
#
# # Add the context and turn it into RDF
# jsonld = as_json_object(yaml_to_json(joe_smith, cntxt))
# print(jsonld)
# g = Graph()
# g.parse(data=jsonld, format="json-ld")
# print(g.serialize(format="turtle").decode())
#
# from pyshex.evaluate import evaluate
#
# r = evaluate(g, shex,
#              start="http://example.org/sample/example1/Person",
#              focus="http://example.org/context/42")
# print("Conforms" if r[0] else r[1])
