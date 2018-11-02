#!/usr/bin/env python3
'''
Interface to spreadsheet

Tab: List of top-level requirements, starts on line 3
Same columns as [subsys code]

Tab: [subsys code], starts on line 3
0  5    6     7    8     9      10   11        14         15
A  F    G     H    I     J      K    L         O          P
id,name,label,text,vtext,vlatex,goal,rationale,validation,note

Tab: subsys codes, starts on line 3
0
A
code

Tab: Your selected top-level reqs, starts on line 2
0
A
id

'''

from . import data
from dune import latex

# A B C D E F G H I J  K  L  M  N  O  P  Q  R  S T  U  V
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

# Map columns to key values for requirements. 
requirements_schema = dict(
    ssid=lambda r: int(r[0].value),
    name=lambda r: r[5].value,
    label=lambda r: r[6].value,
    text=lambda r: r[7].value,
    vtext=lambda r: r[8].value,
    vlatex=lambda r: r[9].value,
    goal=lambda r: r[10].value,
    rationale=lambda r: r[11].value,
    validation=lambda r: r[14].value,
    note=lambda r: r[15].value
)
selected_schema = dict(
    refid=lambda r: int(r[0].value)
)

def load_row(row, schema):
    '''
    Load a row into a data structure following the given schema 
    '''
    ret = dict()
    for k,f in schema.items():
        ret[k] = f(row)
    return ret

def load_rows(rows, schema):
    '''
    Load a rows into list of data structure following schema.

    Rows are expected to have been prefiltered to remove any bogosity.
    '''
    ret = list()
    for row in rows:
        r = load_row(row, schema)
        ret.append(r);
    return ret;

def rows(sheet, first_row=0):
    '''
    Convert sheet to list of rows
    '''
    ret = [r for r in list(sheet.get_rows())[first_row:] if r[0].value]
    return ret;

def load_sheets(book):
    '''
    Return a dictionary mapping a canonical name to a sheet
    '''
    bynative = {s.name:s for s in book.sheets()}
    code_tab = [k for k in bynative.keys() if "chapter codes" in k.lower()][0]
    code_sheet = bynative[code_tab]
    codes = [r[0].value for r in rows(code_sheet,2) if r[0]]

    chapter = [k for k in bynative.keys() if k in codes]
    if len(chapter) != 1:
        print(chapter)
        print (codes)
        print (bynative.keys())
        assert len(chapter)==1
        
    chapter = chapter[0]
    chapter_sheet = bynative[chapter]

    toplevel_tab = [k for k in bynative.keys() if "top-level requirements" in k.lower()][0]
    toplevel_sheet = bynative[toplevel_tab];

    selected_tab = [k for k in bynative.keys() if "selected top-level" in k.lower()][0]
    selected_sheet = bynative[selected_tab]

    return dict(toplevel=toplevel_sheet,
                code=chapter,
                codes=codes,
                subsys=chapter_sheet,
                selected=selected_sheet)
    
all_schema = dict(toplevel = (2, requirements_schema),
                  subsys = (2, requirements_schema),
                  selected = (1, selected_schema))

def load_book(book):
    '''
    Parse the book into a data structure
    '''
    sheets = load_sheets(book)
    ret = dict()
    for name in 'toplevel subsys selected'.split():
        skip, schema = all_schema[name]
        ret[name] = load_rows(rows(sheets[name], skip), schema)
    # special case
    ret['code'] = sheets['code']
    ret['codes'] = sheets['codes']
    return ret


def massage(dat):
    '''
    Return a new data structure that "cleans up" what load_book returns.
    '''
    dat = dict(dat)

    # and clean up the short 'selected' to just be a list of integers
    dat['selected'] = [o['refid'] for o in dat['selected']]

    code = dat['code']
    dat['subsys'] = [dict(d, gid="%s-%d"%(code, d['ssid'])) for d in dat['subsys']]
    dat['toplevel'] = [dict(d, gid="TOP-%d"%d['ssid']) for d in dat['toplevel']]

    # collate by label.
    bylabel = dict()
    for obj in dat['subsys']:
        bylabel[obj['label']] = obj
    dat['bylabel'] = bylabel

    # resolve the top level reqs selected by the subsys
    sstop = list()
    topbyssid={d['ssid']:d for d in dat['toplevel']}
    for ssid in dat['selected']:
        sstop.append(topbyssid[ssid])
    dat['sstop'] = sstop

    return dat;
    
