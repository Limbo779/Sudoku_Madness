import numpy as np

def give_box(sudoku,row,col):
    l = []
    if (row+1 <= 3):
        if (col+1 <= 3):
            for i in range(3):
                for j in range(3):
                    l.append(sudoku[i][j])
        elif (col+1 <= 6):
            for i in range(3):
                for j in range(3,6):
                    l.append(sudoku[i][j])
        else:
            for i in range(3):
                for j in range(6,9):
                    l.append(sudoku[i][j])
    
    elif (row+1 <= 6):
        if (col+1 <= 3):
            for i in range(3,6):
                for j in range(3):
                    l.append(sudoku[i][j])
        elif (col+1 <= 6):
            for i in range(3,6):
                for j in range(3,6):
                    l.append(sudoku[i][j])
        else:
            for i in range(3,6):
                for j in range(6,9):
                    l.append(sudoku[i][j])
    
    else:
        if (col+1 <= 3):
            for i in range(6,9):
                for j in range(3):
                    l.append(sudoku[i][j])
        elif (col+1 <= 6):
            for i in range(6,9):
                for j in range(3,6):
                    l.append(sudoku[i][j])
        else:
            for i in range(6,9):
                for j in range(6,9):
                    l.append(sudoku[i][j])

    return l

def give_d_0(sudoku,row,col):
    l = []
    S_ = np.transpose(sudoku)
    l += (S_[col].tolist())
    l += give_box(sudoku,row,col)
    l += sudoku[row]
    l = list(set(l))
    l = list(np.array(l,dtype=int))[1::]

    return l

def normalize(matrix, max_iters=1000, tol=1e-9):
    """
    Perform Sinkhorn-Knopp normalization to make the input matrix doubly stochastic.

    Parameters:
        matrix (np.ndarray): A non-negative square matrix.
        max_iters (int): Maximum number of iterations.
        tol (float): Tolerance for convergence.

    Returns:
        np.ndarray: A doubly stochastic matrix.
    """
    assert matrix.ndim == 2 and matrix.shape[0] == matrix.shape[1], "Matrix must be square"
    K = matrix.copy()
    
    for i in range(max_iters):
        # Row normalization
        K /= K.sum(axis=1, keepdims=True)
        # Column normalization
        K /= K.sum(axis=0, keepdims=True)
        
        # Check convergence (both row and column sums close to 1)
        row_sums = K.sum(axis=1)
        col_sums = K.sum(axis=0)
        if np.allclose(row_sums, 1, atol=tol) and np.allclose(col_sums, 1, atol=tol):
            break

    return K

def write(st):
    with open("value.txt", "a") as file:
        file.write(st)

sudoku = []
for i in range(9):
    l=list(np.array(input().split(" "),dtype=int))
    sudoku.append(l)
sudoku = np.array(sudoku)
sudoku = sudoku.tolist()

#print(give_d_0(sudoku.tolist(),0,4))

for row in range(9):
    M=np.array([[float(1/9)]*9]*9)

    d_0 = {}
    for col in range(9):
        if (sudoku[row][col] == 0):
            d_0[col] = give_d_0(sudoku,row,col)
        else:
            for j in range(9):
                for i in range(9):
                    if ((sudoku[row][col]==i+1) or (col==j)):
                        M[j][i] = 0
            
            M[col][sudoku[row][col]-1] = 1
    
    for i in list(d_0.keys()):
        for j in d_0[i]:
            M[i][j-1] = 0.0
    
    M = normalize(M)

    write(f"Row {row+1} Matrix\n")
    for i in range(9):
        for j in range(9):
            st = f"({i+1} -> {j+1} : {M[i][j]}   ) "
            write(st)
        write("\n")


    write("\n\n")