import numpy as np


def lu(Matrix):
    """
    LU decomposition of a square matrix A using Gaussian elimination.
    PA = LU where
        P is a permutation matrix
        L is a lower triangular matrix
        U is an upper triangular matrix

    Parameters
    ----------
    A : np.array
        A square matrix.

    Returns
    -------
    P : np.array
        A permutation matrix.
    L : np.array
        A lower triangular matrix.
    U : np.array
        An upper triangular matrix.

    raises
    ------
    ValueError
        If the matrix is not square.
    """

    # Check if the matrix is square
    if Matrix.shape[0] != Matrix.shape[1]:
        raise ValueError("Matrix must be square")

    n = Matrix.shape[0]  # number of rows/columns
    A = Matrix.copy().astype(float)  # Make a copy of A and convert to float
    P = np.eye(n, dtype=float)  # Initialize P as the identity matrix

    # Loop over the columns of A
    for col in range(n):
        # Find the index of the row with the largest pivot element
        iMax = int(np.argmax(np.abs(A[col:, col])) + col)

        # Skip if the pivot is zero
        if A[iMax, col] != 0:
            # Swap the rows of A and P for those with the largest pivot element
            A = permute(A, iMax, col)
            P = permute(P, iMax, col)

            for row in range(col + 1, n):
                A[row, col] = (
                    A[row, col] / A[col, col]
                )  # Calculate the multiplier and store in A for later use
                A[row, col + 1 :] = (
                    A[row, col + 1 :] - A[row, col] * A[col, col + 1 :]
                )  # Update the remaining elements in the row using the multiplier

    L = np.tril(A, -1) + np.eye(
        n
    )  # Extract the lower triangular matrix from A and add the identity matrix to make it a proper lower triangular matrix
    U = np.triu(A)  # Extract the upper triangular matrix from A

    return P, L, U


def interactive_lu(P, L, U, col, pivot_row):
    """
    Makes only one step of the LU factorization, updates P,L,U and takes the pivot row to do the Gaussian Elimination

    Parameters
    ----------
    Matrix : np.array
        A square matrix.
    P : np.array
        A permutation matrix.
    L : np.array
        A lower triangular matrix.
    U : np.array
        An upper triangular matrix.
    pivot_row : int
        The index of the pivot row.

    Returns
    -------
    P : np.array
        A permutation matrix.
    L : np.array
        A lower triangular matrix.
    U : np.array
        An upper triangular matrix.

    """

    # Check if the column index is out of bounds, if so return the original P,L,U and -1,-1 as the next column and pivot row
    if col + 1 >= U.shape[1] or col <= -1:
        return P, L, U, -1, -1

    # Convert the L and U matrices to float data type
    U = U.astype(float)
    L = L.astype(float)

    # Find the index of the row with the largest pivot element or use the pivot row if it is already found
    index_maximum = (
        np.argmax(np.abs(U[col:, col])) + col if pivot_row < col else pivot_row
    )

    # Skip if the pivot is zero
    if U[index_maximum, col] != 0:
        # Swap the rows of A and P for those with the largest pivot element
        U = permute(U, index_maximum, col)
        P = permute(P, index_maximum, col)
        L = permute(L - np.eye(L.shape[0]), index_maximum, col) + np.eye(L.shape[0])

        # Gaussian elimination using NumPy's broadcasting
        factors = U[col + 1 :, col] / U[col, col]  # Calculate the multipliers
        L[col + 1 :, col] = U[col + 1 :, col] / U[col, col]  # Update the L matrix
        for i in range(
            col + 1, U.shape[0]
        ):  # Update the remaining elements in the row using the multipliers
            U[i, col + 1 :] = U[i, col + 1 :] - factors[i - col - 1] * U[col, col + 1 :]
        U[col + 1 :, col] = 0  # Set the elements below the pivot to zero

    # Return the updated P,L,U matrices, as well as the next column and pivot row
    return P, L, U, (col + 1), index_maximum


def permute(matrix_to_permute, i: int, j: int):
    """
    Permute the rows of a matrix.

    Parameters
    ----------
    matrix_to_permute : np.array
        A matrix.
    i : int
        The index of the first row.
    j : int
        The index of the second row.

    Returns
    -------
    matrix_to_permute : np.array
        The permuted matrix.

    """

    matrix_to_permute[[i, j], :] = matrix_to_permute[
        [j, i], :
    ]  # Swap the rows of matrix_to_permute using fancy indexing
    return matrix_to_permute


def forward_substitution(A, b):
    """
    Solves the system Ax = b using forward substitution.

    Parameters
    ----------
    A : np.array
        A lower triangular matrix.
    b : np.array
        A vector.

    Returns
    -------
    x : np.array
        A vector.

    """
    A = A.astype(float)  # Convert A to float data type
    b = np.copy(b).astype(
        float
    )  # Make a copy of b and convert it to float data type to avoid modifying the argument

    n = A.shape[0]  # Get the number of rows/columns in A
    x = np.zeros(n)  # Initialize the solution vector, x, with zeros and allocate memory

    if np.any(np.isclose(np.diag(A), 0, atol=1e-15)):
        # Check if the diagonal elements of A are close to zero, indicating a singular matrix
        raise ValueError("Matrix is singular")

    if np.any(np.triu(A, 1) != 0):
        # Check if the upper triangular part of A is not equal to zero
        raise ValueError("Matrix is not lower triangular")

    if b.shape[0] != n:
        # Check if the size of b is not equal to the number of rows/columns of A
        raise ValueError(
            "The size of b is not equal to the number of rows/columns of A"
        )
    if A.shape[0] != A.shape[1]:
        # Check if A is not a square matrix
        raise ValueError("A is not a square matrix")

    for row in range(n):
        # Loop over the rows starting from the first
        b[row] = b[row] - np.dot(
            A[row, :row], x[:row]
        )  # Subtract the dot product of the row in A and the current solution vector from the value of b
        x[row] = (
            b[row] / A[row, row]
        )  # Divide the updated b value by the diagonal element in A to get the solution for x

    return x  # Return the solution vector, x


