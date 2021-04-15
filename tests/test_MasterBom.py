import unittest
from bom_tools import MasterBom
import logging

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

    def test_get_assembly_no_overlap_single_assembly(self):
        mb = MasterBom()
        mb.add_line(("1",12,None))
        mb.add_line(("2",12,None))
        mb.add_line(("3",12,None))
        mb.add_line(("4",12,None))
        mb.add_line(("5",12,None))
        mb.add_line(("6",12,None))
        mb.add_line(("7",12,None))

        assembly = mb.get_assembly(12)
        self.assertEqual(len(assembly), len(mb))

    def test_get_assembly_no_overlap_multiple_assembly(self):
        mb = MasterBom()
        mb.add_line(("1",12,None))
        mb.add_line(("2",12,None))
        mb.add_line(("3",12,None))
        mb.add_line(("4",12,None))
        mb.add_line(("5",12,None))
        mb.add_line(("6",12,None))
        mb.add_line(("7",12,None))
        mb.add_line(("8",11,12))
        mb.add_line(("8",1,1))

        assembly = mb.get_assembly(12)
        self.assertEqual(len(assembly), 8)

        assembly = mb.get_assembly(1)
        self.assertEqual(len(assembly), 8)

    def test_get_assembly_overlap_multiple_assembly(self):
        mb = MasterBom()
        mb.add_line(("1",12,None))
        mb.add_line(("2",12,None))
        mb.add_line(("3",12,None))
        mb.add_line(("4",12,None))
        mb.add_line(("5",12,None))
        mb.add_line(("6",12,None))
        mb.add_line(("7",12,None))
        mb.add_line(("7",1,1))
        mb.add_line(("8",11,12))
        mb.add_line(("8",1,1))

        assembly = mb.get_assembly(12)
        self.assertEqual(len(assembly), 8)

        assembly = mb.get_assembly(1)
        self.assertEqual(len(assembly), 8)

    '''
    def test_parts_bom_grouping(self):
        mb = MasterBom()
        mb.add_line(("1",1,None))
        mb.add_line(("2",1,None))
        mb.add_line(("3",1,None))
        mb.add_line(("4",12,None))
        mb.add_line(("5",3,None))
        pb = mb.parts_frame()
        logging.log(0, pb)
        print(pb)
        self.assertEqual(len(pb), 3)
        self.assertEqual(list(pb["ref-des"])[0], 3)
    '''

