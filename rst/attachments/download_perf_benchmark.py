#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict
from statistics import mean
import timeit
import numpy
import time
import matplotlib.pyplot as plt

ofdb = {
    'func': 'httplib2.Http().request("http://ofdbgw.geeksphere.de/search_json/{title}")',
    'fimport': 'import httplib2',
    'label': 'ofdb'
}

omdb = {
    'func': 'httplib2.Http().request("http://www.omdbapi.com/?s={title}")',
    'fimport': 'import httplib2',
    'label': 'omdb'
}

filmstarts = {
    'func': 'httplib2.Http().request("http://www.filmstarts.de/suche/?q={title}")',
    'fimport': 'import httplib2',
    'label': 'filmstarts'

}

videobuster = {
    'func': 'httplib2.Http().request("http://www.videobuster.de/' \
            'titlesearch.php?tab_search_content=movies' \
            '&view=title_list_view_option_list&search_title={title}")',
    'fimport': 'import httplib2',
    'label': 'videobuster'
}

tmdb = {
    'func': 'httplib2.Http().request("http://api.themoviedb.org/3/search/' \
            'movie?api_key=ff9d65f1e39e8a239124b7e098001a57&query={title}")',
    'fimport': 'import httplib2',
    'label': 'tmdb'
}

def benchmark(string, **kwargs):
    kwargs['func'] = kwargs['func'].format(title=string)
    return timeit.timeit(kwargs['func'], kwargs['fimport'], number=1)

def plot(providers):
    plt.yticks(y_pos, providers)
    plt.xlabel('time in milliseconds')
    plt.title('response time by online source.')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    N = 10
    movies = [
        'Prometheus', 'Avatar', 'Matrix' #, 'Shame', 'Juno',
        #'Hulk', 'Rio', 'Alien', 'Wrong', 'Drive',
    ]

    times = defaultdict(list)

    for _ in range(N):
        for title in movies:
            for algo in [ofdb, tmdb, videobuster, omdb, filmstarts]:
                result = benchmark(title, **algo)
                times[algo['label']].append(result * 1000)

    for k, v in times.items():
        times[k] = (min(v), mean(v), max(v))

    providers = list(times.keys())
    y_pos = numpy.arange(len(times))

    for value, color, label in [(2, 'r', 'max'), (1, 'y', 'avg'), (0, 'g', 'min')]:
        response_ms = [p[value] for p in times.values()]
        plt.barh(y_pos, response_ms, align='center', alpha=0.7, color=color, label=label)

    plot(providers)
