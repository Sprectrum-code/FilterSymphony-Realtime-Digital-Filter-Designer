

class CustomSignal():
    def __init__(self , data_x , data_y):
        self.__signal = [data_x, data_y]
        
    @property
    def signal(self):
        return self.__signal
    
    @ signal.setter
    def signal(self, new_signal):
            self.__signal = new_signal