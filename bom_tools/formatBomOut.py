#formatBomOut.py
from heodb.models import Design, Model, Project, componentFactory
import datetime, os
from heodb import findFirstNumber, findFirstLetters
from copy import deepcopy
from datetime import datetime

class BomFormater(object):
    '''
    Creates bom orginized in various ways
    take the fields in the order they're wanted and the mode of by refDes

    Load in all data that you would want, in the different modes just chooses the data fields
    The fist and second are always the partnumber and refDes.

    '''
    def __init__(self, design):
        self.design = design
        self.bom = [c.split(';') for c in self.design.bom.strip().split('\n') if len(c)]

    def __pullFields(self, key = None):
        '''
        get partnumber, load the part, return all fields
        '''
        fields = []
        for part in self.bom:
            #FIXME
            refDes, partNum, page, group = part
            comp = componentFactory(partNum, mode = 'SHORT')
            d = deepcopy(comp.__dict__)
            d.update({
                'descrip': comp.makeDescrip(),
                'description': comp.makeDescrip(),
                'ref_des':refDes,
                'part_num': comp.part_number_short,
                'page': page,
                'group': group,
                'group_in': group,
                'manu_name' : comp.manufacturer.manu_name,
                'package_type' : comp.package_type.package,
                'supplier' : comp.supplier.supplier

            })
            fields.append(d)
        totalParts = len(fields)
        uniqueParts = len(set(field['part_num'] for field in fields))
        #longestRefDes = max(len(field['ref_des'] for field in fields))
        if key is not None:
            return {'fields':sorted(fields, key = key), 'totalParts':totalParts, 'uniqueParts':uniqueParts}
        else:
            return {'fields':fields, 'totalParts':totalParts, 'uniqueParts':uniqueParts}

    def __orderByPartNum(self):
        '''
        Return a sorted tuple of the data sorted by partnumber
        '''
        return self.__pullFields(key = lambda x: x['part_num'])

    def __orderByRefDes(self):
        '''
        1 entry per refDes
        '''
        return self.__pullFields(key = lambda x: (findFirstLetters(x['ref_des'][0]), findFirstNumber(x['ref_des'][0])))

    def __orderByGrouping(self):
        return self.__pullFields(key = lambda x: (findFirstLetters(x['ref_des'][0]), findFirstNumber(x['ref_des'][0])))
    #return self.__pullFields(key = lambda x: (x['page'], x['group'], findFirstLetters(x['ref_des'][0]), findFirstNumber(x['ref_des'][0])))

    def refDesBom(self, fields, data):
        out = []
        for line in data:
            out.append([line[field] for field in fields])
        return out

    def partNumBom(self, fields, data):
        dataDict = {d['part_num']:d for d in data}
        for d in dataDict.values():
            part_num = d['part_num']
            d.update(
                {'count':0, 'refs':[]}
            )
        for d in data:
            part_num = d['part_num']
            dataDict[part_num]['count'] += 1
            dataDict[part_num]['refs'].append(d['ref_des'])

        out = []

        for line in dataDict.values():
            out.append([line[field] for field in fields])
        return out

    def makeBom(self, fields, mode = 'REFDES'):
        '''
        mode PARTNUM -> sort by part number
        mode REFDES  -> sort by ref des
        '''
        title = []
        for field in fields:
            if field == 'count':
                title.append('Count')
            elif field == 'part_num':
                title.append('Part Number')
            elif field in ('ref_des', 'refs') :
                title.append('Ref Des')
            elif field == 'description':
                title.append('Description')
            else:
                title.append(" ".join(field.split('_')).title())

        bomOut = [title]
        dataOffset = -2
        if mode == 'REFDES':
            info = self.__orderByRefDes()
            bomOut.extend(self.refDesBom(fields, info['fields']))
        else:
            info = self.__pullFields()
            bomOut.extend(self.partNumBom(fields, info['fields']))
        return bomOut, info

    def writeBom(self, fDir, bomOut, totalParts, uniqueParts, bomType = '', header = True, footer = True, delim = '\t'):
        '''
        Write the bom to a file
        '''
        fName = os.path.join(fDir, self.bomName(bomType) + '.csv')

        with open(fName, 'w') as fBom:
            if header:
                fBom.write('\n'.join(['#{}'.format(line) for line in self.bomHeader()]))
            for line in bomOut:
                fBom.write('\n{}'.format(delim.join(["{}".format(ent) for ent in line])))
            if footer:
                fBom.write('\nTotal Parts: {}\nUnique Parts: {}'.format(totalParts, uniqueParts))

    def bomName(self, bomType):
        return "{}_{}_{}_{}Bom".format(
                self.design.model.project.proj_name.replace(' ', '_'),
                self.design.model.model_name.replace(' ', '_'),
                self.design.rev_name.replace(' ', '_'), bomType
            )

    def bomHeader(self):
        now = datetime.now()
        return ['Hobbs ElectroOptics LLC',
                now.strftime("%B %d %Y %H:%M"),
                'Project: {}'.format(self.design.model.project.proj_name),
                'Model: {}'.format(self.design.model.model_name),
                'Rev: {}'.format(self.design.rev_name)]

    def writeExcelBom(self, fDir, bomOut, bomType):
        import xlsxwriter

        fName = os.path.join(fDir, self.bomName(bomType) + '.xlsx')

        row = 0
        col = 0
        with xlsxwriter.Workbook(fName) as fBom:
            sheet = fBom.add_worksheet()
            for item in self.bomHeader():
                sheet.write(row, col, item)
                row += 1

            for line in bomOut:
                col = 0
                for column in line:
                    sheet.write(row, col, str(column).strip().strip('"'))
                    col += 1
                row += 1

    def digikeyBom(self, fDir):
        fields = ['count', 'manu_num']
        bomOut, data = self.makeBom(fields, mode = 'PARTNUM')
        fName = os.path.join(fDir, self.bomName('Digikey') + '.csv')
        delim = ','
        with open(fName, 'w') as fBom:
            for line in bomOut:
                fBom.write('\n{}'.format(delim.join([str(ent).replace(',', '') for ent in line])))

    def designBom(self, fDir):

        data = self.__orderByGrouping()
        #raise Exception(d)
        sortedBom = [[b['ref_des'], b['part_num'], b['page'], b['group']] for b in data['fields']]

        groupTag = None
        pageTag = None
        bom = []
        for part in sortedBom:
            refDes, partNum, page, group = part
            if page != pageTag:
                bom.append('\n--Page:{}'.format(page))
                pageTag = page
            if group != groupTag:
                bom.append('--Group:{}'.format(group))
                groupTag = group
            comp = componentFactory(partNum, mode = 'SHORT')
            bom.append("{},{}".format(refDes,comp.makeBomLine()))

        self.writeBom(fDir, bom, data['totalParts'], data['uniqueParts'], bomType = 'Design', footer = False, delim = '')


    def EDABom(self, fDir):
        fields = ['ref_des', 'part_num','manu_name','manu_num','package_type', 'page', 'group_in']
        bom, data = self.makeBom(fields, mode = 'REFDES')
        self.writeBom(fDir, bom, data['totalParts'], data['uniqueParts'], bomType = 'EDA', delim = '\t')

    def PartsBom(self, fDir):
        fields = ['part_num', 'count', 'manu_num','manu_name','package_type','supplier']
        bom, data = self.makeBom(fields, mode = 'PARTNUM')
        self.writeBom(fDir, bom, data['totalParts'], data['uniqueParts'], bomType = 'Parts', delim = ';')

    def OrderBom(self, fDir):
        fields = ['manu_num','package_type','description','ref_des','count']
        bom, data = self.makeBom(fields, mode = 'PARTNUM')
        bomOut = [['Line'] + bom[0]]
        for i,line in enumerate(bom[1:]):
            bomOut.append([str(i+1)] + line)

        self.writeExcelBom(fDir, bomOut, 'Order')

    def genBom(self, dirName, allBoms, bomType):
        if allBoms:
            self.designBom(dirName)
            self.OrderBom(dirName)
        elif(bomType == 0):
            self.designBom(dirName)
        elif(bomType == 1):
            self.OrderBom(dirName)
