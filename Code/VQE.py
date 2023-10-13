import numpy as np
import qiskit as qk
import FindPauli
from scipy.optimize import minimize
from tqdm import tqdm


backend = qk.Aer.get_backend('qasm_simulator') #backedn for running the curcuits

#Different basis' to measure in

base_circuit = qk.QuantumCircuit(1, 1)
basis_x = base_circuit.copy()
basis_x.h(0)
basis_y = basis_x.copy()
basis_y.sdg(0)
basis_z = base_circuit.copy()
basis_i = base_circuit.copy()
basis_circuits = [basis_x, basis_y, basis_z]

text_form_dict = {
    'X' : 0,
    'Y' : 1,
    'Z' : 2
}
def copy_and_compose(circuit, basis, qubit):
    new_circuit = circuit.copy()
    
    basis_circuit = basis_circuits[basis]

    new_circuit = circuit.compose(basis_circuit, qubits=qubit)

    return new_circuit


def measure_and_count(circuit, bits, shots):

    if len(bits) == 0:
        return 1

    total = 0

    circuit.measure(bits, bits)
    job = backend.run(circuit, shots=shots)
    counts = job.result().get_counts()

    for key in counts: #to avoid KeyError
        key_factor = 1
        for num in key:
            if num == '1':
                key_factor *= -1
        total += key_factor*counts[key]/shots

    return total



#create the ansatz: a number of qubits that fits the size of the
#strings in our Pauli matrix form Hamiltonian.

#very inspired by lecture notes
def ansatz(theta, size):
    qreg = qk.QuantumRegister(size)
    creg = qk.ClassicalRegister(size)
    circuit = qk.QuantumCircuit(qreg, creg)
    idx = 0
    for i in range(size):
        circuit.rx(theta[idx], qreg[i])
        idx += 1

    for i in range(size-1):
        circuit.cx(qreg[i], qreg[i+1])

    for i in range(size):
        circuit.ry(theta[idx],qreg[i])
        idx += 1

    for i in range(size-1):
        circuit.cx(qreg[i],qreg[i+1])

    return circuit


def one_run(theta, string_list, size, shots):

    Energy = 0
    
    for string_tuple in string_list:

        circuit = ansatz(theta, size)
        factor = string_tuple[0]
        string = string_tuple[1]
        #basis transform
        measure_qbits = []
        for i, gate in enumerate(string):
            if (gate != 'I'):
                circuit = copy_and_compose(circuit, text_form_dict[gate], i)
                measure_qbits.append(i)
        Energy += factor*measure_and_count(circuit, measure_qbits, shots)

    return Energy

def solver(string_list, size, learning_rate, shots):

    # newtons method
    epoch = 0
    delta_energy = 1
    max_epochs = 400
    theta = np.random.uniform(low = 0, high = np.pi, size = 2*size)
    energy = one_run(theta, string_list, size, shots)
    while (epoch < max_epochs) and (delta_energy > 1e-4):
        grad = np.zeros_like(theta)
        for idx in range(theta.shape[0]):
            theta_temp = theta.copy()
            theta_temp[idx] += np.pi/2
            E_plus = one_run(theta_temp, string_list, size, shots)
            theta_temp[idx] -= np.pi
            E_minus = one_run(theta_temp, string_list, size, shots)
            grad[idx] = (E_plus - E_minus)/2
        theta -= learning_rate*grad
        new_energy = one_run(theta_temp, string_list, size, shots)
        delta_energy = np.abs(new_energy - energy)
        energy = new_energy
        epoch += 1

    return new_energy, epoch, theta

def get_all_min(n, size, learning_rate, number_shots, PauliStrings, epochs, min_energy_k):
    Energy_VQE = np.zeros(n)
    for index, PauliString in enumerate(tqdm(PauliStrings)):
        _, epochs[index], angles = solver(PauliString, size, learning_rate, number_shots)
        Energy_VQE[index] = one_run(angles, PauliString, size, number_shots)
        if epochs[index] < (epochs[index-1] - 5):
            _, epochs[index], angles= solver(PauliString, size, learning_rate, number_shots)
        Energy_VQE[index] = one_run(angles, PauliString, size, number_shots)
    for j in range(len(Energy_VQE)):#for multiprocessing purposes
        min_energy_k[j] = Energy_VQE[j]