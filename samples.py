# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:23:17 2017

@author: stubb
"""
import numpy as np
samples = []
#file = open("samples.txt","r")
mti = {"A":0,"B":1,"C":2,"D":3,"E":4}
#A = file.readline()
samples = []
with open("samples.txt","r") as f:
    for A in f:
        print(" ")
        print(A)
        rank = int(A[17])+1
        #print("rank",rank)
        cost = [A[47],A[50],A[53],A[56],A[59]]
        #print("cost",cost)
        cost = np.array(list(map(int,cost)))
        #print("cost",cost)
        score = int(A[64])*10 + int(A[65])
        
        #print("score:",A[64],"*10 +",A[65])
        exp = A[81]
        #print("exp",exp)
        exp = mti[exp]
        #print("exp",exp)
        sample = [None,None,rank,exp,score,cost,None,None]
        print(sample)
        samples.append(sample)
print("lols")
[print(s) for s in samples]
array = np.array
samples = [[None, None, 1, 0, 1, array([0, 3, 0, 0, 0]), None, None], [None, None, 1, 0, 1, array([0, 0, 0, 2, 1]), None, None], [None, None, 1, 0, 1, array([0, 1, 1, 1, 1]), None, None], [None, None, 1, 0, 1, array([0, 2, 0, 0, 2]), None, None], [None, None, 1, 0, 10, array([0, 0, 4, 0, 0]), None, None], [None, None, 1, 0, 1, array([0, 1, 2, 1, 1]), None, None], [None, None, 1, 0, 1, array([0, 2, 2, 0, 1]), None, None], [None, None, 1, 0, 1, array([3, 1, 0, 0, 1]), None, None], [None, None, 1, 1, 1, array([1, 0, 0, 0, 2]), None, None], [None, None, 1, 1, 1, array([0, 0, 0, 0, 3]), None, None], [None, None, 1, 1, 1, array([1, 0, 1, 1, 1]), None, None], [None, None, 1, 1, 1, array([0, 0, 2, 0, 2]), None, None], [None, None, 1, 1, 10, array([0, 0, 0, 4, 0]), None, None], [None, None, 1, 1, 1, array([1, 0, 1, 2, 1]), None, None], [None, None, 1, 1, 1, array([1, 0, 2, 2, 0]), None, None], [None, None, 1, 1, 1, array([0, 1, 3, 1, 0]), None, None], [None, None, 1, 2, 1, array([2, 1, 0, 0, 0]), None, None], [None, None, 1, 2, 1, array([0, 0, 0, 3, 0]), None, None], [None, None, 1, 2, 1, array([1, 1, 0, 1, 1]), None, None], [None, None, 1, 2, 1, array([0, 2, 0, 2, 0]), None, None], [None, None, 1, 2, 10, array([0, 0, 0, 0, 4]), None, None], [None, None, 1, 2, 1, array([1, 1, 0, 1, 2]), None, None], [None, None, 1, 2, 1, array([0, 1, 0, 2, 2]), None, None], [None, None, 1, 2, 1, array([1, 3, 1, 0, 0]), None, None], [None, None, 1, 3, 1, array([0, 2, 1, 0, 0]), None, None], [None, None, 1, 3, 1, array([3, 0, 0, 0, 0]), None, None], [None, None, 1, 3, 1, array([1, 1, 1, 0, 1]), None, None], [None, None, 1, 3, 1, array([2, 0, 0, 2, 0]), None, None], [None, None, 1, 3, 10, array([4, 0, 0, 0, 0]), None, None], [None, None, 1, 3, 1, array([2, 1, 1, 0, 1]), None, None], [None, None, 1, 3, 1, array([2, 0, 1, 0, 2]), None, None], [None, None, 1, 3, 1, array([1, 0, 0, 1, 3]), None, None], [None, None, 1, 4, 1, array([0, 0, 2, 1, 0]), None, None], [None, None, 1, 4, 1, array([0, 0, 3, 0, 0]), None, None], [None, None, 1, 4, 1, array([1, 1, 1, 1, 0]), None, None], [None, None, 1, 4, 1, array([2, 0, 2, 0, 0]), None, None], [None, None, 1, 4, 10, array([0, 4, 0, 0, 0]), None, None], [None, None, 1, 4, 1, array([1, 2, 1, 1, 0]), None, None], [None, None, 1, 4, 1, array([2, 2, 0, 1, 0]), None, None], [None, None, 1, 4, 1, array([0, 0, 1, 3, 1]), None, None], [None, None, 2, 0, 20, array([0, 0, 0, 5, 0]), None, None], [None, None, 2, 0, 30, array([6, 0, 0, 0, 0]), None, None], [None, None, 2, 0, 10, array([0, 0, 3, 2, 2]), None, None], [None, None, 2, 0, 20, array([0, 0, 1, 4, 2]), None, None], [None, None, 2, 0, 10, array([2, 3, 0, 3, 0]), None, None], [None, None, 2, 0, 20, array([0, 0, 0, 5, 3]), None, None], [None, None, 2, 1, 20, array([0, 5, 0, 0, 0]), None, None], [None, None, 2, 1, 30, array([0, 6, 0, 0, 0]), None, None], [None, None, 2, 1, 10, array([0, 2, 2, 3, 0]), None, None], [None, None, 2, 1, 20, array([2, 0, 0, 1, 4]), None, None], [None, None, 2, 1, 20, array([0, 2, 3, 0, 3]), None, None], [None, None, 2, 1, 20, array([5, 3, 0, 0, 0]), None, None], [None, None, 2, 2, 20, array([0, 0, 5, 0, 0]), None, None], [None, None, 2, 2, 30, array([0, 0, 6, 0, 0]), None, None], [None, None, 2, 2, 10, array([2, 3, 0, 0, 2]), None, None], [None, None, 2, 2, 10, array([3, 0, 2, 3, 0]), None, None], [None, None, 2, 2, 20, array([4, 2, 0, 0, 1]), None, None], [None, None, 2, 2, 20, array([0, 5, 3, 0, 0]), None, None], [None, None, 2, 3, 20, array([5, 0, 0, 0, 0]), None, None], [None, None, 2, 3, 30, array([0, 0, 0, 6, 0]), None, None], [None, None, 2, 3, 10, array([2, 0, 0, 2, 3]), None, None], [None, None, 2, 3, 20, array([1, 4, 2, 0, 0]), None, None], [None, None, 2, 3, 10, array([0, 3, 0, 2, 3]), None, None], [None, None, 2, 3, 20, array([3, 0, 0, 0, 5]), None, None], [None, None, 2, 4, 20, array([0, 0, 0, 0, 5]), None, None], [None, None, 2, 4, 30, array([0, 0, 0, 0, 6]), None, None], [None, None, 2, 4, 10, array([3, 2, 2, 0, 0]), None, None], [None, None, 2, 4, 20, array([0, 1, 4, 2, 0]), None, None], [None, None, 2, 4, 10, array([3, 0, 3, 0, 2]), None, None], [None, None, 2, 4, 20, array([0, 0, 5, 3, 0]), None, None], [None, None, 3, 0, 40, array([0, 0, 0, 0, 7]), None, None], [None, None, 3, 0, 50, array([3, 0, 0, 0, 7]), None, None], [None, None, 3, 0, 40, array([3, 0, 0, 3, 6]), None, None], [None, None, 3, 0, 30, array([0, 3, 3, 5, 3]), None, None], [None, None, 3, 1, 40, array([7, 0, 0, 0, 0]), None, None], [None, None, 3, 1, 50, array([7, 3, 0, 0, 0]), None, None], [None, None, 3, 1, 40, array([6, 3, 0, 0, 3]), None, None], [None, None, 3, 1, 30, array([3, 0, 3, 3, 5]), None, None], [None, None, 3, 2, 40, array([0, 7, 0, 0, 0]), None, None], [None, None, 3, 2, 50, array([0, 7, 3, 0, 0]), None, None], [None, None, 3, 2, 40, array([3, 6, 3, 0, 0]), None, None], [None, None, 3, 2, 30, array([5, 3, 0, 3, 3]), None, None], [None, None, 3, 3, 40, array([0, 0, 7, 0, 0]), None, None], [None, None, 3, 3, 50, array([0, 0, 7, 3, 0]), None, None], [None, None, 3, 3, 40, array([0, 3, 6, 3, 0]), None, None], [None, None, 3, 3, 30, array([3, 5, 3, 0, 3]), None, None], [None, None, 3, 4, 40, array([0, 0, 0, 7, 0]), None, None], [None, None, 3, 4, 50, array([0, 0, 0, 7, 3]), None, None], [None, None, 3, 4, 40, array([0, 0, 3, 6, 3]), None, None], [None, None, 3, 4, 30, array([3, 3, 5, 3, 0]), None, None]]
