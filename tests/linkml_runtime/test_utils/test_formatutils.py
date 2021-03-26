import unittest

from linkml_runtime.utils.formatutils import camelcase, underscore, lcamelcase, be, split_line, wrapped_annotation


class FormatUtilsTestCase(unittest.TestCase):
    def test_formats(self):
        self.assertEqual("ThisIsIt", camelcase("this is it"))
        self.assertEqual("ThisIsIT", camelcase("  this   is iT   "))
        self.assertEqual("IBeY", camelcase("i be y "))
        self.assertEqual("ThisIsIt", camelcase("This__is_it"))

        self.assertEqual("this_is_it", underscore(" this is it "))
        self.assertEqual("this_is_it", underscore("this   is   it"))

        self.assertEqual("thisIsIt", lcamelcase("   this   is\t  it\n"))

        self.assertEqual('abc', be('  abc\n'))
        self.assertEqual('', be(None))
        self.assertEqual('', be('   '))

    def test_linestuff(self):
        text = "This is a mess'o test that goes on for a long way.  It has some carriage\n returns embedded in it " \
               "but otherwise it drags on and on and on until the cows come home.  Splitline covers this we hope."
        self.assertEqual(["This is a mess'o test that goes on for a long way. It has some carriage returns embedded"
                          " in it but otherwise it ",
                          'drags on and on and on until the cows come home. Splitline covers this we hope. '],
                         split_line(text))
        self.assertEqual(["This is a mess'o ", 'test that goes on ', 'for a long way. It ', 'has some carriage ',
                          'returns embedded in ', 'it but otherwise it ', 'drags on and on and ', 'on until the cows ',
                          'come home. ', 'Splitline covers ', 'this we hope. '], split_line(text, 20))
        self.assertEqual(['X' * 100 + ' '], split_line('X'*100, 20))
        self.assertEqual("""This is a mess'o test that goes on for a long way.  It has some carriage
	returns embedded in it but otherwise it drags on and on and on until the cows come home. Splitline covers this we 
	hope. """, wrapped_annotation(text))



if __name__ == '__main__':
    unittest.main()
