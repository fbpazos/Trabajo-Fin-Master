from unittest import TestCase
import pytest
from bqplot import pyplot as plt
from BNumMet.Interpolation import polinomial, piecewise_linear, pchip, splines
from BNumMet.Visualizers.InterpolationVisualizer import InterpolVisualizer
import numpy as np


class test_PolyInterpolation(TestCase):
    def test_interpolation(self):
        """
        Test the interpolation of a polynomial of degree 3
        """
        x = np.array([1, 2, 3, 4])
        y = np.array([1, 4, 9, 16])
        u = np.array([1.5, 2.5, 3.5])
        v = polinomial(x, y, u)
        self.assertTrue(np.allclose(v, np.array([2.25, 6.25, 12.25])))
        self.assertTrue(np.allclose(polinomial(x, y, x), y))

    def test_notOrdered(self):
        """
        Test the interpolation of a polynomial of degree 3 with unsorted x - this should work aka True
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [6.25])
        u = np.arange(1, 4.1, 0.1)
        v = polinomial(x, y, u)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertTrue(np.isclose(v[i1], 6.25))


class test_piecewise_linearInterpolation(TestCase):
    def test_interpolation(self):
        """
        Test the piecewise linear interpolation
        """
        x = np.array([1, 2, 3, 4])
        y = np.array([1, 4, 9, 16])
        u = np.arange(1, 4.2, 0.1)
        v = piecewise_linear(x, y, u)

        for i in range(len(x)):

            index = np.where(np.isclose(u, x[i]))[0][0]
            print(index, v[index], x[i], y[i])
            self.assertTrue(np.isclose(v[index], y[i]))

    def test_notOrdered(self):
        """
        Test the piecewise linear interpolation with unsorted x - this should NOT work aka is False
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = piecewise_linear(
            x, y, u, sorted=True
        )  # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertFalse(np.isclose(v[i1], -5))

    def test_notOrdered_unsorted(self):
        """
        Test the piecewise linear interpolation with unsorted x - this should work aka True
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = piecewise_linear(x, y, u, sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertTrue(np.isclose(v[i1], -5))


class test_pchip(TestCase):
    def test_interpolation(self):
        """
        Test the pchip interpolation
        """
        x = np.array([1, 2, 3, 4])
        y = np.array([1, 4, 9, 16])
        u = np.arange(1, 4.2, 0.1)
        v = pchip(x, y, u)

        for i in range(len(x)):

            index = np.where(np.isclose(u, x[i]))[0][0]
            print(index, v[index], x[i], y[i])
            self.assertTrue(np.isclose(v[index], y[i]))

    def test_notOrdered(self):
        """
        Test the pchip interpolation with unsorted x - this should NOT work aka is False
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = pchip(
            x, y, u, sorted=True
        )  # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertFalse(np.isclose(v[i1], -5))

    def test_notOrdered_unsorted(self):
        """
        Test the pchip interpolation with unsorted x - this should work aka True
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = pchip(x, y, u, sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertTrue(np.isclose(v[i1], -5))


class test_splines(TestCase):
    def test_interpolation(self):
        """
        Test the splines interpolation
        """
        x = np.array([1, 2, 3, 4])
        y = np.array([1, 4, 9, 16])
        u = np.arange(1, 4.2, 0.1)
        v = splines(x, y, u)

        for i in range(len(x)):

            index = np.where(np.isclose(u, x[i]))[0][0]
            print(index, v[index], x[i], y[i])
            self.assertTrue(np.isclose(v[index], y[i]))

    def test_notOrdered(self):
        """
        Test the splines interpolation with unsorted x - this should NOT work aka is False
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = splines(
            x, y, u, sorted=True
        )  # Sorted = True makes the assumption that x is sorted - IT IS NOT

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertFalse(np.isclose(v[i1], -5))

    def test_notOrdered_unsorted(self):
        """
        Test the splines interpolation with unsorted x - this should work aka True
        """
        x = np.array([1, 2, 3, 4] + [2.5])
        y = np.array([1, 4, 9, 16] + [-5])
        u = np.arange(1, 4.1, 0.1)
        v = splines(x, y, u, sorted=False)

        # find the index of the point 2.5 on u
        i1 = np.where(np.isclose(u, 2.5))[0][0]

        print(i1, v[i1])

        self.assertTrue(np.isclose(v[i1], -5))


