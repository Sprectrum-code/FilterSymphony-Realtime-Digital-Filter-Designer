import pyqtgraph as pg

class Zero(pg.ScatterPlotItem):
    def __init__(self):
        self.real = 0
        self.imaginary = 0
        self.conjugate = None