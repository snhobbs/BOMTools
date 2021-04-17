'''
Internal repersentation of a Bill of Materials
- Internal Part Number or mapping to manufacturer info
- Ref Des
- Assembly Code
 Combination of ref des and assembly code have to be unique
- Requires a Parts DataBase to get all the additional data from the code
'''
import pandas as pd # type: ignore
import numpy as np # type: ignore
import spreadsheet_wrangler

class MasterBom:
    def __init__(self, df=None):
        if df is None:
            df = pd.DataFrame({"ref-des":[], "pn":[], "assembly":[]})
        self._df = pd.DataFrame(df)

    def __len__(self):
        return len(self._df)

    def add_line(self, line: tuple):
        new_row={"ref-des": line[0], "pn": line[1], "assembly": line[2]}
        self._df = self._df.append(new_row, ignore_index=True)

    '''returns true if the combination of ref and assembly are unique'''
    def is_legal(self) -> bool:
        for column in self._df.columns:
            for pt in column:
                if type(pt) not in (str, int, float, np.int64, np.float64):
                    return False
        for pt in self._df["assembly"].unique():
            assembly_df = self._df[self._df["assembly"] == pt]
            if not assembly_df["ref-des"].is_unique:
                return False
        return True

    def get_assembly(self, assembly):
        return spreadsheet_wrangler.filter_df(self._df, on="pn", value=assembly, column="ref-des", blank_defaults=True)
