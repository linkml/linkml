all: test

TESTS = $(patsubst %_test, %, $(patsubst tests/%, %, $(basename $(shell ls tests/*_test.pro))))

test: $(patsubst %,test-%, $(TESTS))

test-%:
	./tests/run-test.sh tests/$*_test.pro

tests/biolink.pro:
	cd .. && pipenv run python3 linkml/generators/lpgen.py tests/test_biolink_model/yaml/biolink-model.yaml > semantics/$@

tests/biolink.sexpr:
	cd .. && pipenv run python3 linkml/generators/lpgen.py -f sexpr tests/test_biolink_model/yaml/biolink-model.yaml > semantics/$@

%-is-coherent: %.pro
	swipl  -l linkml.pro -g "['tests/std_header.pro'],['$<'],forall(nr_unsatisfiable(X),writeln(unsat(X))),forall(inconsistent(X),writeln(inconsistent(X)))"


x:
	echo $(TESTS)
