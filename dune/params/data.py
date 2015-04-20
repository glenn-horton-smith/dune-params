#!/usr/bin/env python
'''
DUNE Params Data Objects
'''

from collections import namedtuple

class Unit(namedtuple("Unit","name comment latex")):
    pass

class Param(namedtuple("Param","variable name value unit category provenance description notes")):
    pass

class ParamSet:
    def __init__(self):
        self.units = dict()     # name to Unit
        self.params = dict()    # variable to Param
