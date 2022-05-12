import argparse
from IPython.display import display
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()  
parser.add_argument('-filename',type = str)
parser.add_argument('-local',action = "store_true", default = False)
parser.add_argument('-score',type = str)
parser.add_argument('-d',type = int, default= 8)
args = parser.parse_args()

def NW(S1,S2,m,n):
    x = -np.inf * np.ones([m, n]) #DP matrix
    y = np.zeros([m,n]) #pointer for traceback, 0:top left, 1:top, 2:left

    for i in range(0,m):
        x[i,0] = -d*i
        y[i,0] = 1
    for i in range(0,n):
        x[0,i] = -d*i
        y[0,i] = 2
    for s in range(1,m):
        for t in range(1,n):
            temp = [x[s-1,t-1]+ score[S1[s-1]][S2[t-1]], x[s-1,t]-d, x[s,t-1]-d]
            x[s,t] = max(temp)
            y[s,t] = np.argmax(temp)
    i, j = m-1,n-1
    while i>0 or j>0:
        if y[i,j] == 0: 
            i = i-1; j = j-1
        elif y[i,j] == 1: 
            i = i-1
            S2.insert(j,'-')
        elif y[i,j] == 2: 
            j = j-1
            S1.insert(i,'-')
    print(''.join(S1))
    print(''.join(S2))

def SW(S1,S2,m,n):
    x = -np.inf * np.ones([m, n]) #DP matrix
    y = np.zeros([m,n]) #pointer for traceback, 0:top left, 1:top, 2:left 3:stop

    for i in range(0,m):
        x[i,0] = 0
        y[i,0] = 3
    for i in range(0,n):
        x[0,i] = 0
        y[0,i] = 3
    for s in range(1,m):
        for t in range(1,n):
            temp = [x[s-1,t-1] + score[S1[s-1]][S2[t-1]], x[s-1,t]-d, x[s,t-1]-d, 0]
            x[s,t] = max(temp)
            y[s,t] = np.argmax(temp)
    (i,j) = np.unravel_index(np.argmax(x), x.shape)
    del S1[i:]
    del S2[j:]
    while i>0 or j>0:
        if y[i,j] == 3:
            break
        elif y[i,j] == 0: 
            i = i-1; j = j-1
        elif y[i,j] == 1: 
            i = i-1
            S2.insert(j,'-')
        elif y[i,j] == 2: 
            j = j-1
            S1.insert(i,'-')
    del S1[:i]
    del S2[:j]
    print(''.join(S1))
    print(''.join(S2))

with open(args.filename,'r') as f:
    seq = f.readlines()
    seq1_list, seq2_list = list(seq[0].replace('\n','')) ,list(seq[1])
    m, n = len(seq1_list)+1, len(seq2_list)+1


score = pd.read_csv("score.txt",skiprows=(1),delim_whitespace=True,)
d = args.d #gap penalty

if args.local:
    SW(seq1_list,seq2_list,m,n)
else:
    NW(seq1_list,seq2_list,m,n)
