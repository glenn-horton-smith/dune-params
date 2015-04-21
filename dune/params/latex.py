#!/usr/bin/env python
'''
Provide support to render a dune.param.data.ParamSet as latex
'''

from .data import ParamSet
from jinja2 import Template
from collections import namedtuple

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
        ret[var+'_unit'] = p.units[p.unit].latex
        if p.unit:
            ret[var+'_siunitx'] = r'\SI{%s}{%s}' % (p.value, p.units[p.unit].latex)
        else:
            ret[var+'_siunitx'] = r'\SI{%s}{%s}' % (p.value, p.units[p.unit].latex)
        # ret[var+'_name'] = p.name
        # ret[var+'_category'] = p.category
        # ret[var+'_provenance'] = p.provenance
        # ret[var+'_description'] = p.description
        # ret[var+'_notes'] = p.notes
    return ret


def render(ps, template_text):
    '''Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.

    The template has available the original ParamSet as "params" and
    an additional dictionary keyed by variable name called latex, the
    values of which has .value and .unit with forms suitable for the
    args to \SI{}{}, .sicmd for a siunitx command and defname for a
    name to use as a macro (all '-' and '_' removed).

    '''
    tmpl = Template(template_text)

    aux = dict()
    LaTeX = namedtuple('LaTeX', 'unit value sicmd defname')
    for p in ps.params.values():

        value = p.value
        unit = ps.units[p.unit].latex
        if unit:
            sicmd = r'\SI{%s}{%s}' % (value, unit)
        else:
            sicmd = r'\num{%s}' % (value,)
        defname = r'\%s' % p.variable.replace('_','')
        aux[p.variable] = LaTeX(unit, value, sicmd, defname)

    return tmpl.render(params=ps.params, latex=aux)
