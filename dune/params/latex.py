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

    # extend the special data for convenience
    input_parameters = list(ps.params.values())
    LaTeX = namedtuple('LaTeX', 'sicmd defname'.split() + list(input_parameters[0].__dict__.keys()))

    for p in input_parameters:

        value = p.value
        unit = ps.units[p.unit].latex
        precision_raw = getattr(p, 'precision') or 0
        #print 'PRECISION: %s"%s"' % (type(precision_raw), precision_raw)
        precision = '[round-mode=places,round-precision=%s]' % int(float(precision_raw))
        if unit:
            sicmd = r'\SI%s{%s}{%s}' % (precision, value, unit)
        else:
            sicmd = r'\num%s{%s}' % (precision,value)
        defname = r'\%s' % p.variable.replace('_','')

        dat = dict(p.__dict__)
        dat['unit'] = unit
        dat['sicmd'] = sicmd
        dat['defname'] = defname
        lat = LaTeX(**dat)
        aux[p.variable] = lat

    env = Environment(loader = FileSystemLoader(osp.dirname(template)),
                  block_start_string='~{', block_end_string='}~',
                  variable_start_string='~{{', variable_end_string='}}~')

    tmpl = env.get_template(osp.basename(template))
    return tmpl.render(data=aux, **aux)
