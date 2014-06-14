#!/usr/bin/env python

from collections import defaultdict
from statistics import mean
import time
import timeit
import numpy
import matplotlib.pyplot as plt
from functools import partial
from hugin.harvest.session import Session

def benchmark(s, q):
    return s.submit(q)


if __name__ == "__main__":

    movies = [
            'Prometheus', 'Avatar', 'Matrix', 'Shame', 'Juno', 'Drive',
            'Hulk', 'Rio', 'Alien', 'Wrong'
            ]

    s = Session(parallel_downloads_per_job=10, cache_path='lecachex')
    times = defaultdict(list)
    for x in range(10):
        for title in movies:
            for provider in ['ofdbmovie', 'tmdbmovie', 'videobustermovie', 'omdbmovie', 'filmstartsmovie']:
                q = s.create_query(title=title, cache=True, providers=[provider], amount=1, retries=150)
                result = timeit.Timer(partial(benchmark, s, q)).timeit(number=1)
                times[provider].append(result * 1000)

    for k, v in times.items():
        times[k] = (min(v), mean(v), max(v))

    providers = list(times.keys())
    y_pos = numpy.arange(len(providers))

    for value, color in [(2, 'r'), (1, 'y'), (0, 'g')]:
        response_ms = [p[value] for p in times.values()]
        plt.barh(y_pos, response_ms, align='center', alpha=0.7, color=color)

    plt.yticks(y_pos, providers)
    plt.xlabel('time in milliseconds')
    plt.title('libhugin download performance by online source.')
    plt.show()
