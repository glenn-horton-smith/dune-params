#!/usr/bin/env python

from dune.params.units import Q

def test_div():
    x = Q('3.6 meter')
    y = Q('1.6 millimeter / microsecond')
    z = x/y
    assert z
    print((type(x),type(y),type(z)))
    print((z.to('millisecond')))

