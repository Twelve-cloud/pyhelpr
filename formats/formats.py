#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
formats.py: Diverse special functions to format strings.
"""


def commas(num: int, sep: int) -> str:
    """
    commas: Formatting positive number 'number' to print it with commas,
    which divide groups of number.
        1) number - number to format.
        2) separator - amount of symbols to divide string.
    """
    digits = str(num)
    assert digits.isdigit()

    result = ''
    while digits:
        digits, last = digits[:-sep], digits[-sep:]
        result = (last + ',' + result) if result else last

    return result


def money(num: int, sep: int = 3, width: int = 0, cur: str = '$') -> str:
    """
    money: Formatting number 'number' to print it with commans, 2 decimals,
    leading symbol '$' and optional addition.
        1) number - number to change view.
        2) separator - amount of symbols to divide string.
        3) numwidth - amount of additional spaces.
        4) currency - symbol of currency before number.
    """
    sign = '-' if num < 0 else ''
    number = abs(num)

    whole = commas(int(number), sep)
    fract = f'{num:.2f}'[-2:]

    num = f'{sign}{whole}.{fract}'
    return f'{cur}{num:>{width}}'
