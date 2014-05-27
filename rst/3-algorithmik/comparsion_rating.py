#!/usr/bin/env python

import difflib
from itertools import combinations_with_replacement
from adj_dlevenshtein import string_similarity_ratio
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance


if __name__ == "__main__":

    titles = ['Spiderman', 'Superman', 'Batman', 'Iron-Man']

    for str1, str2 in combinations_with_replacement(titles, 2):
        print(str1, "vs", str2)
        print("difflib:", round(difflib.SequenceMatcher(None, str1, str2).ratio(),2))
        print("damlev: ", round(1 - normalized_damerau_levenshtein_distance(str1, str2), 2))
        print()
