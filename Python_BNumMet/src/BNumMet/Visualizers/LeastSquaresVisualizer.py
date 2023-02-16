import numpy as np
from bqplot import pyplot as plt
import ipywidgets as widgets
import bqplot as bq
from ..LinearSystems import qr_solve


class LSPVisualizer:
    """
    Visualizer for the least squares method with the examples of
        * Exponential function
        * Polynomial function
        * Sine and Cosine functions
    """

    def __init__(
        self, x_data_lsp=np.array([0, 1, 2, 3]), y_data_lsp=np.array([4.5, 2.4, 1.5, 1])
    ):
        if len(x_data_lsp) != len(y_data_lsp):
            raise ValueError("x_data_lsp and y_data_lsp must have the same length")
        if len(x_data_lsp) < 2:
            raise ValueError(
                "x_data_lsp and y_data_lsp must have at least 2 points... Too boring otherwise"
            )
        self.x_data_lsp = np.array(x_data_lsp, dtype=np.float64)
        self.y_data_lsp = np.array(y_data_lsp, dtype=np.float64)

        min_max_xdata = np.min(self.x_data_lsp), np.max(self.x_data_lsp)
        self.x = np.linspace(
            np.min(x_data_lsp) - 0.2 * (min_max_xdata[1] - min_max_xdata[0]),  # min x
            np.max(x_data_lsp) + 0.2 * (min_max_xdata[1] - min_max_xdata[0]),  # max x
            1000,  # number of points
        )  # for plotting the fitted curve

    def initialize_components(self):
        # 1. Dropdown for selecting the function type
        self.function_type = widgets.Dropdown(  #
            options=["Only data", "Polynomial", "Exponential", "Sines & Cosines"],
            value="Only data",
            description="Function:",
            disabled=False,
        )
        self.function_type.observe(self.selector_function, names="value")
        # 2. Int text for selecting the polynomial degree
        self.polynomial_degree = widgets.BoundedIntText(
            value=1,
            description="Degree:",
            disabled=False,
            # make smaller width
            layout=widgets.Layout(width="75%"),
            min=0,
        )
        self.polynomial_degree.observe(self.degree_change_poly, names="value")
        # 3. Int text for selecting the number of sines and cosines
        self.sine_cosine_degree = widgets.BoundedIntText(
            value=1,
            description="Sines & Cosines degree:",
            disabled=False,
            min=0,
        )
        self.sine_cosine_degree.observe(self.degree_change_sine_cosine, names="value")

        # 4. Checkbox for Error Bound Visualization
        self.error_bound = widgets.Checkbox(
            value=False,
            description="Error Bound",
            disabled=False,
        )

        # 5. Remarks about LSP output Math
        self.remarks = widgets.HTMLMath(
            value="",
            placeholder="LSP Remarks",
            description="Remarks:",
        )

        # 6. Figure
        self.x_sc = bq.LinearScale()  # x scale
        self.y_sc = bq.LinearScale()  # y scale
        ax_x = bq.Axis(scale=self.x_sc, grid_lines="solid", label="X")
        ax_y = bq.Axis(
            scale=self.y_sc,
            orientation="vertical",
            tick_format="0.4e",
            grid_lines="solid",
            label="Y",
        )
        # Set up the plot figure
        self.fig = bq.Figure(
            marks=[],
            axes=[ax_x, ax_y],
            title="Least Squares Method",
        )

        self.grid = widgets.GridspecLayout(4, 4)
        self.grid[:, 0:2] = self.fig
        self.grid[0:2, 2:] = widgets.VBox([self.function_type])
        # self.grid[1, 3] --> self.errorBound
        self.grid[2:, 2:] = self.remarks

        # Plot the data (Since it will be the same for all the functions)
        points = bq.Scatter(
            x=self.x_data_lsp,
            y=self.y_data_lsp,
            scales={"x": self.x_sc, "y": self.y_sc},
        )
        self.fig.marks = [points]

    def degree_change_poly(self, change):
        """
        This function is called when the polynomial degree is changed
        """
        curve, c, err = self.polynomial_lsp(change["new"])
        self.fig.marks = [self.fig.marks[0], curve]
        self.polynomial_remarks(c, err)

    def degree_change_sine_cosine(self, change):
        """
        This function is called when the sine and cosine degree is changed
        """
        curve, c, err = self.sine_cosine_lsp(change["new"])
        self.fig.marks = [self.fig.marks[0], curve]
        self.sine_cosine_remarks(c, err)

    def selector_function(self, change):
        """
        This function is called when the function type is changed
        """
        to_draw = [self.fig.marks[0]]
        to_grid = [self.function_type]
        if change["new"] == "Only data":
            ...
        elif change["new"] == "Polynomial":
            to_grid.append(self.polynomial_degree)
            self.polynomial_degree.max = (
                len(self.x_data_lsp) - 1
            )  # max degree is number of data points - 1
            curve, c, err = self.polynomial_lsp(self.polynomial_degree.value)
            to_draw.append(curve)
            self.polynomial_remarks(c, err)

        elif change["new"] == "Exponential":
            curve, c, err = self.exponential_lsp()
            to_draw.append(curve)
            self.exponential_remarks(c, err)

        elif change["new"] == "Sines & Cosines":
            to_grid.append(self.sine_cosine_degree)
            self.sine_cosine_degree.max = (
                len(self.x_data_lsp) - 1
            ) // 2  # max degree is half the number of data points - 1
            curve, c, err = self.sine_cosine_lsp(self.sine_cosine_degree.value)
            to_draw.append(curve)
            self.sine_cosine_remarks(c, err)

        with self.fig.hold_sync():
            self.fig.marks = to_draw
            self.grid[0:2, 2:] = widgets.VBox(to_grid)

    def exponential_lsp(self):
        """
        This function returns the exponential function that best fits the data Using LSP

        Returns
        -------
        curve : bqplot.Lines
            The curve that best fits the data
        a : float
            The coefficient of the exponential function
        b : float
            The coefficient of the exponential function
        """
        # Create the A matrix
        A = np.ones((len(self.x_data_lsp), 2))
        A[:, 1] = self.x_data_lsp
        # Solve the system
        c = qr_solve(A, np.log(self.y_data_lsp))

        # Revert the log on c[0]
        c[0] = np.exp(c[0])

        # Plot the curve
        # Evaluate the exponential function
        y = c[0] * np.exp(c[1] * self.x)
        # Plot the curve
        curve = bq.Lines(
            x=self.x,
            y=y,
            scales={"x": self.x_sc, "y": self.y_sc},
        )

        err = np.linalg.norm(
            np.log(self.y_data_lsp) - A @ np.array([np.log(c[0]), c[1]]), 2
        )

        return curve, c, err

    def exponential_remarks(self, c, err):
        """
        This function updates the remarks section of the widget

        Parameters
        ----------
        c : np.array
            The coefficients of the exponential function in the form of c[0]*x^c[1]
        """
        self.remarks.value = f"The exponential function that best fits the data is: <br>$y = {c[0]:.4f}e^{{{c[1]:.4f}x}}$ <br><br> The coefficients of the exponential function are: <br>$c_0 = {c[0]:.4f}$ <br>$c_1 = {c[1]:.4f}$ <br><br> The error is: {err:.4f}$"

    def polynomial_lsp(self, degree):
        """
        This function returns the polynomial function of the given degree that best fits the data Using LSP

        Parameters
        ----------
        degree : int
            The degree of the polynomial function

        Returns
        -------
        curve : bqplot.Lines
            The curve that best fits the data
        c : np.array
            The coefficients of the polynomial function in the form of c[0] + c[1]*x + c[2]*x^2 + ... + c[degree]*x^degree
        """
        # Create the A matrix
        A = np.zeros((len(self.x_data_lsp), degree + 1))
        for i in range(degree + 1):
            A[:, i] = self.x_data_lsp**i
        # Solve the system
        c = qr_solve(A, self.y_data_lsp)
        # Plot the curve
        # Evaluate the polynomial function
        y = np.array(
            [np.sum([c[i] * x**i for i in range(degree + 1)]) for x in self.x]
        )
        # Plot the curve
        curve = bq.Lines(
            x=self.x,
            y=y,
            scales={"x": self.x_sc, "y": self.y_sc},
        )

        err = np.linalg.norm(self.y_data_lsp - A @ c)

        return curve, c, err

    def polynomial_remarks(self, c, err):
        """
        This function returns the remarks for the polynomial function

        Parameters
        ----------
        c : np.array
            The coefficients of the polynomial function in the form of c[0] + c[1]*x + c[2]*x^2 + ... + c[degree]*x^degree

        Returns
        -------
        remarks : str
            The remarks for the polynomial function
        """

        # Create the remarks
        remarks = "The polynomial function is:<br> $"

        for i in range(len(c)):
            if i == 0:
                remarks += f"{c[i]:.2f}"
            elif i == 1:
                remarks += "+" if np.sign(c[i]) >= 0 else "" + f"{c[i]:.2f}x"
            else:
                remarks += "+" if np.sign(c[i]) >= 0 else "" + f"{c[i]:.2f}x^{i}"

        remarks += "$ <br><br> The coefficients of the polynomial function are: <br> "

        for i in range(len(c)):
            remarks += f"$c_{i} = {c[i]:.2f}$<br> "

        remarks += f"<br> The error is {err:.4f}"

        self.remarks.value = remarks

    def sine_cosine_lsp(self, degree):
        """
        This function returns the sine and cosine function of the given degree that best fits the data Using LSP

        Parameters
        ----------
        degree : int
            The degree of the sine and cosine function

        Returns
        -------
        curve : bqplot.Lines
            The curve that best fits the data
        c : np.array
            The coefficients of the sine and cosine function in the form of c[0] + c[1]*sin(x) + c[2]*cos(x) + ... + c[degree]*sin(degree*x) + c[degree+1]*cos(degree*x)
        """
        # Create the A matrix
        A = np.ones((len(self.x_data_lsp), 2 * degree + 1))
        for i in range(1, degree + 1):
            A[:, 2 * i - 1] = np.sin(i * self.x_data_lsp)
            A[:, 2 * i] = np.cos(i * self.x_data_lsp)
        # Solve the system
        c = qr_solve(A, self.y_data_lsp)
        # Plot the curve
        # Evaluate the sine and cosine function
        y = np.array(
            [
                np.sum(
                    [
                        c[i] * np.sin(i * x) + c[i + 1] * np.cos(i * x)
                        for i in range(1, degree + 1)
                    ]
                )
                + c[0]
                for x in self.x
            ]
        )
        # Plot the curve
        curve = bq.Lines(
            x=self.x,
            y=y,
            scales={"x": self.x_sc, "y": self.y_sc},
        )

        err = np.linalg.norm(self.y_data_lsp - A @ c)

        return curve, c, err

    def sine_cosine_remarks(self, c, err):
        """
        This function returns the remarks for the sine and cosine function

        Parameters
        ----------
        c : np.array
            The coefficients of the sine and cosine function in the form of c[0] + c[1]*sin(x) + c[2]*cos(x) + ... + c[degree]*sin(degree*x) + c[degree+1]*cos(degree*x)

        Returns
        -------
        remarks : str
            The remarks for the sine and cosine function
        """

        # Create the remarks
        remarks = "The sine and cosine function is:<br> $"
        # first coefficient
        remarks += f"{c[0]:.2f}"

        for i in range(1, len(c) // 2 + 1):
            remarks += "+" if np.sign(c[2 * i - 1]) >= 0 else ""
            remarks += f"{c[2*i - 1]:.2f}\sin({i}x)"
            remarks += "+" if np.sign(c[2 * i]) >= 0 else ""
            remarks += f"{c[2*i]:.2f}\cos({i}x)"

        remarks += (
            "$ <br><br> The coefficients of the sine and cosine function are: <br> "
        )

        for i in range(len(c)):
            remarks += f"$c_{i} = {c[i]:.2f}$ <br>"

        remarks += f"<br> The error is: {err:.4f}"

        self.remarks.value = remarks

    def run(self):
        self.initialize_components()

        return self.grid
