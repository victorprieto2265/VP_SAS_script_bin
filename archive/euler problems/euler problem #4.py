#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Largest palindrome project

A palindromic number reads the same both ways. The largest palindrome made from the product of 
two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.

Created on Sat Sep 22 19:28:50 2018

@author: Victor Prieto
"""

def palindrome_checker(n):
    y = list(n)
    left = y[0] + y[1] + y[2]
    right = y[-1] + y[-2] + y[-3]
    if right == left:
        print(n, 'is a palindrome!')
        return True
    else:
        return False

#for x in range (10000, 9000, -1):
#    if palindrome_checker(str(x)) == 1:
#        print('we done here')
#        break
#    else:
#        print('no go')

for a in range (999, 100, -1):
    for b in range (999, 100, -1):
        c = str(a*b)
        if len(c) < 6 or int(c) < 888888:
            break
        elif palindrome_checker(str(c)) == 1:
            print(c, 'is the palindrome?')
            break
        else:
            None
        