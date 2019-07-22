from itertools import combinations
data = open('/Users/heruojin/Desktop/item.txt', 'r')
# define a filter function,see:https://stackoverflow.com/questions/4484690/how-to-filter-a-dictionary-in-python
def filteritemset(item, by_key = lambda x: True, by_value = lambda x: True):
    return dict((k, v) for k, v in item.items() if by_key(k) and by_value(v))
#get the support of a single item and then filter by count>100
#get the support of each pair in one basket
#get the pairset where pair is from itemfilter
#get the pairfilter where count>100
#do same procedure for tripleset
itemcount={}
paircount={}
triplecount={}
confpair ={}
conftriple={}
for line in data:
    basket = line.strip().split(" ")
    for item in basket:
        if item in itemcount:itemcount[item]=itemcount[item]+1
        else: itemcount[item]=1
    pair = combinations(sorted(basket),2)
    for p in pair:
        if p in paircount:paircount[p]=paircount[p]+1
        else:paircount[p]=1
    triple = combinations(sorted(basket),3)
    for t in triple:
        if t in triplecount:triplecount[t]=triplecount[t]+1
        else:triplecount[t]=1
itemfilter = dict(filteritemset(itemcount, by_value = lambda k: k >100))
pairset = dict(filteritemset(paircount, by_key = lambda k: k[0] in itemfilter and k[1] in itemfilter ))
pairfilter = dict(filteritemset(pairset, by_value = lambda k: k>100))
tripleset = dict(filteritemset(triplecount, by_key = lambda k: k[0] in itemfilter and k[1] in itemfilter and k[2] in itemfilter))
triplefilter = dict(filteritemset(tripleset, by_value = lambda k: k>100))
#compute the confidence score for each pair in pairfilter and rank all the scores
for pair in pairfilter:
    confpair[(pair[0],pair[1])] = pairfilter[pair]/itemfilter[pair[0]]
    confpair[(pair[1],pair[0])] = pairfilter[pair]/itemfilter[pair[1]]
confpair = sorted(confpair.items(), key=lambda kv: kv[1], reverse = True)
for triple in triplefilter:
    conftriple[( triple[0],triple[1],triple[2]) ]= triplefilter[triple]/pairfilter[(triple[0],triple[1])]
    conftriple[( triple[1],triple[2],triple[0]) ]= triplefilter[triple]/pairfilter[(triple[1],triple[2])]
    conftriple[( triple[0],triple[2],triple[1]) ] = triplefilter[triple]/pairfilter[(triple[0],triple[2])]
conftriple = sorted(conftriple.items(), key=lambda kv: (-kv[1],kv[0][0],kv[0][1]))
#output for 2(e)
for i in range(5):
    print(conftriple[i][0][0],conftriple[i][0][1],'=>',conftriple[i][0][2], '\t', conftriple[i][1])
