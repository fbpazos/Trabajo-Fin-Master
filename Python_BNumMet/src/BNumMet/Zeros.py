import numpy as np
from BNumMet.Interpolation import interPoly


def bisect(f, interval, stopIters=100, iters=False, *args):
    """
    Finds a zeros over the given interval using the Bisection method and tolerance ~ machine precision

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
    x = x1
    iterations = 0
    while f1 and iterations < stopIters:
        iterations += 1
        x = 0.5 * (x0 + x1)
        faux = f(x, *args)
        if faux * f1 < 0:
            x0 = x
            f0 = faux
        else:
            x1 = x
            f1 = faux
    if iters:
        return x, iterations
    return x


def secant(fun, interval, stopIters=100, iters=False, *args):
    """
    Finds a zeros over the given interval using the secant method

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
    f0 = fun(x0, *args)
    f1 = fun(x1, *args)

    print(f0, f1)
    if f0 * f1 > 0:
        raise ValueError("The function has no zeros in the given interval")

    iterations = 0
    while abs(x1 - x0) > np.finfo(float).eps and iterations < stopIters:
        iterations += 1
        x2 = x0
        x0 = x1
        x1 = x1 + (x1 - x2) / (fun(x2, *args) / fun(x1, *args) - 1)

    if iters:
        return x1, iterations
    return x1


def newton(fun, funPrime, startPoint, stopIters=100, iters=False, *args):
    """
    Finds a zeros over the given interval using the Newton-Raphson method

    params:
        f: function to find the zeros
        interval: interval where the zeros are searched
        *args: arguments of the function f

    returns:
        x: zeros of the function f

    raises:
        ValueError: if the function has no zeros in the given interval

    """
    previousX = startPoint - 1
    xn = startPoint
    fn = fun(xn, *args)
    if funPrime(xn, *args) == 0:
        raise ValueError("The derivative of the function is zero")

    iterations = 0
    while (
        fn != 0
        and not np.isclose(xn - previousX, 0)
        and funPrime(xn, *args) != 0
        and iterations < stopIters
    ):
        iterations += 1

        previousX = xn
        xn = xn - fn / funPrime(xn, *args)
        fn = fun(xn, *args)

    if iters:
        return xn, iterations
    return xn


def IQI(f, xVals, stopIters=100, iters=False, *args):
    """
    Finds a zeros over the given interval using the Inverse Quadratic Interpolation method

    params:
        f: function to find the zeros
        xVals : [x0,x1,x2]
        *args: arguments of the function f

    returns:
        x: zeros of the function f

    raises:
        ValueError: if the function has no zeros in the given interval

    """
    x0, x1, x2 = xVals
    iterations = 0
    while abs(x1 - x0) > np.finfo(float).eps and iterations < stopIters:
        iterations += 1
        f0, f1, f2 = f(x0, *args), f(x1, *args), f(x2, *args)
        aux1 = (x0 * f1 * f2) / ((f0 - f1) * (f0 - f2))
        aux2 = (x1 * f0 * f2) / ((f1 - f0) * (f1 - f2))
        aux3 = (x2 * f1 * f0) / ((f2 - f0) * (f2 - f1))
        new = aux1 + aux2 + aux3
        x0, x1, x2 = new, x0, x1

    if iters:
        return x0, iterations
    return x0


def fZero(f, interval, stopIters=100, iters=False, *args):
    """
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
