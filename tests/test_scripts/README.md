# Script tests

This set of tests tries the various options of the generators. All of the inputs to this set of tests can be found
in the `input` directory, with the results being recorded in `output`

**Note:** Do NOT push the output directory.  The github actions will re-generate this directory whenever changes
are committed. While `output` is included in `.gitignore`, git will still try to include int in a submission.  An 
easy work-around for this is to issue
```bash
> git update-index --remove tests/test_scripts/output 
```
whenever `output` content starts showing as being changed