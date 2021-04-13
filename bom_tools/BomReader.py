from bom_tools import PartsDataStore, tools, MasterBom
import pandas as pd  # type: ignore
import csv


def read_bom_to_parts_store(fname: str) -> tuple:
    df = pd.read_csv(fname, header=0, skipinitialspace=True,
                     index_col=0, sep=";", comment="#", quotechar='"',
                     quoting=csv.QUOTE_MINIMAL, engine="python")

    return (PartsDataStore(
       {"pn": df["internal-num"], "mfr": df["mfr"], "mfr-num": df["mfr-num"]}),
       MasterBom({
           "ref-des": df["ref-des"],
           "pn": df["internal-num"],
           "assembly": df["assembly"]}))
