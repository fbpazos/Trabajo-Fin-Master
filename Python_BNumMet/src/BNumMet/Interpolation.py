import numpy as np


def polinomial(x, y, u):
    """
    Computes the polynomial interpolation of a set of points (x,y) at the points u

    params:
        x: list of x coordinates
        y: list of y coordinates
        u: list of points where the interpolation is computed

    returns:
        v: list of values of the interpolation at the points u
    """
    n = len(x)
    v = np.zeros(
        len(u)
    )  # Create a vector of zeros of the same size as u, to store the result
    for i in range(n):
        w = np.ones(len(u))
        for j in range(n):
            if j != i:
                w *= (u - x[j]) / (x[i] - x[j])
        v += w * y[i]

    return v


def piecewise_linear(x, y, u, sorted=False):
    """
    Computes the piecewise lineal interpolation of a set of points (x,y) at the points u, (x,y) ACCORDING TO THE ALGORITHM IN THE BOOK

    params:
        x: list of x coordinates
        y: list of y coordinates
        u: list of points where the interpolation is computed
        sorted (optional): if the points are sorted or not (default: False)

    returns:
        v: list of values of the interpolation at the points u
    """
    if not sorted:
        # Sort the points
        x = np.array(x)
        y = np.array(y)
        ind = np.argsort(x)  # Get the indices of the sorted array
        x = x[ind]  # Sort the x coordinates
        y = y[ind]  # Sort the y coordinates

    delta = np.diff(y) / np.diff(
        x
    )  # Compute the slopes of the lines -- here we are using the fact that x is sorted
    n = len(x)

    k = np.ones(len(u)).astype(
        int
    )  # Create a vector of ones of the same size as u, to store the result
    for i in range(1, n):
        k[x[i - 1] <= u] = int(
            i
        )  # Find the index of the points in u that are between x[i] and x[i+1] and store the index in k

    s = [
        u[i] - x[k[i] - 1] for i in range(len(u))
    ]  # Compute the distance between the points in u and the points in x that are between x[i] and x[i+1]

    v = [
        y[k[i] - 1] + s[i] * delta[k[i] - 1] for i in range(len(u))
    ]  # Compute the value of the interpolation at the points in u

    return v


def pchip(x, y, u, sorted=False):
    """
    Piecewise Cubic Hermite Interpolation Polynomial (P.C.H.I.P.) [Based on an old Fortran program by Fritsch and Carlson]

        params:
            x: list of x coordinates
            y: list of y coordinates
            u: list of points where the interpolation is computed
            sorted (optional): if the points are sorted or not (default: False)

        returns:
            v: list of values of the interpolation at the points u
    """

    def pchip_end(h1, h2, delta1, delta2):
        """
        Computes the slopes at the end points of the interval

        params:
            h1: distance between the first two points
            h2: distance between the last two points
            delta1: slope between the first two points
            delta2: slope between the last two points

        returns:
            d1: slope at the first point
            d2: slope at the last point
        """
        # Noncentered, shape-preserving, three-point formula.
        d = ((2 * h1 + h2) * delta1 - h1 * delta2) / (h1 + h2)
        # If slopes of the secant lines are of different sign or If the slopes are not of the same magnitude, use 0.
        if (
            np.sign(delta1) != np.sign(delta2)
            or np.abs(d) > np.abs(3 * delta1)
            or np.abs(d) > np.abs(3 * delta2)
        ):
            d = 0

        return d

    def pchip_slopes(h, delta):
        """
        Slopes for shape-preserving Hermite cubic, computes the slopes
            - Interior Points
                * d(k) = 0 <- delta(k-1) && delta(k) different signs or both are 0
                * d(k) = Weighted Harmonic Mean <- Same sign delta(k-1) && delta (k)
            - EndPoints
                Call pchip end :)

        params:
            h: list of distances between points
            delta: list of slopes between points

        returns:
            d: list of slopes for the Hermite cubic
        """
        d = np.zeros(len(h))

        k = np.where(np.sign(delta[0:-1]) * np.sign(delta[1:]) > 0)[
            0
        ]  # Find the indices of the points where the slopes are of the same sign
        k = k + 1  # Add 1 to the indices to get the indices of the slopes

        w1 = 2 * h[k] + h[k - 1]
        w2 = h[k] + 2 * h[k - 1]
        d[k] = (w1 + w2) / (
            w1 / delta[k - 1] + w2 / delta[k]
        )  # Compute the slopes of the lines

        # end points
        d[0] = pchip_end(h[0], h[1], delta[0], delta[1])

        d = np.append(d, pchip_end(h[-2], h[-3], delta[-2], delta[-3]))

        return d

    # Sort the points
    x = np.array(x)
    y = np.array(y)
    if not sorted:
        ind = np.argsort(x)  # Get the indices of the sorted array
        x = x[ind]  # Sort the x coordinates
        y = y[ind]  # Sort the y coordinates

    # First derivative
    h = np.diff(x)
    delta = np.diff(y) / h

    d = pchip_slopes(h, delta)

    n = len(x)
    c = (3 * delta - 2 * d[:-1] - d[1:]) / (h)
    b = (d[:-1] - 2 * delta + d[1:]) / (h**2)

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
        y[k[i] - 1] + s[i] * (d[k[i] - 1] + s[i] * (c[k[i] - 1] + s[i] * b[k[i] - 1]))
        for i in range(len(u))
    ]  # Compute the value of the interpolation at the points in u

    return v


def splitnetx(x, y, u, sorted=False):
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

        res = np.linalg.solve(np.diag(a, -1) + np.diag(b) + np.diag(c, 1), r)

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
        y[k[i] - 1] + s[i] * (d[k[i] - 1] + s[i] * (c[k[i] - 1] + s[i] * b[k[i] - 1]))
        for i in range(len(u))
    ]  # Compute the value of the interpolation at the points in u

    return v
