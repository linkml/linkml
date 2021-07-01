# Generator testing

All tests are based around the [kitchen_sink](input/kitchen_sink.yaml) schema

Note for testing

 * test_pythongen will create [kitchen_sink.py](output/kitchen_sink.py)
     * this is imported by other tests
     * if you change the yaml schema we recommend you run test_pythongen
     * it may be possible to get into a state where the generated python code has errors and you need to revert
    