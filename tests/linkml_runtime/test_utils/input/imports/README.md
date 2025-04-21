A tree of imports like:

```
main
|- linkml:types
|- s1
|  |- s1_1
|  |- s1_2
|     |- s1_2_1
|        |- s1_2_1_1
|           |- s1_2_1_1_1
|           |- s1_2_1_1_2
|- s2
|  |- s2_1
|  |- s2_2
|- s3
   |- s3_1
   |- s3_2
```

This is used to test SchemaView's logic for complex import hierarchies,
eg.
- overrides
- imports closure completeness
- (at some point) monotonicity
- etc. 

Currently, each schema...
- Contains one `Main` class with a value whose default is overridden to indicate which module defined it, this is used to test overrides.
- Contains a class like `S2` that carries the name of the module to ensure that unique classes are gotten from the whole tree
- Each node in the tree outwards from `main` will carry the 'special classes' from the parents, overriding them as with `main` to
  get a more detailed picture of override order: eg. `s1_2_1` will also define `S1_2` and override its `ifabsent` field, 
  which `S1_2` should override since it's the importing schema.