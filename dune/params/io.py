#!/usr/bin/env python
'''
Load in or export out parameters
'''
from .data import Unit, Param, ParamSet

import xlrd

def load(filename):
    if filename.endswith('.xls'):
        return load_xls(filename)



def load_xls(filename):
    wb = xlrd.open_workbook(filename)

    ps = ParamSet()

    # slurp unit work sheet
    ws = wb.sheet_by_name('Units')
    for irow in range(1,ws.nrows):
        row = ws.row(irow)
        name,com,lat = [str(cell.value).strip() for cell in row[:3]]
        ps.units[name] = Unit(name,com,lat)

    # slurp parameters work sheet
    ws = wb.sheet_by_name('Parameters')
    for irow in range(1,ws.nrows):
        row = ws.row(irow)
        _,name,var,val,unit,prov,desc,note = [str(cell.value).strip() for cell in row[:8]]
        var.replace('-','_')
        ps.add(Param(var, val, unit, name, prov, desc, note))

    return ps


def dump_xls(paramset, filename):
    raise NotImplemented
