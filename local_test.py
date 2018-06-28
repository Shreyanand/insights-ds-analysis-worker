#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 11:04:25 2018

@author: shrey
"""
import os
import json
tests = [ ['cpu_count','cache_size'], ['cache_size'], ['cpu_count','vendor'], ['vendor'], ['model_name','vendor'] ]
for i in tests:
    name = "graphs" + str(i) + ".json"
    params = {"PARSER_NAME": "2018-04-11/insights_parsers_cpuinfo_cpuinfo", "COL_NAME": i, "OUTFILE_NAME":name  }
    os.environ["PARAMS"] = json.dumps(params)
    print(os.environ.get('PARAMS'))
    runfile(os.path.join(os.getcwd(),"app.py"), wdir=os.getcwd())