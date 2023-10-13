import numpy as np
import FindPauli
import VQE
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme(font_scale=1.5)
from tqdm import tqdm
import utils
import multiprocessing

if __name__ == '__main__':
    np.seterr(all='ignore')
    E1, E2, V11, V12, V21, V22 = [0, 4, 3, 0.2, 0.2, -3]

    H_0 = np.array([[E1, 0], [0, E2]])
    H_I = np.array([[V11, V12], [V21, V22]])

    name = 'TestCases/onequbitTrue.pdf'
    nameVQE = 'TestCases/onequbitVQE.pdf'

    n = 5
    n_true = 100
    lmb_true = np.linspace(0, 1, n_true)
    space_lambda = np.linspace(0,1 , n)
    Energy_True = np.zeros(n_true)

    for i in range(n_true):
        H = H_0 + lmb_true[i]*H_I
        Energy_True[i] = utils.eigen(H)[0][0]

    number_shots = 1_000
    learning_rate = 0.3
    lmbvalues = np.linspace(0.0, 1.0, n)
    min_energy = [multiprocessing.Array('d', len(lmbvalues)) for i in range(10)]
    epochs = np.zeros(len(lmbvalues))
    PauliStrings = [FindPauli.find_pauli(H_0 + lmb*H_I, size=1) for lmb in lmbvalues]

    processes = [multiprocessing.Process(
        target=VQE.get_all_min, args=(n, 1, learning_rate, number_shots, 
                           PauliStrings, epochs, min_energy[k])) for k in range(len(min_energy))]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    Ana = [lmb_true, Energy_True]
    Pred = [space_lambda, min_energy, 'VQE']
    fig, error = utils.Ana_Pred_Plot(Ana, Pred, error=True, xlabel=r'$\lambda$', ylabel='Energy')
    plt.savefig('onequbitVQE.pdf')