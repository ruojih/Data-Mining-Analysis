import numpy as np
import pandas as pd 
usr_show = open('user-shows.txt','r')
show = open('shows.txt','r')
names = [line.strip() for line in show]
m = 9985
n = 563
def sqrt_inv(P):
    return np.linalg.inv(np.sqrt(P))
#compute P and Q
R = np.zeros((m,n),dtype=int)
P = np.zeros((m,m), dtype=int)
Q = np.zeros((n,n), dtype=int)
i = 0
for line in usr_show:
    line = line.strip().split(' ')
    line = [int(r) for r in line]
    R[i] = np.array(line)
    P[i][i] = sum(line)
    i = i+1
for i in range(n):
    Q[i][i] = sum(R.T[i])
#compute gamma for user-user
Gamma1 = np.dot(sqrt_inv(P),R)
Gamma1 = np.dot(Gamma1,R.T)
Gamma1 = np.dot(Gamma1,sqrt_inv(P))
Gamma1 = np.dot(Gamma1,R)
Gamma1 = pd.DataFrame(Gamma1,columns=names)
alex = Gamma1.iloc[499,0:100]
alex.sort_values(ascending=False)
#compute gamma for item-item
Gamma2 = np.dot(R,sqrt_inv(Q))
Gamma2 = np.dot(Gamma2,R.T)
Gamma2 = np.dot(Gamma2,R)
Gamma2 = np.dot(Gamma2,sqrt_inv(Q))
Gamma2 = pd.DataFrame(Gamma2,columns=names)
alex2 = Gamma2.iloc[499,0:100]
alex2.sort_values(ascending=False)
