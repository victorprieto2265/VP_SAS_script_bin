#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Euler project problem #3

largest prime factor:
    
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?

Created on Thu Sep 13 12:42:26 2018

@author: Victor Prieto
"""


n = 600851475143

#here, I need to determine if x is prime
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

#this code block needs to produce numbers starting at n/2, then n/3...

for d in range (int(n**0.5), 25, -1):
    if n % d == 0:
        y = primality_test(d)
        if y == 0:
            print(n/d, 'is not prime.')
            continue
        if y == 1:
            print(d, 'is prime!!')
            break
    else:
        None
    
print(d, 'is the greatest prime divisor')