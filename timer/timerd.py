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
    def onDecorator(func: Callable) -> Callable:
        """
        onDecorator is an original decorator.

        Args:
            func (Callable): original function.

        Returns:
            Callable: wrapper for function.
        """
        def onCall(*args: tuple, **kwargs: dict) -> Any:
            """
            onCall is a wrapper for original function.

            Returns:
                Any: returns what function returns.
            """
            start = clock()
            result = func(*args, **kwargs)
            performing_time = clock() - start

            onCall.total += performing_time

            if performing_time < onCall.best:
                onCall.best = performing_time

            if trace:
                print(
                    f'{label}{func.__name__}: {performing_time:.5f}, '
                    f'{onCall.total:.5f}, {onCall.best:.5f}'
                )

            return result

        onCall.total = 0
        onCall.best = sys.maxsize
        return onCall
    return onDecorator
