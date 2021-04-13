from bom_tools import generate_kicost_bom
import unittest


class TestBomCompiler(unittest.TestCase):
    def test_generate_kicost_bom(self):
        generate_kicost_bom("../examples/example_bom.csv")
