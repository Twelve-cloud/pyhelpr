#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
argtest.py: Contains decorators for test ranges, types and values.

Usage:
@rangetest(m=(1, 12), d=(1, 31), y=(1900, 2023))
def date(m, d, y):
    print(f'date = {m}/{d}/{y}')


@typetest(a=int, c=float)
def sum(a, b, c, d):
    print(a + b + c + d)


@valuetest(word1=str.islower, word2=(lambda x: x[0].isupper()))
def msg(word1='mighty', word2='Larch', label=True):
    print(f'{label} {word1} {word2}')


date(1, 2, 1960)
# date(1, 33, 1960)
sum(1, 2, 3.0, 4)
sum(1, d=4, b=2, c=3.0)
# sum(1, d=4, b=2, c=99)
msg()
msg('majestic', 'Moose')
# msg('Giant', 'Redwood')
# msg('great', word2='elm')
"""


from typing import Callable, Any, Union


def argtest(argchecks: dict, failif: Callable) -> Callable:
    """
    argtest is a wrapper for original decorator.

    Args:
        argchecks (dict): arguments for checking.
        failif (Callable): lambda that fails if arg fails.

    Returns:
        Callable: original decorator.
    """
    def on_decorator(func: Callable) -> Union[Callable, Any]:
        """
        on_decorator is a original decorator.

        Args:
            func (Callable): decorated function.

        Raises:
            TypeError: if arg in failif fails.

        Returns:
            Union[Callable, Any]: if __debug__ is True then original function
                                  otherwise the result of the decorated function.
        """
        if not __debug__:
            return func
        else:
            code = func.__code__
            parameters = list(code.co_varnames[:code.co_argcount])

            def on_error(argname: str, criteria: tuple) -> None:
                """
                on_error is a function that raise an Exception.

                Args:
                    argname (str): name of the argument that don't pass.
                    criteria (tuple): range where the value of the argument must be.

                Raises:
                    TypeError: exception when argument fails.
                """
                raise TypeError(f'{func.__name__} argument "{argname}" not {criteria}')

            def on_call(*pargs: tuple, **kwargs: dict) -> Any:
                """
                on_call is a wrapper for decorated function.

                Returns:
                    Any: result of the decorated function.
                """
                positionals = parameters[:len(pargs)]

                for (argname, criteria) in argchecks.items():
                    if argname in kwargs:
                        if failif(kwargs[argname], criteria):
                            on_error(argname, criteria)
                    elif argname in positionals:
                        position = positionals.index(argname)

                        if failif(pargs[position], criteria):
                            on_error(argname, criteria)
                return func(*pargs, **kwargs)
            return on_call
    return on_decorator


def rangetest(**argchecks: dict) -> Union[Callable, Any]:
    """
    rangetest is a function that defines range tests.

    Returns:
        Union[Callable, Any]: if __debug__ then decorated function
                              otherwise result of the decorated function.
    """
    return argtest(argchecks, lambda arg, vals: arg < vals[0] or arg > vals[1])


def typetest(**argchecks: dict) -> Union[Callable, Any]:
    """
    typetest is a function that defines type tests.

    Returns:
        Union[Callable, Any]: if __debug__ then decorated function
                              otherwise result of the decorated function.
    """
    return argtest(argchecks, lambda arg, type: not isinstance(arg, type))


def valuetest(**argchecks: dict) -> Union[Callable, Any]:
    """
    valuetest is a function that defines value tests.

    Returns:
        Union[Callable, Any]: if __debug__ then decorated function
                              otherwise result of the decorated function.
    """
    return argtest(argchecks, lambda arg, tester: not tester(arg))
