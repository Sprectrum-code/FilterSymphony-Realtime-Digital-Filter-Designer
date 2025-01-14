import pyqtgraph as pg
from PyQt5.QtCore import QTimer

class SignalViewer(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.__current_signal = None
        self.__current_signal_plotting_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        self.curve = self.plot(pen='b')
        
    @property
    def current_signal(self):
        return self.__current_signal
    
    @current_signal.setter
    def current_signal(self , new_signal):
        self.__current_signal = new_signal
    
    @property
    def current_signal_plotting_index(self):
        return self.__current_signal_plotting_index
    
    @current_signal_plotting_index.setter
    def current_signal_plotting_index(self , new_index):
        self.__current_signal_plotting_index = new_index
    
    def play_timer(self):
        self.timer.start()
    
    def pause_timer(self):
        self.timer.stop()
    
    def update_plot(self):
        '''
        Update the signal viewer each timer tick
        '''
        if self.current_signal_plotting_index < len(self.current_signal[0]):
            if(self.current_signal_plotting_index < 100):
                self.curve.setData(self.current_signal[0][:self.current_signal_plotting_index], self.current_signal[1][:self.current_signal_plotting_index])
            else:
                self.curve.setData(self.current_signal[0][self.current_signal_plotting_index-100:self.current_signal_plotting_index], self.current_signal[1][self.current_signal_plotting_index-100:self.current_signal_plotting_index])
            self.current_signal_plotting_index += 1
        else:
            self.timer.stop()
    