#!/usr/bin/env python

import dune.params.io as dpio
import common 

def test_load():
    dat = dpio.load(common.example_xls)
    assert dat.units
    assert dat.params
