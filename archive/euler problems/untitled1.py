#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 09:38:32 2018

@author: Victor Prieto
"""
import time
start_time = time.time()

def delbart(t,n):
    if n > 0:
        if not (t%n):
            if delbart(t, n-1):
                return True
            else:
                return False
        else:
            return False
    else:
        return True

i = 20
while not delbart(i,20):
    i +=20

print (i)

print("--- %s seconds ---" % (time.time() - start_time))