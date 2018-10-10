#!/usr/bin/env python3
'''
Interface to spreadsheet

Item,Type,System,Quantity/Parameter,Requirement,Goal,Explanation,Comments,Notes,ProtoDUNE Validation,Simulation Validation
'''

from . import data
from dune import latex

# A B C D E F G H I J  K  L  M  N  O  P  Q  R  S T  U  V
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

def load_row(cat, row):
    '''
    Load a row from the spread sheet.  There are things we need to fix:
    1) need a "short name"
    2) need a way to parse "comparison operator", number and unit from requirement
    3) 
    '''
    qp = row[6].value

    req = row[9].value

    validation = dict(protodune=row[14].value, simulation=row[15].value)

    return data.Spec(
        category = cat,
        label = qp,
        number = int(row[0].value),
        field = row[2].value,
        system = row[1].value,
        title = row[5].value,
        requirement = req,
        goal = row[10].value,          # maybe make this an enum?
        explanation = row[11].value,
        comment = "", # row[7].value,
        notes = "", # row[8].value,
        validation = validation)


def load_sheet(sheet, required_columns=22):
    ret = list()
    sheet.name
    for row in list(sheet.get_rows())[2:]:
        if not row:
            continue
        if required_columns != len(row):
            print ("skipping row with wrong number of columns %d != %d" % (len(row), required_columns))
            continue
        r = load_row(sheet.name, row)
        ret.append(r)
    return ret
        

def load_book(book):
    ret = list()
    for sheet in book.sheets():
        ret += load_sheet(sheet)
    return ret
