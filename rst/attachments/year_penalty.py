#!/usr/bin/env python

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
import math
import pprint
from adj_dlevenshtein import string_similarity_ratio

def compare(search_title, titles):
    ratings = {}
    for title in titles:
        t, y = title.split(',')
        st, sy = search_title.split(',')
        penalty = 1 - round( abs(int(y) - int(sy)) / max(int(y), int(sy)) * 10, 3 )
        rating = string_similarity_ratio(t, st) * penalty
        ratings[title] = rating
    return ratings



if __name__ == '__main__':
    a = 'The East, 2013'
    b = [
        'The East, 2002', 'The East, 2009', 'The East, 1995', 'The East, 2014',
        'The East, 2001', 'The East, 2013', 'The East, 2012'
    ]

    ratings = compare(a, b)
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    pprint.pprint(ratings)



