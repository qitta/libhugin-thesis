#!/usr/bin/env python

from collections import defaultdict
from statistics import mean
import time
import timeit
import numpy
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
    'func': 'httplib2.Http().request("http://www.videobuster.de/titlesearch.php?tab_search_content=movies&view=title_list_view_option_list&search_title={title}")',
    'fimport': 'import httplib2',
    'label': 'videobuster'
}

tmdb = {
    'func': 'httplib2.Http().request("http://api.themoviedb.org/3/search/movie?api_key=ff9d65f1e39e8a239124b7e098001a57&query={title}")',
    'fimport': 'import httplib2',
    'label': 'tmdb'
}


def benchmark(string, **kwargs):
    kwargs['func'] = kwargs['func'].format(title=string)
    return timeit.timeit(
        kwargs['func'], kwargs['fimport'], number=1
    )


if __name__ == "__main__":

    movies = [
            'Prometheus', 'Avatar', 'Matrix', 'Shame', 'Juno', 'Drive',
            'Hulk', 'Rio', 'Alien', 'Wrong'
            ]

    times = defaultdict(list)
    for x in range(10):
        for title in movies:
            for algo in [ofdb, tmdb, videobuster, omdb, filmstarts]:
                result = benchmark(title, **algo)
                times[algo['label']].append(result * 1000)
                time.sleep(0.5)

    for k, v in times.items():
        times[k] = (min(v), mean(v), max(v))

    providers = list(times.keys())
    y_pos = numpy.arange(len(providers))

    for value, color in [(2, 'r'), (1, 'y'), (0, 'g')]:
        response_ms = [p[value] for p in times.values()]
        plt.barh(y_pos, response_ms, align='center', alpha=0.7, color=color)

    plt.yticks(y_pos, providers)
    plt.xlabel('time in milliseconds')
    plt.title('download performance by online source.')
    plt.show()
