import numpy as np
from ..Interpolation import interPoly, piecewiseLinear, pchip, splitnetx
from bqplot import pyplot as plt
import ipywidgets as widgets
import bqplot as bq

class InterpolVisualizer:
    def __init__(self,xInitial,yInitial,uInitial) -> None:
        '''
        Initializes the Class

        Parameters:
            - xInitial: Initial x coordinates
            - yInitial: Initial y coordinates
            - uInitial: Initial mesh
        '''
        if len(xInitial) != len(yInitial):
            raise Exception("The length of the X and Y coordinates must be the same")

        self.x = np.array(xInitial).astype(float)
        self.y = np.array(yInitial).astype(float)
        self.u = np.array(uInitial).astype(float)
        
        self.Originals = [self.x,self.y,self.u]

        self.methods = {
            'InterPoly':[interPoly,"blue"],
            'Piecewise Linear':[piecewiseLinear,"green"],
            'Pchip':[pchip,"orange"],
            'SplitNetX':[splitnetx,"purple"]
        }



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

        '''
        Checkboxes
        ======================
        One checkbox for every possible interpolation method
        Every checkbox will be associated with a method called update_checkboxes that will update the plot according to the updated checkboxes. 
        Additionally, the checkbox will have the same color as the color of associated interpolation method
        '''
        self.checkboxes = []
        for key,val in self.methods.items():
            checkbox = widgets.Checkbox(description=key, value=True, style={'background': val[1]})
            checkbox.observe(self.update_checkboxes, 'value')
            self.methods[key].append(checkbox)
            self.checkboxes.append(checkbox)
            

        '''
        Reset button
        ======================
        Button to reset the points to the original ones, linked to the method reset
        '''
        self.reset_button = widgets.Button(description='Reset')
        self.reset_button.on_click(self.reset)

        '''
        Range slider
        ======================
        Slider to change the mesh size, linked to the method update_Mesh, with a default minimum of the minimum of the original points - 0.5*(max-min) 
        and a default maximum of the maximum of the original points + 0.5*(max-min).
        '''
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
        self.slider.observe(self.update_Mesh,'value')

       
    def scatterDots(self):
        '''
        Updates ScatteredDots - the scatter plot of the data - according to the new points
        It observers the changes in the x and y coordinates of the scatter plot and links them to the update_X and update_Y methods
        It also lets adding new points
        '''
        self.ScatteredDots = bq.Scatter(x=self.x,y=self.y, scales={'x': self.x_sc, 'y': self.y_sc}, colors=['red'],name="Points",enable_move = True, enable_add = False, display_legend=False, labels=["Points"])
        
        # observe change XY
        self.ScatteredDots.observe(self.update_X,'x')
        self.ScatteredDots.observe(self.update_Y,'y')
        self.ScatteredDots.interactions = {'click':  'add'}

    
    def interpolLines(self):
        '''
        Updates the interpolation lines according to the new points
        It creates an array of Lines for every interpolation method that is checked in the checkboxes
        '''
        self.InterpolLines = [
            bq.Lines(x=self.u,y=val[0](self.x,self.y,self.u),scales={'x': self.x_sc, 'y': self.y_sc}, colors=[val[1]],name=key, display_legend=False, labels=[key], enable_move = False, enable_add = False) 
            for key,val in self.methods.items()
                if val[2].value
            ]

    def update_X(self,change):
        '''
        Updates the x coordinates and the plot according to the new x coordinates if the change is not None and does not contain Repetitions (Definition of a function)
        It also updates the slider according to the new x coordinates

        This method will always be called when the x coordinates are changed and before the y coordinates are changed.
        '''
        self.x = change['new'] if change is not None and change["name"]=="x" and len(list(change['new'])) == len(set(change["new"])) else self.x

        self.slider.min = min(self.x) - (max(self.x)-min(self.x))/2
        self.slider.max = max(self.x) + (max(self.x)-min(self.x))/2

    def update_Y(self,change):
        '''
        Updates the y coordinates and the plot according to the new y coordinates if the change is not None and contains the same number of points as X 
        It makes new scattering and inteprolation lines and updates the plot.
        Also, it updates Scales and Axes according to the new points

        This method will always be called when the y coordinates are changed and after the x coordinates are changed.
        '''
        with self.widgetsgrid.hold_sync():
            self.y = change['new'] if change is not None and change["name"]=="y" and len(list(change['new'])) == len(self.x) else self.y

            self.scatterDots()
            self.interpolLines()

            toUpdate = [*self.InterpolLines,self.ScatteredDots]

            self.Fig.marks = toUpdate
            
            yVals = [j for line in self.InterpolLines for j in line.y]
            if len(yVals) != 0:
                self.y_sc.min = min(yVals)
                self.y_sc.max = max(yVals)

    def update_Mesh(self, change):
        '''
        Updates the mesh and the plot according to the new mesh
        '''
        self.u = np.linspace(change['new'][0], change['new'][1], 100)
        
        self.update_X(None)
        self.update_Y(None)
        
        # Reset X scale
        self.x_sc.min = min(self.u)
        self.x_sc.max = max(self.u)

    def update_checkboxes(self, change):
        '''
        Updates the plot according to the new checkboxes
        '''
        self.update_X(None)
        self.update_Y(None)
    def reset(self, b):
        '''
        Resets everything to what it was at the beginning of the program
        '''
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
        '''
        Runner method : Creates all the widgets and displays the plot with a given layout
        '''
        self.x_sc = bq.LinearScale()
        self.y_sc = bq.LinearScale()
        ax_x = bq.Axis(scale=self.x_sc, grid_lines='solid', label='X')
        ax_y = bq.Axis(scale=self.y_sc, orientation='vertical', tick_format='0.2f',grid_lines='solid', label='Y')
        
        
        self.initializeComponents()
        self.interpolLines()
        self.scatterDots()

        self.Fig = bq.Figure(marks=[*self.InterpolLines, self.ScatteredDots], axes=[ax_x, ax_y], title='Interpolation Visualizer', legend_location='top-right', animation_duration=1000, )

        self.Toolbar = bq.Toolbar(figure=self.Fig)

        self.checkboxesVbox = widgets.VBox(self.checkboxes)
        tools = widgets.VBox([self.checkboxesVbox,self.slider,self.reset_button])
        
        self.widgetsgrid = widgets.GridspecLayout(11, 7)
        
        self.widgetsgrid[0,:] = self.Toolbar
        self.widgetsgrid[1:,:4] = self.Fig
        self.widgetsgrid[1:,4:] = tools

        return self.widgetsgrid

class InterpolVisualizer_UnOptimized:
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
        self.slider.observe(self.update_Mesh,'value')
        self.reset_button.on_click(self.reset)
        for checkbox in self.checkboxes:
            checkbox.observe(self.update_checkboxes,'value')

    
        self.checkboxesVbox = widgets.VBox(self.checkboxes)

        

    def initializeBQPlot(self):
        '''
        Initializes the bqplot figure
        Applies the scatter plot and the interpolation for the initial points
        '''

        self.fig = plt.figure(title='Interpolation Visualizer')
        
        self.Toolbar = plt.Toolbar(figure=self.fig)

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
        self.y = change['new'] if change is not None and change["name"]=="y" and  len(self.x) == len(list(change['new']))  else self.y

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
        
        widgetsgrid = widgets.GridspecLayout(11, 7)
        
        widgetsgrid[0,:] = self.Toolbar
        widgetsgrid[1:,:4] = self.fig
        widgetsgrid[1:,4:] = tools
        
        
        
        return widgetsgrid