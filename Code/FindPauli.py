import numpy as np
import utils

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.array([[1, 0], [0, -1]])
I = np.array([[1, 0], [0, 1]])

mats = np.array([I, X, Y, Z])
mats_name = np.array(['I', 'X', 'Y', 'Z'])
mats2 = np.zeros((16, 4, 4), dtype=complex)
mats2_name = []
mats3 = np.zeros((64, 8, 8), dtype=complex)
mats3_name = []

# find all 4x4 pauli combinations
i = 0
for k, mat1 in enumerate(mats):
    for j, mat2 in enumerate(mats):
        mats2[i, :, :] = np.kron(mat1, mat2)
        mats2_name.append(mats_name[k] + mats_name[j])
        i += 1

# find all 8x8 pauli combinations
i = 0
mat3_dict = {}
for k, mat1 in enumerate(mats2):
    for j, mat2 in enumerate(mats):
        name = mats2_name[k] + mats_name[j]
        mats3[i, :, :] = np.kron(mat1, mat2)
        mats3_name.append(name)
        mat3_dict[name] = np.kron(mat1,mat2)
        i += 1


def flatten_to_tuple(array):
    if type(array[0]) == tuple:
        return array, True
    else:
        flatter = []
        for wrapper in array:
            for element in wrapper:
                flatter.append(element)
        return flatter, False

def isPowerOfTwo (x):
    return (x and (not(x & (x - 1))))

def pad_matrix(H):
    if not isPowerOfTwo(len(H)):
        new_size = len(H) + 1
        add = 1
        while not isPowerOfTwo(new_size):
            new_size += 1
            add += 1
        temp_H = np.zeros((new_size, new_size))
        for i in range(len(H)):
            for k in range(len(H)):
                temp_H[i, k] = H[i, k]
        for i in range(1, add+1):
            temp_H[-i, -i] = 1
        return temp_H
    else:
        return H
    
#Goes through every combination and sees if it fits with any of the criterias
def find_pauli(H, comp=False, size = 3):
        H = pad_matrix(H)
        use_mats = [mats, mats2, mats3][size-1]
        use_mats_name = [mats_name, mats2_name, mats3_name][size-1]
        coeffs = []
        for i, pauli in enumerate(use_mats):
            tmp = pauli@H
            tmp_trace = np.trace(tmp)
            if tmp_trace != 0:
                if comp:
                    coeffs.append((tmp_trace/2**size, use_mats_name[i]))
                else:
                    coeffs.append((np.real(tmp_trace/2**size), use_mats_name[i]))
        flat = False
        while not flat:
            coeffs, flat = flatten_to_tuple(coeffs)
        return coeffs

def reconstruct(string_list):
    size = len(string_list[0][1])
    sum = np.zeros((2**size, 2**size))
    use_mats = np.array([mats, mats2, mats3][size-1])
    use_mats_name = np.array([mats_name, mats2_name, mats3_name][size-1])
    for tuple in string_list:
        coeff = tuple[0]
        string = tuple[1]
        index = np.where(use_mats_name==string)[0][0]
        sum = np.real(sum + coeff*use_mats[index])
    return sum

def print_coeffs(coeffs_lists, varible_list, size=3, comp=False):

    Final_eq = ''

    Collect_dict = {}

    for i, list in enumerate(coeffs_lists):
        for coeff in list:
            try:
                Collect_dict[coeff[1]] += ' + ' + str(coeff[0]) + varible_list[i]
            except:
                Collect_dict[coeff[1]] = str(coeff[0]) + varible_list[i]
    for key in Collect_dict:
        Final_eq += '(' + Collect_dict[key] + ')' + key + ' + '
    Fianl_eq = Final_eq[:-3]
    return Final_eq

if __name__ == "__main__":

    A1 = np.zeros((8,8));A1[0,0]=-2;A1[1,1]=-1;A1[3,3]=1;A1[4,4]=2
    A2 = np.zeros((8,8));A2[0,2]=1;A2[2,0]=1;A2[2,4]=1;A2[4,2]=1
    A3 = np.zeros((8,8));A3[1,1]=1;A3[3,3]=1
    A4 = np.zeros((8,8));A4[1,3]=1;A4[3,1]=1
    A5 = np.zeros((8,8));A5[2,2]=1

    LIST = [A1,A2,A3,A4,A5]
    varible_list = ['a', 'b', 'c', 'd', 'f']
    solutions = []

    for H_part in LIST:
        solutions.append(find_pauli(H_part))
    #print(solutions)
    #reconstruct(solutions, varible_list)
    #print_coeffs(solutions, [r'\varepsilon', r'\sqrt{6}V', '3W', '3V', '4W'])
