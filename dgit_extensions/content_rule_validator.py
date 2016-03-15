#!/usr/bin/env python 

import os, sys
from dgitcore.plugins.validator import ValidatorBase
from dgitcore.config import get_config, ChoiceValidator
from dgitcore.helper import compute_sha256 

class ContentRuleValidator(ValidatorBase):     
    """
    Simple validator backend for the datasets.

    Parameters
    ----------
    """
    def __init__(self): 
        self.enable = False 
        self.token = None 
        self.url = None 
        super(ContentRuleValidator, self).__init__('content-rule-validator', 
                                                   'v0', 
                                                   "Apply content validation rules")

    def config(self, what='get', params=None): 
        
        if what == 'get': 
            return {
                'name': 'content-rule-validator', 
                'nature': 'validator',
                'variables': ['enable'], 
                'defaults': { 
                    'enable': {
                        "value": 'y',
                        "description": "Enable content validation",
                        "validator": ChoiceValidator(['y','n'])
                    },
                }
            }
        else:
            self.enable = params['content-rule-validator']['enable']


    def evaluate(self, repomanager, key): 
        """
        Evaluate the repo
        
        Parameters
        ----------

        repo manager
        repo
        """
        repo = repomanager.get_repo_details(key)    
        rootdir = repo['rootdir']    
        package = repo['package'] 
        
        files = package['resources'] 
        print('files', len(files))
        for f in files: 
            print(f['relativepath'])
            coded_sha256 = f['sha256'] 
            computed_sha256 = compute_sha256(os.path.join(rootdir,
                                                          f['relativepath']))
            if computed_sha256 != coded_sha256: 
                print("Sha 256 mismatch between file and datapackage")
    


    
def setup(mgr): 
    
    obj = ContentRuleValidator() 
    mgr.register('validator', obj)

