import re
import sys
from itertools import combinations
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)
data = sc.textFile('/Users/heruojin/Desktop/friend.txt').cache()
data = data.map(lambda line: line.strip().split("\t")).cache()
def findfriend(usr,data):
    ## map procedure
    def fm(line):
        usr = int(line[0])
        if len(line) > 1:
            friends = line[1].split(",")
            friends = sorted(map(int,friends))
        else:
            friends = ''
        commonfriend = [(common,1)for common in combinations(friends,2)]
        alreadyfriend = [(tuple(sorted([usr,friend])),0) for friend in friends]
        return alreadyfriend+commonfriend
    data = data.flatMap(lambda line: fm(line)).cache()
    
    # reduce procedure for specific usr
    data = data.filter(lambda pair:usr in pair[0]).cache()
    data = data.reduceByKey(lambda x,y:(x+y)*x*y).cache()
    #already friend, count=0; have commom friend but not alreadyfriend, count++
    # map the top 10 people you may know for specific usr
    data = data.filter(lambda pair: pair[1] != 0)
    data = data.map(lambda pair: [pair[0][1],pair[1]] if usr == pair[0][0] else [pair[0][0],pair[1]]).cache()
    data = data.sortBy(lambda pair:(-pair[1],pair[0])).cache()
    data= data.map(lambda pair:pair[0]).cache()
    #item
    #output
    recommend = data.take(10)
    recommend = str(recommend)
    usr = str(usr)
    output = [usr,recommend[1:-1]]
    output = '\t'.join(output)
    print(output)
# ans for q1:
usr = [924,8941,8942,9019,9020,9021,9022,9990,9992,9993]
for u in usr:
    findfriend(u,data)
sc.stop()

