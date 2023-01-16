import numpy as np
from ..Interpolation import polinomial, piecewise_linear, pchip, splines
from bqplot import pyplot as plt
import ipywidgets as widgets
import bqplot as bq


class InterpolVisualizer:
    def __init__(
        self,
        xInitial=list(np.arange(1, 7, 1).astype(float)),
        yInitial=[16, 18, 21, 17, 15, 12],
        uInitial=list(np.arange(1, 6.1, 0.1)),
    ) -> None:
        """
        Initializes the Class

        Parameters:
            - xInitial: Initial x coordinates
            - yInitial: Initial y coordinates
            - uInitial: Initial mesh
        """
        if len(xInitial) != len(yInitial):
            raise ValueError("The length of the X and Y coordinates must be the same")

        self.x = np.array(xInitial).astype(float)
        self.y = np.array(yInitial).astype(float)
        self.u = np.array(uInitial).astype(float)

        self.Originals = [self.x, self.y, self.u]

        self.methods = {
            "InterPoly": [polinomial, "blue"],
            "Piecewise Linear": [piecewise_linear, "green"],
            "Pchip": [pchip, "orange"],
            "Splines": [splines, "purple"],
        }

    def initializeComponents(self):
        """
        Initializes the components of the GUI
        Components:
            - Checkboxes
                Checkboxes for each interpolation method
            - Slider
                Slider for the mesh size
            - Reset Button
                Button to reset the points
        """

        """
        Checkboxes
        ======================
        One checkbox for every possible interpolation method
        Every checkbox will be associated with a method called update_checkboxes that will update the plot according to the updated checkboxes. 
        Additionally, the checkbox will have the same color as the color of associated interpolation method
        """
        self.checkboxes = []
        for key, val in self.methods.items():
            checkbox = widgets.Checkbox(
                description=key, value=True, style={"background-color": val[1]}
            )
            checkbox.observe(self.update_checkboxes, "value")
            checkbox.background_color = val[1]
            # Change background color
            checkbox.style.handle_color = val[1]

            self.methods[key].append(checkbox)
            self.checkboxes.append(checkbox)

        """
        Reset button
        ======================
        Button to reset the points to the original ones, linked to the method reset
        """
        self.reset_button = widgets.Button(
            description="Reset", button_style="danger", tooltip="Reset", icon="undo"
        )
        self.reset_button.on_click(self.reset)

        """
        Range slider
        ======================
        Slider to change the mesh size, linked to the method update_Mesh, with a default minimum of the minimum of the original points - 0.5*(max-min) 
        and a default maximum of the maximum of the original points + 0.5*(max-min).
        """
        values = [min(self.x), max(self.x)]
        self.slider = widgets.FloatRangeSlider(
            value=values,
            min=values[0] - (values[1] - values[0]) / 2,
            max=values[1] + (values[1] - values[0]) / 2,
            step=0.1,
            description="Mesh:",
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format=".1f",
        )
        self.slider.observe(self.update_Mesh, "value")

        """
        Auto Zoom button
        ======================
        Button to auto zoom the plot, linked to the method auto_zoom
        """
        self.auto_zoom_button = widgets.Button(
            description="Auto Zoom",
            button_style="info",
            tooltip="Auto Zoom",
            icon="search-plus",
        )
        self.auto_zoom_button.on_click(self.auto_zoom)

    def auto_zoom(self, change):
        """
        Auto zooms the plot
        """

        self.x_sc.min = min(self.u)
        self.x_sc.max = max(self.u)
        yVals = [j for line in self.interpolationLines for j in line.y]
        if len(yVals) != 0:
            self.y_sc.min = min(yVals)
            self.y_sc.max = max(yVals)

    def scatterDots(self):
        """
        Updates ScatteredDots - the scatter plot of the data - according to the new points
        It observers the changes in the x and y coordinates of the scatter plot and links them to the update_X and update_Y methods
        It also lets adding new points
        """
        self.ScatteredDots = bq.Scatter(
            x=self.x,
            y=self.y,
            scales={"x": self.x_sc, "y": self.y_sc},
            colors=["red"],
            name="Points",
            enable_move=True,
            enable_add=False,
            display_legend=False,
            labels=["Points"],
        )

        # observe change XY
        self.ScatteredDots.observe(self.update_X, "x")
        self.ScatteredDots.observe(self.update_Y, "y")
        self.ScatteredDots.interactions = {"click": "add"}

    def interpolLines(self):
        """
        Updates the interpolation lines according to the new points
        It creates an array of Lines for every interpolation method that is checked in the checkboxes
        """
        self.interpolationLines = [
            bq.Lines(
                x=self.u,
                y=val[0](self.x, self.y, self.u),
                scales={"x": self.x_sc, "y": self.y_sc},
                colors=[val[1]],
                name=key,
                display_legend=False,
                labels=[key],
                enable_move=False,
                enable_add=False,
            )
            for key, val in self.methods.items()
            if val[2].value
        ]

    def update_X(self, change):
        """
        Updates the x coordinates and the plot according to the new x coordinates if the change is not None and does not contain Repetitions (Definition of a function)
        It also updates the slider according to the new x coordinates

        This method will always be called when the x coordinates are changed and before the y coordinates are changed.
        """
        self.x = (
            change["new"]
            if change is not None
            and change["name"] == "x"
            and len(list(change["new"])) == len(set(change["new"]))
            else self.x
        )

        self.slider.min = min(self.x) - (max(self.x) - min(self.x)) / 2
        self.slider.max = max(self.x) + (max(self.x) - min(self.x)) / 2

    def update_Y(self, change):
        """
        Updates the y coordinates and the plot according to the new y coordinates if the change is not None and contains the same number of points as X
        It makes new scattering and inteprolation lines and updates the plot.
        Also, it updates Scales and Axes according to the new points

        This method will always be called when the y coordinates are changed and after the x coordinates are changed.
        """

        with self.widgetsgrid.hold_sync():

            self.y = (
                change["new"]
                if change is not None
                and change["name"] == "y"
                and len(list(change["new"])) == len(self.x)
                else self.y
            )

            self.scatterDots()
            self.interpolLines()

            toUpdate = [*self.interpolationLines, self.ScatteredDots]

            self.Fig.marks = toUpdate

            # Update Scales and Axes

            # yVals = [j for line in self.interpolationLines for j in line.y]
            # if len(yVals) != 0:
            # self.y_sc.min = min(yVals)
            # self.y_sc.max = max(yVals)

    def update_Mesh(self, change):
        """
        Updates the mesh and the plot according to the new mesh
        """
        minX = min(self.x)
        maxX = max(self.x)
        leftX = change["new"][0] if (change["new"][0]) < minX else minX
        rightX = change["new"][1] if (change["new"][1]) > maxX else maxX

        self.u = np.linspace(leftX, rightX, 100)
        self.slider.value = [leftX, rightX]

        self.update_X(None)
        self.update_Y(None)

        # Reset X scale
        # self.x_sc.min = min(self.u)
        # self.x_sc.max = max(self.u)

    def update_checkboxes(self, change):
        """
        Updates the plot according to the new checkboxes
        """
        self.update_X(None)
        self.update_Y(None)

    def reset(self, b):
        """
        Resets everything to what it was at the beginning of the program
        """
        self.x = self.Originals[0]
        self.y = self.Originals[1]
        self.u = self.Originals[2]

        values = [min(self.x), max(self.x)]
        self.u = np.linspace(values[0], values[1], 100)

        self.update_X(None)
        self.update_Y(None)

        # Reset Y scale
        self.y_sc.min = min(self.y)
        self.y_sc.max = max(self.y)

        # Reset X scale
        self.x_sc.min = min(self.x)
        self.x_sc.max = max(self.x)

    def run(self):
        """
        Runner method : Creates all the widgets and displays the plot with a given layout
        """
        self.x_sc = bq.LinearScale(stabilize=True)
        self.y_sc = bq.LinearScale(stabilize=True)
        ax_x = bq.Axis(scale=self.x_sc, grid_lines="solid", label="X")
        ax_y = bq.Axis(
            scale=self.y_sc,
            orientation="vertical",
            tick_format="0.2f",
            grid_lines="solid",
            label="Y",
        )

        self.initializeComponents()
        self.interpolLines()
        self.scatterDots()

        # Reset Y scale
        self.y_sc.min = min(self.y)
        self.y_sc.max = max(self.y)

        # Reset X scale
        self.x_sc.min = min(self.x)
        self.x_sc.max = max(self.x)

        self.Fig = bq.Figure(
            marks=[*self.interpolationLines, self.ScatteredDots],
            axes=[ax_x, ax_y],
            title="Interpolation Visualizer",
            legend_location="top-right",
            animation_duration=1000,
        )

        self.Toolbar = bq.Toolbar(figure=self.Fig)

        self.checkboxesVbox = widgets.VBox(
            [
                widgets.HBox(
                    [
                        widgets.Button(
                            description="",
                            style={"button_color": i.background_color},
                            disabled=True,
                            layout=widgets.Layout(width="20px"),
                        ),
                        i,
                    ]
                )
                for i in self.checkboxes
            ]  # BUTTON + CHECKBOX PAIR -- Fake Legend
        )
        tools = widgets.VBox(
            [
                self.checkboxesVbox,
                self.slider,
                widgets.HBox([self.reset_button, self.auto_zoom_button]),
            ]
        )

        self.widgetsgrid = widgets.GridspecLayout(11, 7)

        self.widgetsgrid[0, :] = self.Toolbar
        self.widgetsgrid[1:, :4] = self.Fig
        self.widgetsgrid[1:, 4:] = tools

        return self.widgetsgrid
