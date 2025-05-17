import spreadsheet_wrangler
import os
import click
import pandas


def get_pseudonyms():
    '''
    Returns dictionary of common BOM pseudonyms. Use with extract_columns_by_pseudonyms to rename columns to common names.
    '''
    return {
        "designator": ["Reference", "reference", "reference(s)", "ref des"],
        "value": ["comment", "Value"],
        "footprint" : ["Package", "package", "pattern"],
        "LCSC": ["JLCPCB Part #", "LCSC Part Number", "JLCPCB #"]
    }


def read(fname, pseudonyms):
    '''
    read file, return dataframe with standard column names
    '''
    df = spreadsheet_wrangler.extract_columns_by_pseudonyms(spreadsheet_wrangler.read_file_to_df(fname), pseudonyms)
    return df


def main(fname):
    '''
    Drop all rows marked DNP.
    Rename columns to match jlcpcb.
    Drop all unneeded columns.
    '''
    df = read(fname, get_pseudonyms())
    df = df[df["DNP"] != 1]

    column_aliases = {
        "JLCPCB Part #" :"LCSC",
        "Comment" :"value",
        "Designator" :"designator",
        "Footprint": "footprint"
    }

    df_sel = df[list(column_aliases.values())]
    df_sel.columns = column_aliases.keys()
    df_out = pandas.DataFrame(df_sel)
    return df_out


@click.command()
@click.option("--fname", "-f", required=True)
def click_main(fname):
    df = main(fname)
    f_base, _ = os.path.splitext(fname)
    df.to_csv(f"{f_base}-JLC.csv")


if __name__ == "__main__":
    click_main()
