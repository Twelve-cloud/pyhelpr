#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
speedr.py: Tests speed of one or more Python versions. System runs on
Python 2.X and Python 3.X and can print output in both versions. Timeit module
is used to test speed. Changes $listif3 to list in generators for Python 3.X
and to empty string for Python 2.X to force Python 3.X work as Python 2.X.

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
runner(stmts, pythons, tracecmd)
"""


import timeit
import sys
import os


DEFNUM = 1000
DEFREP = 5


def runner(stmts: list, pythons: list = None, tracecmd: bool = False) -> None:
    """
    runner: Runs statements from stmts and measures its speed.
        1) stmts - [(number?, repeat?, statement)].
        2) pythons - [(python version?, path to Python)] or None if current.
    """
    print(sys.version)

    for (number, repeat, stmt) in stmts:
        number = number or DEFNUM
        repeat = repeat or DEFREP

        if not pythons:
            ispy3 = sys.version[0] == '3'
            stmt = stmt.replace('$listif3', 'list' if ispy3 else '')
            best = min(timeit.repeat(stmt=stmt, number=number, repeat=repeat))
            print(f'{best:.4f} [{stmt!r}]')
        else:
            print('-' * 80)
            print(f'[{stmt!r}]')

            for (ispy3, python) in pythons:
                stmt = stmt.replace('$listif3', 'list' if ispy3 else '')
                stmt = stmt.replace('\t', ' ' * 4)
                lines = stmt.split('\n')
                args = ' '.join('"%s"' % line for line in lines)
                cmd = f'{python} -m timeit -n {number} -r {repeat} {args}'
                print(python)

                if tracecmd:
                    print(cmd)

                print('\t' + os.popen(cmd).read().rstrip())
