#!/usr/bin/env python

from matplotlib.pyplot import step, legend, xlim, ylim, show
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import difflib, timeit


DL = {
    'func': '1 - normalized_damerau_levenshtein_distance("{s1}", "{s2}")',
    'fimport': 'from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance',
    'label': 'dameraudamerau  levenshtein'
}

RO = {
    'func' : 'difflib.SequenceMatcher(None, "{s1}", "{s2}", autojunk=False).ratio()',
    'fimport' : 'import difflib',
    'label': 'ratcliff_obershelp'
}

L = {
    'func' : '1 - distance.nlevenshtein("{s1}", "{s2}")',
    'fimport' : 'import distance',
    'label': 'levenshtein'
}

J = {
    'func' : '1 - distance.jaccard("{s1}", "{s2}")',
    'fimport' : 'import distance',
    'label' : 'jaccard'
}

ADL = {
    'func' : 'adj_dlevenshtein.string_similarity_ratio("{s1}", "{s2}")',
    'fimport' : 'import adj_dlevenshtein',
    'label' : 'adjusted damerau levenshtein'
}

def benchmark(s1, s2, n, **kwargs):
    return timeit.timeit(
        kwargs['func'].format(s1=s1, s2=s2), kwargs['fimport'], number=n
    )

def add_plot(plt, data, label):
    plt.plot(
        [y for y, _ in data],
        [x for _, x in data],
        label=label
    )


if __name__ == "__main__":

    s1 = 'klasjdlaksjd alskdj aklsdj aklsjd laksj dlaskdj ist Great'
    s2 = 'jee jee xyz noooo'

    data = []
    for algo in [RO]:
        print('Benchmarking {algo}'.format(algo=algo['label']))
        step = 30
        for num in range(1, 500 + 1, step):
            fac = num // step + 1
            print(fac)
            value = benchmark(s1 * fac, s2 * fac, 1000, **algo)
            data.append((fac, value * 1000))
        add_plot(plt, data, algo['label'])
        data = []

    plt.title('String compare analysis with ,,Only God Forgives (2011)"')
    plt.ylabel('time in milliseconds')
    plt.xlabel('amount of string comparisons')

    # plt.xscale('log')
    plt.yscale('log')

    plt.axes().xaxis.set_ticks_position('bottom')
    plt.axes().yaxis.set_ticks_position('left')

    legend()
    plt.show()
