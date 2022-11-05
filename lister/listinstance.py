#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listinstance.py: Provides class with pretty str output for custom classes.
"""


class ListInstance:
    """
    ListInstance: When inheriting, it provides str output with __str__ method,
    which uses __attrnames method for gathering attributes. It gathers only
    object attributes (not from its Class or Superclass). That's because
    self.__dict__ contains only objects attributes (not object parent's attrs).
    """
    def __attrnames(self) -> str:
        return ', '.join([f'{key}={getattr(self, key)}' for key in sorted(self.__dict__)])

    def __str__(self) -> str:
        return f'[Instance of {self.__class__.__name__} at {hex(id(self))}: {self.__attrnames()}]'
