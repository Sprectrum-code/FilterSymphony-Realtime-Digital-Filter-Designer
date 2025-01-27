import pyqtgraph as pg
from enums.types import Type
import numpy as np
import copy
class Pole(pg.PlotDataItem):
    def __init__(self, data, conjugate = None):
        super().__init__([data[0]], [data[1]], symbol ='x')
        self.__real = data[0]
        self.__imaginary = data[1]
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
        
    def __deepcopy__(self, memo):
        # Avoid deepcopying attributes that are not necessary or problematic
        copied_pole = Pole((self.__real, self.__imaginary))
        copied_pole.identity = self.identity
        if self.conjugate:
            copied_conjugate = copy.deepcopy(self.conjugate, memo)
            copied_pole.conjugate = copied_conjugate
            copied_conjugate.conjugate = copied_pole
        return copied_pole