class test_InterpolationVisualizer(TestCase):
    # Run before each test

    def runtest_setup(self):
        try:
            plt.close(self.interpolVisualizer.fig)
        except AttributeError:
            pass

        x = list(np.arange(1, 7, 1).astype(float))
        y = np.array([16, 18, 21, 17, 15, 12], dtype=float)
        u = list(np.arange(1, 6.1, 0.1).astype(float))

        self.interpolVisualizer = InterpolVisualizer(x, y, u)
        self.interpolVisualizer.run()

        print("Setting Up - Interpolation Visualizer Test")

    def test_no_param_init(self):
        """
        Test the interpolation visualizer with no parameters passed in - should use default values for x, y, u
        """
        x = list(np.arange(1, 7, 1).astype(float))
        y = np.array([16, 18, 21, 17, 15, 12], dtype=float)
        u = list(np.arange(1, 6.1, 0.1).astype(float))

        interpolVisualizer = InterpolVisualizer()
        interpolVisualizer.run()

        self.assertTrue(all(interpolVisualizer.x == x))
        self.assertTrue(all(interpolVisualizer.y == y))
        self.assertTrue(all(interpolVisualizer.u == u))

    def test_raiseException_lenXnotEqualLenY(self):
        self.runtest_setup()

        x = [1, 2, 3, 4]
        y = [1, 4, 9, 16, 25]
        u = [1, 2, 3, 4, 5]

        with self.assertRaises(ValueError):
            InterpolVisualizer(x, y, u)

    def test_updatePoints(self):
        self.runtest_setup()

        oldX = self.interpolVisualizer.ScatteredDots.x
        oldY = self.interpolVisualizer.ScatteredDots.y

        # 1. Adding a point will correctly update the scattered dots
        self.interpolVisualizer.ScatteredDots.x = np.append(
            self.interpolVisualizer.ScatteredDots.x, 7
        )
        self.interpolVisualizer.ScatteredDots.y = np.append(
            self.interpolVisualizer.ScatteredDots.y, 7
        )
        self.assertTrue(
            len(self.interpolVisualizer.ScatteredDots.x) == len(oldX) + 1
            and len(self.interpolVisualizer.ScatteredDots.y) == len(oldY) + 1
        )

        # 2. Adding same Val of X will not update the scattered dots
        self.interpolVisualizer.ScatteredDots.x = np.append(
            self.interpolVisualizer.ScatteredDots.x, 7
        )
        self.interpolVisualizer.ScatteredDots.y = np.append(
            self.interpolVisualizer.ScatteredDots.y, 7
        )
        self.assertTrue(
            len(self.interpolVisualizer.ScatteredDots.x) == len(oldX) + 1
            and len(self.interpolVisualizer.ScatteredDots.y) == len(oldY) + 1
        )

        # 3. Adding Y without X will not update the scattered dots
        self.interpolVisualizer.ScatteredDots.y = np.append(
            self.interpolVisualizer.ScatteredDots.y, 7
        )
        self.assertTrue(len(self.interpolVisualizer.ScatteredDots.y) == len(oldY) + 1)

    def test_updateMesh(self):
        self.runtest_setup()

        oldU = self.interpolVisualizer.u
        old_x_sc = self.interpolVisualizer.x_sc.min
        old_y_sc = self.interpolVisualizer.y_sc.min

        self.assertTrue(
            old_x_sc is not None and old_y_sc is not None
        )  # The values for SC are set from the begining

        # Modify the mesh should NOT modify sc_x and sc_y
        self.interpolVisualizer.slider.value = [-8.0, 20]

        self.assertTrue(self.interpolVisualizer.x_sc.min == old_x_sc)
        self.assertTrue(self.interpolVisualizer.y_sc.min == old_y_sc)

        # Modify the mesh should modify u
        self.assertTrue(
            self.interpolVisualizer.u[0] == self.interpolVisualizer.slider.min
            and self.interpolVisualizer.u[-1] == self.interpolVisualizer.slider.max
        )

    def test_updateCheckboxes(self):
        self.runtest_setup()

        self.interpolVisualizer.interpolLines()
        self.assertTrue(
            len(self.interpolVisualizer.interpolationLines)
            == len(self.interpolVisualizer.methods)
        )

        self.interpolVisualizer.checkboxes[0].value = False
        self.assertTrue(
            len(self.interpolVisualizer.interpolationLines)
            == len(self.interpolVisualizer.methods) - 1
        )

    def test_reset(self):
        self.runtest_setup()

        oldX = self.interpolVisualizer.ScatteredDots.x
        oldY = self.interpolVisualizer.ScatteredDots.y

        # 1. Adding a point will correctly update the scattered dots
        self.interpolVisualizer.ScatteredDots.x = np.append(
            self.interpolVisualizer.ScatteredDots.x, 7
        )
        self.interpolVisualizer.ScatteredDots.y = np.append(
            self.interpolVisualizer.ScatteredDots.y, 7
        )

        self.interpolVisualizer.reset(None)

        self.assertTrue(
            (self.interpolVisualizer.ScatteredDots.x == oldX).all()
            and (self.interpolVisualizer.ScatteredDots.y == oldY).all()
        )
