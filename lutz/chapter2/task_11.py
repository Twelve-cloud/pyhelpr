#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os


open('myfile.txt', 'w').write('Hello file world!\n')
data = open('myfile.txt').read()
print(data)
os.popen('rm myfile.txt')
