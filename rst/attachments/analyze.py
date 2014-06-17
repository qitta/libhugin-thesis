#!/usr/bin/env python
# encoding: utf-8

from collections import Counter
from statistics import mean
from utils import analyze_folder
import pprint, os, sys, json

PROVIDERS = ['tmdb', 'ofdb', 'omdb', 'videobuster', 'filmstarts']

def json_iterator():
    for folder in os.listdir(sys.argv[1]):
        if not os.path.isdir(folder):
            continue

        providers = analyze_folder(folder)
        for provider, json_file in providers.items():
            yield provider, json_file

def count_attribute(attribute):
    results = {provider: Counter() for provider in PROVIDERS}
    for provider, json_file in json_iterator():
        for attr in json_file[attribute] or ['Kein Genre']:
            results[provider][attr] += 1
    return results

def count_attribute_len(attribute):
    results = {provider: [] for provider in PROVIDERS}
    for provider, json_file in json_iterator():
        results[provider].append(len(json_file[attribute] or []))
    return results

if __name__ == '__main__':
    counts = count_attribute('genre')
    pprint.pprint(counts)

    counts = count_attribute_len('genre')
    for prov, gen in counts.items():
        print('{p}: ({i}/{a}/{x})'.format(
            p=prov, i=min(gen), a=round(mean(gen), 2), x=max(gen))
        )
        for i in range(8):
            print('#{i}: {c}'.format(i=i, c=gen.count(i)))
