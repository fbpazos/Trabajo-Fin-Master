from scipy.optimize import brentq
from BNumMet.NonLinear import zBrentDekker
import numpy as np
import json


# Matlabs Brent's method
def zBrentDekkerMAT(f, interval, stopIters=1000, iters=False, *args):
    """
    NOTE: This is a direct copy of the matlab function fzero  https://www.mathworks.com/help/matlab/ref/fzero.html by Mathworks Inc. This is not my code. I have only modified it to work with python. I have not tested it for accuracy. I own no rights to this code. I am only using it for educational purposes.

    Finds a zeros over the given interval using a combination of Bisection and secant method
    params:
        f: function to find the zeros
        interval: interval where the zeros are searched
        *args: arguments of the function f
    returns:
        x: zeros of the function f
    raises:
        ValueError: if the function has no zeros in the given interval
    """

    x0, x1 = interval
    f0 = f(x0, *args)
    f1 = f(x1, *args)

    if f0 * f1 > 0:
        raise ValueError("The function has no zeros in the given interval")

    xn = x0
    fn = f0

    d = x1 - xn
    e = d

    iterations = 0
    while f1 and iterations < stopIters:
        iterations += 1
        if np.sign(f0) == np.sign(f1):
            x0 = xn
            f0 = fn
            d = x1 - xn
            e = d
        elif np.sign(f0) < np.sign(f1):
            x0, x1, xn = x1, x0, x1
            f0, f1, fn = f1, f0, f1

        # Convergence test and possible exit
        m = 0.5 * (x0 - x1)
        tolerance = 2.0 * np.finfo(float).eps * max(abs(x1), 1.0)
        if abs(m) <= tolerance or f1 == 0.0:
            break

        # Bisection or interpolation
        if abs(e) < tolerance or abs(fn) <= abs(f1):
            # Bisection
            d = m
            e = m
        else:
            # Interpolation
            s = f1 / fn
            if x0 == xn:
                # Linear interpolation
                p = 2.0 * m * s
                q = 1.0 - s
            else:
                # Inverse quadratic interpolation
                q = fn / f0
                r = f1 / f0
                p = s * (2.0 * m * q * (q - r) - (x1 - xn) * (r - 1.0))
                q = (q - 1.0) * (r - 1.0) * (s - 1.0)

            if p > 0.0:
                q = -q
            else:
                p = -p
            # Is interpolated point acceptable?
            if 2.0 * p < 3.0 * m * q - abs(tolerance * q) and p < abs(0.5 * e * q):
                e = d
                d = p / q
            else:
                d = m
                e = m

        # Next point
        xn = x1
        fn = f1
        if abs(d) > tolerance:
            x1 += d
        else:
            x1 -= np.sign(x1 - x0) * tolerance

        f1 = f(x1, *args)

    if iters:
        return x1, iterations
    return x1


global iterScipy, iterBNM, iterMatlab


iterScipy, iterBNM, iterMatlab = 0, 0, 0


def f_scipy(x, f):
    global iterScipy
    iterScipy += 1
    return f(x)


def f_BNM(x, f):
    global iterBNM
    iterBNM += 1
    return f(x)


def f_Matlab(x, f):
    global iterMatlab
    iterMatlab += 1
    return f(x)


def experiment(scipyTol, bnmTol, evalFunc=1):
    global iterScipy, iterBNM, iterMatlab

    intervalsWidthIncrease = [i for i in range(1, 10000)]

    def create_function(i, evalFunc):
        if evalFunc == 1:
            return lambda x: (x - 1) * x ** (i - 1)
        else:
            return lambda x: (x - 0.1) * x ** (i - 1)

    functions = [(i, create_function(i, evalFunc=evalFunc)) for i in range(1, 10, 2)]

    results = {"Scipy": {}, "BNM": {}, "Matlab": {}}

    for order, f in functions:
        order = f"x^{order}"
        results["Scipy"][order] = []
        results["BNM"][order] = []
        results["Matlab"][order] = []
        for i in intervalsWidthIncrease:
            iterScipy, iterBNM, iterMatlab = 0, 0, 0

            scipyFun = lambda x: f_scipy(x, f)
            BNMFun = lambda x: f_BNM(x, f)
            matlabFun = lambda x: f_Matlab(x, f)
            a = 0.08
            b = 1.1 + i
            x1 = brentq(scipyFun, a, b, maxiter=1000, xtol=scipyTol)
            x2 = zBrentDekker(BNMFun, (a, b), stop_iters=1000, tol=bnmTol)
            x3 = zBrentDekkerMAT(
                matlabFun, (a, b), stopIters=1000
            )  # No tolerance for matlab

            results["Scipy"][order].append((i, iterScipy, x1))
            results["BNM"][order].append((i, iterBNM, x2))
            results["Matlab"][order].append((i, iterMatlab, x3))

    return results


for i in [1, 2]:
    with open(f"./Demos/Timings/Results/NonLinear/NonLinearTimings_{i}.json", "w") as f:
        json.dump(experiment(1e-15, 1e-15, evalFunc=i), f, indent=4)

    with open(
        f"./Demos/Timings/Results/NonLinear/NonLinearTimings_diffTol_bnm_{i}.json", "w"
    ) as f:
        json.dump(experiment(1e-15, 0, evalFunc=i), f, indent=4)

    with open(
        f"./Demos/Timings/Results/NonLinear/NonLinearTimings_diffTol_scipy_{i}.json",
        "w",
    ) as f:
        json.dump(experiment(1e-42, 1e-15, evalFunc=i), f, indent=4)
"""
# Save results to file
with open("./Demos/Timings/Results/NonLinear/NonLinearTimings_2.json", "w") as f:
    json.dump(experiment(1e-15, 1e-15), f, indent=4)

with open(
    "./Demos/Timings/Results/NonLinear/NonLinearTimings_diffTol_bnm_2.json", "w"
) as f:
    json.dump(experiment(1e-15, 1e-17), f, indent=4)

with open(
    "./Demos/Timings/Results/NonLinear/NonLinearTimings_diffTol_scipy_2.json", "w"
) as f:
    json.dump(experiment(1e-17, 1e-15), f, indent=4)
"""
