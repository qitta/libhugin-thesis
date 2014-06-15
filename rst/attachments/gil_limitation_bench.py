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
    y_pos = numpy.arange(len(threads))
    values = [x for _, x in times]

    plt.barh(y_pos, values, align='center', alpha=0.7, color='g')
    plt.yticks(y_pos, threads)
    plt.xlabel('time in seconds')
    plt.title('python threaded cpu bound limitation because of the GIL.')
    plt.show()


if __name__ == '__main__':

    CNT = 100000000
    times = []

    for thread_cnt in range(0, 9, 2):
        if thread_cnt == 0:
            thread_cnt = 1

        threads = []

        # starting timer and threads
        start = time.time()
        for z in range(1, thread_cnt + 1):
            t = Thread(target=countdown, args=(CNT//thread_cnt,))
            threads.append(t)
            t.start()

        # joining threads and stoping timer
        for t in threads:
            t = t.join()

        end = time.time() # stoping timer
        times.append( (thread_cnt, end - start) )
    plot(sorted(times))
