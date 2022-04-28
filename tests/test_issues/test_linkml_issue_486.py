import unittest


from linkml_runtime.linkml_model import SlotDefinition
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.get("/linkml_slot/", response_model=SlotDefinition)
async def linkml_slot(name: str):
    slot = SlotDefinition(name, description='foo')
    return slot

client = TestClient(app)


class FastAPICase(unittest.TestCase):

    def test_fastapi_basic(self):
        """
        Test basic fastAPI functionality

        Taken from https://fastapi.tiangolo.com/tutorial/testing/

        This is expected to succeed
        """
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test_fastapi_with_linkml(self):
        """
        Test for https://github.com/linkml/linkml/issues/486

        Currently fails with

        ```
        TypeError: non-default argument 'mixins' follows default argument
        ```
        """
        response = client.get("/linkml_slot/")
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()
