'''
Internal repersentation of a Bill of Materials
- Internal Part Number or mapping to manufacturer info
- Ref Des
- Assembly Code
 Combination of ref des and assembly code have to be unique
- Requires a Parts DataBase to get all the additional data from the code
'''
import pandas as pd # type: ignore
import numpy as np
from bom_tools import tools

'''Remove the ref-des that are duplicates and have a universal config'''
def remove_overlapping_ref_des(df):
    if df["ref-des"].is_unique:
        return df
    for i, row in df.iterrows():
        ref = str(row["ref-des"])
        assembly = str(row["assembly"])
        if list(df["ref-des"]).count(ref) > 1 and len(assembly) > 0:
            df = df.drop(df.index[[i]])
    return df

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

    def parts_frame(self) -> pd.DataFrame:
        assert(self.is_legal())
        return self._df.group_by("pn")
        #return tools.group_by(self._df, "ref-des", "pn")

    '''Exclude all parts not marked for this assembly'''
    def get_assembly(self, assembly):
        # Cycle through selecting the parts marked explicitly
        filtered_df = self._df.loc[(self._df["assembly"] == assembly) | (self._df["assembly"].isnull())]
        return remove_overlapping_ref_des(filtered_df)
