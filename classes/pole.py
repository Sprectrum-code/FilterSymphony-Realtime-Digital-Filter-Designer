import pyqtgraph as pg
from enums.types import Type
import numpy as np
class Pole(pg.PlotDataItem):
    def __init__(self, data, conjugate = None):
        super().__init__([data[0]], [data[1]], symbol ='x')
        self.real = data[0]
        self.imaginary = data[1]
        self.conjugate = conjugate
        self.identity = Type.POLE
        self.plots_control = None

    @property
    def real(self):
        return self.__real
    
    @real.setter
    def real(self, new_data):
        self.__real = new_data
        self.setData([new_data], [self.imaginary])
        
    @property
    def imaginary(self):
        return self.__imaginary
    
    @imaginary.setter
    def imaginary(self, new_data):
        self.__imaginary = new_data
        self.setData([self.real], [new_data])