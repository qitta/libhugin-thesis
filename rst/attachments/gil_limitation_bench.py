#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy
from threading import Thread
import time

def countdown(n):
    while n > 0:
        n -= 1

def plot(times):
    threads = [x for x, _ in times]
    values = [x for _, x in times]
    y_pos = numpy.arange(len(threads))

    plt.barh(y_pos, values, align='center', alpha=0.7, color='g')
    plt.yticks(y_pos, threads)
    plt.xlabel('time in seconds')
    plt.title('python threaded cpu bound limitation because of the GIL.')
    plt.show()


if __name__ == '__main__':
    CNT = 100000000
    times = []

    for thread_cnt in range(0, 9, 2):
        thread_cnt = max(1, thread_cnt)

        cnt = range(1, thread_cnt + 1)
        threads = [Thread(target=countdown, args=(CNT // thread_cnt, )) for _ in cnt]
        for thread in threads:
            thread.start()

        start = time.time()
        for thread in threads:
            thread.join()
        times.append((thread_cnt, time.time() - start))

    plot(sorted(times))
