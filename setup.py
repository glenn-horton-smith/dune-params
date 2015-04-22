#!/usr/bin/env python
from glob import glob
from setuptools import setup

setup(name='dune-params',

      # fixme: should make a dune-python to that does not much more
      # than provides the top-level "dune" module and maybe some
      # README describing how to add new submodules.

      provides = [ 'dune', "dune.params" ],
      requires = ['dune'],
      version='0.0.2-dev',
      url='https://github.com/DUNE/dune-params',
      author='Brett Viren',
      author_email='bv@bnl.gov',
      packages = ['dune', 'dune.params'],
      data_files = [('share/dune-param/templates/text', glob('templates/text/*.txt')),
                    ('share/dune-param/templates/latex', glob('templates/latex/*.tex')),
                    ('share/dune-param/data', glob('data/*.xls')),
                ],
      install_requires = [l for l in open("requirements.txt").readlines() if l.strip()],
      entry_points='''
      [console_scripts]
      dune-params=dune.params.main:main
      ''',
      )
