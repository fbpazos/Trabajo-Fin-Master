import sys
import os
from unittest import TestCase
import unittest
import numpy as np
from random import randint

from BNumMet.LinearSystems import lu, permute, interactive_lu
from BNumMet.Visualizers.LUVisualizer import LUVisualizer


class test_LU(TestCase):
    def test_lu_simple(self):
        """
        Test the LU decomposition by running it on a fixed matrix and checking that the result is correct
        """
        A = np.array([[10, -7, 0], [-3, 2, 6], [5, -1, 5]])
        P, L, U = lu(A)
        # print(P@A)
        print(P)
        print(L)
        print(U)

        self.assertTrue(np.allclose(P @ A, L @ U))

    def test_lu_random(self):
        """
        Test the LU decomposition by running it on a random matrix and checking that the result is correct
        """
        A = np.random.rand(10, 10)
        P, L, U = lu(A)

        self.assertTrue(np.allclose(P @ A, L @ U), msg=f"P@A != L@U\n{P@A} != {L@U}")

    def test_lu_random_ints(self):
        """
        Test the LU decomposition by running it on a random INTEGER matrix and checking that the result is correct
        This test is useful to check that the algorithm works with integer matrices as well because the python maintains the type of the elements of the matrix when performing operations
        """
        A = np.random.randint(0, 10, (10, 10))
        P, L, U = lu(A)

        self.assertTrue(np.allclose(P @ A, L @ U), msg=f"P@A != L@U\n{P@A} != {L@U}")

    def test_lu_notSquare(self):
        """
        Test that the LU decomposition raises a ValueError when the matrix is not square
        """
        A = np.array([[10, -7, 0], [-3, 2, 6], [5, -1, 5], [1, 2, 3]])
        with self.assertRaises(ValueError):
            P, L, U = lu(A)

    def test_permute(self):
        """
        Test the permute function by running it on a fixed matrix and checking that the result is correct
        It also checks that the function does not modify the original matrix
        """
        A = np.array([[10, -7, 0], [-3, 2, 6], [5, -1, 5]])

        for i in range(A.shape[0]):
            self.assertTrue(
                np.allclose(permute(A, i, i), A)
            )  # Check trivial permutation
        self.assertTrue(
            np.allclose(
                permute(A, 0, 1), np.array([[-3, 2, 6], [10, -7, 0], [5, -1, 5]])
            )
        )  # swap 1st and 2nd rows
        self.assertFalse(
            np.allclose(A, np.array([[10, -7, 0], [-3, 2, 6], [5, -1, 5]]))
        )  # It is not the same matrix as A - initially

    def test_interactive_lu(self):
        """
        Test the interactive LU decomposition by running it on a fixed matrix and checking that the result is correct
        we do not test the visualizer here, just the algorithm, with automated pivoting (i.e. iMax = -1)
        """
        A = np.array([[10, -7, 0], [-3, 2, 6], [5, -1, 5]])
        L = np.eye(A.shape[0])
        U = A.copy()
        P = np.eye(A.shape[0])

        lastColumn = 0
        while lastColumn > A.shape[1]:
            P, L, U, lastColumn, iMax = interactive_lu(P, L, U, lastColumn, -1)
            self.assertTrue(np.allclose(P @ A, L @ U))


