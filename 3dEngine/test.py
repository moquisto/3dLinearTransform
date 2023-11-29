import numpy as np
"""
A1 = np.array([
    [8, 0, 0],
    [0, 8, 0],
    [0, 0, 8]
])
#Scale by 2

A2 = np.array([
    [1, 1, 1], 
    [1, 1, 1],
    [1, 1, 1]
])
#Rotation pi/2 anticlockwise

A3 = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

matrices = [A2, A3, A1]
result = ""

for i in range(len(matrices)):
    if i != len(matrices) - 1:
        matrices[i+1] = matrices[i+1]@matrices[i]
    else:
        result = matrices[i]

print(result)
print(A1@A3@A2)

#This works well enough

L = [1, 4, 2, 5]
L.sort()
print(L)
"""

matrix = np.array([
    [2, 0, 0],
    [0, 2, 0],
    [0, 0, 1]
])

vector = [1, 6, 3]

x = (matrix@vector)
print(x)
print(x[0])