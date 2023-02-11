import numpy as np


def pretty_print_matrix(matrix):
    # Initialize the string to represent the matrix
    res = " \\begin\{pmatrix\}\n"

    # Loop through each row in the matrix
    for row in matrix:
        # Join the elements in each row with " & " and add a line break at the end
        res += " & ".join([str(x) for x in row]) + "\\\\\n"

    # Close the matrix representation
    res += "\end\{pmatrix\}"

    # Return the final string
    return res


def sort_interpolation_values(x, y):
    x = np.array(x)
    y = np.array(y)
    ind = np.argsort(x)  # Get the indices of the sorted array
    x = x[ind]  # Sort the x coordinates
    y = y[ind]  # Sort the y coordinates

    return x, y


if __name__ == "__main__":
    print("Module")
