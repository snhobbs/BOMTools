# Take the JLCPCB data base in JSON and a BOM with the ref des and JLCPCB numbers.
# Return a BOM with the manufacturer and manufacturers part number appended
import click
import sqlite3
import os
import pandas
from spreadsheet_wrangler import read_file_to_df, read_pseodonyms, extract_columns_by_pseudonyms

ordering = ("Manufacturer", "Package","MFR.Part", "Solder Joint", "Description")

@click.command()
@click.option("--database", "-d", default="parts.db")
@click.option("--bom", "-b", default="BOM.csv")
@click.option("--out", "-o", default=None)
@click.option("--save", "-s", type=bool, default=True)
def command(database, bom, out, save):
    bom = os.path.realpath(bom)
    if out is None:
        split = bom.split(".")
        out = f"{split[0]}_Expanded.xlsx"
    else:
        save = True
    pseudonyms = '{"LCSC Part": ["LCSC", "JLC", "JLCPCB"]}'
    df = read_file_to_df(bom)
    pseudonyms=read_pseodonyms(pseudonyms)
    left = extract_columns_by_pseudonyms(df, pseudonyms)
    right = extract_columns_by_pseudonyms(df, pseudonyms)
    assert("LCSC Part" in df.columns)

    # initialize to empty columns
    for column in ordering:
        if column in df:
            df[column + "_l"] = df[column] # rename the existing column
        df[column] = [""]*len(df)

    dbfile = os.path.realpath(database)
    db = sqlite3.connect(dbfile)
    selection = ",".join(["\"{}\"".format(p) for p in ordering])
    print(selection)
    for _, line in df.iterrows():
        command = "select {} from parts where \"LCSC Part\"=\"{}\"".format(selection, line["LCSC Part"])
        print(command)
        data = db.execute(command)
        data = list(data)[0]
        print(data)
        for column, value in zip(ordering, data):
            line[column] = value

    if save:
        df.to_excel(out, index=False)
        print(f"Saved to {out}")
    else:
        print(df)


if __name__ == "__main__":
    command()
