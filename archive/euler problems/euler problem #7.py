#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10001st prime

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

Created on Mon Sep 24 15:09:29 2018

@author: Victor Prieto
"""

import time
start_time = time.time()

d = 0

def primality_test(x):
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    
    i = 3
    sqrt_x = x**0.5
    
    while i <= sqrt_x:
        if x % i == 0:
            return False
        i = i+2
        
    return True

for x in range(1, 1000000):
    if primality_test(x) == 1:
        d += 1
    if d == 10002:
        break

print('the', d-1, 'th prime is: ', x)



print("--- %s seconds ---" % (time.time() - start_time))