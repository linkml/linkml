Modules for the split mode of the JSON Schema generator (`test_jsonschemagen_split.py`).

- `core.yaml` imports `control` and `vendor`, and is the module the tests start from.
- `control.yaml` imports `units`, so `units` reaches `core` only through it.
- `vendor.yaml` lives under another host, so references to it stay absolute.
- `notes.yaml` defines types only, so it gets no document of its own.
