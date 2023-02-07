#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sum square difference

The sum of the squares of the first ten natural numbers is:
1 squared + 2 squared + ... + 10 squared = 385

The square of the sum of the first ten natural numbers is:
(1 + 2 + ... + 10) squared = 55 squared = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and 
the square of the sum is 3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and 
the square of the sum.

Created on Mon Sep 24 11:29:13 2018

@author: Victor Prieto
"""

import time
start_time = time.time()

#sum of the squares of the first ten natural numbers
end = 100
y = 0
z = 0

for x in range(1, end+1):
    y += x**2

print('the sum of the squares of the first', end, 'natural numbers is: ', y)

#square of the sum of the first ten natural numbers
for x in range(1, end+1):
    z += x

a = z**2

print('the square of the sum of the first', end, 'natural numbers is: ', a)

b = a - y

print('the difference between the sum of the squares of the first', end, 'natural numbers is: ', b)


print("--- %s seconds ---" % (time.time() - start_time))