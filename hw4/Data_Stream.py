import numpy as np
import matplotlib.pyplot as plt
from math import *

delta = e**(-5)
epsilon = e*(10**(-4))
p = 123457

words = open('words_stream.txt')
counts = open('counts.txt')
hash_param = open('hash_params.txt')

n_buckets = int(e/epsilon)+1 #10000
n_hash = 5

a=[]
b=[]
for param in hash_param:
    param1,param2 = param.strip().split('\t')
    a.append(int(param1))
    b.append(int(param2))

#define hash function, return {1, ..., n_buckets}
def hash_fun(a,b,p,n_buckets,x):
    result = []
    for i in range(5):
        y = x % p
        hash_val=(a[i]*y + b[i]) % p
        result.append(hash_val % n_buckets)
    return result

F_matrix = np.zeros((5,10000))
F_est = {}
F = []
t = 0
#hash each word to baskets for each hash function
for word in words:
    t = t+1
    word = word.strip()
    word = int(word)
    hash_result = hash_fun(a,b,p,n_buckets,word)
    for i in range(5):
        hash_val = hash_fun(a,b,p,n_buckets,word)
        F_matrix[i][hash_result[i]] =  F_matrix[i][hash_result[i]]+1
error = []
for line in counts:
    ID,count = line.strip().split('\t')
    ID = int(ID)
    count = int(count)
    hash_result = hash_fun(a,b,p,n_buckets,ID)
    F_est[ID] = min(F_matrix[i][hash_result[i]] for i in range(5))
    F.append(count/t)
    error.append((F_est[ID]-count)/count)

plt.loglog(F, error,'+')
plt.title("Relative Error v.s. Frequency")
plt.xlabel("Frequency - log scale")
plt.ylabel("Relative Error - log scale")
plt.grid()
plt.show()