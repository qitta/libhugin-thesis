#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict
from statistics import mean
from functools import partial
from hugin.harvest.session import Session
import timeit, numpy
import matplotlib.pyplot as plt

def benchmark(s, q):
    return s.submit(q)

def plot(times):
    providers = list(times.keys())
    y_pos = numpy.arange(len(providers))

    for value, color in [(2, 'r'), (1, 'y'), (0, 'g')]:
        response_ms = [p[value] for p in times.values()]
        plt.barh(y_pos, response_ms, align='center', alpha=0.7, color=color)

    plt.yticks(y_pos, providers)
    plt.xlabel('time in milliseconds')
    plt.title('libhugin download performance by online source.')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    do_cache = False
    movies = [
        'Prometheus', 'Avatar', 'Matrix', 'Shame', 'Juno', 'Drive',
        'Hulk', 'Rio', 'Alien', 'Wrong'
    ]

    providers = [
        'ofdbmovie', 'tmdbmovie', 'videobustermovie', 'omdbmovie', 'filmstartsmovie'
    ]

    N = 3

    s = Session(parallel_downloads_per_job=1, cache_path='.')
    times = defaultdict(list)

    for _ in range(N):
        for title in movies:
            for provider in providers:
                qry = s.create_query(
                    title=title, cache=do_cache, providers=[provider],
                    amount=1, retries=150
                )
                result = timeit.Timer(partial(benchmark, s, qry)).timeit(number=1)
                times[provider].append(result * 1000)

    for key, value in times.items():
        times[key] = (min(value), mean(value), max(value))

    plot(times)
