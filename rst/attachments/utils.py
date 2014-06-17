#!/usr/bin/env python
# encoding: utf-8

import os
import json

def analyze_folder(path):
    data = {}
    for f in os.listdir(path):
        with open(os.path.join(path, f), 'r') as fp:
            provider, _, _ = f.split(';')
            data[provider] = json.loads(fp.read())
    return data
