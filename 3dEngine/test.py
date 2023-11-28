import numpy as np
"""
A1 = np.array([
    [2, 0],
    [0, 2]
])
#Scale by 2

A2 = np.array([
    [0, -1], 
    [1, 0]
])
#Rotation pi/2 anticlockwise

A3 = np.array([
    [0, -1],
    [1, 0]
])

matrices = [A3, A2, A1]
result = ""

for i in range(len(matrices)):
    if i != len(matrices) - 1:
        matrices[i+1] = matrices[i+1]@matrices[i]
    else:
        result = matrices[i]

print(result)
print(A1@A2@A3)

#This works well enough
"""
L = [1, 4, 2, 5]
L.sort()
print(L)


