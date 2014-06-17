#!/usr/bin/env python

from collections import defaultdict, OrderedDict
from statistics import mean
import time
import timeit
import numpy
import matplotlib.pyplot as plt
from functools import partial
from hugin.harvest.session import Session
from pylab import *
import pprint

THREADS = 10
RUNS = 3

def benchmark(s, q):
    r = s.submit(q)
    return r

def run(label, providers):
    times = defaultdict(list)
    for thread in range(0, THREADS + 1, 2):
        thread = max(1, thread)
        s = Session(parallel_downloads_per_job=thread)
        q = s.create_query(title='Sin', cache=False, amount=THREADS,
                strategy='flat', providers=providers)
        result = timeit.Timer(partial(benchmark, s, q)).timeit(number=RUNS)
        times[thread].append(result/RUNS)

    times = OrderedDict(sorted(times.items(), key=lambda t: t[0]))
    print(times)
    t = [x[0] for x in times.items()]
    s = [x[1] for x in times.items()]
    plot(t, s, 'o-', label=label)

if __name__ == "__main__":

    config = {
        'api providers':['tmdbmovie', 'ofdbmovie','omdbmovie']
        #'no api providers':['videobustermovie', 'filmstartsmovie'],
        #'api + no api providers':[ 'tmdbmovie', 'ofdbmovie', 'omdbmovie', 'videobustermovie', 'filmstartsmovie' ]
    }

    for label, providers in config.items():
        run(label, providers)

    xlim(1, THREADS)
    xlabel('number of download threads')
    ylabel('time in seconds')
    title('libhugin threaded download comparsion')
    grid(True)
    legend()

    show()
