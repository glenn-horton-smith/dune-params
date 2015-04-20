#!/usr/bin/env python
from glob import glob
from setuptools import setup

setup(name='dune-params',
      provides = [ "dune.params" ],
      version='0.0.0',
      url='https://github.com/DUNE/dune-params',
      author='Brett Viren',
      author_email='bv@bnl.gov',
      packages = ['dune','dune.params'],
      data_files = [('data',glob('data/*.xls'))],
      install_requires = [l for l in open("requirements.txt").readlines() if l.strip()],
      entry_points='''
      [console_scripts]
      dune-params=dune.params.main:main
      ''',
      )
