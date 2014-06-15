#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict
import timeit
import matplotlib.pyplot as plt
from functools import partial
from hugin.harvest.session import Session

N_THREADS = 20
N_MOVIES = 20

def benchmark(s, q):
    return s.submit(q)

def run(label, providers):
    times = defaultdict(list)
    for thread in range(1, N_THREADS + 1):
        s = Session(parallel_downloads_per_job=thread)
        q = s.create_query(
            title='Sin', cache=False, amount=N_MOVIES, retries=5,
            strategy='flat', providers=providers
        )
        result = timeit.Timer(partial(benchmark, s, q)).timeit(number=5)
        times[thread].append(result)

    plt.plot(
        [x[0] for x in times.items()],
        [x[1] for x in times.items()],
        label=label
    )

def plot():
    plt.xlim(1, N_THREADS)
    plt.xlabel('number of download threads', fontsize=14)
    plt.ylabel('time in seconds', fontsize=14)
    plt.title('libhugin threaded download comparsion', fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    config = {
        'api': ['tmdbmovie', 'ofdbmovie', 'omdbmovie'],
        'no api': ['videobustermovie', 'filmstartsmovie'],
        'api + no api': [
            'tmdbmovie', 'ofdbmovie', 'omdbmovie',
            'videobustermovie', 'filmstartsmovie'
        ]
    }

    for label, providers in config.items():
        run(label, providers)

    plot()
