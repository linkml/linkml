"""Class for validation of JSON-LD contexts."""

import json
import logging

from rdflib import Graph, term
from yaml import safe_load

LINKML_URI = "https://w3id.org/linkml"

logger = logging.getLogger(__name__)


class RdfExpectations:
    """Calculates the expected RDF graph.
    It does not use for URI generation any of the code available in the `linkml`
    package on purpose to avoid bug contagion!"""

    _schema_yaml: dict = {}
    _g: Graph = Graph()
    _schema_uri: str = ""

    def __init__(self, schema_path, schema_jsonld) -> None:
        # read in the raw schema and the JSON-LD
        self._read_yaml_file(schema_path)
        self._generate_rdf_graph(schema_jsonld)

    def _generate_rdf_graph(self, schema_jsonld) -> None:
        """Generate an RDF Graph object from a json string.

        :param schema_jsonld: JSON-LD schema
        :type schema_jsonld: _type_
        """
        self._g = Graph().parse(data=schema_jsonld, format="json-ld")
        logger.info("ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️")
        logger.info("ℹ️ℹ️      JSON-LD       ℹ️ℹ️")
        logger.info(json.dumps(schema_jsonld, indent=2))
        logger.info("ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️ℹ️")
        logger.info("🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢")
        logger.info("🐢🐢 RDF Graph (Turtle) 🐢🐢")
        logger.info(self._g.serialize(format="ttl"))
        logger.info("🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢🐢")

    def _read_yaml_file(self, schema_path) -> None:
        """Read a LinkML schema as YAML.

        :param schema_path: path to the YAML file
        :type schema_path: _type_
        """
        logger.info(f"\n‼️‼️‼️ Processing '{schema_path}' ‼️‼️‼️")

        with open(schema_path) as schema_file:
            self._schema_yaml = safe_load(schema_file)

    def check_expectations(self) -> None:
        """Run standard checks of the generated JSON-LD graph against the source YAML."""
        self.expected_id_uri()
        self.expected_namespaces()
        self.expected_classes()
        self.expected_slots()

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
        for subject, predicate in self._g.subject_predicates(object=term.URIRef(f"{LINKML_URI}/SchemaDefinition")):
            assert str(subject) == self._schema_uri
            assert str(predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        return self._schema_uri

    def expected_namespaces(self):
        if "prefixes" in self._schema_yaml:
            rdf_namespaces = {
                str(ns)
                for _, ns in self._g.subject_objects(predicate=term.URIRef("http://www.w3.org/ns/shacl#namespace"))
            }
            assert rdf_namespaces == set(self._schema_yaml["prefixes"].values())

    def expected_classes(self):
        if "classes" in self._schema_yaml:
            schema_classes = set()
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
                            "`class_uri` is neither a URI nor a CURIE and "
                            + "no `default_prefix` is provided to create a CURIE"
                        )
                else:
                    if "default_prefix" in self._schema_yaml:
                        class_uri = self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]] + class_name
                    else:
                        class_uri = self._schema_yaml["id"] + "/" + class_name
                schema_classes.add(class_uri)
            assert schema_classes == {
                str(cls_name) for _, cls_name in self._g.subject_objects(predicate=term.URIRef(f"{LINKML_URI}/classes"))
            }

    def expected_slots(self):
        if "slots" in self._schema_yaml:
            schema_slots = set()
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
                            "`slot_uri` is neither a URI nor a CURIE and "
                            + "no `default_prefix` is provided to create a CURIE"
                        )
                else:
                    if "default_prefix" in self._schema_yaml:
                        slot_uri = self._schema_yaml["prefixes"][self._schema_yaml["default_prefix"]] + slot_name
                    else:
                        slot_uri = self._schema_yaml["id"] + slot_name
                schema_slots.add(slot_uri)
            assert schema_slots == {
                str(slot_name) for _, slot_name in self._g.subject_objects(predicate=term.URIRef(f"{LINKML_URI}/slots"))
            }
