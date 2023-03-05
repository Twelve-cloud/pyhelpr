#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mapattrs.py: Provides instruments for mapping attributes with their inheritance sources (classes).
"""


from typing import Union
import pprint


def trace(obj, label='', end='\n') -> None:
    """
    trace: Provides beautiful output.
    """
    print(label + pprint.pformat(obj) + end)


def filterdictvals(dict_, value_) -> dict:
    """
    filterdictvals: Returns dictionary dict_ without value value_.
    filterdictvals(dict(a=1, b=2, c=1), 1) => {'b': 2}.
    """
    return {key: value for (key, value) in dict_.items() if value != value_}


def invertdict(dict_) -> dict:
    """
    invertdict: Inverts dict, where values become keys and keys become values.
    invertdict(dict(a=1, b=2, c=1)) => {1: ['a', 'c'], 2: ['b']}.
    """
    def keysof(value_):
        return sorted(key for key in dict_.keys() if dict_[key] == value_)

    return {value: keysof(value) for value in set(dict_.values())}


def dflr(cls) -> list:
    """
    dflr: Returns inheritance path for Python 2.X classic classes,
    or for any classes when classes don't have diamond structure.
    """
    here = [cls]

    for sup in cls.__bases__:
        here += dflr(sup)

    return here


def inheritance(instance) -> Union[list, tuple]:
    """
    inheritance: Returns inheritance path for any classes (DFLR for Python 2.X classic classes
    and non-diamod structure) and (MRO for Python2.X new-style classes and Python 3.X all classes).
    """
    if hasattr(instance.__class__, '__mro__'):
        return (instance,) + instance.__class__.__mro__
    else:
        return [instance] + dflr(instance.__class__)


def mapattrs(instance, withobject=False, bysource=False) -> dict:
    """
    mapattrs: Returns dict with keys, which represent inherited attributes of instance and values
    which represent objects from which attributes has been inherited.
        1) instance - instance.
        2) withobject - with/without attributes from object class.
        3) bysource - group by object/attributes (default by attributes).
    """
    attr2obj = {}
    inherits = inheritance(instance)

    for attr in dir(instance):
        for obj in inherits:
            if hasattr(obj, '__dict__') and attr in obj.__dict__:
                attr2obj[attr] = obj
                break

    if not withobject:
        attr2obj = filterdictvals(attr2obj, object)

    return attr2obj if not bysource else invertdict(attr2obj)
