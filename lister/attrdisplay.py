#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
attrdisplay.py: Provides classes which manage classes attributes.
"""


from __future__ import annotations
from typing import Any, Type


class AttrDisplayR:
    """
    AttrDisplayR: When inheriting, it provides repr output with __repr__ method,
    which uses __gatherAttrs method for gathering attributes. It gathers only
    object attributes (not from its Class or Superclass). That's because
    self.__dict__ contains only objects attributes (not object parent's attrs).
    """
    def __gatherAttrs(self: AttrDisplayR) -> str:
        return ', '.join([f'{key}={getattr(self, key)}' for key in sorted(self.__dict__)])

    def __repr__(self: AttrDisplayR) -> str:
        return f'[{self.__class__.__name__}: {self.__gatherAttrs()}]'


class AttrDisplayI:
    """
    AttrDisplayI: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers only
    object attributes (not from its Class or Superclass). That's because
    self.__dict__ contains only objects attributes (not object parent's attrs).
    """
    def __attrnames(self: AttrDisplayI) -> str:
        return ', '.join([f'{key}={getattr(self, key)}' for key in sorted(self.__dict__)])

    def __str__(self: AttrDisplayI) -> str:
        return f'[Instance of {self.__class__.__name__} at {hex(id(self))}: {self.__attrnames()}]'


class AttrDisplayL:
    """
    AttrDisplayL: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers object
    attributes, its class attributes and attributes from all classes inherited
    by its class. That's because dir's used there instead of __dict__.
    """
    def __attrnames(self: AttrDisplayL) -> str:
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

    def __str__(self: AttrDisplayL) -> str:
        chapter = f'Instance of {self.__class__.__name__} at {hex(id(self))}'
        chapter = f'{chapter:^100}'
        attributes = f'\n{self.__attrnames()}'
        return chapter + attributes


class AttrDisplayT:
    """
    AttrDisplayT: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers object
    attributes, its class attributes and attributes from all classes inherited
    by its class. That's because dir's used there instead of __dict__.
    It also prints which class does attribute belong.
    """
    def __attrnames(self: AttrDisplayT, obj: Any) -> str:
        inner_border = '*' * 47 + 'Inners' + '*' * 47 + '\n'
        other_bother = '*' * 47 + 'Others' + '*' * 47 + '\n'

        inners = [x for x in obj.__dict__ if x.startswith('__') and x.endswith('__')]
        others = [x for x in obj.__dict__ if x not in inners]

        inners = [f'{x:^20}' + '\n' if i % 5 == 4 else f'{x:^20}' for i, x in enumerate(inners)]
        others = [f'{i + 1:>4}){x:^48}{str(getattr(self, x)):^48}\n' for i, x in enumerate(others)]

        if inners and '\n' not in inners[-1]:
            inners[-1] += '\n'

        inners = ''.join(inners)
        others = ''.join(others)

        if not inners:
            inner_border = ''
        if not others:
            other_bother = ''

        return inner_border + inners + other_bother + others + '\n\n'

    def __listclass(self: AttrDisplayT, aClass: Type):
        if aClass not in self.__visited:
            self.__visited[aClass] = True
            attrs = self.__attrnames(aClass)
            above = ''

            for super in aClass.__bases__:
                above += self.__listclass(super)

            result = f'Class {aClass.__name__} at {hex(id(self))}'
            result = f'{result:-^100}'
            result = f'{result}\n{attrs}{above}'
            return result

        return ''

    def __str__(self: AttrDisplayT) -> str:
        self.__visited = {}
        chapter = f'Instance of {self.__class__.__name__} at {hex(id(self))}'
        chapter = f'{chapter:-^100}'
        attrs = f'\n{self.__attrnames(self)}{self.__listclass(self.__class__)}'
        return chapter + attrs
