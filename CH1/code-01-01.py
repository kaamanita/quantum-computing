#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import multiprocessing as mp

def factorial(x):
    result = 1
    for i in range(2, x+1):
        result *= i
    return result

def main():
    items = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    pool = mp.Pool(processes=4)
    results = pool.map(factorial, items)
    print(results)

if __name__ == '__main__':
    mp.freeze_support()
    main()   
