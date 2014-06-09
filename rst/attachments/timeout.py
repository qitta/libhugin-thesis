#!/usr/bin/env python

from hugin.harvest.session import Session
from statistics import mean
from collections import Counter
import sys

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fd:
        movies = fd.read().splitlines()
    cnt = Counter()
    s = Session()
    for provider in ['ofdbmovie', 'omdbmovie', 'tmdbmovie', 'videobustermovie', 'filmstartsmovie']:
        retries = []
        for movie in movies[0:100]:
            title, year, imdbid = movie.split(';')
            q = s.create_query(title=title, year=year, cache=False, imdbid=imdbid, providers=[provider], amount=1, retries=150)
            r = s.submit(q)
            num = r[0]._retries
            retries.append(num)
        cnt[provider] = (min(retries), mean(retries),max(retries))
    print(cnt)

