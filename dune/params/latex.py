#!/usr/bin/env python
'''
Provide support to render a dune.param.data.ParamSet as latex
'''

import os.path as osp
from .data import ParamSet
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple

def render(ps, template):
    '''Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.

    The template has available the original ParamSet as "params" and
    an additional dictionary keyed by variable name called latex, the
    values of which has .value and .unit with forms suitable for the
    args to \SI{}{}, .sicmd for a siunitx command and defname for a
    name to use as a macro (all '-' and '_' removed).

    '''

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

    env = Environment(loader = FileSystemLoader(osp.dirname(template)),
                  block_start_string='~{', block_end_string='}~',
                  variable_start_string='~{{', variable_end_string='}}~')

    tmpl = env.get_template(osp.basename(template))
    return tmpl.render(ps=ps, params=ps.dict(), latex=aux, **aux)
