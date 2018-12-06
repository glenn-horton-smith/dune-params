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
import re
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
    for k,f in list(schema.items()):
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

def get_matches(patterns, strings):
    ret = list()
    for pattern in patterns:
        for s in strings:
            if re.search(pattern,s.lower()):
                ret.append(s)
    return ret


    

def load_sheets(book, chapter_code, top = ("SP-FD","DP-FD")):
    '''
    Return a dictionary mapping a canonical name to a sheet

    "chapter" and "subsys" are synonyms in the taxonomy.

    If chapter code is in the "top" list then take not from the
    subsys tab but from the "List of top-level requirements" tab.
    '''
    bytab = {s.name:s for s in book.sheets()}
    tabs = bytab.keys()

    tl_patterns = ["top-level with latex","list of top-level requirements"]
    tl_tabname = get_matches(tl_patterns, tabs)[0] # may fail to find tab
    tl_sheet = bytab[tl_tabname]

    if chapter_code in top:
        ss_sheet = tl_sheet
    else:
        ss_patterns = ["your chapter"]
        ss_tabs = get_matches(ss_patterns, tabs)
        if not ss_tabs:
            ss_tabs = get_matches([chapter_code.lower()], tabs)
        if not ss_tabs:
            raise (ValueError, "bogus spreadsheet")
        ss_tabname = ss_tabs[0] # may fail to find tab
        ss_sheet = bytab[ss_tabname]

    sel_patterns = ["your selected"]
    sel_tabname = get_matches(sel_patterns, tabs)[0] # may fail to find tab
    sel_sheet = bytab[sel_tabname]

    return dict(toplevel=tl_sheet,
                code=chapter_code,
                subsys=ss_sheet,
                selected=sel_sheet)
    
all_schema = dict(toplevel = (2, requirements_schema),
                  subsys = (2, requirements_schema),
                  selected = (1, selected_schema))

def load_book(book, chapter_code):
    '''
    Parse the book into a data structure
    '''
    sheets = load_sheets(book, chapter_code)
    ret = dict()
    for name in 'toplevel subsys selected'.split():
        skip, schema = all_schema[name]
        ret[name] = load_rows(rows(sheets[name], skip), schema)
    # special case
    ret['code'] = sheets['code']
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
    
