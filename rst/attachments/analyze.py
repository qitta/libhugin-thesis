#!/usr/bin/env python

from collections import Counter
from statistics import mean
import pprint
import os
import sys
import json


def analyze_folder(path):
    d = {}
    for f in os.listdir(path):
        with open(os.path.join(path, f), 'r') as fp:
            provider, _, _ = f.split(';')
            d[provider] = json.loads(fp.read())
    return d

def count_genre(attribute):
    d = {
        'tmdb': Counter(),
        'ofdb': Counter(),
        'omdb': Counter(),
        'videobuster': Counter(),
        'filmstarts': Counter()
    }
    attrs = [attribute]
    for folder in os.listdir(sys.argv[1]):
        if os.path.isdir(folder):
            providers = analyze_folder(folder)
            for provider, value in  providers.items():
                if value[attribute]:
                    for attr in value[attribute]:
                        d[provider][attr] += 1
                else:
                    d[provider]['none'] += 1
    return d

def count_genre_len(attribute):
    d = {
        'tmdb': list(), 'ofdb': list(), 'omdb': list(),
        'videobuster': list(), 'filmstarts': list()
    }
    attrs = [attribute]
    for folder in os.listdir(sys.argv[1]):
        if os.path.isdir(folder):
            providers = analyze_folder(folder)
            for provider, value in  providers.items():
                if value[attribute]:
                    d[provider].append(len(value[attribute]))
                else:
                    d[provider].append(0)

    return d

if __name__ == '__main__':
    d = count_genre('genre')
    pprint.pprint(d)

    d = count_genre_len('genre')
    for prov, gen in d.items():
        print(prov, 'min:', min(gen), 'mean:', round(mean(gen), 2), 'max:', max(gen))
        for x in range(8):
            print('Num:', x, 'Count:', gen.count(x))


