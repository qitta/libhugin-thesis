#!/usr/bin/env python

from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
import math
import pprint
from adj_dlevenshtein import string_similarity_ratio

def compare(search_title, titles):
    ratings = {}
    for title in titles:
        t, y = title.split(';')
        st, sy = search_title.split(';')
        penalty = 1 - min(1, abs(int(y) - int(sy)) / 15)
        rating = round((string_similarity_ratio(t, st) * 3 + penalty) / 4, 3)
        ratings[title] = rating
    return ratings

def compare_dl(search_title, titles):
    ratings = {}
    for title in titles:
        rating = round(string_similarity_ratio(search_title, title), 3)
        ratings[title] = rating
    return ratings


if __name__ == '__main__':
    a = 'Matrix; 1999'
    b = [
        'Matrix; 1999', 'Matrix; 2000', 'Matrix; 2001', 'Matrix; 1997',
        'Matrix, The; 1999', 'The Matrix; 2013', 'The East; 1999'
    ]

    ratings = compare(a, b)
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    pprint.pprint(ratings)

    ratings = compare_dl(a, b)
    ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    pprint.pprint(ratings)



