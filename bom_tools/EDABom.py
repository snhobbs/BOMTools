import re

def filter_non_purchased_bom(df):
    drop = []
    char_find = re.compile("[A-z]+")
    for i, row in df.iterrows():
        for pt in ["TP", "MH", "A"]:
            for ref in char_find.findall(row["ref-des"]):
                if pt.lower() == ref.lower():
                    drop.append(i)
                    break
    len_0 = len(df)
    df = df.drop(drop)
    assert(len(df) == len_0 - len(drop))
    return df


class EDABom:
    def __init__(self, df):
        eda = filter_non_purchased_bom(df)
        self._df = eda
