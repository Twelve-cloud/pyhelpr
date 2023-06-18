#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classtree.py: Contains functions to print classes tree from class and instance.
"""


from typing import Any, Type


def classtree(cls: Type, indent: int = 3) -> None:
    """
    classtree: Prints classes tree from class.
        1) cls - any class in a tree.
        2) indent - indentation for each new level.
    """
    print('.' * indent + cls.__name__)
    for supercls in cls.__bases__:
        classtree(supercls, indent + 3)


def instancetree(inst: Any, indent: int = 3) -> None:
    """
    instancetree: Prints classes tree from instance.
        1) inst - any instance of any class.
        2) indent - indentation for each new level.
    """
    print(f'Tree of {inst}')
    classtree(inst.__class__, indent)
