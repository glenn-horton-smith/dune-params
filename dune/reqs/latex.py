#!/usr/bin/env python
'''
Provide support to render a dune reqs as latex
'''

import os.path as osp
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple

def render(dat, template):
    '''Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.

    The template has available the original ParamSet as "params" and
    an additional dictionary keyed by variable name called latex, the
    values of which has .value and .unit with forms suitable for the
    args to \SI{}{}, .sicmd for a siunitx command and defname for a
    name to use as a macro (all '-' and '_' removed).

    '''

    byname = {d.category+d.label:d for d in dat}


    env = Environment(loader = FileSystemLoader(osp.dirname(template)),
	              comment_start_string = '\#{',
	              comment_end_string = '}',
                      block_start_string='~{',
                      block_end_string='}~',
                      variable_start_string='~{{',
                      variable_end_string='}}~')
    tmpl = env.get_template(osp.basename(template))

    return tmpl.render(specs=dat, byname=byname)
