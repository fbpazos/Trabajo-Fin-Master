import numpy as np
def prettyPrintMatrix(matrix):
    res = " \\begin\{pmatrix\}\n"
    for row in matrix:
        res += " & ".join([str(x) for x in row]) + "\\\\\n"
    res += "\end\{pmatrix\}"
    return res
    
def sortInterpolVals(x,y):
    x = np.array(x)
    y = np.array(y)
    ind = np.argsort(x) # Get the indices of the sorted array
    x = x[ind] # Sort the x coordinates
    y = y[ind] # Sort the y coordinates

    return x,y

if __name__ == "__main__":
    print("Module")
    