#!/usr/bin/env python
'''
Provide support to render a dune.param.data.ParamSet as latex
'''

from .data import ParamSet
from jinja2 import Template

def wash(ps):
    '''Return a dict which washes a ParamSet for LaTeX.

    All variable names are converted to underscore and will hold the
    value.  The other elements of a parameter will be set to variables
    with the element name appended.  Such as:

    <var>_unit : hold the units in LaTeX suitable for placing in siunitx
    <var>_name : the human readable name

    etc for _provenance, _description and _notes.

    '''
    ret = dict()

    for p in ps.params:
        var = p.variable.replace('-','_')
        ret[var] = p.value
        ret[var+'_name'] = p.name
        ret[var+'_unit'] = p.units[p.unit].latex
        ret[var+'_category'] = p.category
        ret[var+'_provenance'] = p.provenance
        ret[var+'_description'] = p.description
        ret[var+'_notes'] = p.notes
    return ret


def template(ps, template_text):
    '''
    Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.
    '''
    tmpl = Template(template_text)
    dat = wash(ps)
    return tmpl.render(**dat)
