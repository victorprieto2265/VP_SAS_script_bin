#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 01:17:48 2018

@author: Victor Prieto
"""

array = []

for x in range(1, 1000):
    if x % 3 == 0 or x % 5 == 0:
        array.append(x)
        
print(sum(array))
        
