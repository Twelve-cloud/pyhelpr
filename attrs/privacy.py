#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
privacy.py: Instruments that emulate private and public section from other languages.

Usage:
@private('name', 'age', '__str__')
class Person:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

    def __str__(self):
        return self.name


mark = Person('mark', 22, 'programmer')
print(mark.job)
# print(mark.age)
# mark.name = 'Not Mark'
# print(mark)


@public('name', 'age')
class Person2:
    def __init__(self, name, age, job):
        self.name = name
        self.age = age
        self.job = job

    def __str__(self):
        return self.name


mark = Person2('mark', 22, 'programmer')
print(mark.age)
mark.name = 'Not Mark'
print(mark)
# print(mark.job)
"""


from typing import Callable, Type, Any


class BuiltinsMixin:
    """
    BuiltinsMixin is a class, that override all __x__ methods via descriptors.
    """
    class ProxyDesc:
        """
        ProxyDesc is a descriptor class that manage concrete __x__ method
        and redirect managing to underlying class.
        """
        def __init__(self: Type, attrname: str) -> None:
            self.attrname = attrname

        def __get__(self: Type, instance: Type, owner: Type) -> Any:
            return instance.__class__.__getattr__(instance, self.attrname)

    builtins = [
        'repr', 'str', 'bytes', 'format', 'lt', 'le', 'eq',
        'ne', 'gt', 'ge', 'hash', 'bool', 'len', 'call',
        'getitem', 'setitem', 'delitem', 'iter', 'next',
        'reversed', 'contains', 'add', 'sub', 'mul', 'truediv',
        'floordiv', 'mod', 'divmod', 'pow', 'lshift', 'rshifh',
        'and', 'or', 'radd', 'rsub', 'rmul', 'rtruediv',
        'rfloordiv', 'rmod', 'rdivmod', 'rpow', 'rlshift',
        'rrshift', 'rand', 'ror', 'rxor', 'iadd', 'isub',
        'imul', 'itruediv', 'ifloordiv', 'imod', 'ipow',
        'ilshift', 'irshift', 'iand', 'ior', 'ixor',
        'neg', 'pos', 'abs', 'invert', 'round', 'complex',
        'int', 'float', 'enter', 'exit'
    ]

    for attr in builtins:
        exec(f'__{attr}__ = ProxyDesc("__{attr}__")')


def access_control(fail_if: Callable) -> Callable:
    """
    access_control is a wrapper for original decorator.

    Args:
        fail_if (Callable): function that checks attributes for privacy.

    Returns:
        Callable: original decorator.
    """
    def on_decorator(aClass: Type) -> Type:
        """
        on_decorator is a ogirinal decorator.

        Args:
            aClass (Type): class that should be decorated.

        Raises:
            TypeError: when trying to get access to private attributes.
            TypeError: when trying to change value of private attributes.

        Returns:
            Type: wrapper class where the managing of attributes is happening.
        """
        if not __debug__:
            return aClass
        else:
            class Wrapper(BuiltinsMixin):
                """
                Wrapper is a wrapper class where the managing of attributes is happening.

                Args:
                    BuiltinsMixin (_type_): class which overrides all __x__ methods.
                """
                def __init__(self: Type, *args: tuple, **kwargs: dict) -> None:
                    self._wrapped = aClass(*args, **kwargs)

                def __getattr__(self: Type, attr: str) -> Any:
                    if fail_if(attr):
                        raise TypeError('private attribute fetch: ' + attr)
                    else:
                        return getattr(self._wrapped, attr)

                def __setattr__(self: Type, attr: str, value: any) -> None:
                    if attr == '_wrapped':
                        self.__dict__[attr] = value
                    elif fail_if(attr):
                        raise TypeError('private attribute change: ' + attr)
                    else:
                        setattr(self._wrapped, attr, value)
            return Wrapper
    return on_decorator


def private(*attributes: tuple) -> Type:
    """
    private is a function that defines private decorator.

    Returns:
        Type: wrapper for original decorator with the lambda for privacy.
    """
    return access_control(fail_if=(lambda attr: attr in attributes))


def public(*attributes: tuple) -> Type:
    """
    public is a function that defines public decorator.

    Returns:
        Type: wrapper for original decorator with the lambda for publicity.
    """
    attributes = attributes + tuple([f'__{attr}__' for attr in BuiltinsMixin.builtins])
    return access_control(fail_if=(lambda attr: attr not in attributes))
