#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
attrdisplay.py: Provides class with pretty repr output for custom classes.
"""


class AttrDisplay:
    """
    AttrDisplay: When inheriting, it provides repr output with __repr__ method,
    which uses gatherAttrs method for gathering attributes. It gathers only
    object attributes (not from its Class or Superclass). That's because
    self.__dict__ contains only objects attributes (not object parent's attrs).
    """
    def gatherAttrs(self) -> str:
        attrs = [f'{key}={getattr(self, key)}' for key in sorted(self.__dict__)]
        return ', '.join(attrs)

    def __repr__(self) -> str:
        return f'[{self.__class__.__name__}: {self.gatherAttrs()}]'
