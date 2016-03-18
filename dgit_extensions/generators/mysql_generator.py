#!/usr/bin/env python 

import os, sys, getpass, traceback 
from dgitcore.helper import cd 
from dgitcore.plugins.generator import GeneratorBase
from dgitcore.config import get_config, ChoiceValidator, NonEmptyValidator 
import MySQLdb

class MySQLGenerator(GeneratorBase):     
    """
    Simple generator backend for the datasets.

    Parameters
    ----------
    """
    def __init__(self): 
        self.enable = False 
        self.host = None
        self.port = 3036 
        self.username = None
        self.password = None
        super(MySQLGenerator, self).__init__('mysql-generator', 
                                             'v0', 
                                             "Materialize queries in dataset")
        
    def config(self, what='get', params=None): 
        
        if what == 'get': 
            return {
                'name': 'mysql-generator', 
                'nature': 'generator',
                'variables': ['enable', 'host', 'port', 'db', 'username', 'password'], 
                'defaults': { 
                    'enable': {
                        "value": 'y',
                        "description": "Enable content validation",
                        "validator": ChoiceValidator(['y','n'])
                    },
                    'host': {
                        "value": 'localhost',
                        "description": "MySQL server host name",
                        "validator": NonEmptyValidator()
                    },
                    'port': {
                        "value": '3306',
                        "description": "MySQL server port",
                        "validator": NonEmptyValidator()
                    },
                    'db': {
                        "value": '',
                        "description": "DB for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                    'username': {
                        "value": getpass.getuser(),
                        "description": "Username for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                    'password': {
                        "value": '',
                        "description": "Password for MySQL access",
                        "validator": NonEmptyValidator()
                    },
                }
            }
        else:
            if 'mysql-generator' not in params: 
                self.enable = 'n'
            else: 
                self.enable = params['mysql-generator']['enable'] 
                if self.enable == 'n': 
                    return 
                    
                # Collect parameters
                self.host = params['mysql-generator']['host']
                self.port = int(params['mysql-generator']['port'])
                self.db = params['mysql-generator']['db']
                self.username = params['mysql-generator']['username']
                self.password = params['mysql-generator']['password']
            
                # Test the connection 
                try: 
                    db=MySQLdb.connect(host=self.host,
                                       port=self.port, 
                                       db=self.db,
                                       user=self.username,
                                       passwd=self.password)
                    if db is None: 
                        print("Unable to connect to MySQL Server. Please check ini file") 
                        self.enable = 'n'
                    db.close() 

                except:
                    traceback.print_exc()
                    print("Unable to connect to MySQL Server. Please check ini file") 
                    self.enable = 'n'


    def  evaluate(self, repo, files, params=None): 
        
        if len(files) == 0: 
            # Nothing to do 
            return [] 

        db=MySQLdb.connect(host=self.host,
                           port=self.port, 
                           db=self.db,
                           user=self.username,
                           passwd=self.password)
        cur = db.cursor()

        result = []
        with cd(repo.rootdir): 
            for f in files: 
                query = open(f, 'r').read()
                cur.execute(query)                
                
                content = ""
                num_fields = len(cur.description)
                field_names = [i[0] for i in cur.description]
                content += "\t".join(field_names)
                for row in cur.fetchall():
                    content += "\n" + "\t".join(list(row))
                print(content)
                result.append({
                    'target': files[0],
                    'generator': self.name,
                    'status': 'OK',
                    'message': ''
                })
        return result 

def setup(mgr): 

    obj = MySQLGenerator() 
    mgr.register('generator', obj)

