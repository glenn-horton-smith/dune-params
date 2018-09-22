#!/usr/bin/env python3
'''
LaTeX support
'''
conversions = {
    "<":r'$<$',
    "<<": r'$\ll$',
    ">":r'$>$',
    ">>": r'$\gg$',
     "°":r'$^\circ$',
    '±':r'$\pm$',
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

def clean(string):
    return ''.join([symbol(s) for s in string])

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
    
