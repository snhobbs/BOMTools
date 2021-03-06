from spreadsheet_wrangler import cluster, uncluster, compare, extract_columns_by_pseudonyms, read_csv_to_df, read_file_to_df, uncluster_regex
from . MasterBom import MasterBom
from . EDABom import EDABom
from . PartsDataStore import PartsDataStore
import pandas as pd  # type: ignore
import csv
import os
import numpy as np # type: ignore
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
    "value": ["val"],
    "pattern": []
}


def read_file_to_formated_df(fname: str) -> pd.DataFrame:
    df = read_file_to_df(fname)
    columns = extract_columns_by_pseudonyms(df, column_names)
    formated_df = pd.DataFrame(columns)
    return formated_df

def expand_grouped_by_ref_des(df: pd.DataFrame) -> pd.DataFrame:
    return uncluster_regex(df, "ref-des", "[A-z]+[0-9]+")

def read_parts_store(fname: str) -> PartsDataStore:
    df = read_file_to_formated_df(fname)
    return PartsDataStore(df)

def read_master_bom(fname: str) -> tuple:
    df = read_file_to_formated_df(fname)
    #expanded_df = expand_grouped_by_ref_des(df)
    expanded_df = df
    return (PartsDataStore(expanded_df), MasterBom(expanded_df))

def read_bom_to_parts_store(fname: str) -> tuple:
    return read_master_bom(fname)

def read_bare_bom(fname: str) -> MasterBom:
    df = read_file_to_formated_df(fname)
    #expanded_df = expand_grouped_by_ref_des(df)
    expanded_df = df
    return MasterBom(expanded_df)

def read_eda_bom(fname: str) -> EDABom:
    df = read_file_to_formated_df(fname)
    expanded_df = expand_grouped_by_ref_des(df)
    return EDABom(expanded_df)
