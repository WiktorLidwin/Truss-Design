import numpy as np
import math
from scipy.io import loadmat




data = loadmat('TrussDesign_test.mat')

# Access the parameters
C = data['C']
Sx = data['Sx']
Sy = data['Sy']
X = data['X'][0]
Y = data['Y'][0]
L = data['L']

L = L * 3.07199999

def dist(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

rows, cols = C.shape


M = np.zeros((rows*2,  cols))
Lengths = np.zeros((cols))



for i in range(cols):
    j1 = -1
    j2 = -1
    for j in range(rows):
        if C[j, i] == 1:
            if j1 == -1:
                j1 = j
            else:
                j2 = j
    M[j1, i] = (X[j2] - X[j1]) / dist((X[j2], Y[j2]), (X[j1], Y[j1]))
    M[j2, i] = -1 * M[j1, i]
    M[j1 + rows, i] = (Y[j2] - Y[j1]) / dist((X[j2], Y[j2]), (X[j1], Y[j1]))
    M[j2 + rows, i] = -1 * M[j1 + rows, i]
    Lengths[i] = dist((X[j2], Y[j2]), (X[j1], Y[j1]))
    
    
S = np.concatenate((Sx, Sy), axis=0)

A = np.concatenate((M, S), axis=1)
Z = np.linalg.inv(A) 
R =Z @ L

Cost = np.sum(Lengths) + 10* cols


Wl =  M = np.zeros((rows*2,  1))

def getPcrit(length):
    return 40/length #TODO

maxAlpha = 10000
m_fail = 0
Pcrits = np.zeros((cols))
for i in range(cols):
    pcrit = getPcrit(Lengths[i])
    Pcrits[i] = pcrit
    tension = Z[i]@L
    if(tension > 0):
        continue
    alpha = -1.0*pcrit / tension 
    if (alpha < maxAlpha):
        maxAlpha = alpha
        m_fail = i
        
# print(maxAlpha)
# print(Pcrits)
# print(L*maxAlpha)



print("Load: " + str(np.sum(L)) + " oz")
print("Member forces in oz")
for i in range(cols):
    Dir = "(N)"
    val = 0
    if (R[i] > 0):
        Dir= "(T)"
        val = R[i][0]
    else:
        Dir = "(C)"
        val = -1.0 * R[i][0]
    print("m"+str(i+1)+": " + str(np.round(val, 2)) + " "+Dir)
print("Reaction forces in oz:")
print("Sx1: "+str(np.round(R[-3][0], 2)))
print("Sy1: "+str(np.round(R[-2][0], 2)))
print("Sy2: "+str(np.round(R[-1][0], 2)))
print("Cost of truss: $" + str(Cost))
print("Theoretical max load/cost ratio in oz/$: " + str(np.round(np.sum(L * maxAlpha)/Cost,4)))
print("Member to fail: "+ str(m_fail+1))

# max load is L * maxAlpha
# this is only valid if load is increase proportionally
# so if the load is initally at J1 and J2 it is assumed to remain there 