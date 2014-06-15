#!/usr/bin/env python
# encoding: utf-8

from hugin.harvest.session import Session
from statistics import mean
from collections import Counter
import sys

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fd:
        movies = fd.read().splitlines()

    cnt = Counter()
    sess = Session()
    providers = [
        'ofdbmovie', 'omdbmovie', 'tmdbmovie', 'videobustermovie', 'filmstartsmovie'
    ]

    N = 100

    for provider in providers:
        retries = []
        for movie in movies[:N]:
            title, year, imdbid = movie.split(';')
            r = sess.submit(
                sess.create_query(
                    title=title, year=year, cache=False, imdbid=imdbid,
                    providers=[provider], amount=1, retries=150
                )
            )
            retries.append(r[0]._retries)

        cnt[provider] = (min(retries), mean(retries), max(retries))
        print(cnt)
