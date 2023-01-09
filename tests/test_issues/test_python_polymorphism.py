import  unittest

from linkml.generators.pythongen import PythonGenerator

from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase
from linkml_runtime.utils.compile_python import compile_python
from linkml.validators import JsonSchemaDataValidator
from linkml_runtime.utils.schemaview import SchemaDefinition, SchemaView
from .model.polymorphism_schema import gen_person_and_organisation_example_data, gen_person_and_organisation_schema, gen_type_hierarchy_example_schema
import json

class PydanticPolymorphismTestCase(TestEnvironmentTestCase):
    env = env

    def test_pythongenerator_loads_poly(self):
        gen = PythonGenerator(gen_person_and_organisation_schema())
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        json_data = json.loads(gen_person_and_organisation_example_data())
        cont = mod.Container(**json_data)
        self.assertEquals(len([x for x in cont.things if type(x) == mod.Person]),1)
        self.assertEquals(len([x for x in cont.things if type(x) == mod.Organisation]),1)
    
    def test_type_hierarchy(self):
        gen_range_not_specified = PythonGenerator(gen_type_hierarchy_example_schema())
        output = gen_range_not_specified.serialize()
        with open("/tmp/python-dataclass-out.py","w") as f:
            f.write(output)
        mod = compile_python(output, "testschema")
        _ = mod.Person(id=1)
        _ = mod.Person(id=2,category='http://example.org/Person')
        _ = mod.Person(id=3,category='x:Person')
        self.assertRaises(ValueError, lambda: mod.Person(id=7, category='x:NamedThing'))

    
    def test_class_instantiation_without_designator(self):
        gen = PythonGenerator(gen_person_and_organisation_schema())
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        person = mod.Person(height=80,full_name="Frank", id=1)
        organisation =mod.Organisation(number_of_employees=70, id=2)
        named = mod.NamedThing(full_name="banana", id=3)
        self.assertEqual(person.height, 80)
        self.assertEqual(organisation.number_of_employees,70)
        self.assertTrue(type(named) == mod.NamedThing)
        self.assertEqual(named.thingtype,"x:NamedThing")
        self.assertEqual(person.thingtype,"http://testbreaker/not-the-uri-you-expect")
        self.assertEqual(organisation.thingtype,"x:Organisation")
        forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="x:ForProfit")
        self.assertIsInstance(forProfit, mod.ForProfit)
        forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="http://example.org/ForProfit")
        self.assertIsInstance(forProfit, mod.ForProfit)

    def test_type_designator_ranges(self):
        gen = PythonGenerator(gen_person_and_organisation_schema("uri"))
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="x:ForProfit")
        self.assertIsInstance(forProfit, mod.ForProfit)
        forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="http://example.org/ForProfit")
        self.assertIsInstance(forProfit, mod.ForProfit)
        gen = PythonGenerator(gen_person_and_organisation_schema("string"))
        output = gen.serialize()
        mod = compile_python(output, "testschema")
        forProfit = mod.Organisation(id=5, number_of_employees=1, thingtype="ForProfit")
        self.assertIsInstance(forProfit, mod.ForProfit)

