#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timer.py: Homegrown timing tools for function calls.
Does total time, best-of time, and best-of-totals time.
"""


from collections.abc import Callable
import time
import sys


timer = time.clock if sys.platform[:3] == 'win' else time.time


def total(func: Callable, *args, reps: int = 1000, **kwargs) -> float:
    """
    total: Returns total time to run func() reps times.
        1) reps - number of func's calls.
        2) func - function to check time.
    """
    start = timer()

    for i in range(reps):
        func(*args, **kwargs)

    total_time = timer() - start
    return total_time


def bestof(func: Callable, *args, reps: int = 100, **kwargs) -> float:
    """
    bestof: Returns time of quickest func() among reps runs.
        1) reps - number of func's calls.
        2) func - function to check time.
    """

    for i in range(reps):
        start = timer()
        func(*args, **kwargs)
        performing_time = timer() - start

        if performing_time < sys.maxsize:
            best = performing_time

    return best


def bestoftotal(func: Callable, *args, treps: int = 1000, freps: int = 100, **kwargs) -> float:
    """
    bestoftotal: Returns best of reps1 runs of total of reps2 runs of func.
        1) treps - number of total's calls.
        2) freps - number of func's calls in each total function.
        2) func - function to check time.
    """
    return min(total(func, *args, reps=freps, **kwargs) for i in range(treps))
