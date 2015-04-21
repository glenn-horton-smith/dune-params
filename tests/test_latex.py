#!/usr/bin/env python

import os.path as osp

from jinja2 import Environment, FileSystemLoader

from dune.params import io, latex

import common


def _test_jinja():
    '''
    Test basic Jinja
    '''
    ps = io.load(common.example_xls)
    env = Environment(loader = FileSystemLoader(common.template_dir),
                  block_start_string='~{', block_end_string='}~',
                  variable_start_string='~{{', variable_end_string='}}~')

    t = env.get_template('dump.tex')
    print t.render(params=ps.dict(), **ps.dict())

def test_dune_params():
    '''
    Test dune.params latex renderer
    '''
    ps = io.load(common.example_xls)
    text = latex.render(ps, osp.join(common.template_dir, 'dump.tex'))
    print text

if '__main__' == __name__:
    test_dune_params()
