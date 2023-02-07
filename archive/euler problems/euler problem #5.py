#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smallest multiple

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

Created on Sun Sep 23 01:38:14 2018

@author: Victor Prieto
"""

import time
start_time = time.time()

d = 0
end = 20
divisors = (11, 12, 13, 14, 15, 16, 17, 18, 19, 20)

for n in range (1, 10000000000):
    for x in divisors:
        if n % x != 0:
            break
        if x == end:
            print ('we done!')
            d = n
            break
        elif n % x == 0:
            continue
    if d != 0:
        break

print(d)

print("--- %s seconds ---" % (time.time() - start_time))