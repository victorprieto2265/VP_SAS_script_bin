#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summation of primes

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

Created on Tue Sep 25 15:32:14 2018

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




print("--- %s seconds ---" % (time.time() - start_time))