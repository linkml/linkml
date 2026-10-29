These modules are the fixtures for the split mode of the JSON Schema generator, which `test_jsonschemagen_split.py` tests.

- `core.yaml` imports `control`, `vendor` and `notes`, and is the module the tests start from.
- `control.yaml` imports `units`, so `core` imports `units` only through `control`.
- `vendor.yaml` has its `id` under another host, so references to it stay absolute.
- `notes.yaml` defines types only, so it gets no document of its own.
