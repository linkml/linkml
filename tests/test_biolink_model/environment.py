import os

from tests.utils.test_environment import TestEnvironment

env = TestEnvironment(__file__)

if not getattr(env, "_checked", False):
    setattr(env, "_checked", True)
    # Check whether the biolink model is current
    import requests

    from linkml import BIOLINK_MODEL_URI

    actual_model_path = os.path.relpath(env.input_path('biolink-model.yaml'), env.cwd)
    if os.path.exists(actual_model_path):
        expected_model_path = BIOLINK_MODEL_URI + '.yaml'
        resp = requests.get(expected_model_path)
        if resp.ok:
            expected_biolink_model = resp.text
            with open(actual_model_path) as f:
                actual_biolink_model = f.read()
            if expected_biolink_model != actual_biolink_model:
                print(f"NOTE: test biolink model ({actual_model_path}) "
                      f"does not match online model ({expected_model_path})")
