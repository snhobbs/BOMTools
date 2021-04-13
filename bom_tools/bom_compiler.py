'''
bom_compiler.py
Takes a master BOM and generates different types.
'''
import click
from . import tools, read_bom_to_parts_store

def generate_kicost_bom(master):
    parts, bom = read_bom_to_parts_store(master)
    fname = master + 'kicost.csv'
    lines = []
    parts_frame = bom.parts_frame()
    for ref_des, pn in zip(parts_frame["ref-des"], parts_frame["pn"]):
        mfr_num = parts.get_part_line(pn)["mfr-num"]
        lines.append("%s,%d,%s"%(mfr_num, len(ref_des), " ".join(ref_des)))

    with open(fname, "w") as f:
        f.write("\n".join(lines))


@click.group()
def gr1():
    pass

'''
Three columns manf#, refs, qty
'''
@click.option("--master", "-m", type=str, required=True, help="Master BOM file")
@gr1.command()
def kicost(master):
    return generate_kicost_bom(master)

if __name__ == "__main__":
    gr1()
