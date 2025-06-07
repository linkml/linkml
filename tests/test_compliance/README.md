# Compliance Tests

This will become a comprehensive test of every LinkML feature for every supported framework/generator.

It also generates reports that can be used by LinkML users to determine if a given construct is supported
for validation for a framework of choice.

The compliance test suite will also generate a collection of example schemas and positive and negative
test files that can be examined, used in documentation, or reused in non-Python LinkML frameworks.
See [porting LinkML](https://linkml.io/linkml/howtos/port-linkml.html).

## How it works

We use pytest due to its ability to parametrize tests, and in particular generate combinatorial tests.
This is important for exhaustive testing of how different constructs combine. See for example the inlining
tests.

Each test corresponds to a particular linkml construct or feature and is parameterized by:

- schema parameters, that define different combinations of values for the metamodel element
- data parameters, that define different combinations of test data
- a generator/framework (e.g. pydantic, jsonschema)

Each test run corresponds to a particular combination of generator and schema parameters and data parameters, and will perform
two sets of test assertions:

- Does the generated output using the framework work, and does it contain the expected text/values?
- Does the example data validate or fail to validate as expected?

For efficiency, the schema tests are only performed once for any one schema combination.

As a side effect, the parameterized schema, generated artefacts, and test positive and negative test data
are written to the `output` folder. This can be used for documentation, or for porting LinkML to other
languages.

A number of reports are written:

- overall summary report, that indicates whether a feature is supported for a given framework
- coverage report (TODO):
    - what % of LinkML constructs are tested?
    - which generators are tested?
- markdown summary (TODO)

### Schema Tests

See code for examples

The basic idea is that a schema dictionary is created, including `_mapping` annotations that indicate
how this particular piece of the schema is meant to look when generated using a given framework

### Data Tests

See code for examples

Each positive or negative instance is tested for a given framework. The framework should validate positive
examples and fail to validate negative examples.

Note that we treat every framework as a potential validator; even if the primary goal of the pydantic
generator is to create useful classes for programming, it can also serve as a validator.

An additional category is "coercion", where the framework accepts formally invalid data casts/coerces/repairs
it to the normative type. So called "Postelian mode". In some cases, the framework will accept it "as if" it
is coerced. For example, json-schema validators will accept ints where the range is a float ("pre-coercion").

Note that we do not expect every framework to validate every feature fully

- JSON-Schema by its nature will not detect dangling foreign keys or uniqueness constraints
- The Python dataclasses framework is design to perform maximal coercion
- SQLite does not support enums
- etc

A report is generate that allows users to see precisely what the expected behavior is for any given
construct in any framework.

Note for some frameworks no data validation is performed. This will later be synced with ongoing work
with the LinkML validator.


## Troubleshooting

If you make a change to a generator then it may cause one of the tests here to fail. E.g. a test may
make syntactic assumptions. We try and find a balance between rigor and rigidity, so this should not
happen too frequently for stable generators.

## Adding Tests

When adding a test for a new schema feature, follow the structure of the existing tests.
These have two blocks: the first generates the schema (possibly from parameters), and then
generates output from that schema using different generators using `validated_schema`.

The second part generates test data, and then runs the tests using `check_data`

Be sure to pass in the correct test name as a first argument to `validated_schema`; this quick check
can ensure you are not accidentally importing from elsewhere:

```
grep "from tests.test_compliance.test_compliance_ import" tests/test_compliance/*py
```

## A note on OWL tests

Currently data validation using OWL is off by default, and data tests pass.

In order to run the OWL tests, you should have ROBOT in your path. The unit test
suite will then generate turtle files containing both ontology and data, and
use HermiT to validate. Note this is currently slow.
