#!/usr/bin/env python
# encoding: utf-8

import matplotlib.pyplot as plt
import timeit

FUNCS = [{
    'func': '1 - normalized_damerau_levenshtein_distance("{s1}", "{s2}")',
    'fimport': 'from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance',
    'label': 'dameraudamerau  levenshtein'
}, {
    'func': 'difflib.SequenceMatcher(None, "{s1}", "{s2}", autojunk=False).ratio()',
    'fimport': 'import difflib',
    'label': 'ratcliff_obershelp'
}, {
    'func': '1 - distance.nlevenshtein("{s1}", "{s2}")',
    'fimport': 'import distance',
    'label': 'levenshtein'
}
, {
    'func': 'adj_dlevenshtein.string_similarity_ratio("{s1}", "{s2}")',
    'fimport': 'import adj_dlevenshtein',
    'label': 'adjusted damerau levenshtein'
}]

def benchmark(s1, s2, n, **kwargs):
    return timeit.timeit(
        kwargs['func'].format(s1=s1, s2=s2), kwargs['fimport'], number=n
    )

def plot(N, STEP):
    plt.title('String compare analysis with ,,Erdmännchen" vs ,,Khaleesi"')
    plt.ylabel('time in milliseconds')
    plt.xlabel('string multiplication factor')
    plt.xlim(1, N / STEP)

    # plt.xscale('log')
    plt.yscale('log')

    plt.axes().xaxis.set_ticks_position('bottom')
    plt.axes().yaxis.set_ticks_position('left')
    plt.grid(True)

    plt.legend()
    plt.show()

def add_plot(plt, data, label):
    plt.plot(
        [y for y, _ in data],
        [x for _, x in data],
        'o-',
        label=label
    )

if __name__ == "__main__":
    s1 = 'Erdmännchen'
    s2 = 'Khaleesi'
    data = []
    N, STEP = 100, 5

    for algo in FUNCS:
        print('Benchmarking {algo}'.format(algo=algo['label']))
        for num in range(1, N + 1, STEP):
            fac = num // STEP + 1
            print(num, fac, STEP)
            timing = benchmark(s1 * fac, s2 * fac, 50, **algo)
            data.append((fac, timing * 100))
        add_plot(plt, data, algo['label'])
        data = []

    plot(N, STEP)
