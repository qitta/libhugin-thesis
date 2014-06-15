#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from statistics import mean
import pprint
import sys
import os
import json

PROVIDERS = ['tmdb', 'ofdb', 'omdb']

def analyze_folder(path):
    data = {}
    for f in os.listdir(path):
        with open(os.path.join(path, f), 'r') as fp:
            provider, _, _ = f.split(';')
            data[provider] = json.loads(fp.read())
    return data

def analyze():
    results = {p: [] for p in PROVIDERS}
    for folder in filter(os.path.isdir, os.listdir(sys.argv[1])):
        for name, metadata in analyze_folder(folder).items():
            if name not in PROVIDERS:
                continue

            rating = metadata.get('rating')
            if rating:
                results[name].append(float(rating))

    return results

def calculate_min_mean_max(data):
    rating_stats = {name: Counter() for name in PROVIDERS}
    for name, ratings in data.items():
        rating_stats[name] = (min(ratings), round(mean(ratings), 2), max(ratings))
    return rating_stats

def count_ratings(data):
    rating_counts = {name: Counter() for name in PROVIDERS}
    for name, metadata in data.items():
        for value in metadata:
            rating_counts[name][value] += 1
    return rating_counts

def plot_distribution(data):
    colors = ['r', 'g', 'b']
    _, axes = plt.subplots(len(data), sharex=True, sharey=True)
    axes = list(axes)

    axes[0].set_ylabel('Number of given ratings')
    axes[0].set_xlabel('Rating')

    for idx, provider in enumerate(data.keys()):
        ax = axes.pop()
        ratings = Counter()
        for i in range(10 + 1):
            ratings[i] = 0

        for rating, times in data[provider].items():
            ratings[round(rating * 2) / 2] += times

        X = np.array(list(ratings.keys()))
        Y = np.array(list(ratings.values()))

        ax.bar(X, Y, 0.4, color=colors.pop())
        ax.set_title('Rating Distribution of "{p}"'.format(p=provider))
        ax.set_xticks(X)
        ax.grid(True)

    plt.show()

if __name__ == '__main__':
    data = analyze()
    plot_distribution(count_ratings(data))
    pprint.pprint(calculate_min_mean_max(data))
