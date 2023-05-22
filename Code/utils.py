
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

# H = [[r'\epsilon_{00} + H_z', 0, 0, 'H_x'], [0, r'\epsilon_{10} - H_z', 'H_x', 0], [0, 'H_x', r'\epsilon_{01} - H_z', 0], ['H_x', 0, 0, r'\epsilon_{11} + H_z']]
# print(matrix_to_latex(H))
