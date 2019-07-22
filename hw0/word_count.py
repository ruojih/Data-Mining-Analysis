import re
import sys
from pyspark import SparkConf, SparkContext
conf = SparkConf()
sc = SparkContext(conf=conf)
lines = sc.textFile(sys.argv[1])
words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))
words = words.filter(lambda w:len(w)>0)
words = words.filter(lambda w: w[0].isalpha())
wordscap = words.map(lambda w: (w[0].lower(),1))
counts = wordscap.reduceByKey(lambda n1, n2: n1 + n2)
counts = wordscap.reduceByKey(lambda n1, n2: n1 + n2).sortByKey(ascending=True)
counts.coalesce(1).saveAsTextFile(sys.argv[2])
sc.stop()

