from bom_tools import read_bom_to_parts_store
import unittest


class TestBomReader(unittest.TestCase):
    def test_read_bom_to_parts_store(self):
        pds, mb = read_bom_to_parts_store("../examples/example_bom.csv")
