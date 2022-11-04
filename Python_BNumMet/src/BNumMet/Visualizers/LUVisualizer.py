import numpy as np
import ipywidgets as widgets
from IPython.display import display, Math
from ..LinearEquations import interactive_lu


class LUVisualizer:
    def __init__(self, matrix):
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
            value=prettyPrintMatrix(self.P, True), placeholder="$P$", description="$P:$"
        )

        ## Output for the matrix L
        self.outL = widgets.HTMLMath(
            value=prettyPrintMatrix(self.L, True), placeholder="$L$", description="$L:$"
        )

        ## Output for the matrix U
        self.outU = widgets.HTMLMath(
            value=prettyPrintMatrix(self.U, True), placeholder="$U$", description="$U:$"
        )

        ## Output for the matrix L*U
        self.outPLU = widgets.HTMLMath(
            value=prettyPrintMatrix(self.L @ self.U, True),
            placeholder="$LU$",
            description="$LU:$",
        )

        ## Output for the matrix P*A
        self.outA = widgets.HTMLMath(
            value=prettyPrintMatrix(self.P @ self.A, True),
            placeholder="$PA$",
            description="$PA:$",
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
                # if the step is 0, then the buttons are disabled except for the first column
                if (
                    j == self.step
                    and i >= self.step
                    and self.step != self.A.shape[1] - 1
                    and not np.isclose(self.U[i, j], 0)
                ):
                    # color green for available buttons
                    row.append(
                        widgets.Button(
                            description=f"{self.A[i,j]:.2f}",
                            disabled=False,
                            layout=widgets.Layout(width="125px", height="30px"),
                            button_style="success",
                        )
                    )
                else:
                    row.append(
                        widgets.Button(
                            description=f"{self.A[i,j]:.2f}",
                            disabled=True,
                            layout=widgets.Layout(width="125px", height="30px"),
                        )
                    )
                row[-1].index = (i, j)
                # Observer for the button
                row[-1].on_click(self.matrixPivotButton)

            self.buttonsMatrix.append(row)

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

        self.grid[4, 0] = self.outPLU
        self.grid[4, 1] = self.outA

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
        self.P, self.L, self.U, self.step, _ = interactive_lu(
            self.P, self.L, self.U, self.step, b.index[0]
        )
        with self.grid.hold_sync():
            # Update the output
            self.updateOutput()
            # Update the buttons
            self.updateButtons()

    def updateButtons(self):
        """
        Update the buttons in the matrix, when a step is performed, blocks the buttons that are not available anymore

        Returns
        -------
        None
        """
        # Update the buttons
        for i in range(len(self.buttonsMatrix)):
            for j in range(len(self.buttonsMatrix[i])):
                # if the step is 0, then the buttons are disabled except for the first column
                if (
                    j == self.step
                    and i >= self.step
                    and self.step != self.A.shape[1] - 1
                    and not np.isclose(self.U[i, j], 0)
                ):
                    self.buttonsMatrix[i][j].disabled = False
                    self.buttonsMatrix[i][j].button_style = "success"
                else:
                    self.buttonsMatrix[i][j].disabled = True
                    self.buttonsMatrix[i][j].button_style = ""

                self.buttonsMatrix[i][j].description = f"{self.U[i,j]:.2f}"

    def updateOutput(self):
        """
        Update the output widgets

        Returns
        -------
        None
        """
        # Update the outputs
        self.outP.value = prettyPrintMatrix(self.P, True)
        self.outL.value = prettyPrintMatrix(self.L, True)
        self.outU.value = prettyPrintMatrix(self.U, True)
        self.outPLU.value = prettyPrintMatrix(self.L @ self.U, True)
        self.outA.value = prettyPrintMatrix(self.P @ self.A, True)
        # self.outChecker.value = str(np.allclose(self.P@self.A,self.L@self.U))

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


def prettyPrintMatrix(matrix, simple=False):
    res = "  \\begin{pmatrix} \n"
    for row in matrix:
        res += " & ".join([str(round(x, 3)) for x in row]) + "\\\\ \n"
    res += "\\end{pmatrix} "

    return Math(res) if not simple else res
