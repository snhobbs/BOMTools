'''
bom_compiler.py
Takes a master BOM and generates different types.
'''
import click, os, pandas, io, csv
from . import MasterBom, tools, PartsDataStore


def sort_by_parts(df):
    return tools.group_by(df, "mfr-num", "ref-des")


class Bom:
    @classmethod
    def read_csv(cls, fname):
        return Bom(pandas.read_csv(fname, header=0, skipinitialspace=True, index_col=0, sep=";", comment="#", quotechar='"', quoting=csv.QUOTE_MINIMAL, engine="python"))

    def __init__(self, df):
        self.df = df
        self.parts_frame = sort_by_parts(self.df)


@click.group()
def gr1():
    pass

'''
Three columns manf#, refs, qty
'''
@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command()
def kicost(master):
    bom = Bom.read_csv(master)
    fname = master + 'kicost.csv'
    lines = []
    for mfr_num, ref_des in zip(bom.parts_frame["mfr-num"], bom.parts_frame["ref-des"]):
        lines.append("%s,%d,%s"%(mfr_num, len(ref_des), " ".join(ref_des)))

    with open(fname, "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    gr1()
