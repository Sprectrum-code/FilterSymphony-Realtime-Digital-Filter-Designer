import pyqtgraph as pg 

class Viewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground((30, 41, 59))
        self.showGrid(x= True, y= True , alpha = 0.25)
        