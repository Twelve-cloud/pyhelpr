#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fssize: Provides class what calculates file's size.
"""


import glob
import os


class FileSizeChecker:
    """
    FileSizeChecker: Provides interface for getting a list of the files with their size.
    It can be printed or got as tuple (filesize, filename).
    """
    def __init__(self, dirpath=r'.'):
        self.__files_pathes = glob.glob(dirpath + os.sep + '*.py')

    def get_files_size(self):
        return [(os.path.getsize(filename), filename) for filename in self.__files_pathes]

    def print_files_size(self):
        for fname in self.__files_pathes:
            print(f'File: {fname[fname.rfind(os.sep) + 1:]:<32}Size: {os.path.getsize(fname):<32}')
