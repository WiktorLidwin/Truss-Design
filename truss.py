import numpy as np
import math
from scipy.io import loadmat




data = loadmat('TrussDesign_test.mat')

# Access the parameters
#  ASSUME PIN SUPPORT IS AT 0,0
# No negative numbers for X and Y
C = data['C']
Sx = data['Sx']
Sy = data['Sy']
X = data['X'][0]
Y = data['Y'][0]
L = data['L']

alpha = 1.0 #scaling, use max alpha from previous calculation to get max support weight
L = L * alpha

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
    return 3054.789*length**(-2.009)

Uncertainty = 1.36

maxAlpha = 100000000
m_fail = 0
Pcrits = np.zeros((cols))
for i in range(cols):
    pcrit = getPcrit(Lengths[i])
    Pcrits[i] = pcrit
    tension = Z[i]@L
    if(tension > 0):
        continue
    alpha_t = -1.0*pcrit / tension 
    if (alpha_t < maxAlpha):
        maxAlpha = alpha_t
        m_fail = i
        

# print(Pcrits)
# print(L*maxAlpha)

print("******************************")
print("Forces\n")
print("Load: " + str(np.sum(np.abs(L))) + " oz")
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


print("\n\n******************************\nCost/Max Weight Values\n")
print("Cost of truss: $" + str(Cost))
print("Theoretical max load/cost ratio in oz/$: " + str(np.round(np.sum(np.abs(L) * maxAlpha)/Cost,4)))
print("Theoretical max load in oz: " + str(np.round(np.sum(np.abs(L) * maxAlpha),4)) + " +- " + str(np.round(Uncertainty/Pcrits[m_fail] * np.sum(np.abs(L) * maxAlpha),4)))
print("Member to fail: "+ str(m_fail+1))
print("Truss can support "+ str(np.round(maxAlpha[0],4))+ " times more force")
print("Use alpha = "+ str(np.round(maxAlpha[0] * alpha,4))+ " on next run to get max load calculation")

# print(str(Pcrits[m_fail]))


Joint_Length_Constraint = ""
Joint_Length_Constraint_result = np.all((Lengths >= 7) & (Lengths <= 14))
if (Joint_Length_Constraint_result):
    Joint_Length_Constraint = "Passed"
else:
    Joint_Length_Constraint = "Failed"
    
Truss_span_Constraint = ""
Truss_span_Constraint_min_val = np.min(X)
Truss_span_Constraint_max_val = np.max(X)
if (Truss_span_Constraint_max_val - Truss_span_Constraint_min_val == 31):
    Truss_span_Constraint = "Passed"
else:
    Truss_span_Constraint = "Failed"
    
nonzero_count = np.count_nonzero(L)
Load_to_pin_support_span_Constraint = ""
if (nonzero_count == 1):
    nonzero_indices = np.nonzero(L)
    joint = nonzero_indices[0][0]
    d = dist((0,0),(X[joint],Y[joint]))
    if(d >= 12.5 and d <= 13.5):
        Load_to_pin_support_span_Constraint = "Passed"
    else:
        Load_to_pin_support_span_Constraint = "Failed: Load is " + str(d) +" in away from PIN, expected 12.5 < d < 13.5"
else:
    Load_to_pin_support_span_Constraint = "Failed: " + str(nonzero_count) + " Nonzero Forces(one-dimensional), expected 1"
Cost_Constraint = ""
if (Cost < 300):
    Cost_Constraint = "Passed"
else:
    Cost_Constraint = "Failed"
    
    
print("\n\n******************************\nConstraints\n")
print("Joint Length Constraint: " + Joint_Length_Constraint)
print("Truss Span Constraint: " + Truss_span_Constraint)
print("Load to pin support span Constraint: " + Load_to_pin_support_span_Constraint)
print("Cost Constraint: " + Cost_Constraint)

# max load is L * maxAlpha
# this is only valid if load is increase proportionally
# so if the load is initally at J1 and J2 it is assumed to remain there 