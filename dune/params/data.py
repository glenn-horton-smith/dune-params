#!/usr/bin/env python
'''
DUNE Params Data Objects
'''
from .units import Q

from collections import namedtuple

class Unit(namedtuple("Unit","name comment latex")):
    pass

class Param(object):

    def __init__(self, variable, value, unit=None, name=None, provenance='', description='', notes='', precision=None):
        if type(value) == Q:
            if unit:
                self.q = value.to(unit)
            else:
                unit = getattr(value,'unit', '')
                self.q = value
            value = self.q.magnitude
        else:
            try:
                value = float(value) # fixme: should add type to spread sheet
            except ValueError:
                print(('Failed to convert "%s" = "%s" to float' %(variable, value)))
                raise
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
        self.precision = precision
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
        if unit and unit not in self.units:
            raise ValueError('No such unit: "%s"' % unit)
        self.params[param.variable] = param

    def __getattr__(self, name):
        p = self.params[name]
        return p.q              # mind them!

    def keys(self):
        return list(self.params.keys())

    def items(self):
        return [(k,getattr(k)) for k in list(self.keys())]

    def dict(self):
        return {k:self.params[k] for k in list(self.keys())}
