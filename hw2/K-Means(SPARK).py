import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
import pyspark
import re
import sys
import numpy as np
import matplotlib.pyplot as plt


conf = SparkConf()
sc = SparkContext(conf=conf)
def load_data(line):
    return list(map(float,line.split(' ')))
def l2(u, v):
    u = np.array(u)
    v = np.array(v)
    return np.linalg.norm((u - v), ord=2)
def l1(u, v):
    u = np.array(u)
    v = np.array(v)
    return np.linalg.norm((u - v), ord=1)
def find_cluster(p,c,l):
    d = [(j,p+[l(p,c[j])]+[1])for j in range(10)]
    return sorted(d,key=lambda d:d[1][58])[0]
def new_cluster(point1,point2):
    return [point1[i]+point2[i]for i in range(60)]
def ave(points):
    return [points[i]/points[59]for i in range(58)]

c1 = open('c1.txt')
c2 = open('c2.txt')
c1 = [load_data(line) for line in c1]
c2 = [load_data(line) for line in c2]
data = sc.textFile('data.txt').cache()
data = data.map(lambda line: list(map(float,line.split(" ")))).cache()
cost1=[]
# for the measure l1 and l2
for i in range(20):
    new_c = data.map(lambda point:(find_cluster(point,c1,l2)))
    new_c = new_c.reduceByKey(lambda points1,points2: new_cluster(points1,points2))
    c1 = new_c.map(lambda points:list(ave(points[1]))).collect()
    cost1 = cost1+[sum(new_c.map(lambda p:p[1][58]).collect())]
cost2 = []
for i in range(20):
    new_c = data.map(lambda point:(find_cluster(point,c2,l2)))
    new_c = new_c.reduceByKey(lambda points1,points2: new_cluster(points1,points2))
    c2 = new_c.map(lambda points:list(ave(points[1]))).collect()
    cost2 = cost2+[sum(new_c.map(lambda p:p[1][58]).collect())]
#plot the cost function vs k
plt.plot(range(1,21,1), cost1, 'k')
plt.plot(range(1,21,1), cost2, 'r')
plt.title('cost value vs. iteration round k ')
plt.xlabel('iteration round k')
plt.ylabel('cost value')
plt.legend(['c1', 'c2'], loc='upper right')
plt.grid(True)
plt.show()

sc.stop()
