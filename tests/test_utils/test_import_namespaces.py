import unittest

from linkml.generators.shexgen import ShExGenerator
from tests.test_utils.environment import env


class URLImportTestCase(unittest.TestCase):

    @unittest.skipIf(False, "Finish implementing this")
    def test_import_from_url(self):
        """ Validate namespace bindings """
        shex = ShExGenerator(env.input_path('import_test_l2.yaml')).serialize()
        self.assertEqual("""BASE <http://example.org/l2/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX l1: <http://example.org/l1/>
PREFIX base: <http://example.org/b/>


l1:Int xsd:integer

base:String xsd:string

base:BaseClass CLOSED {
    (  $base:BaseClass_tes base:base_slot @base:String ? ;
       rdf:type [ base:BaseClass ] ?
    )
}

l1:L1Class  (
    CLOSED {
       (  $l1:L1Class_tes (  l1:l1_slot1 @base:String ? ;
             l1:l1_slot2 @l1:Int ?
          ) ;
          rdf:type [ l1:L1Class ] ?
       )
    } OR @<L2Class>
)

<L2Class> CLOSED {
    (  $<L2Class_tes> (  &l1:L1Class_tes ;
          rdf:type [ l1:L1Class ] ? ;
          <l2_slot1> @base:String ? ;
          <l2_slot2> @l1:Int ?
       ) ;
       rdf:type [ <L2Class> ] ?
    )
}""", shex.strip())


if __name__ == '__main__':
    unittest.main()
