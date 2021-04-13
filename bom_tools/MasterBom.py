'''
Internal repersentation of a Bill of Materials
- Internal Part Number or mapping to manufacturer info
- Ref Des
- Assembly Code
 Combination of ref des and assembly code have to be unique
- Requires a Parts DataBase to get all the additional data from the code
'''
import pandas as pd # type: ignore


class MasterBom:
    def __init__(self):
        self._df = pd.DataFrame({"ref":[], "part":[], "assembly":[]})

    def __len__(self):
        return len(self._df)

    def add_line(self, line: tuple):
        new_row={"ref": line[0], "part": line[1], "assembly": line[2]}
        self._df = self._df.append(new_row, ignore_index=True)

    '''returns true if the combination of ref and assembly are unique'''
    def is_legal(self) -> bool:
        for i, pt in enumerate(self._df.ref):
            if len(self._df[self._df.ref == pt]) != len((self._df[self._df.ref == pt].assembly).unique()):
                return False
        return True
