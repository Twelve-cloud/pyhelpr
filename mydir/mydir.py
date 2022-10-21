#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mydir: Module, which prints names defined in other module.
"""


from types import ModuleType


SEPLEN = 60
SEPCHR = '-'


def listing(module: ModuleType, verbose: bool = True) -> None:
    """
    listing: Prints all names of the module 'module'.
        1) module - module, whose names will be printed.
        2) verbose - if True, additional information will be printed.
    """
    sepline = SEPCHR * SEPLEN

    if verbose:
        print(sepline)
        print('name:', module.__name__, 'file:', module.__file__)
        print(sepline)

    for count, attr in enumerate(sorted(module.__dict__)):
        print(f'{count + 1:02}) {attr}', end='  ')
        print('<built-in name>') if attr.startswith('__') else print(getattr(module, attr))

    if verbose:
        print(sepline)
        print(module.__name__, f'has {count + 1} names')
        print(sepline)
