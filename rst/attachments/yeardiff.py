#!/usr/bin/env python
# encoding: utf-8

from collections import Counter
import difflib
import pprint
import os
import sys
import json

COUNTER = 0

def analyze_folder(path):
    result = {}
    for json_file in os.listdir(path):
        with open(os.path.join(path, json_file), 'r') as handle:
            provider, _, _ = json_file.split(';')
            result[provider] = json.loads(handle.read())
    return result

def directors_equal(tmdb, nontmdb, threshold=0.95):
    d1, d2 = tmdb.get('directors', []), nontmdb.get('directors', [])
    if not all((d1, d2)):
        return False

    if len(d1) == len(d2) == 1:
        ratio = difflib.SequenceMatcher(None, d1[0].lower(), d2[0].lower()).ratio()
        return ratio > threshold

def test_print(tmdb, nontmdb):
    global COUNTER
    print("{})\n{}\n{}\n{}\n{}\n".format(
        COUNTER, tmdb['title'], nontmdb['title'],
        tmdb['directors'], nontmdb['directors']
    ))
    COUNTER += 1

def check_similarity(tmdb, nontmdb, threshold=0.90):
    diff = abs(int(tmdb.get('year')) - int(nontmdb.get('year')))
    ratio = difflib.SequenceMatcher(
        None, tmdb['title'].lower(), nontmdb['title'].lower()
    ).ratio()

    # handle movies by imdbid
    if nontmdb.get('imdbid') and tmdb.get('imdbid') == nontmdb.get('imdbid'):
        return diff

    # handle movies with no imdbid
    elif ratio > threshold and diff > 4 and not directors_equal(tmdb, nontmdb):
        test_print(tmdb, nontmdb)
        return diff

def calculate_year_diff():
    results = {p: Counter() for p in ['ofdb', 'omdb', 'videobuster', 'filmstarts']}
    for folder in os.listdir(sys.argv[1]):
        if not os.path.isdir(folder):
            continue

        providers = analyze_folder(folder)
        prov = {k: v for k, v in providers.items() if v.get('year')}
        if 'tmdb' not in prov:
            continue

        for name, jsonfile in prov.items():
            if name == 'tmdb':
                continue

            result = check_similarity(prov['tmdb'], jsonfile)
            if result is not None:
                results[name][result] += 1

    return results

if __name__ == '__main__':
    pprint.pprint(calculate_year_diff())
