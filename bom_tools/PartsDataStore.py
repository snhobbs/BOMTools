import pandas as pd


'''Contains all the data necessary to do a part lookup. Index into this with a code.
This could be the manufacturers number but there could be multiples of that. Store
an internal part number for that.

This could be an accessor for a database or a flat file or whatever
- Internal part number: pn
- Manufacturer name: mfr
- Manfuacturers number: mfr-num
- Notes/Description: notes
'''
class PartsDataStore:
    def __init__(self, df=None):
        if df is None:
            df = pd.DataFrame({"pn":[], "mfr":[], "mfr-num":[]})
        self._df = pd.DataFrame(df)

    '''return the lines found that matches the value in the given column'''
    def get_part_line(self, code, column="pn"):
        return (self._df.loc[self._df[column] == code])

    def __len__(self):
        return len(self._df)
