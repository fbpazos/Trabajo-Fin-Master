# %%
import numpy as np
from time import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from BNumMet.LinearSystems import lu_solve


# %%
def splines(x, y, u, sorted=False, mode=None):
    """
    Finds the piecewise cubic interpolatory spline S(x), with S(x(j)) = y(j), and returns v(k) = S(u(k)).

    params:
        x: list of x coordinates
        y: list of y coordinates
        u: list of points where the interpolation is computed
        sorted (optional): if the points are sorted or not (default: False)

    returns:
        v: list of values of the interpolation at the points u
    """

    def splineslopes(h, delta):
        """
        Computes the slopes of the splines Uses not-a-knot end conditions.

        params:
            h: list of distances between points
            delta: list of slopes between points

        returns:
            d: list of slopes for the splines
        """
        a = np.zeros(len(h)).astype(float)
        b = np.zeros(len(h)).astype(float)
        c = np.zeros(len(h)).astype(float)
        r = np.zeros(len(h)).astype(float)

        a[:-1] = h[1:]
        a[-1] = h[-2] + h[-1]
        b[0] = h[1]
        b[1:] = 2 * (h[1:] + h[:-1])
        b = np.append(b, h[-2])
        c[0] = h[0] + h[1]
        c[1:] = h[:-1]

        #  Right-hand side

        r[0] = ((h[0] + 2 * c[0]) * h[1] * delta[0] + h[0] ** 2 * delta[1]) / c[0]
        r[1:] = 3 * (h[1:] * delta[:-1] + h[:-1] * delta[1:])
        r = np.append(
            r,
            (h[-1] ** 2 * delta[-2] + (2 * a[-1] + h[-1]) * h[-2] * delta[-1]) / a[-1],
        )
        res = lu_solve(np.diag(a, -1) + np.diag(b) + np.diag(c, 1), r)
        # res = np.linalg.solve(np.diag(a, -1) + np.diag(b) + np.diag(c, 1), r)

        return res.astype(float)

    x = np.array(x)
    y = np.array(y)
    if not sorted:
        # Sort the points
        ind = np.argsort(x)  # Get the indices of the sorted array
        x = x[ind]  # Sort the x coordinates
        y = y[ind]  # Sort the y coordinates

    # First derivative
    h = np.diff(x)
    delta = np.diff(y) / h

    d = splineslopes(h, delta)

    n = len(x)
    c = (3 * delta - 2 * d[:-1] - d[1:]) / (h)
    b = (d[:-1] - 2 * delta + d[1:]) / (h**2)

    if mode == "Indexed List":
        k = np.zeros(np.size(u), dtype=int)
        for j in np.arange(1, n - 1):
            k[x[j] <= u] = j

        s = u - x[k]
        v = y[k] + s * (d[k] + s * (c[k] + s * b[k]))
    elif mode == "List Compresion":
        # Find the index of the points in u that are between x[i] and x[i+1]
        k = np.ones(len(u)).astype(
            int
        )  # Create a vector of ones of the same size as u, to store the result
        for i in range(1, n):
            k[x[i - 1] <= u] = int(i)

        s = [
            u[i] - x[k[i] - 1] for i in range(len(u))
        ]  # Compute the distance between the points in u and the points in x that are between x[i] and x[i+1]

        v = [
            y[k[i] - 1]
            + s[i] * (d[k[i] - 1] + s[i] * (c[k[i] - 1] + s[i] * b[k[i] - 1]))
            for i in range(len(u))
        ]  # Compute the value of the interpolation at the points in u

    else:
        print("Mode not recognized")
        v = []

    return v


# %%
def time_Interpolation(mode, size):
    x = list(np.arange(1, 7, 1).astype(float))
    y = [16, 18, 21, 17, 15, 12]

    u = np.random.uniform(0, 8, size)  # Generate random points between 1 and 6

    start = time()
    splines(
        x, y, u, sorted=True, mode=mode
    )  # Compute the interpolation at the random points u
    end = time()

    return end - start


# %%
sizes = np.arange(100, 10000, 100)
sizes = [int(size) for size in sizes]  # Convert to int
n_iters = 100
recalc = False
file = "./Demos/Timings/Results/Interpolation/Interpolation_Timings.json"


results = {"Indexed List": {}, "List Compresion": {}}

for size in sizes:
    print(f"{size:_^50}")
    for mode in results.keys():
        times = []
        for _ in range(n_iters):
            times.append(time_Interpolation(mode, size))
        results[mode][size] = times

        print(
            f"\t{mode} :\n\t\t {np.mean(results[mode][size]):.4f}s",
            f"± {np.std(results[mode][size]):.4f}s",
        )  # Print the average time for the current mode

        # Save the results to a json file, for later use (if needed)
        with open(file, "w+") as f:
            json.dump(results, f, indent=4)
