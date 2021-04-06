"""
part_finder.py
Look through two files and search for an internal part number that looks like `match_pattern`

"""
#!/usr/bin/env python3
import sys, regex, click

#first arg is a digikey csv cart
#second is a newline deliminated list of eoi partnumbers

match_pattern = "\w{3}-\w{4}-\w{2}"
@click.argument("--first", "-f", type=str, required=True, help="Design BOM to compare to. Should have the part number somewhere in the line")
@click.argument("--second", "-s", type=str, required=True, help="Main BOM to search. Typically the distributer BOM or a text schematic")
@click.command
def main(first, second):
    regx = regex.compile(match_pattern)
    with open(first, 'r') as f:
        first_parts = [part.strip() for part in f.read().strip().split('\n')]

    with open(second, 'r') as f:
        st = f.read().strip()
        second_parts = regx.findall(st)

    nfirst = []
    nsecond = []
    for part in first_parts:
        if part not in nfirst:
            nfirst.append(part)

    for part in second_parts:
        if part not in parts:
            nsecond.append(part)

    print("Not in first: ", nfirst)
    print("Not in second: ", nsecond)

if __name__ == "__main__":
    main()
