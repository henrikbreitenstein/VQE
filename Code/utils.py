import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme(font_scale=1.5)
import numpy as np

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
    plt.legend()

    return fig

# H = [[r'\epsilon_{00} + H_z', 0, 0, 'H_x'], [0, r'\epsilon_{10} - H_z', 'H_x', 0], [0, 'H_x', r'\epsilon_{01} - H_z', 0], ['H_x', 0, 0, r'\epsilon_{11} + H_z']]
# print(matrix_to_latex(H))
