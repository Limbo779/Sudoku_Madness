import numpy as np

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

row = 1
while (row != 10):
    write("\n\n\n\n")
    M=np.array([[float(1/9)]*9]*9)

    d_0 = {}
    for j in range(9):
        user_input = input(f"Enter row {row} and column {j+1} not possible cases: ").split()
        if not user_input:
            continue
        # Convert inputs to float first, then cast indices to int
        l = [float(x) for x in user_input]
        if l[0]==0.0:
            continue
        row_idx = int(j+1)
        d_0[row_idx] = [int(x) for x in l]

    for i in list(d_0.keys()):
        for j in d_0[i]:
            M[i-1][j-1] = 0

    print("\n\n")

    d_1 = {}
    for j in range(9):
        user_input = input(f"Enter row {row} and column {j+1} possible cases: ").split()
        if not user_input:
            continue
        # Convert inputs to float first, then cast indices to int
        l = [float(x) for x in user_input]
        if l[0]==0.0:
            continue
        row_idx = int(j+1)
        d_1[row_idx] = [int(x) for x in l]

    for i in list(d_1.keys()):
        for j in d_1[i]:
            M[i-1][j-1] = 1

    M = normalize(M)

    write(f"Row {row} Matrix\n")
    for i in range(9):
        for j in range(9):
            st = f"({i+1} -> {j+1} : {M[i][j]}   ) "
            write(st)
        write("\n")


    write("\n\n")
    row += 1


