This folder contains a FOL specification of the linkml semantics.

The semantics are specified by the rules in
[linkml.pro](linkml.pro). This rules operate over a set of
ground predicates such as is_a/2, class/1, which are generated from a
linkml yaml file using gen-lp, e.g.:

    pipenv run python3 linkml/generators/lpgen.py tests/test_biolink_model/yaml/biolink-model.yaml > semantics/tests/biolink.pro

See [semantics/tests/biolink.pro](tests/biolink.pro) for an
example.

The rules can be used with any logic programming system. NAF or WFS
both fine (TODO: check this claim). The rules are stratified such that
SLD resolution/backtracking can be used if preferred.

For convenience, wrappers for swi-prolog are provided. To run these
you will need to install swi-prolog (v8 series) and to be on a system
with shell.

We include [tests](tests) both as a means to validate the semantics and the
biolink model, but also as examples of the intended semantics of
linkml.

To run a test you can use the Makefile, from this repo run:

    make test-subclass_of

Substituting `subclass_of` with the name of the test.

TODO: instructions on how to validate
