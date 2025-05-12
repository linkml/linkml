import json
import os

from rdflib import Graph, term


class RdfExpectations:
    """Calculates the expected RDF graph.
    It does not use for URI generation any of the code available in the `linkml`
    package on purpose to avoid bug contagion!"""

    _schema_yaml: dict = {}
    _g: Graph = Graph()
    _schema_uri: str = ""

    def __init__(self, schema_yaml, schema_jsonld):
        self._schema_yaml = schema_yaml
        self._g = Graph().parse(data=schema_jsonld, format="json-ld")
        if os.environ.get("DETAILED_OUTPUT"):
            print("ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️")
            print("ℹ️ℹ️      JSON-LD       ℹ️ℹ️")
            print(json.dumps(schema_jsonld, indent=2))
            print("ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️")
            print("🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢")
            print("🐢🐢 RDF Graph (Turtle) 🐢🐢")
            print(self._g.serialize(format="ttl"))
            print("🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢")

    def expected_id_uri(self):

        if "name" in self._schema_yaml:
            if ":" in self._schema_yaml["name"]:
                prefix = self._schema_yaml["name"].split(":")[0]
                self._schema_uri = self._schema_yaml["prefixes"][prefix] + self._schema_yaml["name"].split(":")[1]
            elif "default_prefix" in self._schema_yaml:
                self._schema_uri = (
                    self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]] + self._schema_yaml["name"]
                )
            else:
                self._schema_uri = self._schema_yaml["id"] + "/" + self._schema_yaml["name"]
        else:
            self._schema_uri = self._schema_yaml["id"]
        for subject, predicate in self._g.subject_predicates(
            object=term.URIRef("https://w3id.org/linkml/SchemaDefinition")
        ):
            assert str(subject) == self._schema_uri
            assert str(predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        return self._schema_uri

    def expected_namespaces(self):
        if "prefixes" in self._schema_yaml:
            namespaces = []
            for _, namespace in self._g.subject_objects(predicate=term.URIRef("http://www.w3.org/ns/shacl#namespace")):
                assert str(namespace) in self._schema_yaml["prefixes"].values()
                namespaces.append(str(namespace))
            assert set(self._schema_yaml["prefixes"].values()).issubset(namespaces)
            return namespaces

    def expected_classes(self):
        if "classes" in self._schema_yaml:
            schema_classes = []
            for class_name, cls in self._schema_yaml["classes"].items():
                if cls and "class_uri" in cls:
                    if ":" in cls["class_uri"]:
                        prefix = cls["class_uri"].split(":")[0]
                        class_uri = self._schema_yaml["prefixes"][prefix] + cls["class_uri"].split(":")[1]
                    elif "default_prefix" in self._schema_yaml:
                        class_uri = (
                            self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]]
                            + cls["class_uri"].split(":")[1]
                        )
                    else:
                        raise Exception(
                            "`class_uri` is neither a URI, nor a CURIE and "
                            + "no `default_prefix` is provided to create a CURIE"
                        )
                else:
                    if "default_prefix" in self._schema_yaml:
                        class_uri = self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]] + class_name
                    else:
                        class_uri = self._schema_yaml["id"] + "/" + class_name
                schema_classes.append(class_uri)
            schema_classes = set(schema_classes)
            found_classes = set(
                [
                    str(class_name)
                    for class_name in self._g.subject_objects(predicate=term.URIRef("https://w3id.org/linkml/classes"))[
                        1
                    ]
                ]
            )
            assert schema_classes == found_classes

    def expected_slots(self):
        if "slots" in self._schema_yaml:
            schema_slots = []
            for slot_name, slot in self._schema_yaml["slots"].items():
                if slot and "slot_uri" in slot:
                    if ":" in slot["slot_uri"]:
                        prefix = slot["slot_uri"].split(":")[0]
                        slot_uri = self._schema_yaml["prefixes"][prefix] + slot["slot_uri"].split(":")[1]
                    elif "default_prefix" in self._schema_yaml:
                        slot_uri = (
                            self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]]
                            + slot["slot_uri"].split(":")[1]
                        )
                    else:
                        raise Exception(
                            "`slot_uri` is neither a URI, nor a CURIE and "
                            + "no `default_prefix` is provided to create a CURIE"
                        )
                else:
                    if "default_prefix" in self._schema_yaml:
                        slot_uri = self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]] + slot_name
                    else:
                        slot_uri = self._schema_yaml["id"] + slot_name
                schema_slots.append(slot_uri)
            for _, slot_name in self._g.subject_objects(predicate=term.URIRef("https://w3id.org/linkml/slots")):
                assert str(slot_name) in schema_slots

    def expected_types(self):
        # TODO: test presence of types
        pass

    def expected_enums(self):
        # TODO: test presence of enums
        pass
