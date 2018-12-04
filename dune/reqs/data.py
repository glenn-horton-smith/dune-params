#!/usr/bin/env python3
'''
Requirements data.

Any "short name" here must be composed of only letters.

Item,Type,System,Quantity/Parameter,Requirement,Goal,Explanation,Comments,Notes,ProtoDUNE Validation,Simulation Validation
'''

from collections import namedtuple

from dune import latex


class NumericalRequirement(object):
    def __init__(self, comp, value, unit):
        self.type = "numerical"
        self.comp = comp
        self.value = value
        self.unit = unit

    def latex_dict(self):
        'Return dict with values suitable for use in latex'
        return dict(type=self.type, comp=latex.symbol(self.comp),
                    value=self.value, unit=self.unit, siunitx=latex.siunitx(self.value, self.unit))

class DescriptiveRequirement(object):
    def __init__(self, text):
        self.type = "descriptive"
        self.text = text
    def latex_dict(self):
        'Return dict with values suitable for use in latex'
        return dict(type=self.type, text=self.text)
        

class Spec(namedtuple("Spec", [
        "category",             # short name, globally unique classifying related specs
        "label",                # short name, unique to the category
        "number",               # small integer count
        "field",                # label the field of study determining the spec
        "system",               # label the portion of the experiment do which the spec pertains
        "title",                # a short description that names the spec.
        "requirement",          # a statement of requirement, may be a NumericalRequiement or DescriptiveRequirement
        "goal",                 # a short description of the "stretch goal" for the spec
        "explanation",          # text explaining the choice of the requirement
        "comment",             #
        "notes",                #
        "validation", # dict of validation methods, if any
        ])):

    def latex_dict(self):
        'Return dict with values suitable for use in latex'
        ret = dict()
        for k,v in list(self.items()):
            if hasattr(v, "latex_dict"):
                ret[k] = v.latex_dict()
            else:
                ret[k] = v
        return ret
        
