import pyqtgraph as pg

class Pole(pg.ScatterPlotItem):
    def __init__(self):
        super().__init__()
        self.real = 0
        self.imaginary = 0
        self.conjugate = None