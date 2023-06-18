#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reloader.py: Provides functions to transitive reload of modules.
"""


from importlib import reload
from types import ModuleType
from typing import Any


def transitive_reload(objs: Any, visited: dict, verbose: bool = True) -> None:
    """
    transitive_reload: Reload modules and all their submodules.
        1) objs - names of modules where there are modules to be reload too.
        2) visited - storage of visited modules to restrict cycles.
        3) verbose - if True, additional information will be printed.
    """
    for obj in objs:
        if isinstance(obj, ModuleType) and obj not in visited:
            visited.add(obj)

            if verbose:
                print(f'reloading {obj.__name__}')

            reload(obj)
            transitive_reload(obj.__dict__.values(), visited)


def reloader(*modules: tuple) -> None:
    """
    reloader: Wrapper for transitive_reload function.
        1) modules - tuple of modules to be reload.
    """
    transitive_reload(modules, set())
