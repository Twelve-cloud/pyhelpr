#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listinherited.py: Provides class with pretty str output for custom classes.
"""


class ListInherited:
    """
    ListInherited: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers object
    attributes, its class attributes and attributes from all classes inherited
    by its class. That's because dir's used there instead of __dict__.
    """
    def __attrnames(self) -> str:
        inner_border = '*' * 47 + 'Inners' + '*' * 47 + '\n'
        other_bother = '*' * 47 + 'Others' + '*' * 47 + '\n'

        inners = [x for x in dir(self) if x.startswith('__') and x.endswith('__')]
        others = [x for x in dir(self) if x not in inners]

        inners = [f'{x:^20}' + '\n' if i % 5 == 4 else f'{x:^20}' for i, x in enumerate(inners)]
        others = [f'{i + 1:>4}){x:^48}{str(getattr(self, x)):^48}\n' for i, x in enumerate(others)]

        if '\n' not in inners[-1]:
            inners[-1] += '\n'

        inners = ''.join(inners)
        others = ''.join(others)

        return inner_border + inners + other_bother + others

    def __str__(self) -> str:
        chapter = f'Instance of {self.__class__.__name__} at {hex(id(self))}'
        chapter = f'{chapter:^100}'
        attributes = f'\n{self.__attrnames()}'
        return chapter + attributes
