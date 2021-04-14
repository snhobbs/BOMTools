from bom_tools import PartsDataStore, tools, MasterBom
import pandas as pd  # type: ignore
import csv
import os

def bom_df_to_parts_store(df : pd.DataFrame) -> tuple:
    return (PartsDataStore(
       {"pn": df["internal-num"], "mfr": df["mfr"], "mfr-num": df["mfr-num"]}),
       MasterBom({
           "ref-des": df["ref-des"],
           "pn": df["internal-num"],
           "assembly": df["assembly"]}))

def read_bom_to_parts_store(fname: str) -> tuple:
    name, ext = os.path.splitext(fname)
    ext = ext.lower()
    if ext == ".csv":
        df = pd.read_csv(fname, header=0, skipinitialspace=True,
                index_col=0, sep=";", comment="#", quotechar='"',
                quoting=csv.QUOTE_MINIMAL, engine="python")

    elif ext in [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods",".odt"]:
        df = pd.read_excel(fname, sheet_name=0, header=0, skiprows=0,
                comment="#")

    return bom_df_to_parts_store(df)
