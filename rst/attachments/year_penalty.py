#!/usr/bin/env python
# encoding: utf-8

from adj_dlevenshtein import string_similarity_ratio
from pprint import pprint

def compare(search_title, titles, max_years=15):
    ratings = {}
    for title in titles:
        t, y = title.split(';')
        st, sy = search_title.split(';')
        year_sim = 1 - min(1, abs(int(y) - int(sy)) / max_years)
        rating = round((string_similarity_ratio(t, st) * 3 + year_sim) / 4, 3)
        ratings[title] = rating
    return ratings

def compare_dl(search_title, titles):
    s = string_similarity_ratio
    return {title: round(s(search_title, title), 3) for title in titles}

if __name__ == '__main__':
    a = 'Matrix; 1999'
    b = [
        'Matrix; 1999', 'Matrix; 2000', 'Matrix; 2001', 'Matrix; 1997',
        'Matrix, The; 1999', 'The Matrix; 2013', 'The East; 1999'
    ]

    for func in (compare, compare_dl):
        ratings = func(a, b)
        ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
        pprint(ratings)
