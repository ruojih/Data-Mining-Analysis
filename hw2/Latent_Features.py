##latent factor remmondation
import numpy as np
import matplotlib.pyplot as plt
data = open('ratings.train.txt','r')
def l2(u):
    return np.linalg.norm(u, ord=2)**2
##Initialization of P and Q
P={}
Q={}
k=20
N=40
lam =0.1
eta = 0.01
for line in data:
    line = line.strip().split('\t')
    mov_id = int(line[1])
    usr =int(line[0])
    if mov_id not in Q:
        Q[mov_id] = np.random.uniform(low=0, high=np.sqrt(5/20), size=(1,20))
    if usr not in P:
        P[usr] = np.random.uniform(low=0, high=np.sqrt(5/20), size=(1,20))
##update of P and Q for each iteration
def update(P_initial=P,Q_initial=Q,k=20,eta = 0.01,lam =0.1):
    file = open('/Users/heruojin/Desktop/ratings.train.txt','r')
    for item in file:
        item = item.strip().split('\t')
        u =int(item[0])
        mov_i = int(item[1])
        rating = int(item[2])
        qi = Q[mov_i]
        pu = P[u]
        error = 2*(rating-np.dot(qi,pu.reshape(k,1))[0])
        qi = qi+eta*(error*pu-2*lam*qi)
        pu = pu+eta*(error*qi-2*lam*pu)
        Q[mov_i] =qi
        P[u]=pu
    return P,Q
E=[]
for iterations in range(N):
    P,Q = update(P,Q)
    ##compute error
    data.seek(0)
    error=0
    for line in data:
        line = line.strip().split('\t')
        u =int(line[0])
        mov_id = int(line[1])
        rating = int(line[2])
        qi = Q[mov_id]
        pu = P[u].reshape(k,1)
        error = error + (rating-np.dot(qi,pu)[0])**2
    data.seek(0)
    for m_id in Q:
        qi = Q[m_id]
        qi_trans = qi.reshape(20,1)
        error = error+lam*l2(qi)
    for u in P:
        pu = P[u]
        pu_trans = pu.reshape(20,1)
        error = error+lam*l2(qi)
    E = E+[error[0]]
t = range(1,41,1)
s =E
fig, ax = plt.subplots()
ax.plot(t, s)
ax.set(xlabel='iteration k', ylabel='error', title='error value vs. k')
ax.grid()
plt.show()