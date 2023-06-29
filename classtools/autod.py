#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autod.py: Contains tools to decorate all methods automatically.

UsageFirst:
from timetools.timerd import timer
from attrtools.privacy import public


class A(metaclass=decorate_all(timer(trace=True))):
    def say_hello(self):
        print('hello')


a = A()
a.say_hello()

UsageSecond:
from timetools.timerd import timer
from attrtools.privacy import public


class A(metaclass=MetaDecorate(decorators=[timer(trace=True), ])):
    def say_hello(self):
        print('hello')


a = A()
a.say_hello()
"""


from typing import Type, Callable, Sequence
from types import FunctionType


def decorate_all(decorator: Callable) -> Type:
    """
    decorate_all is a callable object that returns metaclass that applies decorator for all methods.

    Args:
        decorator (Callable): decorator what applies to all methods.

    Returns:
        Type: metaclass
    """
    class MetaDecorate(type):
        def __new__(meta: Type, classname: str, supers: tuple, classdict: dict) -> Type:
            for attr, value in classdict.items():
                if type(value) is FunctionType:
                    classdict[attr] = decorator(value)
            return type.__new__(meta, classname, supers, classdict)
    return MetaDecorate


class MetaDecorate:
    """
    MetaDecorate is a metaclass that applies decorators for all methods.
    """
    def __init__(self: Type, decorators: Sequence) -> None:
        """
        Args:
            decorators (Sequence): sequence of decorators what applies to all methods.
        """
        self.decorators = decorators

    def __call__(self: Type, classname: str, supers: tuple, classdict: dict) -> Type:
        for attr, value in classdict.items():
            if type(value) is FunctionType:
                for decorator in self.decorators:
                    classdict[attr] = decorator(value)
        return type(classname, supers, classdict)
