#!/usr/bin/env python
'''
Provide support to render a dune reqs as latex
'''

import os.path as osp
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple

def render(dat, template):
    '''Apply the dat data structure to the template and return LaTeX
    text.
    '''

    env = Environment(loader = FileSystemLoader(osp.dirname(template)),
	              comment_start_string = '\#{',
	              comment_end_string = '}',
                      block_start_string='~{',
                      block_end_string='}~',
                      variable_start_string='~{{',
                      variable_end_string='}}~')
    tmpl = env.get_template(osp.basename(template))

    return tmpl.render(**dat)

def render_multi(dat, template, multi):
    '''Like render() but output multiple files based on filemap.

    The "multi" associates a key with a dictionary.  For each item,
    the dictionary is merged with the dat structure.  The return value
    is dictionary with the same keys as "multi" and with each value
    the corresponding LaTeX content.
    '''

    env = Environment(loader = FileSystemLoader(osp.dirname(template)),
	              comment_start_string = '\#{',
	              comment_end_string = '}',
                      block_start_string='~{',
                      block_end_string='}~',
                      variable_start_string='~{{',
                      variable_end_string='}}~')
    tmpl = env.get_template(osp.basename(template))

    ret = dict();
    for key,extra in list(multi.items()):
        mdat = dict(dat, **extra)
        text = tmpl.render(**mdat)
        ret[key] = text
    return ret
        
