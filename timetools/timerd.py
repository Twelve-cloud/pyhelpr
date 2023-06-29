#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timerd.py: Hontains decorator for measuring function performing time.


Usage:
@timer(trace=True, label='[CCC]===>')
def listcomp(N):
    return [x * 2 for x in range(N)]


listcomp(1000)
listcomp(500000)
listcomp(60000000)
"""


from typing import Callable, Any
import time
import sys


clock = time.clock if sys.platform[:3] == 'win' else time.time


def timer(label: str = '', trace: bool = True) -> Callable:
    """
    timer is a wrapper for original decorator to add parameters to decorator.

    Args:
        label (str, optional): text before trace message. Defaults to ''.
        trace (bool, optional): whether print message or not. Defaults to True.

    Returns:
        Callable: original decorator.
    """
    def on_decorator(func: Callable) -> Callable:
        """
        on_decorator is an original decorator.

        Args:
            func (Callable): original function.

        Returns:
            Callable: wrapper for function.
        """
        def on_call(*args: tuple, **kwargs: dict) -> Any:
            """
            on_call is a wrapper for original function.

            Returns:
                Any: returns what function returns.
            """
            start = clock()
            result = func(*args, **kwargs)
            performing_time = clock() - start

            on_call.total += performing_time

            if performing_time < on_call.best:
                on_call.best = performing_time

            if trace:
                print(
                    f'{label}{func.__name__}: {performing_time:.5f}, '
                    f'{on_call.total:.5f}, {on_call.best:.5f}'
                )

            return result

        on_call.total = 0
        on_call.best = sys.maxsize
        return on_call
    return on_decorator
