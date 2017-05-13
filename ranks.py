# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:14:04 2017

@author: Ebbe
"""

import numpy as np

def main():
    print(" ")
    print("Analysis rank 1")
    cost1 = np.array([3,4,5])
    score1 = np.array([1,10])
    
    analyze(cost1,score1)
    print(" ")
    print("Analysis rank 2")
    cost1 = np.array([5,6,7,8])
    score1 = np.array([10,20,30])
    
    analyze(cost1,score1)
    
    print(" ")
    print("Analysis rank 3")
    cost1 = np.array([7,8,9,10,11,12,13,14])
    score1 = np.array([30,40,50])
    
    analyze(cost1,score1)
    
    
def analyze(cost,score):
    print("   ")
    avgcost = np.average(cost)
    avgscore = np.average(score)
    print("Cost:",cost,"Average:",avgcost)
    print("Score:",score,"Average:",avgscore)
    
    
    print(avgscore)
    
    mat = [[s/c for c in cost] for s in score]
    mat = np.array(mat)
    print(mat)
    
   
    avgscoreformol = np.average(mat,axis=0)
    
    print("Average score for the cost:",avgscoreformol)
    
    avgscoreforscore = np.average(mat,axis=1)

    print("Average cost for the score:",avgscoreforscore)

    
if __name__ == '__main__':
    main()