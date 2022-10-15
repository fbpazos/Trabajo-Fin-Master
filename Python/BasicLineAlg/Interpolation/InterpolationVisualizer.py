import numpy as np
from interpolation import interPoly, piecewiseLinear, pchip, splitnetx
from bqplot import pyplot as plt
import ipywidgets as widgets

class InterpolVisualizer:
    def __init__(self,xInitial,yInitial,uInitial):
        
        
        if len(xInitial) != len(yInitial):
            raise Exception("The length of the X and Y coordinates must be the same")

        


        self.x = np.array(xInitial).astype(float)
        self.y = np.array(yInitial).astype(float)
        self.u = np.array(uInitial).astype(float)
        
        self.Originals = [self.x,self.y,self.u]

    def initializeComponents(self):
        '''
        Initializes the components of the GUI
        Components:
            - Checkboxes
                Checkboxes for each interpolation method
            - Slider
                Slider for the mesh size
            - Reset Button
                Button to reset the points
        '''
        self.checkboxes = [
            widgets.Checkbox(description='InterPoly', value=True, style={'background': 'lightblue'}),
            widgets.Checkbox(description='Piecewise Linear', value=True,style={'background': 'lightgreen'}),
            widgets.Checkbox(description='Pchip', value=True,style={'background': 'bisque'}),
            widgets.Checkbox(description='SplitNetX', value=True,style={'background': 'violet'})

            # for more interpolation methods, add more checkboxes here
        ]
        # Reset button
        self.reset_button = widgets.Button(description='Reset')

        # Range slider
        values = [min(self.x), max(self.x)]
        self.slider = widgets.FloatRangeSlider(
            value=values,
            min=values[0] - (values[1]-values[0])/2 ,
            max=values[1] + (values[1]-values[0])/2,
            step=0.1,
            description='Mesh:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )
        # Linking the widgets to the functions
        self.slider.observe(self.update_Mesh, 'value')
        self.reset_button.on_click(self.reset)
        for checkbox in self.checkboxes:
            checkbox.observe(self.update_checkboxes, 'value')

    
        self.checkboxesVbox = widgets.VBox(self.checkboxes)

    def initializeBQPlot(self):
        '''
        Initializes the bqplot figure
        Applies the scatter plot and the interpolation for the initial points
        '''

        self.fig = plt.figure(title='Interpolation Visualizer')
        
        self.interpolate()
        self.scattering()    
        plt.legend()

    def scattering(self):
        '''
        Plots the initial points
        Makes the points draggable and links them to the update_points function
        Makes the points Addable and links them to the update_points function
        '''
        self.scatterPlot = plt.scatter(self.x, self.y, colors=['red'], stroke='red',label="Points")
        self.scatterPlot.enable_move = True
        self.scatterPlot.enable_add = True
        self.scatterPlot.observe(self.update_pointsX, 'x')
        self.scatterPlot.observe(self.update_pointsY, 'y')
        self.scatterPlot.interactions = {'click':  'add'}

    def update_pointsX(self,change):
        '''
        Updates the X coordinates of the points
        The reason of this function is that the bqplot library does not allow to update the X and Y coordinates at the same time, but it prioritizes the X coordinates according to our order or code

        After updating the X coordinates, it updates the Y coordinates because the Observer of the Y coordinates is called after the Observer of the X coordinates

        params:
            change: the change in the X coordinates
        '''
        self.x = change['new'] if change is not None and change["name"]=="x" and len(list(change['new'])) == len(set(change["new"])) else self.x
        
    def update_pointsY(self,change):
        '''
        Updates the Y coordinates of the points
        This will happen after the X coordinates are updated, therefore interpolating the new points

        This methods also updates the mesh

        It allows to add new points and it serves as a Nexus for the other functions to update the points
        '''

        plt.clear()
        self.y = change['new'] if change is not None and change["name"]=="y" else self.y

        self.slider.min = min(self.x) - (max(self.x)-min(self.x))/2
        self.slider.max = max(self.x) + (max(self.x)-min(self.x))/2

        self.interpolate()
        self.scattering()
        
        plt.legend()

    def update_Mesh(self, change):
        '''
        Updates the mesh and the plot according to the new mesh
        '''
        self.u = np.linspace(change['new'][0], change['new'][1], 100)
        self.update_pointsX(None)
        self.update_pointsY(None)

    def update_checkboxes(self, change):
        '''
        Updates the plot according to the new checkboxes
        '''
        self.update_pointsX(None)
        self.update_pointsY(None)

    def reset(self, b):
        '''
        Resets the points to the original ones
        '''
        self.x = self.Originals[0]
        self.y = self.Originals[1]
        self.u = self.Originals[2]
        self.update_pointsX(None)
        self.update_pointsY(None)

    def interpolate(self):
        '''
        Checks each checkbox and interpolates the selected functions and interpolates them 
        '''
        if self.checkboxes[0].value:
            plt.plot(self.u, interPoly(self.x, self.y, self.u), colors=['blue'], stroke='blue',label="InterPoly")
        if self.checkboxes[1].value:
            plt.plot(self.u, piecewiseLinear(self.x, self.y, self.u), colors=['green'], stroke='green',label="PieceWise Linear")
        if self.checkboxes[2].value:
            plt.plot(self.u, pchip(self.x, self.y, self.u), colors=['orange'], stroke='orange',label="PCHIP")
        if self.checkboxes[3].value:
            plt.plot(self.u, splitnetx(self.x, self.y, self.u), colors=['purple'], stroke='purple',label="SplitnetX")

        # for more interpolation methods, add more if statements here
        

    def run(self):
        '''
        Runs the GUI by displaying the components and the bqplot figure
        '''
        self.initializeComponents()
        self.initializeBQPlot()

        tools = widgets.VBox([self.checkboxesVbox,self.slider,self.reset_button])
        
        widgetsgrid = widgets.GridspecLayout(10, 7)
        widgetsgrid[:,:4] = self.fig
        widgetsgrid[1:,4:] = tools
        
        
        return widgetsgrid