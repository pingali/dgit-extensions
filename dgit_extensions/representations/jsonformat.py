#!/usr/bin/env python

import os, sys, glob2, json
import json_delta 
from collections import OrderedDict
from dgitcore.plugins.representation import RepresentationBase
from dgitcore.config import get_config
from dgitcore.helper import cd
import daff 
from messytables import type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor, any_tableset

class JSONRepresentation(RepresentationBase):
    """
    Process tables in various forms

    Parameters
    ----------
    """
    def __init__(self):
        self.enable = 'y'
        super(JSONRepresentation, self).__init__('json-representation',
                                                 'v0',
                                                 "Compute schema and diffs for JSON/dictionaries")

    def config(self, what='get', params=None):

        if what == 'get':
            return {
                'name': 'json-representation',
                'nature': 'representation',
                'variables': [],
            }

    def can_process(self, filename): 
        
        for ext in ['json']: 
            if filename.lower().endswith(ext):
                return True 
                
        return False 

        
    def get_schema(self, filename):
        """
        Guess JSON schema. Not supported yet
        """
        return []


    def get_diff(self, filename1, filename2):

        ext = filename1.split(".")[-1].lower() 
        if ext not in ['json']: 
            return None

        d1 = json.loads(open(filename1).read())
        d2 = json.loads(open(filename2).read())
        diff = json_delta.diff(d1, d2, verbose=False)

        #[
        #    [['validator', 'metadata-validator', 'files', 1], '*.txt'],  # List addition 
        #    [['track', 'excludes', 3], 'datapackage.json'], 
        #    [['username'], 'pingali1'] # value change
        #    [['track', 'includes', 2]], # List deletion 
        #    [['auto-push']], # key deletion
        #    [['hello'], 12]] # new key 
        #]

        changes = { 
            'New keys or values': 0,
            'Keys deleted': 0,
            'List values added': 0,
            'List values deleted': 0
            }
        
        for d in diff:
            if len(d) == 2: 
                if isinstance(d[0][-1], int):
                    changes['List values added'] += 1 
                else: 
                    changes['New keys or values'] += 1 
            else: 
                if isinstance(d[0][-1], int):
                    changes['List values deleted'] += 1 
                else: 
                    changes['Keys deleted'] += 1 

        summary = { 
            'data': {}
        }
        for c in changes: 
            summary['data'][c] = [c, changes[c]]

        return summary


def setup(mgr):

    obj = JSONRepresentation()
    mgr.register('representation', obj)


