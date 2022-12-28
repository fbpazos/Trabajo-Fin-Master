from BNumMet.NonLinear import *
from BNumMet.Visualizers.NonLinearVisualizer import NonLinearVisualizer
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


class Test_NonLinearVisualizer(TestCase):
    def test_no_param_init(self):
        """
        Tests if NonLinearVisualizer is initialized correctly without parameters (i.e. default values are used)
        """

        self.nonLinearVisualizer = NonLinearVisualizer()
        self.nonLinearVisualizer.run()

        fun = lambda x: (x - 1) * (x - 4) * np.exp(-x)
        interval = (0, 3)

        x = np.linspace(interval[0], interval[1], 100)

        self.assertTrue(np.allclose(self.nonLinearVisualizer.f(x), fun(x)))
        self.assertEqual(self.nonLinearVisualizer.x0, interval[0])
        self.assertEqual(self.nonLinearVisualizer.x1, interval[1])
