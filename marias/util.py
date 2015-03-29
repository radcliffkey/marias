'''
Created on Mar 29, 2015

@author: Radoslav Klic
'''

def rotateList(l, movesLeft):
    if not l:
        return l
    firstIdx = movesLeft % len(l)
    return l[firstIdx:] +l[:firstIdx]
