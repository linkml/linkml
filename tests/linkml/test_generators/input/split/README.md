# Split generation test case

Test that pydantic generator can correctly generate split schemas -
rather than rolling all classes/slots into a single module, generate them
in modules for each imported schema.

- Detect all imported classes
- Create correct relative imports
- Don't include all classes, only those that are actually used
