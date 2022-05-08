import argparse
import numpy as np


parser = argparse.ArgumentParser()  
parser.add_argument('-seq1')
parser.add_argument('-seq2')
args = parser.parse_args()

seq1_list, seq2_list, m, n = list(args.seq1), list(args.seq2), len(args.seq1)+1, len(args.seq2)+1
x = -np.inf * np.ones([m, n]) #DP matrix
y = np.zeros([m,n]) #pointer for traceback, 0:top left, 1:top, 2:left

for i in range(0,m):
    x[i,0] = -2*i
    y[i,0] = 1
for i in range(0,n):
    x[0,i] = -2*i
    y[0,i] = 2
for s in range(1,m):
    for t in range(1,n):
        temp = [x[s-1,t-1]+(2 if args.seq1[s-1]==args.seq2[t-1] else -1), x[s-1,t]-2, x[s,t-1]-2]
        x[s,t] = max(temp)
        y[s,t] = np.argmax(temp)

i, j = m-1,n-1
while i>0 or j>0:
    if y[i,j] == 0: 
        i = i-1; j = j-1
    elif y[i,j] == 1: 
        i = i-1
        seq2_list.insert(j,'-')
    elif y[i,j] == 2: 
        j = j-1
        seq1_list.insert(i,'-')

print(''.join(seq1_list))
print(''.join(seq2_list))