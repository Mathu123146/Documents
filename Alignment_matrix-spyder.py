# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import random

s1=input('Enter Sequence 1:')
s2=input('Enter Sequence 2:')

s1 = '-' + s1
s2 = '-' + s2

print(s1,s2)

m1 = len(s1)+1
n = len(s2)+1

m = np.ones((m1,n)) * -100
parent = np.zeros((m1,n,2))
m[:,0] = 0
m[0,:] = 0

match = 2
mismatch = -1

def allign(i,j):
   
    global s1,s2,m,parent
   
    if i>0 and j>0:
        if m[j][i-1] == -100:
            allign(i-1,j)
        if m[j-1][i-1] == -100:
            allign(i-1,j-1)
        if m[j-1][i] == -100:
            allign(i,j-1)
       
        if s1[i-1] == s2[j-1]:
            if m[j-1][i-1] != -100:
                m[j][i] = m[j-1][i-1]+match
                parent[j][i] = [i-1,j-1]
               
        else:
            l = np.array([m[j][i-1],m[j-1][i-1],m[j-1][i]])
            l = l + mismatch
           
            if l[1] >= l[0] and l[1]>=l[2]:
               m[j][i] = l[1]
               parent[j][i] = [i-1,j-1]
           
            elif l[0]>=l[0] and l[0]>=l[2]:
                m[j][i] = l[0]
                parent[j][i] = [i-1,j]
           
            else:
                m[j][i] = l[2]
                parent[j][i] = [i,j-1]

allign(len(s1),len(s2))

print(m)
pi,pj = len(s1),len(s2)

traceback=[]


while pi!=0 and pj!=0:
    print(pi,pj)
    traceback+=[[pi,pj]]
    pi,pj = int(parent[pj][pi][0]),int(parent[pj][pi][1])
   
traceback+=[[0,0]]
   
s_1 , s_2 = '',''
for i in range(len(traceback)-1):
    x,y = traceback[i][0],traceback[i][1]
    x_,y_ = traceback[i+1][0],traceback[i+1][1]
    if x_!=x and y_!=y:
        s_1 += s1[x-1]
        s_2 += s2[y-1]
    if y_==y:
        s_2 += '_'
        s_1 += s1[x-1]
    if x_==x:
        s_1 += '_'
        s_2 += s2[y-1]
       
s_1,s_2 = s_1[::-1],s_2[::-1]    
print(f"{s1}\n{s2}\n")
print(f"{s_1}\n{s_2}")
# print(parent[])

def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap_open=-5, gap_extend=-1):
    # Initialize the scoring matrix with zeroes
    rows = len(seq1) + 1
    cols = len(seq2) + 1
    score_matrix = [[0 for j in range(cols)] for i in range(rows)]

    # Initialize the gap penalties
    gap_open_penalty = gap_open
    gap_extend_penalty = gap_extend

    # Fill in the scoring matrix
    for i in range(1, rows):
        for j in range(1, cols):
            # Calculate the match score
            if seq1[i-1] == seq2[j-1]:
                match_score = score_matrix[i-1][j-1] + match
            else:
                match_score = score_matrix[i-1][j-1] + mismatch

            # Calculate the gap scores
            gap_in_seq1 = score_matrix[i-1][j] + gap_open_penalty + gap_extend_penalty
            gap_in_seq2 = score_matrix[i][j-1] + gap_open_penalty + gap_extend_penalty

            # Take the maximum of the three scores
            score_matrix[i][j] = max(match_score, gap_in_seq1, gap_in_seq2, 0)

    # Find the maximum score and its position
    max_score = max(max(row) for row in score_matrix)
    max_pos = [(i, j) for i in range(rows) for j in range(cols) if score_matrix[i][j] == max_score]

    return max_score, max_pos