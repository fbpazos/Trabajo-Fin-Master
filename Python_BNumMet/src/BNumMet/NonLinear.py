import numpy as np
from BNumMet.Interpolation import polinomial

global exceptions
exceptions = [ValueError("The function has no zeros in the given interval")]


def bisect(f, interval, stop_iters=100, iters=False, *args):
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
        raise exceptions[0]
    x = x1
    iterations = 0
    while f1 and iterations < stop_iters:
        iterations += 1
        x = 0.5 * (x0 + x1)
        faux = f(x, *args)
        if faux * f1 < 0:
            x0 = x
        else:
            x1 = x
            f1 = faux
    if iters:
        return x, iterations
    return x


def secant(fun, interval, stop_iters=100, iters=False, *args):
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
        raise exceptions[0]

    iterations = 0
    while abs(x1 - x0) > np.finfo(float).eps and iterations < stop_iters:
        iterations += 1
        x2 = x0
        x0 = x1
        x1 = x1 + (x1 - x2) / (fun(x2, *args) / fun(x1, *args) - 1)

    if iters:
        return x1, iterations
    return x1


def newton(fun, funPrime, startPoint, stop_iters=100, iters=False, *args):
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
        and iterations < stop_iters
    ):
        iterations += 1

        previousX = xn
        xn = xn - fn / funPrime(xn, *args)
        fn = fun(xn, *args)

    if iters:
        return xn, iterations
    return xn


def IQI(f, xVals, stop_iters=100, iters=False, *args):
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
    while abs(x1 - x0) > np.finfo(float).eps and iterations < stop_iters:
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


def zBrentDekker(
    f, interval, tol=10 ** (-20), stop_iters=100, iters=False, steps=False, *args
):
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
    # Split the interval into a and b
    a, b = interval
    # Evaluate the function at a and b
    fa = f(a, *args)
    fb = f(b, *args)

    # Check if there are no zeros in the interval
    if fa * fb > 0:  # No zeros guaranteed in the interval
        raise exceptions[0]

    # Initialize the variables for the internal section
    c, fc, d, e = a, fa, b - a, b - a

    # Check if fc is smaller than fb, if so swap the values
    if abs(fc) < abs(fb):
        a, b, c, fa, fb, fc = b, c, b, fb, fc, fb

    # Calculate the tolerance level
    tolerance = 2 * np.finfo(float).eps * abs(b) + tol
    m = 0.5 * (c - b)

    # Initialize iteration and procedure stack
    iterations = 0
    procedure_stack = []

    # Repeat until the tolerance level is met or max iterations is reached
    while abs(m) > tolerance and fb and iterations < stop_iters:
        # Calculate next step
        # =============================================================================================================
        # Check if bisection is forced
        if abs(e) < tolerance or abs(fa) <= abs(fb):
            d = m
            e = m
            procedure_stack.append("Bisection")
        else:
            # Calculate the ratio of fb and fa
            s = fb / fa
            if a == c:
                # Use linear interpolation
                p = 2 * m * s
                q = 1 - s
            else:
                # Use inverse quadratic interpolation
                q = fa / fc
                r = fb / fc
                p = s * (2 * m * q * (q - r) - (b - a) * (r - 1))
                q = (q - 1) * (r - 1) * (s - 1)

            # Correct the sign of p and q
            if p > 0:
                q = -q
            else:
                p = -p

            s = e
            e = d

            # Validate the interpolation
            if 2 * p < 3 * m * q - abs(tolerance * q) and p < abs(0.5 * s * q):
                # The interpolation is valid
                d = p / q
                procedure_stack.append("IQI" if a != c else "Secant")
            else:
                # The interpolation is not valid, we use bisection
                d = m
                e = m
                procedure_stack.append("Bisection")
        a = b
        fa = fb

        b += d if abs(d) > tolerance else np.sign(m) * tolerance
        fb = f(b, *args)
        # =============================================================================================================

        # Update interval
        # =============================================================================================================
        # Correct points accordingly
        if np.sign(fb) == np.sign(fc) != 0:
            # Section: int
            c, fc, d, e = a, fa, b - a, b - a
        # Section: ext
        elif abs(fc) < abs(fb):
            a, b, c, fa, fb, fc = b, c, b, fb, fc, fb

        # Update tolerance and m for the next iteration
        tolerance = 2 * np.finfo(float).eps * abs(b) + tol
        m = 0.5 * (c - b)

        iterations += 1

    zero = b
    if steps and iters:
        return zero, iterations, procedure_stack
    if iters:
        return zero, iterations
    if steps:
        return zero, procedure_stack
    return zero
