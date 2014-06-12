#!/usr/bin/env python

from collections import Counter
from statistics import mean
import difflib
import pprint
import os
import sys
import json

COUNTER = 0

def analyze_folder(path):
    d = {}
    for f in os.listdir(path):
        with open(os.path.join(path, f), 'r') as fp:
            provider, _, _ = f.split(';')
            d[provider] = json.loads(fp.read())
    return d

def directors_equal(tmdb, nontmdb, threshold=0.95):
    d1, d2 = tmdb.get('directors', []), nontmdb.get('directors', [])
    if d1 and d2:
        if len(d1) == 1 and len(d2) == 1:
            if difflib.SequenceMatcher(None, d1[0].lower(), d2[0].lower() ).ratio() > threshold:
                return True

def test_print(tmdb, nontmdb):
    global COUNTER
    fmt = "{})\n{}\n{}\n{}\n{}\n".format(
        COUNTER, tmdb['title'], nontmdb['title'],
        tmdb['directors'], nontmdb['directors']
    )
    print(fmt)
    COUNTER += 1

def check_similarity(tmdb, nontmdb, threshold=0.90):
    diff = abs(int(tmdb.get('year')) - int(nontmdb.get('year')))
    ratio = difflib.SequenceMatcher(
                None, tmdb['title'].lower(), nontmdb['title'].lower()
            ).ratio()

    # handle movies by imdbid
    if nontmdb.get('imdbid'):
        if tmdb.get('imdbid') == nontmdb.get('imdbid'):
            return diff

    # handle movies with no imdbid
    elif ratio > threshold:
        if diff > 4:
        #if diff > 0 and diff < 4:
            if not directors_equal(tmdb, nontmdb):
                test_print(tmdb, nontmdb)
        return diff

def calculate_year_diff():
    results = {p: Counter() for p in ['ofdb', 'omdb', 'videobuster', 'filmstarts']}
    for folder in os.listdir(sys.argv[1]):
        if os.path.isdir(folder):
            providers = analyze_folder(folder)
            prov = {v:k for v, k in providers.items() if k.get('year')}
            if 'tmdb' in prov:
                for name, jsonfile in prov.items():
                    if name != 'tmdb':
                        result = check_similarity(prov['tmdb'], jsonfile)
                        if result is not None:
                            results[name][result] += 1

    return results

if __name__ == '__main__':
    d = calculate_year_diff()
    pprint.pprint(d)
