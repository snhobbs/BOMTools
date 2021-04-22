'''
bom_compiler.py
Takes a bom BOM and generates different types.
'''
import click
from spreadsheet_wrangler import cluster
from bom_tools import *
from bom_tools import MasterBom, read_bare_bom, read_eda_bom, EDABom
import copy
import pandas as pd # type:ignore
import os

class AssemblyBom:
    def __init__(self, df=None):
        self._df=df

'''
Check BOM against a parts list, checks that the BOM is legal and
returns a list of failures
'''
'''ref-des will not be a tuple of all the matching lines, the rest of the line is taken to be the first in the file and carried forward'''
def order_by_ref_des(bom: pd.DataFrame, on: list = None, column: str ="ref-des") -> pd.DataFrame:
    if on is None:
        on=["pn"]
    clustered = cluster(bom, on=on, column=column)
    qty = []
    for refs in clustered[column]:
        qty.append(len(refs))

    clustered.insert(min(len(clustered.columns), 3), column="qty", value=qty)
    #for col in ["notes", "function", "assembly"]: # drop columns that are not maintained with clustering
    #    if col in clustered.columns:
    #        clustered.drop(columns=col, inplace=True)
    return clustered

'''format a bom bom into the kicost format'''
def generate_kicost_bom(df: pd.DataFrame) -> list:
    sorted_df = order_by_ref_des(df)
    lines = []
    for _, row in sorted_df.iterrows():
        line = "%s,%d,%s"%(row["mfr-num"], row["qty"], " ".join(row["ref-des"]))
        lines.append(line)
    return lines

'''
Expands a BOM from an EDA bom with heirachical parts. Duplicated parts have an underscore such as C1_x. Requires
a bare BOM with the same ref des.
'''
def expand_hierarchical_bom(master_bom: MasterBom, eda_bom: EDABom) -> MasterBom:
    base_refs = [] # break the base part from the expanded
    # Add the row back and merge the data frames on this row.
    # Drop that row when exporting
    for _, row in eda_bom._df.iterrows():
        ref = row["ref-des"]
        for div in ['_', '-', '.', ',']:
            if len(ref.split(div)) > 1:
                ref = div.join(ref.split(div)[:-1])
                break
        base_refs.append(ref)
    eda_bom._df.rename(columns={"ref-des":"expanded-ref-des"}, inplace=True)
    eda_bom._df.insert(0, "ref-des", base_refs)
    eda_bom._df = eda_bom._df.merge(master_bom._df, on="ref-des", how="left")
    eda_bom._df.drop(columns=["ref-des"], inplace=True)
    eda_bom._df.rename(columns={"expanded-ref-des":"ref-des"}, inplace=True)
    return eda_bom._df

@click.group()
def gr1():
    pass

@click.option("--bom", "-b", type=str, required=True, help="BOM file")
@gr1.command(help='''Three columns manf#, refs, qty''')
def kicost(bom):
    lines = generate_kicost_bom(bom)
    fname = os.path.split(os.path.splitext(bom)[0])[-1]
    fname = f'{fname}_kicost.csv'
    with open(fname, "w") as f:
        f.write("\n".join(lines))

@click.option("--bom", "-b", type=str, required=True, help="Bom file")
@click.option("--on", type=str, multiple=True, help="Column to compare value")
@click.option("--column", type=str, default="ref-des", help="Column to cluster into array")
@gr1.command("cluster", help='''Generate Bom ordered by value with clustered ref-des''')
def cluster_command(bom, on, column):
    if len(on) > 0:
        on = list(on)
    else:
        on = None
    fname = os.path.split(os.path.splitext(bom)[0])[-1]
    master_bom = read_bare_bom(bom)
    df = order_by_ref_des(master_bom._df, on=on, column=column)
    df.to_excel(f'{fname}_clustered_on_{column}.xlsx', index=False)

@click.option("--bom", "-b", type=str, required=True, help="bom BOM file")
@click.option("--assembly", "-a", type=str, required=True, help="Assembly name")
@gr1.command(help='''Expand a bom bom into an assembly BOM. Blank assembly entries are included, a value in the assembly over rides the default.''')
def assembly(bom, assembly):
    parts, master_bom = read_bom_to_parts_store(bom)
    assembly_bom = master_bom.get_assembly(assembly)
    fname = os.path.split(os.path.splitext(bom)[0])[-1]
    assembly_bom.to_excel(f'{fname}_Assembly_{assembly}.xlsx', index=False)

@click.option("--bom", "-b", type=str, required=True, help="bom BOM file")
@click.option("--parts", "-p", type=str, required=True, help="Parts data store")
@gr1.command(help='''Take a bare bom BOM and expand the part details from a part store to generate a master BOM''')
def fill(bom, parts):
    master_bom = read_bare_bom(bom)
    parts = read_parts_store(parts)
    if len(parts._df["pn"][0]) > 11:
        for _, row in parts._df.iterrows():
            row["pn"] = "-".join(row["pn"].split("-")[:-1]) # remove last section of part number
    bom_df = master_bom._df
    bom_df = bom_df.merge(parts._df, on="pn", how="left") # include all DNPs, unknown parts won't cause an error
    fname = os.path.split(os.path.splitext(bom)[0])[-1]
    bom_df.to_excel(f'{fname}_FilledBom.xlsx', index=False)

@click.option("--bom", "-b", type=str, required=True, help="bom BOM file")
@gr1.command()
def check(bom):
    parts, master_bom = read_bom_to_parts_store(bom)
    if bom.is_legal():
        print("Bom Check Passed")
    else:
        print("Bom Check Failed")

@click.option("--bom", "-b", type=str, required=True, help="bom BOM file")
@click.option("--eda", "-e", type=str, required=True, help="EDA File")
@gr1.command()
def expand_hierarchy(bom: str, eda: str) -> None:
    master_bom = read_bare_bom(bom)
    eda_bom = read_eda_bom(eda)
    expanded_bom = expand_hierarchical_bom(master_bom, eda_bom)
    fname = os.path.split(os.path.splitext(bom)[0])[-1]
    expanded_bom._df.to_excel(f'{fname}_Expanded.xlsx', index=False)

if __name__ == "__main__":
    gr1()
