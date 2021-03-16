# Making changes to the underlying model

## Steps
1. Edit [tests/input/meta.yaml](), [tests/input/includes/types.yaml]() and/or [tests/input/includes/mappings.yaml]().
  Be sure to update the version # if the changes are significant using SemVer rules.
2. Run [tests/newmodel.sh]().  This copies ALL changes in the test directory up to the base directory.
3. Run *all* unit tests in `tests/test_base`.  Make sure that all changes are as expected.
4. Run [tests/newmodel.sh]() a second time.
5. Run ALL unit tests and verify that everything passes and all changes are expected.

## Notes
* The testing philosophy in this package is `"If there isn't a test for it, it doesn't exist".`  If, for instance,
a new type is introduced in types.yaml, tests need to be added in the appropriate spot (either test_issues or a basic
test package).  It is the developer's responsibility to assure that if, at a later date, a developer says "What is this for?
What happens if I remove it?" the removal or other change in behavior will result in a testing failure.  If not, the
change can be considered accidental and can be changed or removed w/o concern.
