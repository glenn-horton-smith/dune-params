#!/usr/bin/env python3
'''
Interface to spreadsheet

Item,Type,System,Quantity/Parameter,Requirement,Goal,Explanation,Comments,Notes,ProtoDUNE Validation,Simulation Validation
'''

from . import data
from dune import latex

def load_row(cat, row):
    '''
    Load a row from the spread sheet.  There are things we need to fix:
    1) need a "short name"
    2) need a way to parse "comparison operator", number and unit from requirement
    3) 
    '''
    qp = row[3].value           # fixme, need explicit "short name"
    req = row[4].value,         # fixme, need to parse this
    if req:
        req = latex.clean(req[0])
    else:
        req=''
    validation = dict(protodune=row[9].value, simulation=row[10].value)

    return data.Spec(
        category = cat,
        label = qp.replace(" ","").replace("/","").replace("-",""),
        number = int(row[0].value),
        field = row[1].value,
        system = row[2].value,
        title = qp,
        requirement = req,
        goal = row[5].value,          # maybe make this an enum?
        explanation = row[6].value,
        comment = row[7].value,
        notes = row[8].value,
        validation = validation)


def load_sheet(sheet):
    ret = list()
    sheet.name
    for row in list(sheet.get_rows())[1:]:
        r = load_row(sheet.name, row)
        ret.append(r)
    return ret
        

def load_book(book):
    ret = list()
    for sheet in book.sheets():
        ret += load_sheet(sheet)
    return ret
