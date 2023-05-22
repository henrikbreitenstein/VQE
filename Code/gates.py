import numpy as np

#One qubit gates
px = np.array([[0, 1], [1, 0]])
py = np.array([[0, -1j], [1j, 0]])
pz = np.array([[1, 0], [0, -1]])

H = (1/np.sqrt(2))*np.array([[1, 1], [1, -1]])
S = np.array([[1, 0], [0, 1j]])

gates_list = [px, py, pz, H, S]
gates_name_list = [r'\sigma_x', r'\sigma_y', r'\sigma_z', r'H', r'S']
