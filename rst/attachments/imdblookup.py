#!/usr/bin/env python

import os
import sys
import json
import time
from hugin.harvest.session import Session


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

def create_folders(folderlist):
    cnt = len(folderlist)
    for num, folder in enumerate(folderlist):
        print('{}/{} creating: {}.'.format(num, cnt, folder))
        os.system('mkdir "metadata/{}"'.format(folder.replace('/', '|')))

def fetch_data(session=None, title=None, year=None, src=None, mid=None, folder=None, source=None):
    q = session.create_query(
        title=title.replace('|', '/'),
        year=year,
        imdbid=mid,
        providers=[src],
        amount=1,
        retries=150,
        language='de',
        cache=True
    )
    r = session.submit(q)
    if r:
        name = 'metadata/{}/{};{};{}.json'.format(folder, source, title, year)
        with open(name, 'w') as f:
            f.write(json.dumps(r[0].result_dict))
    else:
        return folder

def file_exists(folder, source):
    title, year, _ = folder.split(';')
    fmt = 'metadata/{}/{};{};{}.json'.format(folder, source, title, year)
    return os.path.isfile(fmt)


def print_flush(msg):
    print(' ' * 80 + '\r', end='')
    print('{}\r'.format(msg), end='')



if __name__ == '__main__':

    if sys.argv[1] not in ['create', 'download']:
        print('Wrong usage. Use "create" or "download"')
        sys.exit(0)

    if sys.argv[1] == 'create':
        moviefolders = read_file(sys.argv[2])
        create_folders(moviefolders)

    if sys.argv[1] == 'download':
        not_found = []
        folders = os.listdir(sys.argv[2])
        folderlist = [
            i for i in folders if os.path.isdir('metadata/{}'.format(i))
        ]
        s = Session(
            parallel_jobs=1,
            parallel_downloads_per_job=2,
            timeout_sec=20,
            cache_path='.'
        )
        for source in ['omdb', 'videobuster','filmstarts', 'tmdb', 'ofdb']:
            cnt_not_found = 0
            for num, folder in enumerate(folderlist):
                msg = '{} <= [{}:{}:{}]'.format(source, num, len(folderlist), cnt_not_found)
                print_flush(msg)
                t, y, mid = folder.split(';')
                if not file_exists(folder, source):
                    r = fetch_data(
                        session=s, title=t,
                        src='{}movie'.format(source),
                        mid=mid,
                        year=y,
                        folder=folder,
                        source=source
                    )
                    if r:
                        not_found.append(r)
                        cnt_not_found += 1
            with open('metadata/{}-notfound.txt'.format(source), 'w') as f:
                elements = str(not_found)
                f.write('{}::{}'.format(len(not_found), elements))
            print()
            print(len(folderlist), cnt_not_found, source)
