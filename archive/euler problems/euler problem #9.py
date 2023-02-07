#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a squared plus b squared equals c squared. Example: 3/4/5, 5/12/13

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

Created on Tue Sep 25 15:11:28 2018

@author: Victor Prieto
"""

for a in range(1, 1000):
    for b in range(1, 1000):
        c = (a**2 + b**2)**0.5
        d = a + b + c
        if d == 1000:
            print(a, b, 'and', c, 'adds up to 1000')
            print('the product of abc is equal to', a*b*c)
    