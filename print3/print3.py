#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
print3.py: Contains print3 function which emulates most functionality of print
function from Python 3.X.
"""


import sys


def print3(*args, **kwargs) -> None:
    """
    print3: Emulates most functionality of print function from Python 3.X in
    order to use it in Python 2.X.
        1) sep - word's separator.
        2) end - ending of a output.
        3) file - stream to write.
    """
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    file = kwargs.get('file', sys.stdout)

    output = ''
    for arg in args:
        output += ('' if args.index(arg) == 0 else sep) + str(arg)

    file.write(output + end)
