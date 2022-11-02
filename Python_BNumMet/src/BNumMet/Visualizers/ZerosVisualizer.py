import bqplot as bq
import numpy as np
from ipywidgets import widgets


class ZerosVisualizer:
    def __init__(self, fun, interval):
        self.f = fun
        self.x0, self.x1 = interval
        self.xn = self.x0

        self.f0 = self.f(self.x0)
        self.f1 = self.f(self.x1)
        self.fn = self.f(self.xn)

        if self.f0 * self.f1 > 0:
            raise ValueError("The function has no zeros in the given interval")

        self.e = self.x1 - self.x0

        self.iterations = 0

        self.previousPoints = []
        self.OrignalPoints = (self.x0, self.x1, self.xn)

    def initializeComponents(self):
        # WIDGETS
        # ==========================================================================
        ## Output Widgets
        self.currentSolOut = widgets.Output()  # Current Solution: <x1>
        # Value: <f1>
        # Iterations: <iterations>
        self.helperOut = widgets.Output()  # Next Possible Step: <Bisect/IQI/None>

        ## Button Widgets
        self.resetButton = widgets.Button(
            description="Reset",
            disabled=False,
            button_style="danger",
            tooltip="Reset",
            icon="undo",
        )
        self.resetButton.on_click(self.reset)

        self.revertButton = widgets.Button(
            description="Revert",
            disable=False,
            button_style="warning",
            tooltip="Revert",
            icon="arrow-left",
        )
        self.revertButton.on_click(self.revert)

        # FIGURE
        # ==========================================================================
        self.x_sc = bq.LinearScale()
        self.y_sc = bq.LinearScale()
        ax_x = bq.Axis(scale=self.x_sc, grid_lines="solid", label="X")
        ax_y = bq.Axis(
            scale=self.y_sc,
            orientation="vertical",
            tick_format="0.2f",
            grid_lines="solid",
            label="Y",
        )

        self.Fig = bq.Figure(
            marks=[],
            axes=[ax_x, ax_y],
            title="Zeros of a Function",
            # legend_location="top-right",
            animation_duration=1000,
        )

        # GRID
        # ==========================================================================
        self.grid = widgets.GridspecLayout(3, 3)
        self.grid[:2, :2] = self.Fig
        self.grid[0, 2] = self.currentSolOut
        self.grid[1, 2] = self.helperOut
        self.grid[2, 2] = widgets.HBox([self.resetButton, self.revertButton])

    def reset(self, *args):
        self.x0, self.x1 = self.OrignalPoints[:2]
        self.xn = self.OrignalPoints[2]
        self.f0 = self.f(self.x0)
        self.f1 = self.f(self.x1)
        self.fn = self.f(self.xn)
        self.e = self.x1 - self.x0
        self.iterations = 0
        self.previousPoints = []
        self.newPoints()
        with self.grid.hold_sync():
            self.updateOutputWidgets()
            self.update()

    def revert(self, *args):
        if len(self.previousPoints) > 0:
            self.x0, self.x1, self.xn = self.previousPoints.pop()
            self.xn = self.x0
            self.f0 = self.f(self.x0)
            self.f1 = self.f(self.x1)
            self.fn = self.f(self.xn)
            self.e = self.x1 - self.x0
            self.iterations -= 1
            self.newPoints()
            with self.grid.hold_sync():
                self.updateOutputWidgets()
                self.update()

    def fixPoints(self):
        if np.sign(self.f0) == np.sign(self.f1):
            self.x0 = self.xn
            self.f0 = self.fn
            self.e = self.x1 - self.xn
        elif np.sign(self.f0) < np.sign(self.f1):
            self.x0, self.x1, self.xn = self.x1, self.x0, self.x1
            self.f0, self.f1, self.fn = self.f1, self.f0, self.f1

    def newPoints(self) -> list:
        self.nextPoints = [None, None]

        m = 0.5 * (self.x0 - self.x1)
        self.tol = 2 * np.finfo(float).eps * max(abs(self.x1), 1)
        if abs(m) < self.tol or np.isclose(self.f1, 0):
            return self.nextPoints

        # BISECTION
        self.nextPoints[0] = self.x1 + m

        # IQI
        self.nextPoints[1] = self.x1 + self.IQI_Step()

        return self.nextPoints

    def nextStep(self):
        return "Bisect" if self.e < self.tol or abs(self.fn) < abs(self.f1) else "IQI"

    def updateOutputWidgets(self):
        self.currentSolOut.clear_output()
        with self.currentSolOut:
            print(
                f"Curent Solution: {self.x1}\nValue: {self.f1}\nIterations: {self.iterations}"
            )
        self.helperOut.clear_output()
        with self.helperOut:
            if all(v is not None for v in self.nextPoints):
                print(f"Next Possible Step: {self.nextStep()}")
            else:
                print("Next Possible Step: None - Already at a Solution")

    def functionPlot(self, x, y, name, color, line_style, display_legend=True):
        return bq.Lines(
            x=x,
            y=y,
            scales={"x": self.x_sc, "y": self.y_sc},
            colors=[color],
            display_legend=display_legend,
            labels=[name],
            enable_move=False,
            enable_add=False,
            line_style=line_style,
        )

    def dotsPlot(
        self, x, y, name, color, marker, clicker=False, val=None, display_legend=True
    ):
        dots = bq.Scatter(
            x=x,
            y=y,
            scales={"x": self.x_sc, "y": self.y_sc},
            colors=[color],
            display_legend=display_legend,
            labels=name,
            enable_move=False,
            enable_add=False,
            marker=marker,
        )
        if clicker:
            dots.val = val
            dots.on_element_click(self.selectPoint)
        return dots

    def selectPoint(self, b, *args):
        if self.nextPoints[b.val] is None:
            return

        self.previousPoints.append((self.x0, self.x1, self.xn))
        self.xn = self.x1
        self.fn = self.f1
        self.x1 = self.nextPoints[b.val]
        self.f1 = self.f(self.x1)
        self.fixPoints()
        self.iterations += 1
        newPoints = self.newPoints()
        with self.grid.hold_sync():
            self.updateOutputWidgets()
            self.update()

    def update(self):
        """
        This function plots everything accordingly to the values inside this class (it does not generate any more points)

        Considerations
            1. If the difference between self.x0 and self.x1 is smaller than 1, we "zoom in" the plot (Original Points not to be plotted)
            2. Else we plot also de original Points and zoom out (X Axis) according to the min/max of all posible points (even the new ones)

        """
        toPlot = []

        # ADJUST AXES
        # ==========================================================================
        toCheck = (
            [self.x0, self.x1] + [self.nextPoints[0], self.nextPoints[1]]
            if all(v is not None for v in self.nextPoints)
            else [self.OrignalPoints[0], self.OrignalPoints[1]]
        )
        self.x_sc.min = min(toCheck)
        self.x_sc.max = max(toCheck)
        if abs(self.x0 - self.x1) > 1:
            self.x_sc.min = min(
                self.x_sc.min, self.OrignalPoints[0], self.OrignalPoints[1]
            )
            self.x_sc.max = max(
                self.x_sc.min, self.OrignalPoints[0], self.OrignalPoints[1]
            )

        # Horizontal Line
        # ==========================================================================
        x = [self.x_sc.min, self.x_sc.max]
        y = [0, 0]
        toPlot.append(self.functionPlot(x, y, "Horizontal Line", "#808080", "solid"))

        # PLOT FUNCTION
        # ==========================================================================
        x = np.linspace(self.x_sc.min, self.x_sc.max, 100)
        y = self.f(x)
        toPlot += [self.functionPlot(x, y, "Real Function", "#808080", "dashed")]
        self.y_sc.min = min(y)
        self.y_sc.max = max(y)

        # PLOT ORIGINAL POINTS
        # ==========================================================================
        x = [self.OrignalPoints[0], self.OrignalPoints[1]]
        y = [self.f(x[0]), self.f(x[1])]
        toPlot += [
            self.dotsPlot(x=x, y=y, name="OriginalPoints", color="red", marker="circle")
        ]

        if all(
            v is not None for v in self.nextPoints
        ):  # If there are new points to plot

            # PLOT CURRENT POINTS
            # ==========================================================================
            x = [self.x0, self.x1]
            y = [self.f0, self.f1]
            toPlot += [
                self.dotsPlot(
                    x=x, y=y, name="Current Points", color="black", marker="cross"
                )
            ]
            # PLOT NEW POINTS
            # ==========================================================================
            ## BISECTION
            x = [self.nextPoints[0]]
            y = [0]
            toPlot += [
                self.dotsPlot(
                    x=x,
                    y=y,
                    name="Bisection",
                    color="blue",
                    marker="diamond",
                    clicker=True,
                    val=0,
                )
            ]
            ## IQI
            x = [self.nextPoints[1]]
            y = [0]
            toPlot += [
                self.dotsPlot(
                    x=x,
                    y=y,
                    name="IQI",
                    color="green",
                    marker="rectangle",
                    clicker=True,
                    val=1,
                )
            ]
        else:
            # PLOT SOLUTION
            # ==========================================================================
            x = [self.x1]
            y = [0]
            toPlot += [
                self.dotsPlot(
                    x=x,
                    y=y,
                    name="Solution",
                    color="black",
                    marker="circle",
                    display_legend=True,
                )
            ]

        self.Fig.marks = toPlot

    def run(self):
        self.fixPoints()
        self.initializeComponents()
        aux = self.newPoints()
        with self.grid.hold_sync():
            self.updateOutputWidgets()
            self.update()

        return self.grid

    def IQI_Step(self):
        # Interpolation
        m = 0.5 * (self.x0 - self.x1)
        s = self.f1 / self.fn
        if self.x0 == self.xn:
            # Linear interpolation
            p = 2.0 * m * s
            q = 1.0 - s
        else:
            # Inverse quadratic interpolation
            q = self.fn / self.f0
            r = self.f1 / self.f0
            p = s * (2.0 * m * q * (q - r) - (self.x1 - self.xn) * (r - 1.0))
            q = (q - 1.0) * (r - 1.0) * (s - 1.0)

        if p > 0.0:
            q = -q
        else:
            p = -p
        # Is interpolated point acceptable?

        d = p / q if not np.isclose(q, 0) else m

        return d
