import time 
import numpy as np
features = open('features.txt')
with open('target.txt') as file:
    target = file.read().splitlines()
target = [int(x) for x in target]
train = []
i = 0 
features.seek(0)
for x in features:
    x = x.strip().split(',')
    x = list(map(int,x))
    x.append(target[i])
    x = np.array(x)
    train.append(x)
    i = i+1
#Randomly shuffle the training data
np.random.shuffle(train)
#initialization
l = 0
k = 0
d = 122
n = 6414
w = np.zeros(d)
b = 0
eta = 0.00001
epsilon = 0.01
C = 100 
B = 20
cost1 = 0
cost2 = 0
fk3 = []
fk3.append(100*n)
# define several functions
def prod(x1,x2):
    return sum(x1*x2)

def delta_L_w(x,w,b,l,j):
    s = min(n,(l+1)*B)
    L_w = []
    for i in range(l*B,s):
        if x[i][122]*(prod(w,x[i][0:122])+b) >= 1:
            L_w.append(0)
        else:
            L_w.append(-x[i][122]*x[i][j])
    return sum(L_w)


def delta_L_b(x,w,b,l):  
    s = min(n,(l+1)*B)
    L_b = []
    for i in range(l*B,s):
        if x[i][122]*(prod(w,x[i][0:122])+b) >= 1:
            L_b.append(0)
        else:
            L_b.append(-x[i][122])
    return sum(L_b)

def f(x,w,b):
    res = []
    for i in range(n):
        if 1 - x[i][122]*(prod(w,x[i][0:122])+b)>0:
            res.append(1 - x[i][122]*(prod(w,x[i][0:122])+b))
        else:
            res.append(0)
    return 1/2*prod(w,w)+C*sum(res)
#implement Mini-Batch Gradient Descent
start3 = time.time()
while True:
    cost1 = cost2
    for j in range(d):
        delta_w = w[j]+C*delta_L_w(train,w,b,l,j)
        w[j] = w[j] - eta* delta_w
    delta_b = C*delta_L_b(train,w,b,l)
    b = b - eta*delta_b
    l = l+1%(int(n/B))
    k = k+1
    fk3.append(f(train,w,b))
    cost100 = abs(fk3[k-1] - fk3[k])/fk3[k-1]*100
    cost2 = 0.5*cost1+0.5*cost100
    if cost2 < epsilon:
        break
end3 = time.time()
elapsed3 = end3 - start3

import matplotlib.pyplot as plt
plt.plot(range(1,len(fk)+1,1), fk,'g')
plt.plot(range(1,len(fk2)+1,1), fk2)
plt.plot(range(1,len(fk3)+1,1), fk3)
plt.title('cost fk vs. iteration round k ')
plt.xlabel('iteration round k')
plt.ylabel('cost value')
plt.legend(['BGD', 'SGD','MBGD'], loc='upper right')
plt.grid(True)
plt.show()
