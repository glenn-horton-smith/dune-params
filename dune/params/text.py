#!/usr/bin/env python
'''
Provide support to render a dune.param.data.ParamSet as plain text dump
'''

from .data import ParamSet
from jinja2 import Template

def template(ps, template_text):
    '''
    Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.
    '''
    tmpl = Template(template_text)
    return tmpl.render(params = ps.params, **ps.dict())
