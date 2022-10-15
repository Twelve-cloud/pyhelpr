#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pybench_cases.py: Runs pybench with some tests and in diverse Python versions.
"""


import pybench
import sys


pythons = [
    (0, 'env python2'),
    (1, 'env python3')
]

stmts = [
    (0, 0, '[x ** 2 for x in range(1000)]'),
    (0, 0, 'res=[]\nfor x in range(1000): res.append(x ** 2)'),
    (0, 0, '$listif3(map(lambda x: x ** 2, range(1000)))')
]

tracecmd = '-t' in sys.argv
pythons = pythons if '-a' in sys.argv else None
pybench.runner(stmts, pythons, tracecmd)
