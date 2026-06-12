from jsonasobj2 import loads
from rdflib import Namespace

from linkml.generators.shexgen import ShExGenerator

DCT = Namespace("http://purl.org/dc/terms/")


def test_dct_prefix(input_path):
    """Make sure prefixes are handled correctly"""
    # Issue_6.yaml declares a slot with an illegal ':' in its name.
    # SchemaLoader rejected it at load time; SchemaView-based generation
    # defers name validation to linkml-validate and generates regardless.
    loads(ShExGenerator(input_path("Issue_6.yaml"), format="json").serialize())
    shex = loads(ShExGenerator(input_path("Issue_6_fixed.yaml"), format="json").serialize())
    company_shape = [s for s in shex.shapes if "Company" in s.id][0]
    for expr in company_shape.expression.expressions:
        if expr.min == 0:
            assert str(DCT.created) == expr.predicate
            return
    assert False, "DCT.created predicate not found"
