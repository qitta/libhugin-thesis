import concurrent.futures
from collections import defaultdict
import urllib.request
import time
import urllib3
import httplib2

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


def load_url1(url, timeout):
    c = urllib.request.urlopen(url, timeout=timeout)
    return c.readall()

def load_url2(url, timeout):
    h, c = httplib2.Http().request(url)
    return c

PM = urllib3.PoolManager()
def load_url3(url, timeout):
    return PM.request(url=url, method='GET').data

def download(threads=1, func=None):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(func, url, 60): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                pass
                #print(exc)


if __name__ == '__main__':

    funcs = {
        'urllib': load_url1,
        'httplib2': load_url2,
        'urllib3' : load_url3
    }
    results = defaultdict(dict)
    for name, func in funcs.items():
        run_results = []
        for thread in range(1, 10+1, 1):
            avg_time = 0
            for run in range(1):
                start = int(round(time.time() * 1000))
                download(threads=thread, func=func)
                end = int(round(time.time() * 1000))
                avg_time += end - start
            run_results.append( (thread, avg_time) )
        results[name] = run_results
        run_results = []
    import pprint
    pprint.pprint(results)

    from pylab import *

    for lib in funcs.keys():
        t = [x[0] for x in results[lib]]
        s = [x[1] for x in results[lib]]
        plot(t, s, label=lib)

    xlim(1,10)  # decreasing time

    xlabel('number of download threads')
    ylabel('time in milliseconds')
    title('performance comparsion threaded download')
    grid(True)
    legend()

    show()
