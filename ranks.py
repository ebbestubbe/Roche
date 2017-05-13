# -*- coding: utf-8 -*-
"""
Created on Sat May 13 16:14:04 2017

@author: Ebbe
"""

import numpy as np

#rank1
cost1 = np.array([3,4,5])
score1 = np.array([1,10])

rank1 = [[s/c for c in cost] for s in score]
rank1 = np.array(rank1)
print(rank1)

rank1avgmol = average()