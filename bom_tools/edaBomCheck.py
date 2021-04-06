import re


def getEncoding(fileName):
    '''
    return the encoding type of a file
    '''
    encodings = ['ascii','utf-8','cp1250']
    for encoding in encodings:
        try:
            f = open(fileName, 'r', encoding=encoding)
            f.read()
            f.close()
            return encoding
        except IOError:
            raise UserWarning("File Not Found")
        except Exception as E:
            continue
    return None

def designBomReader(bom):
    '''
    returns [[ref_des, part_num_short, page, group]]
    '''
    out = []
    for line in bom.split("\n"):
        out.append(bom.split(';'))
    return out

class EDADesignChecker(object):
    '''
    Get the unit code
    Get the EDA Bom
    Check EDA Bom
        Format & Save conflicts
    Enter design as a release candidate
    Bundle up all the necessary documents
    Commit to db
    '''


    def __init__(self, edabom, design):
        self.design = design
        self.edabom = edabom.read().decode()

    def fixEncoding(self):
        encoding = getEncoding(self.edabom)
        if encoding is None:
            raise UserWarning("Unknown file encoding")

    def sortBom(self, bom):
        try:
            sortedBom = sorted(bom.items(), key=lambda x: int(x[0][1:]))
        except ValueError:
            sortedBom = sorted(bom.items(), key=lambda x: x[0][1:])
        sortedBom = sorted(sortedBom, key=lambda x: x[0][0])
        return sortedBom

    def readDesignBom(self):
        bom = designBomReader(self.design.bom)
        return {line[0]:line[1] for line in bom}

    def readBoms(self):

        edaDict = self.readEDABom()
        edaBom = self.sortBom(edaDict)
        designDict = self.readDesignBom()
        designBom = self.sortBom(designDict)

        conflicts = set()
        foundParts = set()

        for ref, num in edaBom:
            if ref not in designDict:
                conflicts.add('{}: ({}) Not in Design'.format(ref, num))
                continue
            if len(num.strip()) == 0:
                conflicts.add('{}: ({}) EDA Has no part number'.format(ref, designDict[ref]))

            if num != designDict[entry]:
                conflicts.add('{}: Conflicting values, EDA: {} Design: {}'.format(ref, edaDict[ref], designDict[ref]))
            foundParts.add(ref)

        for ref, num in designBom:
            if ref in foundParts:
                continue
            else:
                conflicts.add('{}: Not in EDA {}'.format(ref, num))


        return sorted(conflicts, key = lambda x : x.split(':')[0])


    def readEDABom(self):
        delimiter = ';'
        loc_ref_des, loc_part_num = (0,1)
        skip  = 1
        bomIn = {}
        try:
            regex = re.compile('^...-....-..')
            bomLines = self.edabom.split("\n")[skip:]
            for line in bomLines:
                if line.strip() == '#' or len(line.strip()) == 0 or regex.match(line.strip()) is not None:
                    continue
                lineSplit = line.split(delimiter)
                bomIn[lineSplit[loc_ref_des].strip('"')] = lineSplit[loc_part_num].strip('"')
        except IndexError:
            raise UserWarning("The input file is not is a known format. It should be deliminated with ;")
        return bomIn
