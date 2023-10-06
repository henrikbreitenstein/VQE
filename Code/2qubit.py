import numpy as np
import FindPauli
from grapher import graph_true, graph_VQE

def main():
    variables = [0, 2.5, 6.5, 7, 2, 3]
    factors = [1, 1, 1, 1, 1, 1]

    H0 = np.zeros((4,4))

    H0_0 = H0; H0_0[0, 0] = variables[0]
    H0_1 = H0; H0_1[1, 1] = variables[1]
    H0_2 = H0; H0_2[2, 2] = variables[2]
    H0_3 = H0; H0_3[3, 3] = variables[3]

    Hx = np.zeros((4,4))
    for i in range(4):
        Hx[i, 3-i] = 1

    Hz = np.eye(4);Hz[2,2] = -1;Hz[3,3] = -1
    LIST = [H0_0, H0_1, H0_2, H0_3, Hx, Hz]
    H = np.zeros((4,4))
    for k in range(len(LIST)):
        H += variables[k]*LIST[k]

    Pauli_String_List = FindPauli.find_pauli(H, size=2)
    
    n_VQE = 30
    n_True = 100

    Hx_True = np.linspace(1, 3, n_True)
    Hx_VQE = np.linspace(1, 3, n_VQE)
    Hz_True = np.linspace(2, 4, n_True)
    Hz_VQE = np.linspace(2, 4, n_VQE)

    name_Hx = 'TestCases/2qubitHx_True.pdf'
    name_Hx_VQE = 'TestCases/2qubitHx_VQE.pdf'
    name_Hz = 'TestCases/2qubitHz_True.pdf'
    name_Hz_VQE = 'TestCases/2qubitHz_VQE.pdf'

    graph_true(4, variables, factors, Hx_True, 'Hx', name_Hx, LIST, 2)
    graph_true(5, variables, factors, Hz_True, 'Hz', name_Hz, LIST, 2)
    graph_VQE(4, variables, factors, Hx_VQE, 'Hx', name_Hx_VQE, LIST, 2)
    graph_VQE(5, variables, factors, Hz_VQE, 'Hz', name_Hz_VQE, LIST, 2)

if __name__ == '__main__':
    main()
