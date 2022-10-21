#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
privacy.py: Provides class which restricts assignments with special attribute.
"""


from typing import Any


class Privacy:
    """
    Privacy: When inheriting, it restricts assignments if values are assigned
    to attributes in self.privates list, otherwise allows assignments.
    """
    def __setattr__(self, attrname: str, value: Any) -> None:
        if attrname in self.privates:
            raise Exception('PrivacyError: Value cannot be assigned.')
        else:
            self.__dict__[attrname] = value
