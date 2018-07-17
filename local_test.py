#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:04:25 2018

@author: shrey
"""
import os
import json
from datetime import datetime as dtm
tests = [ ['cpu_count','cache_size'], ['cache_size'], ['cpu_count','vendor'], ['vendor'], ['model_name','vendor'] ]
#tests = [['cache_siz']]
for i in tests:
    name = 'Analysis_for_' + str(i) + '_at_' + str(dtm.now()) + ".json"
    params = {"PARSER_NAME": "2018-04-11/insights_parsers_cpuinfo_cpuinfo", "COL_NAME": i, "OUTFILE_NAME":name  }
    os.environ["PARAMS"] = json.dumps(params)
    print(os.environ.get('PARAMS'))
    runfile(os.path.join(os.getcwd(),"app.py"), wdir=os.getcwd())