class Test_LUVisualizer(TestCase):
    def runtest_setup(self, A=None):
        """
        Run the setup for the tests of the LUVisualizer

        Parameters
        ----------
        A : np.array
            The matrix to be decomposed. If None, a fixed matrix is put
        """
        self.A = (
            np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float) if A is None else A
        )
        self.luVisualizer = LUVisualizer(self.A)
        self.luVisualizer.run()

    def test_no_param_init(self):
        """
        Test if the LUVisualizer is initialized correctly when no matrix is passed as a parameter to the constructor (i.e. A default matrix is used)
        """
        A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
        self.luVisualizer = LUVisualizer()
        self.luVisualizer.run()

        self.assertTrue(np.allclose(self.luVisualizer.A, A))

    def test_initialazation(self):
        """
        Test if the LUVisualizer is initialized correctly
        """
        self.runtest_setup()
        self.assertEqual(self.luVisualizer.step, 0)
        self.assertTrue(np.allclose(self.A, self.luVisualizer.A))

        self.assertTrue(self.A.shape == self.luVisualizer.P.shape)
        self.assertTrue(self.A.shape == self.luVisualizer.L.shape)

    def test_ValueError(self):
        """
        Test if the LUVisualizer raises a ValueError when the matrix is not square
        """
        with self.assertRaises(ValueError):
            self.luVisualizer = LUVisualizer([[1, 2, 3, 4], [4, 5, 6, 4], [7, 8, 9, 4]])

    def test_step(self):
        """
        Test if step works correctly by clicking one button and then checking if the step has changed, and if the buttons have changed too
        """
        self.runtest_setup()
        # Get buttons which are not disabled
        buttons = [
            button
            for row in self.luVisualizer.buttonsMatrix
            for button in row
            if not button.disabled
        ]

        # Simulate clicking one of the buttons
        buttons[0].click()

        # This should hgave changed the step and the matrix buttons
        self.assertEqual(self.luVisualizer.step, 1)
        buttons2 = [
            button
            for row in self.luVisualizer.buttonsMatrix
            for button in row
            if not button.disabled
        ]
        self.assertNotEqual(buttons, buttons2)

        # The button should be disabled
        self.assertTrue(buttons[0].disabled)
        buttons[0].click()
        self.assertEqual(self.luVisualizer.step, 1)

        buttons2[0].click()
        self.assertEqual(self.luVisualizer.step, 2)

    def test_previousStep(self):
        """
        Test if previousStep works correctly by clicking one button and then going back
        """
        self.runtest_setup()

        oldStep = (
            self.luVisualizer.step,
            self.luVisualizer.L,
            self.luVisualizer.U,
            self.luVisualizer.P,
        )

        self.assertTrue(len(self.luVisualizer.previousSteps) == 0)
        # Get buttons which are not disabled
        buttons = [
            button
            for row in self.luVisualizer.buttonsMatrix
            for button in row
            if not button.disabled
        ]
        # Simulate clicking one of the buttons
        buttons[0].click()
        self.assertTrue(len(self.luVisualizer.previousSteps) == 1)

        self.luVisualizer.previousStep(None)
        self.assertEqual(self.luVisualizer.step, oldStep[0])
        self.assertTrue(np.allclose(self.luVisualizer.L, oldStep[1]))
        self.assertTrue(np.allclose(self.luVisualizer.U, oldStep[2]))
        self.assertTrue(np.allclose(self.luVisualizer.P, oldStep[3]))

    def test_reset(self):
        """
        Test reset button by clicking all buttons and then reset
        It should reset the step and the matrices to the initial values
        """
        self.runtest_setup()

        buttons = [
            button
            for row in self.luVisualizer.buttonsMatrix
            for button in row
            if not button.disabled
        ]
        while len(buttons) > 0:
            buttons[0].click()
            buttons = [
                button
                for row in self.luVisualizer.buttonsMatrix
                for button in row
                if not button.disabled
            ]

        # All buttons should be disabled
        self.assertTrue(
            all(
                [
                    button.disabled
                    for row in self.luVisualizer.buttonsMatrix
                    for button in row
                ]
            )
        )

        self.luVisualizer.reset(None)
        self.assertEqual(self.luVisualizer.step, 0)
        self.assertTrue(np.allclose(self.luVisualizer.L, np.eye(self.A.shape[0])))
        self.assertTrue(np.allclose(self.luVisualizer.U, self.A))
        self.assertTrue(np.allclose(self.luVisualizer.P, np.eye(self.A.shape[0])))
        self.assertTrue(
            any(
                [
                    not button.disabled
                    for row in self.luVisualizer.buttonsMatrix
                    for button in row
                ]
            )
        )

    def test_interactive_lu_proccess(self):
        """
        Test the interactive LU proccess:
        1. Generate a random matrix A (10x10)
        2. Run the interactive LU proccess

        for each step:
            3. Click a random button which is not disabled
            4. Check that P@A = L@U
        """
        self.runtest_setup(np.random.rand(10, 10))
        P = self.luVisualizer.P
        L = self.luVisualizer.L
        U = self.luVisualizer.U
        A = self.luVisualizer.A
        for i in range(self.A.shape[0]):
            buttons = [
                button
                for row in self.luVisualizer.buttonsMatrix
                for button in row
                if not button.disabled
            ]
            if len(buttons) == 0:
                break
            buttons[randint(0, len(buttons) - 1)].click()

            P = self.luVisualizer.P
            L = self.luVisualizer.L
            U = self.luVisualizer.U
            self.assertTrue(
                np.allclose(
                    P @ A,
                    L @ U,
                ),
                msg=f"P@A != L@U\n{P@A} != {L@U}",
            )
