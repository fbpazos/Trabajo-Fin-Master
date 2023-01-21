import numpy as np
from time import time
import json
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib

recalc = False  # Set to True to recalculate the timings
sizes = np.arange(500, 4001, 500)  # Matrix sizes to test
n_iter = 100  # Number of iterations to average over for each matrix size
# file = "./Demos/Timings/Results/Linear Systems/LU_Timings.json"  # File to save/load the results from
file = "./Demos/Timings/Results/Linear Systems/LU_Timings.json"  # File to save/load the results from


def lu_timing(Matrix, mode):  # LU decomposition with np subarrays
    if Matrix.shape[0] != Matrix.shape[1]:
        raise ValueError("Matrix must be square")

    n = Matrix.shape[0]  # number of rows/columns
    A = Matrix.copy().astype(float)  # Make a copy of A and convert to float
    P = np.eye(n, dtype=float)  # Initialize P as the identity matrix

    # Loop over the columns of A
    for col in range(n):
        # Find the index of the row with the largest pivot element
        iMax = int(np.argmax(np.abs(A[col:, col])) + col)

        # Skip if the pivot is zero
        if A[iMax, col] != 0:
            # Swap the rows of A and P for those with the largest pivot element
            A[[iMax, col], :] = A[[col, iMax], :]
            P[[iMax, col], :] = P[[col, iMax], :]

            pivot = A[col, col]

            match mode:
                case "Submatrices":  # Using list indexing twice
                    A[col + 1 :, col] = A[col + 1 :, col] / pivot
                    A[col + 1 :, col + 1 :] = A[col + 1 :, col + 1 :] - (
                        A[col + 1 :, :][:, [col]] @ A[[col], :][:, col + 1 :]
                    )
                case "New Axis":  # Using np.newaxis
                    A[col + 1 :, col] = A[col + 1 :, col] / pivot
                    A[col + 1 :, col + 1 :] = (
                        A[col + 1 :, col][:, np.newaxis]
                        @ A[col, col + 1 :][np.newaxis, :]
                    )
                case "Outer Product":  # Using np.outer
                    A[col + 1 :, col] = A[col + 1 :, col] / pivot
                    A[col + 1 :, col + 1 :] = np.outer(
                        A[col + 1 :, col], A[col, col + 1 :]
                    )
                case "Loop":  # Gaussian elimination
                    for row in range(col + 1, n):
                        A[row, col] = (
                            A[row, col] / A[col, col]
                        )  # Calculate the multiplier and store in A for later use
                        A[row, col + 1 :] = (
                            A[row, col + 1 :] - A[row, col] * A[col, col + 1 :]
                        )  # Update the remaining elements in the row using the multiplier
                case _:
                    raise ValueError("Invalid mode")

    L = np.tril(A, -1) + np.eye(
        n
    )  # Extract the lower triangular matrix from A and add the identity matrix to make it a proper lower triangular matrix
    U = np.triu(A)  # Extract the upper triangular matrix from A

    return P, L, U


if recalc:
    results = {"Submatrices": {}, "New Axis": {}, "Outer Product": {}, "Loop": {}}
    sizes = [int(size) for size in sizes]  # Convert to int

    for size in sizes:
        print(f"{size:_^50}")
        for mode in results.keys():
            times = []
            for _ in range(n_iter):
                A = np.random.rand(size, size)
                start = time()
                lu_timing(A, mode)
                times.append(time() - start)
            results[mode][size] = times  # Store the times for each iteration

            print(
                f"/t{mode} : {np.mean(results[mode][size]):.4f}s"
            )  # Print the average time for the current mode

        # Save the results to a json file, for later use (if needed)
        with open(file, "w+") as f:
            json.dump(results, f, indent=4)
else:
    # Load the results from the json file
    with open(file, "r") as f:
        results = json.load(f)


# Plot the results
df = pd.DataFrame(results)
# map the values to np.mean
df = df.applymap(lambda x: np.mean(x))


# Plot the results using matplotlib
plt.figure()
for mode in results.keys():
    plt.plot(df.index, df[mode], "o-", label=mode)
plt.title("Timings for LU Decomposition Methods")
plt.xlabel("Size")
plt.ylabel("Time (s)")
plt.legend()

# Save the plot to a file with high resolution
plt.savefig("./Demos/Timings/Results/Linear Systems/LU_Timings.png", dpi=1000)
