#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:25:10 2018

@author: Victor Prieto
"""
import time
start_time = time.time()

i = 1
for k in (range(1, 21)):
    if i % k > 0:
        for j in range(1, 21):
            if (i*j) % k == 0:
                i *= j
                break
print (i)

print("--- %s seconds ---" % (time.time() - start_time))