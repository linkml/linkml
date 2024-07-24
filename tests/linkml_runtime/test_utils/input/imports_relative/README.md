# Relative Imports test schemas

This tests the ability for schemaview to follow chains of relative imports - ie. that it resolves 
each schema's relative imports with respect to the *imported* schema rather than the *origin* schema.

This test case handles resolving relative imports in both directions, as well as neighboring directories
starting from `L0_0/L1_0_0/main.yaml` schema. Each directory is labeled with a "level" (`L{n}`) and a second number for 
the "column" of the directory - eg `L1_1_*` is within `L0_1`, and each subdirectory adds more children.

Note that this does **not** test that overrides are parsed correctly, that is tested in the `imports` directory
next to this - this is specifically about relative file handling (the same import ordering should happen regardless of
where the imports are located)

The schema in this directory make a graph like this, starting from main (as absolute paths)

```
main                            --> linkml:types
main                            --> L0_0/L1_0_0/neighbor
main                            --> L0_0/parent
main                            --> L0_1/cousin
main                            --> L0_0/L1_0_0/L2_0_0_0/child
main                            --> L0_0/L1_0_0/L2_0_0_1/child
L0_0/L1_0_0/neighbor            --> L0_0/neighborhood_parent
L0_0/parent                     --> L0_0/L1_0_1/L2_0_1_0/grandchild
L0_0/L1_0_1/L2_0_1_0/grandchild --> L0_0/parent
L0_1/cousin                     --> L0_1/L1_1_0/index
L0_1/L1_1_0/index               --> L0_1/L1_1_0/L2_1_0_0/index
L0_1/L1_1_0/index               --> L0_1/L1_1_0/L2_1_0_1/index
L0_1/L1_1_0/L2_1_0_0/index      --> L0_1/L1_1_0/L2_1_0_0/apple
L0_1/L1_1_0/L2_1_0_1/index      --> L0_1/L1_1_0/L2_1_0_1/banana
L0_0/L1_0_0/L2_0_0_0/child      --> L0_0/L1_0_1/dupe 
L0_0/L1_0_0/L2_0_0_1/child      --> L0_0/L1_0_1/dupe 

```

From the perspective of the main schema, we should end up with a resolved set of imports like:

```
- linkml:types'
- ../neighborhood_parent
- neighbor
- ../parent
- ../L1_0_1/L2_0_1_0/grandchild
- ../../L0_1/L1_1_0/L2_1_0_0/apple
- ../../L0_1/L1_1_0/L2_1_0_0/index
- ../../L0_1/L1_1_0/L2_1_0_1/banana
- ../../L0_1/L1_1_0/L2_1_0_1/index
- ../../L0_1/L1_1_0/index
- ../../L0_1/cousin
- ../L1_0_1/dupe
- ./L2_0_0_0/child
- ./L2_0_0_1/child
- main
```

(see the `imports` test directory and `test_imports_closure_order` for notes on ordering)

The specific things tested by the schemas are:
- same-directory import
- child directory import (`./`)
- parent directory import (`../`)
- double child and parent skips (`../../`, `./path/path`)
- schemas with duplicate names (`child.yaml`, `index.yaml`) that should all be imported
- multiple imports of the same schema (`dupe.yaml`)
- cycles: since importing will mutate the path, ensure that we don't end up importing the same schemas forever.