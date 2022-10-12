import sys
import os
from unittest import TestCase
import numpy as np



from BasicLineAlg.LinearEquations.lu import lu, permute, interative_lu


class test_LU(TestCase):
    def test_lu_simple(self):
        A = np.array([[10, -7, 0],[-3,2,6],[5,-1,5]])
        P,L,U = lu(A)
        #print(P@A)
        print(P)
        print(L)
        print(U)

        self.assertTrue(np.allclose(P@A, L@U))
    
    def test_lu_random(self):
        A = np.random.randint(1,10,(5,5))
        P,L,U = lu(A)

        self.assertTrue(np.allclose(P@A, L@U), msg = f"P@A != L@U\n{P@A} != {L@U}")
    
    def test_lu_notSquare(self):
        A = np.array([[10, -7, 0],[-3,2,6],[5,-1,5],[1,2,3]])
        with self.assertRaises(ValueError):
            P,L,U = lu(A)


    def test_permute(self):
        A = np.array([[10, -7, 0],[-3,2,6],[5,-1,5]])

        for i in range(A.shape[0]):
            self.assertTrue(np.allclose(permute(A, i, i) , A)) # Check trivial permutation
        self.assertTrue(np.allclose(permute(A, 0,1), np.array([[-3,2,6],[10, -7, 0],[5,-1,5]]))) # swap 1st and 2nd rows
        self.assertFalse(np.allclose(A, np.array([[10, -7, 0],[-3,2,6],[5,-1,5]]))) # It is not the same matrix as A - initially
        
    def test_interactive_lu(self):
        A = np.array([[10, -7, 0],[-3,2,6],[5,-1,5]])
        L = np.eye(A.shape[0])
        U = A.copy()
        P = np.eye(A.shape[0])

        lastColumn = 0
        while lastColumn > -1:
            P,L,U,lastColumn,iMax = interative_lu(P,L,U,lastColumn,-1)
            self.assertTrue(np.allclose(P@A, L@U))





