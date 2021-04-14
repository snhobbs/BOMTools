'''
bom_compiler.py
Takes a master BOM and generates different types.
'''
import click
from bom_tools import tools, read_bom_to_parts_store
from bom_tools import *


class AssemblyBom:
    def __init__(self, df=None):
        self._df=df

'''
Check BOM against a parts list, checks that the BOM is legal and
returns a list of failures
'''
def check_bom(master: str) -> bool:
    parts, bom = read_bom_to_parts_store(master)
    return bom.is_legal()

'''format a master bom into the kicost format'''
def generate_kicost_bom(master: str) -> list:
    parts, bom = read_bom_to_parts_store(master)
    lines = []
    full_df = bom._df#.merge(parts._df, how="left", on="pn")
    print(full_df)
    grouped = full_df.groupby("pn")
    for pn, parts in grouped:
        refs = []
        for _, part in parts.iterrows():
            print(part)
            refs.append(part["ref-des"])
            mfr_num = part["mfr-num"]#parts.get_part_line(pn)["mfr-num"]
        line = "%s,%d,%s"%(mfr_num, len(refs), " ".join(refs))
        #print(line)
        lines.append(line)
    return lines


@click.group()
def gr1():
    pass

@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command(help='''Three columns manf#, refs, qty''')
def kicost(master):
    lines = generate_kicost_bom(master)
    fname = master + 'kicost.csv'
    with open(fname, "w") as f:
        f.write("\n".join(lines))

@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@click.option("--assembly", "-a", type=str, required=True, help="Assembly name")
@gr1.command(help='''Expand a master bom into an assembly BOM. Blank assembly entries are included, a value in the assembly over rides the default.''')
def assembly(master, assembly):
    parts, bom = read_bom_to_parts_store(master)
    assembly_bom = bom.get_assembly(assembly)
    fname = os.path.split(os.path.splitext(master)[0])[-1]
    assembly_bom.to_excel(f'{fname}_Assembly_{assembly}.xlsx')

@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@click.option("--parts", "-p", type=str, required=True, help="Parts data store")
@gr1.command(help='''Take a bare Master BOM and expand the part details from a part store to generate a master BOM''')
def fill(master, parts):
    bom = read_bare_bom(master)
    parts = read_parts_store(parts)
    if len(parts._df["pn"][0]) > 11:
        for _, row in parts._df.iterrows():
            row["pn"] = "-".join(row["pn"].split("-")[:-1]) # remove last section of part number
    bom_df = bom._df
    bom_df = bom_df.merge(parts._df, on="pn", how="left") # include all DNPs, unknown parts won't cause an error
    fname = os.path.split(os.path.splitext(master)[0])[-1]
    bom_df.to_excel(f'{fname}_MasterBom.xlsx')

@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command()
def check(master):
    if check_bom(master):
        print("Bom Check Passed")
    else:
        print("Bom Check Failed")

if __name__ == "__main__":
    gr1()
