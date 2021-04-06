#userInterfaceFunctions.py
'''
This module contains all the test user interface function and general formatting tools
'''

def isNumber(num):
    num = str(num)
    try:
        float(num)
        if(num.isalpha()): # removes inf, nan
            return False
        else:
            return True
    except ValueError:
        return False


def sigFigs(x, n):
    import math
    try:
        return round(float(x), int(n - math.ceil(math.log10(abs(x)))))
    except:
        if(x == 0):
            return 0
        else:
            return 'NULL'

def findSciNote(varIn, sciNote):
    import string
    if(isNumber(varIn)):#no sciNote
        return [('',1), float(varIn)]

    varIn = str(varIn).strip(string.punctuation).strip()#strip all symbols

    if(isNumber(varIn)):#no sciNote
        return [('',1), float(varIn)]

    def numCheck(varIn, sciSymbol):
        if(varIn.count(sciSymbol)):
            splitNum = str(varIn).split(sciSymbol)[0]
            if isNumber(splitNum):
                return splitNum
        return False

    for sciSymbol in sciNote:
        num = numCheck(varIn, sciSymbol[0])
        if num is not False:
            return [sciSymbol, float(num)]

    varTest = None
    for i in range(len(varIn)):
        if(isNumber(varIn[:i+1])):
            varTest = varIn[:i+1]
            continue
        else:
            break
    if(isNumber(varTest)):#no sciNote
        return [('',1), float(varTest)]

    raise ValueError('%s is not a recognizable number'%(varIn))

def orderOfMagnitude(varIn):
    decLength = 8
    sciNote = tuple(zip(['f', 'p',  'n',  'u',  'm', 'K', 'k', 'M', 'G',  'T'],[1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 1e3, 1e3, 1e6, 1e9, 1e12]))

    try:
        sciSymbol, num = findSciNote(varIn, sciNote)
        floatVal = num * sciSymbol[1]
    except ValueError:
        return (varIn,'NULL')
    sciIndex = None
    for sciSymbol in sciNote:
        if(abs(floatVal) >= sciSymbol[1]):
            sciIndex = sciSymbol
        else:
            break

    #check if 1 is the best sciNote
    if(1 <= abs(floatVal) < 1000 or abs(floatVal) < sciNote[0][1] or abs(floatVal) == 0.):
        val = sigFigs(floatVal,decLength)
        return str(val), val

    else:
        return ("{}{}".format(sigFigs(floatVal/sciIndex[1],decLength), sciIndex[0])), sigFigs(floatVal,decLength)
