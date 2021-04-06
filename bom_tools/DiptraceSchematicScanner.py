import click
import regex, os, logging

fname = None
@click.option('--file', '-f', required = True, help='Diptrace Ascii Schematic Location')
@click.group()
def gr1(*args, **kwargs):
    if(not os.path.exists(kwargs['file'])):
        print("File not found: ", kwargs['file'])
        raise FileNotFoundError
    else:
        global fname
        fname = kwargs['file']

class Part:
    def __init__(self, name, refdes):
        self.name = name
        self.refdes = refdes
        self.data = {}
        self.libpath = None
        self.pattern = None
        self.userfields = None
        self.basename = None

    def Assign(self, arg, val):
        if(arg == "userfield" and "eoi" not in val.lower()):
            return
        if arg not in self.data:
            self.data[arg] = val

    def GetEOINum(self):
        try:
            uf = self.data["userfield"]
        except KeyError:
            return None

        if "EOI Partnumber" not in uf:
            print(self.name, self.refdes, uf)
        try:
            val = regex.compile('...-....-..')
            eoiLine = val.findall(uf)[0]
            return eoiLine
        except IndexError:
            val = regex.compile('DNP')
            eoiLine = val.findall(uf)[0]
            return eoiLine

@gr1.command()
def LibraryList(*args, **kwargs):
    if(not os.path.exists(fname)):
        raise FileNotFoundError
    ofname = fname.split("/")[-1] + "LibraryList.csv"
    val = regex.compile('".{1,50}"')
    arg = regex.compile('\([0-9,a-z,A-Z]{1,50}')

    parts = []
    NewPartLine = "(Part "
    with open(fname, 'r') as f:
        for line in f:
            if "(Components" in line:
                break
        dic = {}
        for line in f:
            if "(Part " in line:
                resp = val.findall(line)[0].split(" ")
                try:
                    parts.append(Part(*resp))
                except TypeError:
                    parts.append(Part(" ".join(resp[:-1]), resp[-1]))

            else:
                try:
                    a = arg.findall(line)[0]
                    v = val.findall(line)[0].strip('"')
                except IndexError:
                    pass
                parts[-1].Assign(a.strip("(").lower(), v)


    index = 0
    with open(ofname, 'w')as f:
        for part in parts:
            try:
                eoiNum = part.GetEOINum()
            except IndexError:
                logging.getLogger().warning("No EOI part number found in part #%d (%s)"%(index, part.refdes))
            if eoiNum is None:
                eoiNum = str()
            f.write(",".join([part.name, part.refdes, part.data["libpath"], eoiNum]) + "\n")
            index += 1

if __name__ == "__main__":
    gr1()
