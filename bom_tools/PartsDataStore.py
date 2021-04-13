import pandas as pd


'''Contains all the data necessary to do a part lookup. Index into this with a code.
This could be the manufacturers number but there could be multiples of that. Store
an internal part number for that.

This could be an accessor for a database
'''
class PartsDataStore:
    def __init__(self):
        self._df = pd.DataFrame({"pn":[], "manu-name":[], "manu-num":[]})

    '''return the lines found that matches the value in the given column'''
    def get_part_line(self, code, column="pn"):
        return self._df[self._df["column"] == code]
