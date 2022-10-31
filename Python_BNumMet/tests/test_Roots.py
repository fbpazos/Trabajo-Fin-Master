from BNumMet.Zeros import *
import numpy as np
from unittest import TestCase


class test_Roots(TestCase):
    def test_bisect(self):
        """
        Test the bisection method
        """
        f = lambda x: x**2 - 1
        x = bisect(f, [0, 2])
        self.assertTrue(np.isclose(x, 1))

    def test_secant(self):
        """
        Test the secant method
        """
        f = lambda x: x**2 - 1
        x = secant(f, [0, 2])

        self.assertTrue(np.isclose(x, 1))

    def test_newton(self):
        """
        Test the Newton method
        """
        f = lambda x: x**2 - 1
        fprime = lambda x: 2 * x
        x = newton(f, fprime, 3)
        self.assertTrue(np.isclose(x, 1))

    def test_fZero(self):
        """
        Test the fZero method
        """
        f = lambda x: x**2 - 1
        x = fZero(f, [0, 2])
        self.assertTrue(np.isclose(x, 1))

    def test_IQI(self):
        """
        Test the IQI method
        """
        f = lambda x: x**2 - 1
        x = IQI(f, [0, 2 / 3, 2])
        self.assertTrue(np.isclose(x, 1))

    def test_SameSign(self):
        """
        Test if in (a,b) with both f(a),f(b) >0 or <0 then ValueError is raised in all methods

        """
        f = lambda x: x**2 - 1
        methods = [bisect, secant, fZero]
        for method in methods:
            with self.assertRaises(ValueError):
                method(f, [-2, 2])
