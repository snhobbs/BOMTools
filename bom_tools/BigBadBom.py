#addPartInterface.py
from heodb.models import Component, INSTALLED_PART_MODELS
from datetime import datetime
import os

def generateBBB(bbbDir, mode='SHORT'):
    now = datetime.now()
    name = "BigBadBom%s.csv"%mode
    fbbbName = os.path.join(bbbDir, name)
    bbbHeader = "#%s\n#%s\n#ElectroOptical Innovations LLC\n"%(name, now.strftime("%B %d, %Y %H:%M"))

    with open(fbbbName, 'w') as fbbb:
        fbbb.write(bbbHeader)
        for part in INSTALLED_PART_MODELS:
            print(part, type(part), part.part_class)
            if mode == 'SHORT':
                parts = part.objects.filter(part_index = '00').order_by(part.part_class.field_name, part.part_type.field_name, part.exact_num.field_name, part.dash_num.field_name)
            else:
                parts = part.objects.all().order_by(part.part_class.field_name, part.part_type.field_name, part.exact_num.field_name, part.dash_num.field_name)
            for comp in parts:
                fbbb.write(comp.makeBomLine(mode) + '\n')
