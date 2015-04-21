#!/usr/bin/env python
'''
DUNE Params Data Objects
'''
from .units import Q

from collections import namedtuple

class Unit(namedtuple("Unit","name comment latex")):
    pass

class Param(object):

    def __init__(self, variable, value, unit=None, name=None, provenance='', description='', notes=''):
        if type(value) == Q:
            if unit:
                self.q = value.to(unit)
            else:
                unit = value.unit
                self.q = value
            value = self.q.magnitude
        else:
            value = float(value) # fixme: should add type to spread sheet
            self.q = Q(value, unit)            
        if not name:
            name = variable.replace('_',' ').replace('-',' ')
        self.variable = variable
        self.value = value
        self.unit = unit
        self.name = name
        self.provenance = provenance
        self.description = description
        self.notes = notes
    pass

class ParamSet(object):
    def __init__(self):
        self.units = dict()     # by name to Unit
        self.params = dict()    # by variable name

    def add(self, param):
        '''
        Add a parameter to the set.
        '''
        unit = param.unit
        if unit and not self.units.has_key(unit):
            raise ValueError('No such unit: "%s"' % unit)
        self.params[param.variable] = param

    def __getattr__(self, name):
        p = self.params[name]
        return p.q              # mind them!

