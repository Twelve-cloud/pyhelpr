#! /usr/bin/env python3
# -*- coding: utf-8 -*-

S = 'hello world'

# a)
for c in S:
    print(ord(c), end=' ')
print()

# b)
print(sum([ord(c) for c in S]))

# c)
L = [ord(c) for c in S]
print(L)
L = list(map(ord, S))
print(L)
