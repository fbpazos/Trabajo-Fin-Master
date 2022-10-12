from unittest import TestCase

from matplotlib.pyplot import cla
from BasicLineAlg.Interpolation.interpolation import interPoly, piecewiseLinear, pchip, splitnetx
import numpy as np


class test_PolyInterpolation(TestCase):
    def test_interpolation(self):
        '''
        Test the interpolation of a polynomial of degree 3
        '''
        x = np.array([1,2,3,4])
        y = np.array([1,4,9,16])
        u = np.array([1.5,2.5,3.5])
        v = interPoly(x,y,u)
        self.assertTrue(np.allclose(v, np.array([2.25,6.25,12.25])))
        self.assertTrue(np.allclose(interPoly(x,y,x), y))
    def test_notOrdered(self):
        '''
        Test the interpolation of a polynomial of degree 3 with unsorted x - this should work aka True
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[6.25])
        u = np.arange(1,4.1,0.1)
        v = interPoly(x,y,u)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertTrue(np.isclose(v[i1],6.25))

class test_PieceWiseLinearInterpolation(TestCase):
    def test_interpolation(self):
        '''
        Test the piecewise linear interpolation 
        '''
        x = np.array([1,2,3,4])
        y = np.array([1,4,9,16])
        u = np.arange(1,4.2,0.1)
        v = piecewiseLinear(x,y,u)
        
        for i in range(len(x)):
            
            index = np.where(np.isclose(u,x[i]))[0][0]
            print(index,v[index],x[i],y[i])
            self.assertTrue(np.isclose(v[index],y[i]))
    def test_notOrdered(self):
        '''
        Test the piecewise linear interpolation with unsorted x - this should NOT work aka is False
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = piecewiseLinear(x,y,u,sorted=True) # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertFalse(np.isclose(v[i1],-5))
    def test_notOrdered_unsorted(self):
        '''
        Test the piecewise linear interpolation with unsorted x - this should work aka True
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = piecewiseLinear(x,y,u,sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertTrue(np.isclose(v[i1],-5))


class test_pchip(TestCase):
    def test_interpolation(self):
        '''
        Test the pchip interpolation 
        '''
        x = np.array([1,2,3,4])
        y = np.array([1,4,9,16])
        u = np.arange(1,4.2,0.1)
        v = pchip(x,y,u)
        
        for i in range(len(x)):
            
            index = np.where(np.isclose(u,x[i]))[0][0]
            print(index,v[index],x[i],y[i])
            self.assertTrue(np.isclose(v[index],y[i]))
    def test_notOrdered(self):
        '''
        Test the pchip interpolation with unsorted x - this should NOT work aka is False
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = pchip(x,y,u,sorted=True) # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertFalse(np.isclose(v[i1],-5))

    def test_notOrdered_unsorted(self):
        '''
        Test the pchip interpolation with unsorted x - this should work aka True
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = pchip(x,y,u,sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertTrue(np.isclose(v[i1],-5))
 
class test_splitnetx(TestCase):
    def test_interpolation(self):
        '''
        Test the splitnetx interpolation 
        '''
        x = np.array([1,2,3,4])
        y = np.array([1,4,9,16])
        u = np.arange(1,4.2,0.1)
        v = splitnetx(x,y,u)
        
        for i in range(len(x)):
            
            index = np.where(np.isclose(u,x[i]))[0][0]
            print(index,v[index],x[i],y[i])
            self.assertTrue(np.isclose(v[index],y[i]))
    def test_notOrdered(self):
        '''
        Test the splitnetx interpolation with unsorted x - this should NOT work aka is False
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = splitnetx(x,y,u,sorted=True) # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertFalse(np.isclose(v[i1],-5))

    def test_notOrdered_unsorted(self):
        '''
        Test the splitnetx interpolation with unsorted x - this should work aka True
        '''
        x = np.array([1,2,3,4]+[2.5])
        y = np.array([1,4,9,16]+[-5])
        u = np.arange(1,4.1,0.1)
        v = splitnetx(x,y,u,sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u,2.5))[0][0]

        print(i1,v[i1])

        self.assertTrue(np.isclose(v[i1],-5))



       
