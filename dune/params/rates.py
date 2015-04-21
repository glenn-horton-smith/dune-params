#!/usr/bin/env python
'''
Estimate data rates.
'''

from .data import Param

def filter(ps):
    '''
    Take a ParamSet, return a new one loaded with derived rate-related parameters.
    '''
    ps.add(Param('tpc_drift_time', ps.tpc_drift_distance / ps.tpc_drift_velocity, 
                 'millisecond', 'Drift time'))
    return ps
    
