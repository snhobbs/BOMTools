'''
Take a digikey BOM and an EDA BOM
Expand the digikey BOM with the hierarchy parts
Use the name of the columns and the ref des

Get row by ref des in dbom
'''
import pandas as pd
import click

quantity_col = "Quantity"
price_col = "Extended Price"
unit_price_col = "Unit Price"
eoi_part_col = "Customer Reference"
ref_des_col = "Reference Designator"

# Parse bom into
def GetRowIndexByRefDes(dbom, ref_des):
    for i, row in enumerate(dbom[ref_des_col]):
        if ref_des in row.split(','):
            return i
    return None

def SetupBomFrame(dbom):
    for row in dbom:
        dbom[quantity_col] = 0
        dbom[price_col] = 0

def read(eda_file, dbom_file, output_bom):
    eda = pd.read_csv(eda_file, delimiter = ";")
    dbom = pd.read_excel(dbom_file)
    SetupBomFrame(dbom)
    bom_lines = pd.DataFrame()
    for i, ref_des_line in enumerate(eda[ref_des_col]):
        eoi_pn = eda["EOI Partnumber"][i]
        if "TP" in ref_des_line:
            continue
        elif "MH" in ref_des_line:
            continue
        eda_refs = ref_des_line.split(",")
        ref_des_base = eda_refs[0].split("_")[0].strip()
        bom_line = GetRowIndexByRefDes(dbom, ref_des_base)
        if bom_line is None:
            continue

        try:
            bom_line_eoi_part = dbom[eoi_part_col][bom_line]
            parts_match = (eoi_pn in [bom_line_eoi_part, "CFG", "DNP"])
            assert(parts_match)
            #bom_line[ref_des_col][i:i+1] = bom_line[ref_des_col][i:i+1].drop("")
        except TypeError:
            pass
        except AssertionError:
            print(bom_line_eoi_part, eoi_pn)
            raise

        quantity = len(eda_refs) + dbom.loc[bom_line, [quantity_col]].values[0]
        dbom.loc[bom_line, [quantity_col]] = quantity

        per_unit_cost = dbom.loc[bom_line, [unit_price_col]].values[0]
        total_cost = quantity * per_unit_cost
        dbom.loc[bom_line, [price_col]] = total_cost

        refs = dbom.loc[bom_line, [ref_des_col]].values[0]
        refs = refs.upper().split(",")
        refs.remove(ref_des_base)
        refs.extend(eda_refs)
        dbom.loc[bom_line, [ref_des_col]] = ",".join(refs)

    dbom.to_excel(dbom_file)

#eda_file = "edaBom.csv"
#dbom_file = "Timestrech_Rev0_0_7/TimeStretcher_0_0_7_DigikeyBom_8396826.xlsx"
#"Timestrech_Rev0_0_7/TimeStretcher_0_0_7_OrderingBom.xlsx"

@click.command()
@click.option("--eda", type=str, help="EDA BOM")
@click.option("--design", type=str, help="Design BOM")
@click.option("--output", type=str, help="Output BOM")
def expand_heirarchical_schematic(eda_bom, design_bom, output_bom):
    read(eda_bom, design_bom, output_bom)

