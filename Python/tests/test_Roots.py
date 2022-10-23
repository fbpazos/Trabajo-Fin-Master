from BasicLineAlg.Zeros.roots import *
import numpy as np
from unittest import TestCase

class test_Roots(TestCase):
    def test_bisect(self):
        '''
        Test the bisection method
        '''
        f = lambda x: x**2-1
        x = bisect(f,[0,2])
        self.assertTrue(np.isclose(x,1))

    def test_secant(self):
        '''
        Test the secant method
        '''
        f = lambda x: x**2-1
        x = secant(f,[0,2])
        
        self.assertTrue(np.isclose(x,1))

    def test_newton(self):
        '''
        Test the Newton method
        '''
        f = lambda x: x**2-1
        x = newton(f,[0,2])
        self.assertTrue(np.isclose(x,1))

    def test_fZero(self):
        '''
        Test the fZero method
        '''
        f = lambda x: x**2-1
        x = fZero(f,[0,2])
        self.assertTrue(np.isclose(x,1))

    def test_SameSign(self):
        '''
        Test if in (a,b) with both f(a),f(b) >0 or <0 then ValueError is raised in all methods

        '''
        f = lambda x: x**2-1

        with self.assertRaises(ValueError):
            bisect(f,[-2,2])
        with self.assertRaises(ValueError):
            secant(f,[-2,2])
        
        with self.assertRaises(ValueError):
            newton(f,[-2,2])

        with self.assertRaises(ValueError):
            fZero(f,[-2,2])

        


