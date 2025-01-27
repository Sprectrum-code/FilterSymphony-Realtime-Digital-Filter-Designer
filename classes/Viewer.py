import pyqtgraph as pg 
import numpy as np
from classes.customSignal import CustomSignal
class Viewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.setBackground((30, 41, 59))
        self.showGrid(x= True, y= True , alpha = 0.25)
        self.current_signal = None
    
    def format_pole_zero_lists(self,poles_list, zeros_list):
        poles = []
        zeros = []
        for (pole, conj_pole) in poles_list:
            poles.append((pole.real, pole.imaginary))
            if conj_pole:
                poles.append((conj_pole.real, conj_pole.imaginary))
        for (zero, conj_zero) in zeros_list:
            zeros.append((zero.real, zero.imaginary))
            if conj_zero:
                zeros.append((conj_zero.real, conj_zero.imaginary))
        return poles, zeros
        
    def compute_numerator_and_denominator(self, poles, zeros):
        w_range=(0, np.pi) 
        num_points=500
        w = np.linspace(w_range[0], w_range[1], num_points)
        zeros = [z[0] + 1j * z[1] for z in zeros]
        poles = [p[0] + 1j * p[1] for p in poles]
        H = np.ones(len(w), dtype=complex)
        for z in zeros:
            H *= np.exp(-1j * w) - z
        for p in poles:
            H /= np.exp(-1j * w) - p
        return w, H
    
    def update_signal(self):
        self.clear()
        self.plotItem(self.current_signal.signal[0], self.current_signal.signal[1])
    
    
    def compute_phase(self, poles_list, zeros_list):
        poles, zeros = self.format_pole_zero_lists(poles_list, zeros_list)
        frequencies,H = self.compute_numerator_and_denominator(poles, zeros)
        magnitude = np.abs(H)
        self.current_signal =  CustomSignal(frequencies, magnitude)
    
    def compute_magnitude(self, poles_list, zeros_list):
        poles, zeros = self.format_pole_zero_lists(poles_list, zeros_list)
        frequencies,H = self.compute_numerator_and_denominator(poles, zeros)
        phase = np.angle(H)
        self.current_signal = CustomSignal(frequencies, phase)