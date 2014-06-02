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
    results = defaultdict(list)
    for name, func in funcs.items():
        for thread in range(1, 3+1, 1):
            avg_time = 0
            for run in range(10):
                start = int(round(time.time() * 1000))
                download(threads=thread, func=func)
                end = int(round(time.time() * 1000))
                avg_time += end - start
            print(thread, name, avg_time/10)
