#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listtree.py: Provides class with pretty str output for custom classes.
"""


class ListTree:
    """
    ListTree: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers object
    attributes, its class attributes and attributes from all classes inherited
    by its class. That's because dir's used there instead of __dict__.
    It also prints which class does attribute belong.
    """
    def __attrnames(self, obj) -> str:
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

    def __listclass(self, aClass):
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

    def __str__(self) -> str:
        self.__visited = {}
        chapter = f'Instance of {self.__class__.__name__} at {hex(id(self))}'
        chapter = f'{chapter:-^100}'
        attrs = f'\n{self.__attrnames(self)}{self.__listclass(self.__class__)}'
        return chapter + attrs
