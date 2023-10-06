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

#Goes through every combination and sees if it fits with any of the criterias
def find_pauli(H, comp=False, size = 3):
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

def reconstruct(coeffs_lists, varible_list, size=3, comp=False):
    sum = np.zeros((2**size, 2**size))
    for i, list in enumerate(coeffs_lists):
        tmp = np.zeros((2**size, 2**size))
        print(f'Reconstructing: \n {list}')
        for coeff in list:
            if comp:
                tmp = tmp + coeff[0]*mat3_dict[coeff[1]]
            else:
                tmp = tmp + np.real(coeff[0]*mat3_dict[coeff[1]])
        print(utils.matrix_to_latex(tmp.astype(int)))
        sum = sum + tmp
    return utils.matrix_to_latex(sum.astype(int))

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

def string_list(variable_list):
    #variable_list = [epsilon, np.sqrt(6)*V, 3*V, 3*W, 4*W]

    unit = [[(-0.25, 'IZI'), (0.25, 'IZZ'), (-0.5, 'ZII'),
    (-0.5, 'ZIZ'), (-0.75, 'ZZI'), (-0.25, 'ZZZ')],
    [(0.25, 'IXI'), (0.25, 'IXZ'), (0.25, 'XXI'), (0.25, 'XXZ'),
    (0.25, 'YYI'), (0.25, 'YYZ'), (0.25, 'ZXI'), (0.25, 'ZXZ')],
    [(0.25, 'III'), (-0.25, 'IIZ'), (0.25, 'ZII'), (-0.25, 'ZIZ')],
    [(0.25, 'IXI'), (-0.25, 'IXZ'), (0.25, 'ZXI'), (-0.25, 'ZXZ')],
    [(0.125, 'III'), (0.125, 'IIZ'), (-0.125, 'IZI'), (-0.125, 'IZZ'),
    (0.125, 'ZII'), (0.125, 'ZIZ'), (-0.125, 'ZZI'), (-0.125, 'ZZZ')]]

    final = []
    for var, list in zip(variable_list, unit):
        tmp = []
        for part in list:
            tmp.append((var*part[0], part[1]))
        final.append(tmp)

    return final

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
