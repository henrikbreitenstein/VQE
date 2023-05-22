import numpy as np
import grapher
import FindPauli
import VQE


def eigen(A):
    eigenValues, eigenVectors = np.linalg.eig(A)
    idx = np.argsort(eigenValues)
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    return (eigenValues, eigenVectors)
#one qubit curcuit

E1, E2, V11, V12, V21, V22 = [0, 4, 3, 0.2, 0.2, -3]

H_0 = np.array([[E1, 0], [0, E2]])
H_I = np.array([[V11, V12], [V21, V22]])

name = 'TestCases/onequbitTrue.pdf'
nameVQE = 'TestCases/onequbitVQE.pdf'

n = 100

space_lambda = np.linspace(0,1 , n)
Energy_True = np.zeros(n)
Energy_VQE = np.zeros(n)
for i in range(n):
    H = H_0 + space_lambda[i]*H_I
    Energy_True[i] = eigen(H)[0][0]
    
    Pauli_String = FindPauli.find_pauli(H, size=1)
    Energy_VQE[i] = VQE.solver(Pauli_String, 1)


fig = plt.figure()
plt.xlabel(x_label)
plt.ylabel('Energy')
plt.plot(space_lambda, Energy_True)
plt.savefig(f'TestCases/onequbitTrue.pdf')

fig = plt.figure()
plt.xlabel(x_label)
plt.ylabel('Energy')
plt.plot(space_lambda, Energy_VQE)
plt.savefig(f'TestCases/onequbitVQE.pdf')