def backward_substitution(A, b):
    """
    Solves the system Ax = b using backward substitution.

    Parameters
    ----------
    A : np.array
        An upper triangular matrix.
    b : np.array
        A vector.

    Returns
    -------
    x : np.array
        A vector.

    """
    A = A.astype(float)  # Convert A to float
    b = np.copy(b).astype(
        float
    )  # Make a copy of b (We do not want to update the argument while making our calculations) and convert to float

    n = A.shape[0]  # Get the number of rows/columns in the matrix
    x = np.zeros(n)  # Initialize the solution vector, x, with zeros and allocate memory

    if np.any(
        np.isclose(np.diag(A), 0, atol=1e-15)
    ):  # Check if the diagonal elements are close to zero (singular matrix)
        raise ValueError(f"Matrix is singular. The diagonal elements are {np.diag(A)}")

    if np.any(
        np.tril(A, -1) != 0
    ):  # Since it is backward, we check if the lower triangular part is zero
        raise ValueError("Matrix is not upper triangular")

    if b.shape[0] != n:
        raise ValueError(
            "The size of b is not equal to the number of rows/columns of A"
        )
    if A.shape[0] != A.shape[1]:
        raise ValueError("A is not a square matrix")

    for row in range(n - 1, -1, -1):  # Loop over the rows starting from the last
        b[row] = b[row] - np.dot(
            A[row, row + 1 :], x[row + 1 :]
        )  # Calculate the value of b with <A[row, row+1:], x[row+1:]> subtracted (b-<A[row, row+1:], x[row+1:]>)
        x[row] = b[row] / A[row, row]  # x = b'/A[row, row]

    return x


def lu_solve(A, b):
    """
    Solves the system Ax = b using LU factorization.

    Parameters
    ----------
    A : np.array
        A square matrix.
    b : np.array
        A vector.

    Returns
    -------
    x : np.array
        A vector.

    """
    P, L, U = lu(A)  # LU factorization
    y = forward_substitution(L, P @ b)  # Solve Ly = Pb
    x = backward_substitution(U, y)  # Solve Ux = y

    return x


def qr_factorization(A):
    """
    QR using Householder reflections.

    Parameters
    ----------
    A : np.array
        A matrix.

    Returns
    -------
    Q : np.array
        An orthogonal matrix.
    R : np.array
        An upper triangular matrix.

    """
    m, n = A.shape  # Get the shape of the input matrix A
    R = A.copy().astype(float)  # Make a copy of A and convert it to float
    qs = np.zeros((m, n))  # Create an array of zeros with shape (m, n)

    for k in range(n):  # Loop through the columns of A
        x = R[k:, k]  # Get the k-th column of R, starting from the k-th row

        # Calculate the Householder vector:
        # 1. Take the sign of the first element of x
        # 2. Compute the norm of x
        # 3. Create an identity matrix with the same number of rows as x
        # 4. Add the result of step 1 to the identity matrix, scaled by the result of step 2
        qk = np.sign(x[0]) * np.linalg.norm(x) * np.eye(x.shape[0], 1) + x.reshape(
            -1, 1
        )

        # Normalize the Householder vector
        qk = qk / np.linalg.norm(qk)

        # Update the k-th column and the columns below it of R
        R[k:, k:] = R[k:, k:] - 2 * np.dot(qk, np.dot(qk.T, R[k:, k:]))

        # Store the Householder vector in the "qs" matrix
        qs[k:, k] = qk.reshape(-1)

    Q = np.eye(m)  # Create an identity matrix with shape (m, m)
    for k in range(n - 1, -1, -1):  # Loop through the columns of A in reverse order
        qk = qs[k:, k].reshape(-1, 1)  # Get the k-th column of "qs"

        # Update the k-th column and the columns below it of Q
        Q[k:, k:] = Q[k:, k:] - 2 * np.dot(qk, np.dot(qk.T, Q[k:, k:]))
    R = np.triu(R)  # Make R upper triangular
    return Q, R  # Return the matrices Q and R


def qr_solve(A, b):
    """
    Solves the system Ax = b using QR factorization without calculating Q, only R. This is faster than the QR factorization with Q.

    Parameters
    ----------
    A : np.array
        A square matrix.
    b : np.array
        A vector.

    Returns
    -------
    x : np.array
        A vector.

    """
    n = A.shape[0]  # Get the number of rows in A
    R = A.copy().astype(float)  # Create a copy of A and cast it as a float
    b = b.copy().astype(float)  # Create a copy of b and cast it as a float

    for k in range(n):
        x = R[k:, k]  # Get the kth column of R, starting from the kth row
        qk = np.sign(x[0]) * np.linalg.norm(x) * np.eye(x.shape[0], 1) + x.reshape(
            -1, 1
        )  # Householder vector: calculate the Householder reflection vector qk
        qk = qk / np.linalg.norm(qk)  # Normalize qk so it has a length of 1

        R[k:, k:] = R[k:, k:] - 2 * np.dot(
            qk, np.dot(qk.T, R[k:, k:])
        )  # Update the R matrix using qk
        b[k:] = b[k:] - 2 * np.dot(qk, np.dot(qk.T, b[k:]))  # Update b using qk

    R = np.triu(
        R
    )  # Make the lower triangular part of R zero, since it may contain small values due to numerical errors
    x = backward_substitution(
        R, b
    )  # Solve the system R*x = b using backward substitution

    return x  # Return the solution x
