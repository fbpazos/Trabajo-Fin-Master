from unittest import TestCase
from BasicLineAlg.module import prettyPrintMatrix, sortInterpolVals

class test_module(TestCase):
    def test_PrettyPrint(self):
        matrix = [[1,2],[3,4]]
        stringRes =  """ \\begin\\{pmatrix\\}1 & 2\\\\3 & 4\\\\\\end\\{pmatrix\\}"""

        self.assertTrue(prettyPrintMatrix(matrix).replace("\n","") == stringRes)

    def test_SortInterpolVals(self):
        x = [1,3,2]
        y = [4,3,2]
        xRes = [1,2,3]
        yRes = [4,2,3]
        x,y = sortInterpolVals(x,y)

        self.assertTrue((x == xRes).all() and (y == yRes).all())