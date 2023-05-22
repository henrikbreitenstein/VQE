import FindPauli
import VQE
import numpy as np
import matplotlib.pyplot as plt


#sorting eigenvalues from lecture notes
def eigen(A):
    eigenValues, eigenVectors = np.linalg.eig(A)
    idx = np.argsort(eigenValues)
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    return (eigenValues, eigenVectors)

def graph_true(variables_index, base_variables, base_factors, space, x_label, name, LIST, circ_size):
    
    E_true_array = np.zeros(len(space))
    
    for i, X in enumerate(space):
        variables = base_variables
        variables[variables_index] = X*base_factors[variables_index]

        H_true = np.zeros((2**circ_size,2**circ_size))

        for k in range(len(variables)):
            H_true += variables[k]*LIST[k]
        
        E_true_array[i] = eigen(H_true)[0][0]
    
    fig = plt.figure()
    plt.xlabel(x_label)
    plt.ylabel('Energy')
    plt.plot(space, E_true_array)
    plt.savefig(name)

def graph_VQE(variables_index, base_variables, base_factors, space, x_label, name, LIST, circ_size):
    
    E_VQE_array = np.zeros(len(space))
    
    for i, X in enumerate(space):
        variables = base_variables
        variables[variables_index] = X*base_factors[variables_index]
        
        H = np.zeros((2**circ_size,2**circ_size))
        
        for k in range(len(variables)):
            H += variables[k]*LIST[k]
        
        Pauli_String = FindPauli.find_pauli(H, size=circ_size)

        E_VQE_array[i] = VQE.solver(Pauli_String, circ_size)
    
    fig = plt.figure()
    plt.xlabel(x_label)
    plt.ylabel('Energy')
    plt.plot(space, E_VQE_array)
    plt.savefig(f'{name}')



