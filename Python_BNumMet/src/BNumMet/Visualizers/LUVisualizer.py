import numpy as np
import ipywidgets as widgets
from IPython.display import display, Math
from ..LinearSystems import interactive_lu


class LUVisualizer:
    def __init__(self, matrix=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)):
        """
        Parameters
        ----------
        matrix : numpy.ndarray
            Matrix to be decomposed (must be square)

        Returns
        -------
        None

        Exceptions
        ----------
        ValueError
            If the matrix is not square
        """
        self.A = np.array(matrix, dtype=float)
        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError("Matrix must be square")
        self.step = 0
        self.L = np.eye(self.A.shape[0])
        self.U = self.A.copy()
        self.P = np.eye(self.A.shape[0])

        # Stack for previous steps
        self.previousSteps = []

    def initializeComponents(self):
        """
        Initialize the components of the visualizer (Output, Buttons, Grid)

        Returns
        -------
        None
        """
        # OUTPUTS
        # ==========================================================================
        ## Output for the matrix P
        self.outP = widgets.HTMLMath(
            value=prettyPrintMatrix(
                self.P, simple=True, type="pMatrix", step=self.step
            ),
            placeholder="$P$",
            description="$P:$",
        )

        ## Output for the matrix L
        self.outL = widgets.HTMLMath(
            value=prettyPrintMatrix(
                self.L, simple=True, type="lMatrix", step=self.step
            ),
            placeholder="$L$",
            description="$\\tilde{L}:$",
        )

        ## Output for the matrix U
        self.outU = widgets.HTMLMath(
            value=prettyPrintMatrix(
                self.U, simple=True, type="uMatrix", step=self.step
            ),
            placeholder="$U$",
            description="$\\tilde{U}:$",
        )

        ## Output for the checker(PA=LU)
        self.outChecker = widgets.HTMLMath(
            value=str(np.allclose(self.L @ self.U, self.P @ self.A)),
            placeholder="$PA=?LU$",
            description="$PA=?LU$",
        )

        # BUTTONS
        # ==========================================================================
        ## Previous step button
        self.previousButton = widgets.Button(
            description="Previous Step",
            disabled=False,
            button_style="info",
            tooltip="Previous Step",
            icon="arrow-left",
        )
        self.previousButton.on_click(self.previousStep)

        ## Reset button
        self.resetButton = widgets.Button(
            description="Reset",
            disabled=False,
            button_style="danger",
            tooltip="Reset",
            icon="undo",
        )
        self.resetButton.on_click(self.reset)

        # MATRIX
        # ==========================================================================
        self.buttonsMatrix = []
        for i in range(self.A.shape[0]):
            row = []
            for j in range(self.A.shape[1]):
                row.append(widgets.Button(description=f"{self.A[i,j]:.2f}"))
                row[-1].index = (i, j)
                # Observer for the button
                row[-1].on_click(self.matrixPivotButton)

            self.buttonsMatrix.append(row)

        self.updateButtons()

        # GRID
        # ==========================================================================
        self.grid = widgets.GridspecLayout(6, 5)
        # Add components to grid
        self.grid[0:3, 0:3] = widgets.VBox(
            list(map(lambda x: widgets.HBox(x), self.buttonsMatrix))
        )
        self.grid[0, 3] = self.previousButton
        self.grid[1, 3] = self.resetButton

        self.grid[3, 0] = self.outP
        self.grid[3, 1] = self.outL
        self.grid[3, 2] = self.outU

    def matrixPivotButton(self, b):
        """
        Observer for the buttons in the matrix, when a button is clicked, the pivot is performed and the step is updated

        b.index contains the index of the pivot row
        Call luInteractive with PLU, step and index of pivot row
        Update the output

        Parameters
        ----------
        b : Button
            Button that was clicked

        Returns
        -------
        None
        """
        if b.disabled:
            return  # do nothing if the button is disabled
        self.previousSteps.append(
            (self.P.copy(), self.L.copy(), self.U.copy(), self.step)
        )
        with self.grid.hold_sync():
            self.oneStep(b.index[0])
            # Update the buttons
            self.updateButtons()

    def oneStep(self, pivot):
        # Apply the LU decomposition to the matrix
        self.P, self.L, self.U, self.step, _ = interactive_lu(
            self.P, self.L, self.U, self.step, pivot
        )
        # Update the output
        self.updateOutput()

    def updateButtons(self):
        """
        Update the buttons in the matrix, when a step is performed, blocks the buttons that are not available anymore

        Returns
        -------
        None
        """
        # If the all the pivots are 0, then increment the step and update the buttons
        if np.allclose(self.U[self.step :, self.step], 0):
            self.oneStep(-1)

        # Update the buttons
        for i in range(len(self.buttonsMatrix)):
            for j in range(len(self.buttonsMatrix[i])):

                if (  # if the step is 0, then the buttons are disabled except for the first column
                    j == self.step
                    and i >= self.step
                    and self.step != self.A.shape[1] - 1
                    and not np.isclose(self.U[i, j], 0)
                ):
                    self.buttonsMatrix[i][j].disabled = False
                    self.buttonsMatrix[i][j].style.button_color = "LightGreen"
                    self.buttonsMatrix[i][j].style.font_weight = "normal"

                elif (
                    self.step == self.A.shape[1] - 1
                ):  # if the step is the last one, then all the buttons are disabled and the color is gray
                    self.buttonsMatrix[i][j].disabled = True
                    self.buttonsMatrix[i][j].style.button_color = "Gainsboro"
                    self.buttonsMatrix[i][j].style.font_weight = "1000"
                else:  # If they are not the pivot buttons, then they are disabled and the color is LightCoral
                    self.buttonsMatrix[i][j].button_style = ""
                    self.buttonsMatrix[i][j].style.button_color = None
                    if j <= self.step or i <= self.step - 1:
                        self.buttonsMatrix[i][j].style.button_color = "LightCoral"
                    self.buttonsMatrix[i][j].disabled = True
                    self.buttonsMatrix[i][j].style.font_weight = "normal"

                self.buttonsMatrix[i][j].description = f"{self.U[i,j]:.2f}"

    def updateOutput(self):
        """
        Update the output widgets

        Returns
        -------
        None
        """
        # Update the outputs
        self.outP.value = prettyPrintMatrix(
            self.P, simple=True, type="pMatrix", step=self.step
        )
        self.outL.value = prettyPrintMatrix(
            self.L, simple=True, type="lMatrix", step=self.step
        )
        self.outU.value = prettyPrintMatrix(
            self.U, simple=True, type="uMatrix", step=self.step
        )

    def previousStep(self, b):
        """
        Observer for the previous step button, when clicked, it returns the state to the previous step

        Parameters
        ----------
        b : Button
            Button that was clicked (Not used)

        Returns
        -------
        None
        """
        # If there are previous steps, then go back to the previous step
        if len(self.previousSteps) > 0:
            self.P, self.L, self.U, self.step = self.previousSteps.pop()
            with self.grid.hold_sync():
                self.updateOutput()
                # Update the buttons
                self.updateButtons()

    def reset(self, b):
        """
        Observer for the reset button, when clicked, it returns the state to the initial state

        Parameters
        ----------
        b : Button
            Button that was clicked (Not used)

        Returns
        -------
        None
        """

        # Reset the LU decomposition Visualizer to the initial state
        self.step = 0
        self.L = np.eye(self.A.shape[0])
        self.U = self.A.copy()
        self.P = np.eye(self.A.shape[0])

        # Stack for previous steps
        self.previousSteps = []
        with self.grid.hold_sync():
            # Update the output
            self.updateOutput()
            # Update the buttons
            self.updateButtons()

    def run(self):
        """
        Run the LU decomposition Visualizer

        Returns
        -------
        None
        """
        # Run the visualizer
        self.initializeComponents()
        return self.grid


def prettyPrintMatrix(matrix, simple=False, type="normal", step=0):
    res = "  \\begin{pmatrix} \n"

    if type in ["normal", "pMatrix"]:
        for (
            row
        ) in matrix:  # Corresponds to any matrix or the P matrix (Permutation matrix)
            res += " & ".join([str(round(x, 3)) for x in row]) + "\\\\ \n"
    elif type == "lMatrix":  # Corresponds to the L matrix (Lower triangular matrix)
        # Write * everywhere except for the diagonal and the colums before the step
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if (i <= j or j < step) or step == -1:
                    res += str(round(matrix[i][j], 3)) + " & "
                else:
                    res += "* & "
            res = res[:-2] + "\\\\ \n"
    elif type == "uMatrix":  # Corresponds to the U matrix (Upper triangular matrix)
        # Write * on the submatrix [step:, step:]
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if i >= step and j >= step and step != -1:
                    res += "* & "
                else:
                    res += str(round(matrix[i][j], 3)) + " & "
            res = res[:-2] + "\\\\ \n"

    res += "\\end{pmatrix} "

    return Math(res) if not simple else res
