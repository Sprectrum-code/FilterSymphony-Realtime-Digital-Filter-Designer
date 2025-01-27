from PyQt5.QtGui import QIcon
import numpy as np
from scipy.signal import lfilter , zpk2tf 
class Controller():
    def __init__(self, pre_signal_viewer , post_signal_viewer , current_signal):
        self.pre_signal_viewer = pre_signal_viewer
        self.post_signal_viewer = post_signal_viewer
        self.is_signal_viewers_playing = True
        self.current_signal = current_signal.signal
        self.filtered_signal = current_signal.signal
        self.pre_signal_viewer.current_signal = self.current_signal
        self.post_signal_viewer.current_signal = self.filtered_signal
        self.playIcon = QIcon('./icons_setup/icons/play.png')
        self.pauseIcon = QIcon('./icons_setup/icons/pause.png')
        self.complex_zeros = []
        self.complex_poles = []
        self.filter_numerator = 0
        self.filter_denominator = 0
        self.magnitude_viewer = None
        self.phase_viewer = None
        self.designer_viewer = None
    
    def set_current_signal(self):
        self.pre_signal_viewer.current_signal = self.current_signal
        self.post_signal_viewer.current_signal = self.filtered_signal
        self.compute_magnitude_and_phase()
        
    def toggle_play_pause_signal_viewers(self , play_pause_button):
        if(self.is_signal_viewers_playing):
            self.pre_signal_viewer.pause_timer()
            self.post_signal_viewer.pause_timer()
            self.is_signal_viewers_playing = False
            play_pause_button.setIcon(self.playIcon)
        else:
            self.pre_signal_viewer.play_timer()
            self.post_signal_viewer.play_timer()
            self.is_signal_viewers_playing = True
            play_pause_button.setIcon(self.pauseIcon)
            
    def compute_magnitude_and_phase(self):
        self.magnitude_viewer.compute_magnitude(self.designer_viewer.poles_list, self.designer_viewer.zeros_list)
        self.phase_viewer.compute_phase(self.designer_viewer.poles_list, self.designer_viewer.zeros_list)
        
    
    def replay_signal_viewers(self):
        self.pre_signal_viewer.current_signal_plotting_index = 0
        self.post_signal_viewer.current_signal_plotting_index = 0
    
    def modify_signal_viewers_speed(self , new_speed):
        self.pre_signal_viewer.change_viewer_speed(new_speed)
        self.post_signal_viewer.change_viewer_speed(new_speed)
    
    def compute_new_filter(self, zeros , poles):
        # print(zeros[0][0].real)
        # print(zeros[0][0].imaginary)
        # print(zeros[0][0].conjugate.imaginary)
        self.complex_zeros.clear()
        self.complex_poles.clear()
        
        for idx , zero in enumerate(zeros):
            complex_zero = complex(zero[0].real , zero[0].imaginary)
            self.complex_zeros.append(complex_zero)
            if (zero[1] is not None):
                complex_zero = complex(zero[1].real , zero[1].imaginary)
                self.complex_zeros.append(complex_zero)
        
        for idx , pole in enumerate(poles):
            complex_pole = complex(pole[0].real , pole[0].imaginary)
            self.complex_poles.append(complex_pole)
            if (pole[1] is not None):
                complex_pole = complex(pole[1].real , pole[1].imaginary)
                self.complex_poles.append(complex_pole)
            
        numerator , denominator = zpk2tf(self.complex_zeros , self.complex_poles , 1.0)

        self.filter_numerator = numerator
        self.filter_denominator = denominator
        
        filtered_signal = lfilter(self.filter_numerator , self.filter_denominator , self.current_signal[1])
        
        self.filtered_signal = [self.current_signal[0] , filtered_signal.real]
        
        self.set_current_signal()