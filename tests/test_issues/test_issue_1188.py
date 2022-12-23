import os.path
import unittest

from linkml_runtime.loaders import YAMLLoader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env


schema_str = """id: https://examples.r.us/lister
name: lister

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://examples.r.us/lister/

imports:
  - linkml:types

classes:
  C1:
    description: class with an inline list of strings
    attributes:
        thelist:
            multivalued: true
            
  C1i:
    description: class with a list of integers
    attributes:
        thelist:
            multivalued: true
            range: integer
            
  C2:
    description: |-
        class with an inline list of unkeyed classes. Note that ~line 821 in pythongen states that first 
        required field should be key.
    attributes:
        thelist:
            range: UnkeyedClass
            multivalued: true
            inlined_as_list: true
            
  C3:
    description: class with an inline list of keyed classes
    attributes:
        thelist:
            range: KeyedClass
            multivalued: true
            inlined: true
            
  FourClasses:
    description: an upper level container for the above defs
    attributes:
        c1_slot:
            range: C1
            inlined: true
        c1i_slot:
            range: C1i
            inlined: true
        c2_slot:
            range: C2
            inlined: true
        c3_slot:
            range: C3
            inlined: true
            
  FourClassesMulti:
    description: an upper level container for the above defs
    attributes:
        c1_slot:
            range: C1
            inlined: true
            multivalued: true
        c1i_slot:
            range: C1i
            inlined: true
            multivalued: true
        c2_slot:
            range: C2
            inlined: true
            multivalued: true
        c3_slot:
            range: C3
            inlined: true
            multivalued: true
            
  UnkeyedClass:
    description: class without a key.  
    attributes:
        member1:
            required: true
        member2:
        
  KeyedClass:
    description: class with a key
    attributes:
        id:
            identifier: true
        member11:
            required: true
        member12:
"""

input_1 = """
- abc
- def
- ghi
"""

input_1i = """
[1, 27, -12, 0]
"""

input_2 = """
- member1: i2_i1_m1
  member2: i2_i1_m2
- member1: i2_i2_m1
  member2: i2_i2_m2
"""

input_3 = """
- id: i3_i1_id
  member11: i3_i1_member11
  member12: i3_i1_member12
- id: i3_i2_id
  member11: i3_i2_member11
  member12: i3_i2_member12
"""

input_three_classes = """
c1_slot: 
  - abc
  - def
  - ghi
c1i_slot: [1, 27, -12, 0]
c2_slot:
  - member1: i2_i1_m1
    member2: i2_i1_m2
  - member1: i2_i2_m1
    member2: i2_i2_m2
c3_slot:
  - id: i3_i1_id  
    member11: i3_i1_member11  
    member12: i3_i1_member12  
  - id: i3_i2_id  
    member11: i3_i2_member11  
    member12: i3_i2_member12  
"""

input_three_classes_multi = """
c1_slot: 
  - [abc, def, ghi]
  - [jkl]
c2_slot:
  -
    - member1: i2_s1_i1_m1
      member2: i2_s1_i1_m2
    - member1: i2_s1_i2_m1
      member2: i2_s1_i2_m2
  -
    - member1: i2_s2_i2_m1
      member2: i2_s2_i2_m2
c3_slot:
  - i3_s1_i1_id:  
      member11: i3_s1_i1_member11  
      member12: i3_s1_i1_member12  
  - i3_s2_i1_id:  
      member11: i3_s2_i1_member11  
      member12: i3_s2_i1_member12 
    i3_s2_i2_id:  
      member11: i3_s2_i2_member11  
      member12: i3_s2_i2_member12  
    
"""

UPDATE_PYTHON = True
# If you need to debug, you can uncomment this line and switch from self.mod to issue_1188 for imports
# Example
#     from .output.issue_1188 import issue_1188
#     instance = YAMLLoader().load_any(input_three_classes_multi, issue_1188.FourClassesMulti, base_dir=env.cwd)

class InlineListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        gen = PythonGenerator(schema_str, metadata=False)
        output = gen.serialize()
        if UPDATE_PYTHON:
            # Create a readable image of the output for debugging purposes
            issue_1188_directory = os.path.join(env.outdir, 'issue_1188')
            init_file = os.path.join(issue_1188_directory, '__init__.py')
            python_file = os.path.join(issue_1188_directory, 'issue_1188.py')
            os.makedirs(issue_1188_directory, exist_ok=True)
            if not os.path.exists(init_file):
                with open(init_file, 'w'):
                    pass
            with open(python_file, 'w') as pyfile:
                pyfile.write(output)
            print(f"{os.path.relpath(python_file, env.cwd)} created")
        cls.mod = compile_python(output)

    def test_root_inline(self):
        """ Test a list of strings as a root node """
        instance = YAMLLoader().load_any(input_1, self.mod.C1, base_dir=env.cwd)
        self.assertEqual(['abc', 'def', 'ghi'], instance.thelist)
        instance = YAMLLoader().load_any(input_1i, self.mod.C1i, base_dir=env.cwd)
        self.assertEqual([1, 27, -12, 0], instance.thelist)

    def test_root_inline_unkeyed(self):
        """ Test a list of inlined unkeyed classes as a root node """
        instance = YAMLLoader().load_any(input_2, self.mod.C2, base_dir=env.cwd)
        self.assertEqual('i2_i2_m2', instance.thelist[1].member2)

    def test_root_inlined_keyed(self):
        """ Test a list of inlined keyed structures as the root node """
        instance = YAMLLoader().load_any(input_3, self.mod.C3, base_dir=env.cwd)
        self.assertEqual('i3_i2_member12', instance.thelist['i3_i2_id'].member12)

    def test_three_classes(self):
        """ Test various inlined lists as slots IN a root node w/ single occurrences """
        # instance = YAMLLoader().load_any(input_three_classes, self.mod.FourClasses, base_dir=env.cwd)
        from .output.issue_1188 import issue_1188
        instance = YAMLLoader().load_any(input_three_classes, issue_1188.FourClasses, base_dir=env.cwd)
        self.assertEqual(['abc', 'def', 'ghi'], instance.c1_slot.thelist)
        self.assertEqual([1, 27, -12, 0], instance.c1i_slot.thelist)
        self.assertEqual('i2_i2_m2', instance.c2_slot.thelist[1].member2)
        self.assertEqual('i3_i2_member12', instance.c3_slot.thelist['i3_i2_id'].member12)

    def test_three_classes_multi(self):
        """ Test various inlined lists as slots in a root node w/ multi occurrences """
        # instance = YAMLLoader().load_any(input_three_classes_multi, self.mod.FourClassesMulti, base_dir=env.cwd)
        from .output.issue_1188 import issue_1188
        instance = YAMLLoader().load_any(input_three_classes_multi, issue_1188.FourClassesMulti, base_dir=env.cwd)
        self.assertEqual(['jkl'], instance.c1_slot[1].thelist)
        self.assertEqual('i2_s2_i2_m2', instance.c2_slot[1].thelist[0].member2)



if __name__ == '__main__':
    unittest.main()
