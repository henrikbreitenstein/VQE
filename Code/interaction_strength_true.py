import numpy as np
import utils
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme(font_scale=1.5)

def main():

    J = 2.5
    n_eigen = int(2*J + 1)
    n_steps_true = 100
    
    eps = 1
    V_start = 0
    V_stop = 1

    V_space_true = np.linspace(V_start, V_stop, n_steps_true)
    
    H_list_true = [utils.construct_Hamiltonian(J, eps, V) for V in V_space_true]
    
    Energy_True = np.zeros((n_steps_true, n_eigen))
    for i in range(n_steps_true):
        Energy_True[i, :] = utils.eigen(H_list_true[i])[0]
    
    fig = plt.figure(figsize=(10, 8))
    for i in range(n_eigen):
        plt.plot(V_space_true, Energy_True[:, i], label=rf'$E_{i}$')
    
    plt.legend(bbox_to_anchor=(1.015, 1), loc=2, borderaxespad=0.)
    plt.xlabel(r'$V/\varepsilon$')
    plt.ylabel(r'$E/\varepsilon$')
    plt.savefig(f'J{J}_true.pdf', bbox_inches='tight')


if __name__ == '__main__':

    main()