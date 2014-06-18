#!/usr/bin/env python

from hugin.harvest.session import Session
from collections import Counter
import re, json, httplib2, sys, os
import concurrent.futures

FOLDER = 'METADATA'
PROVIDERS = ['omdb', 'videobuster','filmstarts', 'tmdb', 'ofdb']

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

def fetch_data(
        session=None, title=None, year=None,
        src=None, mid=None, folder=None, source=None
    ):
    q = session.create_query(
        title=title.replace('|', '/'), year=year, imdbid=mid, providers=[src],
        amount=1, retries=150, language='de', cache=True, remove_invalid=True
    )
    return session.submit(q)

def get_movie_title(movieid):
    url =  'http://www.imdb.com/title/{imdb_id}'
    headers = {'Accept-Language': 'de'}
    h, c = httplib2.Http().request(url.format(imdb_id=movieid), headers=headers)
    regex = 'itemprop="name".*?>(.*?)</span>.*?\(.*?(\d{4}).*?\)'
    title, year = re.search(regex, c.decode().replace('\n', ' '), flags=re.S).groups()
    return '{};{};{}'.format(title, year, movieid)

def file_exists(folder, source):
    title, year, _ = folder.split(';')
    fmt = '{}/{}/{};{};{}.json'.format(FOLDER, folder, source, title, year)
    return os.path.isfile(fmt)

def create_folder_from_id(movieids):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_title = {executor.submit(get_movie_title, mid) : mid for mid in movieids}
        for future in concurrent.futures.as_completed(future_to_title):
            title = future_to_title[future]
            try:
                data = future.result()
                os.mkdir("{F}/{SF}".format(F=FOLDER, SF=data.replace('/', '|')))
            except Exception as exc:
                print('%r generated an exception: %s' % (title, exc))

def trigger_download(s):
    results = Counter()
    for source in PROVIDERS:
        for num, folder in enumerate(folderlist):
            t, y, mid = folder.split(';')
            if not file_exists(folder, source):
                r = fetch_data(
                    session=s, title=t, src='{}movie'.format(source), mid=mid,
                    year=y, folder=folder, source=source
                )
                if r:
                    name = '{}/{}/{};{};{}.json'.format(FOLDER, folder, source, t, y)
                    with open(name, 'w') as f:
                        movie, *_ = r
                        f.write(json.dumps(movie.result_dict))
                else:
                    results[source] += 1
                    print(r, source, t)
    return results

if __name__ == '__main__':
    if sys.argv[1] == 'fetch':
        folders = os.listdir(FOLDER)
        folderlist = [
             i for i in folders if os.path.isdir('{F}/{SF}'.format(F=FOLDER, SF=i))
        ]
        s = Session(
            parallel_jobs=1, parallel_downloads_per_job=2,
            timeout_sec=20, cache_path='.'
        )
        print(trigger_download(s))
    else:
        movieids = read_file(sys.argv[1])
        if not os.path.exists(FOLDER):
            os.mkdir(FOLDER)
        create_folder_from_id(movieids)
