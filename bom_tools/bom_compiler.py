'''
bom_compiler.py
Takes a master BOM and generates different types.
'''
import click
from bom_tools import tools, read_bom_to_parts_store

'''
Check BOM against a parts list, checks that the BOM is legal and
returns a list of failures
'''
def check_bom(master: str) -> bool:
    parts, bom = read_bom_to_parts_store(master)
    return bom.is_legal()

def generate_kicost_bom(master: str) -> list:
    parts, bom = read_bom_to_parts_store(master)
    lines = []
    parts_frame = bom.parts_frame()
    for ref_des, pn in zip(parts_frame["ref-des"], parts_frame["pn"]):
        mfr_num = parts.get_part_line(pn)["mfr-num"]
        lines.append("%s,%d,%s"%(mfr_num, len(ref_des), " ".join(ref_des)))
    return lines


@click.group()
def gr1():
    pass

'''
Three columns manf#, refs, qty
'''
@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command()
def kicost(master):
    lines = generate_kicost_bom(master)
    fname = master + 'kicost.csv'
    with open(fname, "w") as f:
        f.write("\n".join(lines))

@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command()
def check(master):
    if check_bom(master):
        print("Bom Check Passed")
    else:
        print("Bom Check Failed")

if __name__ == "__main__":
    gr1()
