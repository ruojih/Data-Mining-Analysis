import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
def load_data(filename):
    return np.genfromtxt(filename, delimiter=',')
    
file = open('faces.csv')
A = load_data(file)
n = 2414
Sigma = np.dot(A.T, A)/n
evalue, evector = np.linalg.eigh(Sigma)
rearrangedEvalsVecs = sorted(zip(evalue,evector.T),\
                                    key=lambda x: x[0], reverse=True)
#the fractional reconstruction error
evalue_50 = list(map(lambda x:x[0],rearrangedEvalsVecs))[0:50]
s = np.trace(Sigma)
error = []
s1 = 0
err =0
for i in range(50):
    s1 = s1+evalue_50[i]
    err = 1-s1/s
    error = error+[err]
t = range(1,51,1)
fig, ax = plt.subplots()
ax.plot(t, error)
ax.set(xlabel='k', ylabel='fractional reconstruction error', title='fractional reconstruction error vs. k')
ax.grid()
plt.show()
#Display the first 10 eigenvectors as images
for i in range(10):
    plt.gray()
    evec = rearrangedEvalsVecs[i][1]
    patch = np.reshape(evec, [84, 96])
    im = Image.fromarray(patch)
    plt.imshow(patch)
    plt.show()
#Visualization and Reconstructio
index = [0,23,64,67,256]
#orginal 
for i in index:
    plt.gray()
    patch = A[i]
    patch = np.reshape(patch, [84, 96])
    im = Image.fromarray(patch)
    plt.imshow(patch)
    plt.show()
#FOR DIFFERENT K=1,2,5,10,50
def reconstruction(k,INDEX=index):
    Y = list(map(lambda x:x[1],rearrangedEvalsVecs))[0:k]
    Y = np.array(Y) 
    W = np.dot(A,Y.T)
    Z = np.dot(W,Y)
    for i in index:
        plt.gray()
        patch = Z[i]
        patch = np.reshape(patch, [84, 96])
        im = Image.fromarray(patch)
        plt.imshow(patch,vmin=0, vmax=1)
        plt.show()

