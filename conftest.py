# Root conftest: exclude files that break pytest --doctest-modules collection.
# - golanggen.py conflicts with the golanggen/ package directory
# - datasets.py and validation.py are generated files with broken imports
collect_ignore_glob = [
    "packages/linkml/src/linkml/generators/golanggen.py",
    "packages/linkml_runtime/src/linkml_runtime/linkml_model/datasets.py",
    "packages/linkml_runtime/src/linkml_runtime/linkml_model/validation.py",
]
