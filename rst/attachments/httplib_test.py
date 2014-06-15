#!/usr/bin/env python
# encoding: utf-8

import concurrent.futures
from collections import defaultdict
import urllib.request
import time
import urllib3
import httplib2
import pylab

URLS = [
    'http://www.zeit.de',
    'http://www.heise.de',
    'http://www.golem.de',
    'http://www.linux-pro.de',
    'http://www.krawall.de',
    'http://www.archlinux.de',
    'http://www.archlinux.org',
    'http://www.phoronix.com',
    'http://www.bild.de',
    'http://www.spiegel.de',
    'http://www.zeit.de',
    'http://www.faz.de'
]

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
    return end - start

def plot(results):
    for lib in FUNCS.keys():
        t = [x[0] for x in results[lib]]
        s = [x[1] for x in results[lib]]
        pylab.plot(t, s, label=lib)

    pylab.xlim(1, 10)  # decreasing time
    pylab.xlabel('number of download threads')
    pylab.ylabel('time in milliseconds')
    pylab.title('performance comparsion threaded download')
    pylab.grid(True)
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    N = 10
    results = defaultdict(dict)

    for name, func in FUNCS.items():
        run_results = []
        for threads in range(1, 10 + 1, 1):
            avg_time = sum(download(threads=threads, func=func) for _ in range(N))
            run_results.append((threads, avg_time))
        results[name] = run_results

    plot(results)
