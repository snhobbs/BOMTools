import pandas as pd
import unittest
from bom_tools import tools

class TestTools(unittest.TestCase):
    def test_groupby(self):
        df = pd.DataFrame({"a":[i for i in range(10)], "b":[i for i in range(10)], "c":[i for i in range(10)]})
        sort = tools.group_by(df, "c", "a")
        self.assertEqual(len(sort), 10) # independent values

    def test_groupby_duplicates(self):
        df = pd.DataFrame({"a":[i for i in range(10)], "b":[i for i in range(10)], "c":[i//2 for i in range(10)]})
        sort = tools.group_by(df, "c", "a")
        self.assertEqual(len(sort), 5) # grouped

    def test_groupby_sortby_duplicates(self):
        df = pd.DataFrame({"a":[i for i in range(10)], "b":[i for i in range(10)], "c":[i//2 for i in range(10)]})
        sort = tools.group_by(df, "a", "c")
        self.assertEqual(len(sort), 10) # independent values

    def test_groupby_same_duplicates(self):
        df = pd.DataFrame({"a":[i for i in range(10)], "b":[i for i in range(10)], "c":[i//2 for i in range(10)]})
        sort = tools.group_by(df, "c", "c")
        self.assertEqual(len(sort), 5) # grouped

if __name__ == "__main__":
    unittest.main()