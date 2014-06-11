#!/usr/bin/env python

from collections import defaultdict
from statistics import mean
import time
import timeit
import numpy
import matplotlib.pyplot as plt
from functools import partial
from hugin.harvest.session import Session
from pylab import *
import pprint

def benchmark(s, q):
    r = s.submit(q)
    return r

def run(label, providers):
    times = defaultdict(list)
    for thread in range(1, 21):
        s = Session(parallel_downloads_per_job=thread)
        q = s.create_query(title='Sin', cache=False, amount=20, retries=5,
                strategy='flat', providers=providers)
        result = timeit.Timer(partial(benchmark, s, q)).timeit(number=5)
        times[thread].append(result)
    t = [x[0] for x in times.items()]
    s = [x[1] for x in times.items()]
    plot(t, s, label=label)

if __name__ == "__main__":

    config = {
        'api':['tmdbmovie', 'ofdbmovie', 'omdbmovie'],
        'no api':['videobustermovie', 'filmstartsmovie'],
        'api + no api':[ 'tmdbmovie', 'ofdbmovie', 'omdbmovie', 'videobustermovie', 'filmstartsmovie' ]
    }

    for label, providers in config.items():
        run(label, providers)

    xlim(1,20)  # decreasing time
    xlabel('number of download threads', fontsize=14)
    ylabel('time in seconds', fontsize=14)
    title('libhugin threaded download comparsion', fontsize=14)
    grid(True)
    legend()

    show()
