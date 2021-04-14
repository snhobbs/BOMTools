from bom_tools import PartsDataStore, tools, MasterBom
import pandas as pd  # type: ignore
import csv
import os

# key value pairs of the used name to acceptable names
column_names = {
    "ref-des": ["ref-des"],
    "pn":["pn", "internal-num", "Internal Part Number", "internal-pn"],
    "assembly": ["assembly"],
    "mfr": ["mfr", "Manufacturer"],
    "mfr-num": ["mfr-num", "Manufacturer Number", "Manufacturer Part Number"],
}

'''Finds knowns pseudonyms for columns and includes names them correctly for passing as argument'''
def extract_columns_by_pseudonyms(df, column_names):
    output = {}
    for column, names in column_names.items():
        expanded_names = list()
        expanded_names.extend(pt for pt in names)
        expanded_names.extend(pt.lower() for pt in names)
        expanded_names.extend(pt.upper() for pt in names)

        for name in expanded_names:
            if name in df.columns:
                output[column] = df[name]
    return output

def read_file_to_df(fname: str) -> dict:
    name, ext = os.path.splitext(fname)
    ext = ext.lower()
    if ext == ".csv":
        df = pd.read_csv(fname, header=0, skipinitialspace=True,
                index_col=0, sep=";", comment="#", quotechar='"',
                quoting=csv.QUOTE_MINIMAL, engine="python")

    elif ext in [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods",".odt"]:
        df = pd.read_excel(fname, sheet_name=0, header=0, skiprows=0,
                comment="#")
    return df

def read_parts_store(fname: str) -> PartsDataStore:
    df = read_file_to_df(fname)
    columns = extract_columns_by_pseudonyms(df, column_names)
    return PartsDataStore(columns)

def read_master_bom(fname: str) -> tuple:
    df = read_file_to_df(fname)
    columns = extract_columns_by_pseudonyms(df, column_names)
    return (PartsDataStore(columns), MasterBom(columns))

def read_bom_to_parts_store(fname: str) -> tuple:
    return read_master_bom(fname)

def read_bare_bom(fname: str) -> MasterBom:
    df = read_file_to_df(fname)
    columns = extract_columns_by_pseudonyms(df, column_names)
    return MasterBom(columns)
