from bom_tools import PartsDataStore, tools, MasterBom, EDABom
import pandas as pd  # type: ignore
import csv
import os
import numpy as np
import copy

# key value pairs of the used name to acceptable names
column_names = {
    "ref-des": ["Reference Designator", "ref", "ref_des", "RefDes"],
    "pn":["internal-num", "Internal Part Number", "internal-pn", "Customer Reference", "EOI Partnumber"],
    "assembly": [],
    "mfr": ["Manufacturer"],
    "mfr-num": ["Manufacturer Number", "Manufacturer Part Number"],
    "qty": ["quantity", "count"],
    "price": ["Unit Price"],
}

'''Finds knowns pseudonyms for columns and includes names them correctly for passing as argument'''
def extract_columns_by_pseudonyms(df, column_names):
    included = []
    output = {}
    for name in df.columns:
        for column, names in column_names.items():
            if name.lower() in [pt.lower() for pt in names] or name.lower() == column.lower():
                output[column] = df[name]
                included.append(name)
    for name in df.columns:
        if name not in included and name not in output:
            output[name] = df[name]
    return output

def read_csv_to_df(fname: str) -> dict:
    # Use automatic dialect detection by setting sep to None and engine to python
    kwargs = dict(
        header=0, skipinitialspace=True,
        index_col=None, comment="#", quotechar='"',
        quoting=csv.QUOTE_MINIMAL, engine="python", skip_blank_lines=True
    )
    #try sniffing
    try:
        # Use automatic dialect detection by setting sep to None and engine to python
        kwargs["sep"]=None
        kwargs["delimiter"]=None
        df = pd.read_csv(fname, **kwargs)
        return df
    except Exception as e:
        print(e)
        pass
    try:
        kwargs["sep"]=','
        df = pd.read_csv(fname, **kwargs)
        return df
    except Exception as e:
        print(e)
        pass
    try:
        kwargs["sep"]=';'
        df = pd.read_csv(fname, **kwargs)
        return df
    except Exception as e:
        raise

#sep=None
def read_file_to_df(fname: str) -> dict:
    name, ext = os.path.splitext(fname)
    ext = ext.lower()
    if ext == ".csv":
        df = read_csv_to_df(fname)

    elif ext in [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods",".odt"]:
        df = pd.read_excel(fname, sheet_name=0, header=0, skiprows=0,
                comment="#", skip_blank_lines=True)
    return df

def read_file_to_formated_df(fname: str) -> pd.DataFrame:
    df = read_file_to_df(fname)
    columns = extract_columns_by_pseudonyms(df, column_names)
    formated_df = pd.DataFrame(columns)
    return formated_df

def expand_grouped_by_ref_des(df: pd.DataFrame) -> pd.DataFrame:
    formated_df = df[df["ref-des"] != np.nan]
    expanded_rows = []
    for _, row in formated_df.iterrows():
        refs = row["ref-des"]
        if type(refs) != str:
            continue
        for ref in refs.split(','):
            row["ref-des"] = ref.strip()
            expanded_rows.append(copy.deepcopy(row))
    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df

def read_parts_store(fname: str) -> PartsDataStore:
    df = read_file_to_formated_df(fname)
    return PartsDataStore(df)

def read_master_bom(fname: str) -> tuple:
    df = read_file_to_formated_df(fname)
    expanded_df = expand_grouped_by_ref_des(df)
    return (PartsDataStore(expanded_df), MasterBom(expanded_df))

def read_bom_to_parts_store(fname: str) -> tuple:
    return read_master_bom(fname)

def read_bare_bom(fname: str) -> MasterBom:
    df = read_file_to_formated_df(fname)
    expanded_df = expand_grouped_by_ref_des(df)
    return MasterBom(expanded_df)

def read_eda_bom(fname: str) -> EDABom:
    df = read_file_to_formated_df(fname)
    expanded_df = expand_grouped_by_ref_des(df)
    return EDABom(expanded_df)
