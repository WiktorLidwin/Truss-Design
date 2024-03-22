from scipy.io import savemat
import numpy as np
import math

# Example from hw 6, look at screenshot

C = [
    [1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 1, 0, 1],
]

C = np.array(C)


Sx = [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
Sx = np.array(Sx)


Sy = [
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 1],
    [0, 0, 0],
]
Sy = np.array(Sy)


X = [0, 2, 4, 2]
Y = [0, 0, 0 , 1.5]
X = np.array(X)
Y = np.array(Y)

m = 4.0/9.81
g= 9.81 



L = [
    [0],
    [0],
    [0],
    [-3.0],
    
    [0],
    [m*g],
    [0],
    [0],
]

# Convert the list into a NumPy array
L = np.array(L)



savemat('TrussDesign_test.mat', {'C': C, 'Sx': Sx, 'Sy': Sy, 'X': X, 'Y': Y, 'L': L})