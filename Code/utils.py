import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme(font_scale=1.5)
import numpy as np

def eigen(A):
    eigenValues, eigenVectors = np.linalg.eig(A)
    idx = np.argsort(eigenValues)
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    return (eigenValues, eigenVectors)

def matrix_to_latex(matrix):
    output = r'\begin{bmatrix}'
    for line in matrix:
        try:
            for num in line:
                output += str(num) + ' & '
        except:
            output += str(line) + '   '
        output = output[:-3] +  r' \\ '

    output = output[:-4] + r'\end{bmatrix}'
    return output

def latex_bra_ket(state, bk = 0):
    if bk == 0:
        output = r'\left |'
    if bk == 1:
        output = r'\left <'

    for num in state:
        output +=str(num)

    if bk == 0:
        output += r'\right >'
    if bk == 1:
        output += r'\right |'

    return output

def Ana_Pred_Plot(Ana, Pred, error=False, xlabel='x', ylabel='y'):
    fig, axs = plt.subplots(1, 1, figsize=(7, 7))
    axs.plot(Ana[0], Ana[1], label='Analytical', color = '#4c72b0')
    
    if error:
        xvalues = Pred[0]
        mean_predicted = np.mean(Pred[1], axis=0)
        N = len(Pred[1])

        pred_error = 0
        for i in range(N):
            pred_error += (Pred[1][i] - mean_predicted)**2
        pred_error = np.sqrt(pred_error/N)

        axs.errorbar(xvalues, mean_predicted, yerr=pred_error, fmt='o', color = '#dd8452', label=Pred[2])
    else:
        axs.scatter(Pred[0], Pred[1], color = '#dd8452', label=Pred[2])
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    return fig, pred_error

def dd(a, b):
    if a==b:
        return 1
    else:
        return 0

def construct_spin(S):

    size = int(2*S + 1)
    J_pluss = np.zeros((size, size))
    J_minus = np.zeros((size, size))
    J_z = np.zeros((size, size))

    for i in range(size):
        for k in range(size):
            n = i-S
            m = k-S

            pm_factor = np.sqrt(S*(S+1) -m*n)

            J_pluss[i,k] = dd(m, n+1)*pm_factor
            J_minus[i,k] = dd(m+1, n)*pm_factor
            J_z[i,k] = dd(m,n)*m
    
    return J_z, J_pluss, J_minus

def construct_Hamiltonian(S, eps, V):
    
    J_z, J_pluss, J_minus = construct_spin(S)

    H = eps*J_z - 1/2*V*(J_pluss@J_pluss + J_minus@J_minus)

    return H

# H = [[r'\epsilon_{00} + H_z', 0, 0, 'H_x'], [0, r'\epsilon_{10} - H_z', 'H_x', 0], [0, 'H_x', r'\epsilon_{01} - H_z', 0], ['H_x', 0, 0, r'\epsilon_{11} + H_z']]
# print(matrix_to_latex(H))
