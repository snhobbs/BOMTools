import unittest
from bom_tools import MasterBom

class TestMasterBom(unittest.TestCase):
    def test_add_line(self):
        mb = MasterBom()
        mb.add_line((1,1,1))
        print(mb._df)
        self.assertEqual(len(mb), 1)

    # Single entry is legal
    def test_is_legal_passes(self):
        mb = MasterBom()
        mb.add_line((1,1,1))
        self.assertTrue(mb.is_legal())

    # Conflicting entries are not legal
    def test_is_legal_fails(self):
        mb = MasterBom()
        mb.add_line((1,1,1))
        mb.add_line((1,3,1))
        self.assertFalse(mb.is_legal())

    # Multiple entries with different parts legal
    def test_is_legal_different_parts(self):
        mb = MasterBom()
        mb.add_line((1,1,1))
        mb.add_line((1,12,3))
        self.assertTrue(mb.is_legal())

