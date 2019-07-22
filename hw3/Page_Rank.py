import numpy as np
from pyspark import SparkConf, SparkContext
graph = open('graph-full.txt','r')
beta = 0.8
iteration = 40
n = 1000
edgelist = []
for edge in graph:
    edge = edge.strip().split("\t")
    edgelist = edgelist+[(int(edge[0]),int(edge[1]))]
    

#construct M
M = np.zeros((n,n))
for edge in edgelist:
    i = edge[0]-1
    j = edge[1]-1
    M[j][i] = 1.0
for i in range(0,n):
    deg = 0
    for j in range(0,n):
        if M[j][i] ==1.0: deg = deg+1
    for j in range(0,n):
        if M[j][i] ==1.0: M[j][i] = 1.0/deg
# Initialize  
r1 = np.ones((n,1))/n

#process using rdd
conf = SparkConf()
sc = SparkContext(conf=conf)
M = [M[i] for i in range(n)]
M = sc.parallelize(M)

# Interations
for i in range(iteration):
    r2 = M.map(lambda m:beta*np.dot(m,r1)+(1-beta)/(1.0*n))
    r2 = np.array([x.item() for x in r2.collect()]).reshape(n,1)
    r1 = r2
                                  
#list the top5 and bottom5 node ids
score1 = []
for i in range(n):
    score1 = score1+[(i+1,r2[i].item())]
bottom_5 = sorted(score1, key=lambda x:x[1],reverse= False)[0:5]
top_5 = sorted(score1, key=lambda x:x[1],reverse=True)[0:5]

sc.stop()

## HITS
Lambda = 1
mu = 1
#construct L
L = np.zeros((n,n))
for edge in edgelist:
    i = edge[0]-1
    j = edge[1]-1   
    L[i][j] = 1
# Initialize  
h = np.ones((n,1))

# Interations
L_T = [L.T[i] for i in range(n)]
L = [L[i] for i in range(n)]
h = np.ones((n,1))

# process using rdd
conf = SparkConf()
sc = SparkContext(conf=conf)
L_T= sc.parallelize(L_T)
L = sc.parallelize(L)
for i in range(iteration):
    a = L_T.map(lambda x:np.dot(x,h))
    a = np.array([x.item() for x in a.collect()]).reshape(n,1)
    a = a/max(a)
    h = L.map(lambda x:np.dot(x,a))
    h = np.array([x.item() for x in h.collect()]).reshape(n,1)
    h = h/max(h)
sc.stop()

score2=[]
for i in range(n):
    score2 = score2+[(i+1,h[i].item(),a[i].item())]
bottom_5_h = sorted(score2, key=lambda x:x[1],reverse= False)[0:5]
bottom_5_h = [(x[0],x[1]) for x in bottom_5_h]
top_5_h = sorted(score2, key=lambda x:x[1],reverse=True)[0:5]
top_5_h = [(x[0],x[1]) for x in top_5_h]
bottom_5_a = sorted(score2, key=lambda x:x[2],reverse= False)[0:5]
bottom_5_a = [(x[0],x[2]) for x in bottom_5_a]
top_5_a = sorted(score2, key=lambda x:x[2],reverse=True)[0:5]
top_5_a = [(x[0],x[2]) for x in top_5_a]
