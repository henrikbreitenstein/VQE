import numpy as np
import VQE
import FindPauli
import utils
import multiprocessing
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme(font_scale=1.5)

def main():

    J = 1
    size = J+1
    n_steps_VQE = 3
    n_steps_true = 100
    n_threads = 1
    
    eps = 1
    V_start = 0
    V_stop = 1

    V_space_VQE = np.linspace(V_start, V_stop, n_steps_VQE)
    V_space_true = np.linspace(V_start, V_stop, n_steps_true)
    
    H_list_true = [utils.construct_Hamiltonian(size, eps, V) for V in V_space_true]
    H_list_VQE = [utils.construct_Hamiltonian(size, eps, V) for V in V_space_VQE]
    PauliStrings = [FindPauli.find_pauli(H, size=size) for H in H_list_VQE]
    
    learning_rate = 0.5
    number_shots = 1_000
    epochs = [np.zeros_like(V_space_VQE) for i in range(n_threads)]

    min_energy = [multiprocessing.Array('d', n_steps_VQE) for i in range(n_threads)]

    processes = [multiprocessing.Process(
        target=VQE.get_all_min, args=(n_steps_VQE, size, learning_rate, number_shots, 
                           PauliStrings, epochs[k], min_energy[k])) for k in range(len(min_energy))]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


    Energy_True = np.zeros_like(V_space_true)
    for i in range(n_steps_true):
        Energy_True[i] = utils.eigen(H_list_true[i])[0][0]
    

    Ana = [V_space_true, Energy_True]
    Pred = [V_space_VQE, min_energy, 'VQE']
    fig, error = utils.Ana_Pred_Plot(Ana, Pred, error=True, xlabel=r'$V$', ylabel='Energy')
    plt.savefig('TwoqubitVQE.pdf')


if __name__ == '__main__':

    main()