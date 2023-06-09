import numpy as np
import qiskit as qk
import FindPauli
from scipy.optimize import minimize
from tqdm import tqdm


backend = qk.Aer.get_backend('qasm_simulator') #backedn for running the curcuits

#Different basis' to measure in

def Xbasis(circuit, register):
    circuit.h(register)
    circuit.measure(register, register)
    return circuit

def Ybasis(circuit, register):
    circuit.sdg(register)
    circuit.h(register)
    circuit.measure(register, register)
    return circuit

def Zbasis(circuit, register):
    circuit.measure(register, register)
    return circuit

def Ibasis(circuit, register):
    circuit.measure(register, register)
    return circuit

#for easy basis transform
bases = [Ibasis, Xbasis, Ybasis, Zbasis]
text_form_dict = {
    'I' : 0,
    'X' : 1,
    'Y' : 2,
    'Z' : 3
}


#create the ansatz: a number of qubits that fits the size of the
#strings in our Pauli matrix form Hamiltonian.

#very inspired by lecture notes
def ansatz(theta):
    qreg = qk.QuantumRegister(size)
    creg = qk.ClassicalRegister(size)
    circuit = qk.QuantumCircuit(qreg, creg)
    idx = 0
    for i in range(size):
        circuit.ry(theta[idx], qreg[i])
        idx += 1
    for i in range(size-1):
        circuit.cx(qreg[i], qreg[i+1])

    for i in range(size):
        circuit.rx(theta[idx],qreg[i])
        idx += 1

    for i in range(size-1):
        circuit.cx(qreg[i],qreg[i+1])

    return circuit


def one_run(theta):
    Energy = 0

    if len(np.array(string_list).shape) == 2:

         for string_tuple in string_list:

            circuit = ansatz(theta)

            factor = string_tuple[0]
            string = string_tuple[1]
            #basis transform

            for i, gate in enumerate(string):
                circuit = bases[text_form_dict[gate]](circuit, i)

            job = backend.run(circuit, shots=shots)
            counts = job.result().get_counts()

            for key in counts: #to avoid KeyError
                key_factor = 1
                for num in key:
                    if num == '1':
                        key_factor *= -1
                Energy += factor*key_factor*counts[key]/shots

    else:
        for string_row in string_list:
            for string_tuple in string_row:

                circuit = ansatz(theta)

                factor = string_tuple[0]
                string = string_tuple[1]
                #basis transform

                for i, gate in enumerate(string):
                    circuit = bases[text_form_dict[gate]](circuit, i)

                job = backend.run(circuit, shots=shots)
                counts = job.result().get_counts()

                for key in counts: #to avoid KeyError
                    key_factor = 1
                    for num in key:
                        if num == '1':
                            key_factor *= -1
                    Energy += factor*key_factor*counts[key]/shots

    return Energy

def jacobian(theta: np.array, func=one_run) -> np.array:
    derivative = np.zeros_like(theta)
    for i in range(len(theta)):
        theta[i] += np.pi/2
        derivative[i] = func(theta)
        theta[i] -= np.pi
        derivative[i] -= func(theta)
        derivative[i] = derivative[i]/2
        theta[i] += np.pi/2
    return derivative

def solver(string_list_parameter, size_parameter, shots_parameter=1000):

    global string_list
    global size
    global shots

    string_list = string_list_parameter
    size = size_parameter
    shots = shots_parameter

    theta = np.random.randn(size*2)

    # newtons method
    epochs = 100
    theta = np.random.randn(size*2)
    for epoch in tqdm(range(epochs)):
        print(epoch, one_run(theta))

        grad = np.zeros_like(theta)
        for idx in range(theta.shape[0]):
            theta_temp = theta.copy()
            theta_temp[idx] += np.pi/2
            E_plus = one_run(theta_temp)
            theta_temp[idx] -= np.pi
            E_minus = one_run(theta_temp)
            grad[idx] = (E_plus - E_minus)/2
        theta -= theta/grad
    energy = one_run(theta)

    return energy
