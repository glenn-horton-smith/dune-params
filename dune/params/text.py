#!/usr/bin/env python
'''
Provide support to render a dune.param.data.ParamSet as plain text dump
'''
import os.path as osp

from .data import ParamSet
from jinja2 import Template

from jinja2 import Environment, FileSystemLoader

def render(ps, template):
    '''
    Apply the ParamSet <ps> to the template_text and return the rendered LaTeX text.
    '''
    env = Environment(loader = FileSystemLoader(osp.dirname(template)))
    tmpl = env.get_template(osp.basename(template))
    return tmpl.render(data=ps.dict(), **ps.dict())

