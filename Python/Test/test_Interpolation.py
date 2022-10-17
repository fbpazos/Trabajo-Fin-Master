from unittest import TestCase
import pytest
from bqplot import pyplot as plt
from BasicLineAlg.Interpolation.interpolation import interPoly, piecewiseLinear, pchip, splitnetx
from BasicLineAlg.Interpolation.InterpolationVisualizer import InterpolVisualizer
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



       
class test_InterpolationVisualizer(TestCase):
    # Run before each test
    
    def runtest_setup(self):
        try:
            plt.close(self.interpolVisualizer.fig)
        except AttributeError:
            pass


        x = list(np.arange(1,7,1).astype(float)) 
        y =  np.array([16, 18, 21, 17, 15, 12],dtype=float)
        u = list(np.arange(1,6.1,0.1).astype(float))

        self.interpolVisualizer = InterpolVisualizer(x,y,u)
        self.interpolVisualizer.run()
        plt.show()

        print("Setting Up - Interpolation Visualizer")

    def test_updatePoints(self):
        self.runtest_setup()

        oldX = self.interpolVisualizer.x.copy()
        oldY = self.interpolVisualizer.y.copy()
        # 1. Properly update the points
        self.interpolVisualizer.scatterPlot.x = np.append(self.interpolVisualizer.scatterPlot.x, 5.5)
        self.interpolVisualizer.scatterPlot.y = np.append(self.interpolVisualizer.scatterPlot.y, 14)

        self.assertTrue(len(self.interpolVisualizer.scatterPlot.x) == len(oldX)+1)
        self.assertTrue(len(self.interpolVisualizer.scatterPlot.y) == len(oldY)+1)

        # 2. If same X value is added, it should not update
        self.interpolVisualizer.scatterPlot.x = np.append(self.interpolVisualizer.scatterPlot.x, 5.5)
        self.interpolVisualizer.scatterPlot.y = np.append(self.interpolVisualizer.scatterPlot.y, 14)

        self.assertTrue(len(self.interpolVisualizer.scatterPlot.x) == len(oldX)+1)
        self.assertTrue(len(self.interpolVisualizer.scatterPlot.y) == len(oldY)+1)

        # 3. If ONLY Y value is added, it should not update Y
        self.interpolVisualizer.scatterPlot.y = np.append(self.interpolVisualizer.scatterPlot.y, 14)

        self.assertTrue(len(self.interpolVisualizer.scatterPlot.y) == len(oldY)+1)

    def test_updateMesh(self):
        pass




    