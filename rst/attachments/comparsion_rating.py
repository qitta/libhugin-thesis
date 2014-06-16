#!/usr/bin/env python
# encoding: utf-8

import difflib
from itertools import combinations_with_replacement
from adj_dlevenshtein import string_similarity_ratio
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_dl


if __name__ == "__main__":

    titles = ['Spiderman', 'Superman', 'Batman', 'Iron-Man']

    for str1, str2 in combinations_with_replacement(titles, 2):
        diff_lib = round(difflib.SequenceMatcher(None, str1, str2).ratio(),2)
        damerau_levenshtein = round(1 - norm_dl(str1, str2), 2)
        print(
            "{} <--> {}\ndifflib\t\t {}\ndlevenshtein\t {}\n".format(
                str1, str2, diff_lib, damerau_levenshtein)
        )
