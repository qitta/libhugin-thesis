#!/usr/bin/env python
# encoding: utf-8

from collections import Counter
from utils import analyze_folder
import pprint
import sys

import os
import json

PROVIDERS = {
    'tmdb':2500, 'ofdb':2500, 'omdb':2500, 'videobuster':2444, 'filmstarts':2427
}
def update_value_availability(results, provider):
    name, jsonfile = provider
    for key, value in jsonfile.items():
        if value:
            results[name][key] += 1

def analyze():
    results = {p: Counter() for p in PROVIDERS.keys()}
    for folder in os.listdir(sys.argv[1]):
        if os.path.isdir(folder):
            providers = analyze_folder(folder)
            for provider in providers.items():
                update_value_availability(results, provider)
    return results

def invert_results(data):
    for name, values in data.items():
        for key, cnt in values.items():
            data[name][key] = PROVIDERS[name] - cnt
    return data

if __name__ == '__main__':
    data = analyze()
    pprint.pprint(invert_results(data))
    print()