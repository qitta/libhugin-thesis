#!/usr/bin/env python
# encoding: utf-8

import concurrent.futures
from collections import defaultdict
from statistics import mean
import urllib.request
import time
import urllib3
import httplib2
import pylab

URLS = [
    'http://www.zeit.de', 'http://www.heise.de', 'http://www.golem.de',
    'http://www.krawall.de', 'http://www.phoronix.com', 'http://www.spiegel.de',
    'http://www.zeit.de', 'http://www.faz.de', 'http://www.focus.de',
    'http://www.filmstarts.de', 'http://www.moviepilot.de',
    'http://www.imdb.com', 'http://www.themoviedb.org', 'http://www.debian.org',
    'http://www.freebsd.org/de/'
] # 15 URLS

MAX_THREADS = 10

def fetch_urllib(url, timeout):
    return urllib.request.urlopen(url, timeout=timeout).readall()

def fetch_httplib2(url, timeout):
    h, c = httplib2.Http().request(url)
    return c

PM = urllib3.PoolManager()

def fetch_urllib3(url, timeout):
    return PM.request(url=url, method='GET').data

FUNCS = {
    'urllib': fetch_urllib,
    'httplib2': fetch_httplib2,
    'urllib3': fetch_urllib3
}

def download(threads=1, func=None):
    start = int(round(time.time() * 1000))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(func, url, 60): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                future.result()
            except Exception:
                pass

    end = int(round(time.time() * 1000))
    result = end - start
    return result

def plot(results):
    for lib in FUNCS.keys():
        t = [x[0] for x in results[lib]]
        s = [x[1] for x in results[lib]]
        pylab.plot(t, s, 'o-', label=lib)

    pylab.xlim(1, MAX_THREADS)
    pylab.xlabel('number of download threads')
    pylab.ylabel('time in milliseconds')
    pylab.title('performance scaling multithreaded download')
    pylab.grid(True)
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    N = 3
    results = defaultdict(dict)

    for name, func in FUNCS.items():
        run_results = []
        for threads in range(0, MAX_THREADS + 1, 2):
            threads = max(1, threads)
            avg_time = mean(download(threads=threads, func=func) for _ in range(N))
            run_results.append((threads, avg_time))
        results[name] = run_results

    plot(results)
