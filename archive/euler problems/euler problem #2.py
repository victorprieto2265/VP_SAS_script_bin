#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Euler Project, Problem #2

Even Fibonacci Numbers

Created on Wed Sep 12 17:37:02 2018

@author: Victor Prieto
"""

import functools

a = []

#fibonacci generating code via recursion
@functools.lru_cache()
def fib(n):
    if n == 1:
        return 1
    elif n == 0:
        return 0
    else:
        temp = fib(n-1) + fib(n-2)
        return temp

#append each of the first 33 Fibonacci numbers to the list
for x in range (1, 1000):
    y = fib(x)
    if y % 2 != 0:
        continue
    if y > 4000000:
        print('that is the last fibonacci number')
        break
    a.append(y)
    print(y)
    
#sum the array and print it
x = sum(a)
print(x)