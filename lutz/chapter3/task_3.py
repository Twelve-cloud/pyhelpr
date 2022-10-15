#! /usr/bin/env python3
# -*- coding: utf-8 -*-

D = {'b': 2, 'c': 3, 'a': 1}

# -------------------------------------
for key in sorted(D):
    print(D[key], end=' ')
print()

# -------------------------------------
keys = list(D.keys())
keys.sort()

for key in keys:
    print(D[key], end=' ')
print()
