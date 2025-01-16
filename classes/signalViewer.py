import pyqtgraph as pg
from PyQt5.QtCore import QTimer

class SignalViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.__current_signal = [[],[]]
        self.__current_signal_plotting_index = 0
        self.timer = QTimer()
        self.__cine_speed = 100
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(self.__cine_speed)
        self.setLimits(xMin = 0)
        self.curve = self.plot(pen='b')
        
    @property
    def current_signal(self):
        return self.__current_signal
    
    @current_signal.setter
    def current_signal(self , new_signal):
        self.__current_signal = new_signal
    
    @property
    def cine_speed(self):
        return self.__cine_speed
    
    @cine_speed.setter
    def cine_speed(self , new_speed):
        self.__cine_speed = new_speed
    
    @property
    def current_signal_plotting_index(self):
        return self.__current_signal_plotting_index
    
    @current_signal_plotting_index.setter
    def current_signal_plotting_index(self , new_index):
        self.__current_signal_plotting_index = new_index
    
    def play_timer(self):
        self.timer.start(self.cine_speed)
    
    def pause_timer(self):
        self.timer.stop()
    
    def update_plot(self):
        '''
        Update the signal viewer each timer tick
        '''
        if self.current_signal_plotting_index < len(self.current_signal[0]):
            self.curve.setData(self.current_signal[0][:self.current_signal_plotting_index], self.current_signal[1][:self.current_signal_plotting_index])
            if(self.current_signal_plotting_index <= 50):
                self.setXRange(0, self.current_signal[0][self.current_signal_plotting_index])
            
            elif(self.current_signal_plotting_index + 50 >= len(self.current_signal[0])):
                self.setXRange(self.current_signal[0][self.current_signal_plotting_index - 50], self.current_signal[0][self.current_signal_plotting_index])
            
            else:
                self.setXRange(self.current_signal[0][self.current_signal_plotting_index - 50], self.current_signal[0][self.current_signal_plotting_index + 50])
            self.current_signal_plotting_index += 1
        else:
            self.timer.stop()
    
    def increase_speed(self):
        if(self.cine_speed > 10):
            self.cine_speed -= 10
            self.play_timer()
    
    def decrease_speed(self):
        self.cine_speed += 10    
        self.play_timer()
