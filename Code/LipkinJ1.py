import numpy as np
import FindPauli

variables_J1 = [1, 2]

A1_J1 = np.zeros((4,4)); A1_J1[0, 0] = -1; A1_J1[2,2] = 1
A2_J1 = np.zeros((4,4)); A2_J1[0, 2] = -1; A2_J1[2, 0] = -1

LIST_J1 = [A1_J1, A2_J1]
H_J1 = np.zeros((4,4))

for k in range(2):
    H_J1 += variables_J1[k]*LIST_J1[k]

Pauli_String_List = FindPauli.find_pauli(H_J1, size=2)
print(FindPauli.reconstruct(Pauli_String_List, [1], size=2))

