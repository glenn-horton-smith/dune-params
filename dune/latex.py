#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
LaTeX support
'''
conversions = {
    "<<": r'\ensuremath{\ll}',
    ">>": r'\ensuremath{\gg}',
    '%':r'\%',
}

def symbol(sym):
    '''
    Convert between some string and the LaTeX equivalent, or return
    input if conversion not found.
    '''
    try:
        return conversions[sym.lower()]
    except KeyError:
        return sym

sloppy2utf8 = {
    "<<": r'≪',
    ">>": r'≫',
}
def make_utf8(sym):
    try:
        return sloppy2utf8[sym.lower()]
    except KeyError:
        return sym
        

def clean(string):
    #from pylatexenc.latexencode import utf8tolatex
    #string = ' '.join([make_utf8(s) for s in string.split(' ')])
    #return ' '.join([symbol(s) for s in string.split(' ')])
    # return ' '.join([symbol(s) for s in utf8tolatex(string).split()])
    return string

def siunitx(value, unit, numf='%f', siuopts=''):
    '''
    Return LaTeX string for the given value and unit in the form of an siunitx form.
    '''
    u = r'\SI'
    if siuopts:
        u += '[%s]'%siuopts
    u += '{%s}' % numf
    u += '{%s}'
    return u % (value, symbol(unit))
    
