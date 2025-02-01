from PyQt5.QtGui import QIcon
import numpy as np
from scipy.signal import lfilter , zpk2tf 
from classes.pole import Pole
from classes.zero import Zero
from classes.customSignal import CustomSignal
import pandas as pd
class Controller():
    def __init__(self, pre_signal_viewer , post_signal_viewer , current_signal , ap_filter_phase_viewer , ap_corrected_phase_viewer , signal_page_pre_viewer ,signal_page_post_viewer):
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
        self.ap_corrected_phase_viewer = ap_corrected_phase_viewer
        self.ap_filter_phase_viewer = ap_filter_phase_viewer
        self.all_pass_zeros_poles_list = [[],[]]
        self.original_all_pass_zeros_poles_list = [[],[]]
        self.ap_filter_added = False
        self.signal_page_pre_viewer = pre_signal_viewer
        self.signal_page_post_viewer = post_signal_viewer
        
    def set_current_signal(self):
        self.pre_signal_viewer.current_signal = self.current_signal
        self.signal_page_pre_viewer.current_signal = self.current_signal
        self.post_signal_viewer.current_signal = self.filtered_signal
        self.signal_page_post_viewer.current_signal = self.filtered_signal
        self.compute_magnitude_and_phase()
    
    def browse_signal(self , file_path):
        self.pre_signal_viewer.clear_viewer_content()
        self.post_signal_viewer.clear_viewer_content()
        self.signal_page_pre_viewer.clear_viewer_content()
        self.signal_page_post_viewer.clear_viewer_content()
        read_data = pd.read_csv(file_path)
        time_list = read_data['Time'].tolist()
        signal_list = read_data['Signal'].tolist()
        self.current_signal = CustomSignal(time_list , signal_list).signal
        self.signal_page_pre_viewer.play_timer()
        self.signal_page_post_viewer.play_timer()
        self.replay_signal_viewers()
        self.compute_new_filter(self.designer_viewer.zeros_list , self.designer_viewer.poles_list)
        
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
    
    def calculate_all_pass_filter_phase(self):
        self.ap_filter_phase_viewer.compute_phase(self.all_pass_zeros_poles_list[0] , self.all_pass_zeros_poles_list[1])    
    
    def calculate_corrected_phase(self):
        self.all_pass_zeros_poles_list[0].extend(self.designer_viewer.poles_list)
        self.all_pass_zeros_poles_list[1].extend(self.designer_viewer.zeros_list)
        self.ap_corrected_phase_viewer.compute_phase(self.all_pass_zeros_poles_list[0] , self.all_pass_zeros_poles_list[1])
        
        
    def handle_all_pass_zero_pole_list(self , poles_zeros):
        self.ap_filter_added = True
        self.all_pass_zeros_poles_list[0].clear()
        self.all_pass_zeros_poles_list[1].clear()
        self.original_all_pass_zeros_poles_list[0].clear()
        self.original_all_pass_zeros_poles_list[1].clear()
        pole = poles_zeros[0]
        zero = poles_zeros[1]
        pole = Pole(pole)
        zero = Zero(zero)
        self.all_pass_zeros_poles_list[0].append((pole,None))
        self.all_pass_zeros_poles_list[1].append((zero,None))
        self.original_all_pass_zeros_poles_list[0].append((pole,None))
        self.original_all_pass_zeros_poles_list[1].append((zero,None))
        
    def replay_signal_viewers(self):
        self.pre_signal_viewer.current_signal_plotting_index = 0
        self.post_signal_viewer.current_signal_plotting_index = 0
        self.signal_page_pre_viewer.current_signal_plotting_index = 0
        self.signal_page_post_viewer.current_signal_plotting_index = 0
    
    def modify_signal_viewers_speed(self , new_speed):
        self.pre_signal_viewer.change_viewer_speed(new_speed)
        self.post_signal_viewer.change_viewer_speed(new_speed)
    
    def modify_signal_page_viewers_speed(self , new_speed):
        self.signal_page_pre_viewer.change_viewer_speed(new_speed)
        self.signal_page_post_viewer.change_viewer_speed(new_speed)
    
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