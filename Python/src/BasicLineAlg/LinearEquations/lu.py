import numpy as np
def lu(Matrix):
    '''
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
    '''
    if Matrix.shape[0] != Matrix.shape[1]:
        raise ValueError('Matrix must be square')

    n = Matrix.shape[0] # number of rows/columns
    A = Matrix.copy().astype(float) # Make a copy of A and convert to float 
    P = np.eye(n).astype(float) # Initialize P as the identity matrix
    
    # Loop over the columns of A
    for col in range(n):
        # Find the index of the row with the largest pivot element 
        iMax = int(np.argmax(np.abs(A[col:,col])) + col )

        # Skip if the pivot is zero 
        if A[iMax,col] != 0:
            # Swap the rows of A and P for those with the largest pivot element
            A = permute(A, iMax, col)
            P = permute(P, iMax, col)
            
            # Gaussian elimination
            for row in range(col+1, n):
                A[row,col] = A[row,col]/A[col,col] # Calculate the multiplier and store in A for later use
                A[row,col+1:] = A[row,col+1:] - A[row,col]*A[col,col+1:] # Update the remaining elements in the row using the multiplier

    L = np.tril(A, -1) + np.eye(n) # Extract the lower triangular matrix from A and add the identity matrix to make it a proper lower triangular matrix
    U = np.triu(A) # Extract the upper triangular matrix from A
    

    return P,L,U

def interactive_lu(P, L ,U , col, pivotRow):
    '''
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
    pivotRow : int
        The index of the pivot row.

    Returns
    -------
    P : np.array
        A permutation matrix.
    L : np.array
        A lower triangular matrix.
    U : np.array
        An upper triangular matrix.

    '''

    if col+1 >= U.shape[1] or col<=-1 :
        return P,L,U,-1,-1

    U = U.astype(float)
    L = L.astype(float)

    #col = lastColumn 
    iMax = np.argmax(np.abs(U[col:,col])) + col if pivotRow < col else pivotRow # Find the index of the row with the largest pivot element or use the pivot row if it is already found

    # Skip if the pivot is zero 
    if U[iMax,col] != 0:
        # Swap the rows of A and P for those with the largest pivot element
        U = permute(U, iMax, col)
        P = permute(P, iMax, col)
        L = permute(L-np.eye(L.shape[0]), iMax, col)+np.eye(L.shape[0]) # We cant permute L without changing the values of the diagonal, so we permute L-I and add I to get the same effect
        
        # Gaussian elimination
        for row in range(col+1, U.shape[0]):
            L[row,col] = U[row,col]/U[col,col] # Calculate the multiplier and store in A for later use
            U[row,col] = 0
            U[row,col+1:] = U[row,col+1:] - L[row,col]*U[col,col+1:] # Update the remaining elements in the row using the multiplier


    return P,L,U,(col+1), iMax


def permute(A, i:int, j:int):
    '''
    Permute the rows of a matrix.

    Parameters
    ----------
    A : np.array
        A matrix.
    i : int
        The index of the first row.
    j : int
        The index of the second row.

    Returns
    -------
    A : np.array
        The permuted matrix.

    '''

    A[[i,j],:] = A[[j,i],:] # Swap the rows of A using fancy indexing
    return A
