#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Will print the 100 most time-consuming functions (total time) and the 100
most time-consuming functions (cumulative time).
"""

import pstats
import sys


def main(path, size=None):
    stats = pstats.Stats(path)
    if not size:
        size = 100

    newstats = stats.sort_stats("time")
    newstats.print_stats(size)

    newstats = stats.sort_stats("cumulative")
    newstats.print_stats(size)


if __name__ == "__main__":
    size = sys.argv[2]
    if size:
        size = int(size)
    path = sys.argv[1]
    main(path, size)
