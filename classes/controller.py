from PyQt5.QtGui import QIcon
class Controller():
    def __init__(self, pre_signal_viewer , post_signal_viewer , current_signal):
        self.pre_signal_viewer = pre_signal_viewer
        self.post_signal_viewer = post_signal_viewer
        self.is_signal_viewers_playing = True
        self.current_signal = current_signal.signal
        self.pre_signal_viewer.current_signal = self.current_signal
        filtered_signal = [x*2 for x in self.current_signal]
        self.post_signal_viewer.current_signal = filtered_signal
        self.playIcon = QIcon('./icons_setup/icons/play.png')
        self.pauseIcon = QIcon('./icons_setup/icons/pause.png')
    
    def set_current_signal(self , signal):
        self.current_signal = signal.signal
        self.pre_signal_viewer.current_signal = signal
        filtered_signal = (signal[1]*2)+2
        self.post_signal_viewer.current_signal = filtered_signal
        
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
    
    def replay_signal_viewers(self):
        self.pre_signal_viewer.current_signal_plotting_index = 0
        self.post_signal_viewer.current_signal_plotting_index = 0
    
    def speed_up_signal_viewers(self):
        self.pre_signal_viewer.increase_speed()
        self.post_signal_viewer.increase_speed()
    
    def speed_down_signal_viewers(self):
        self.pre_signal_viewer.decrease_speed()
        self.post_signal_viewer.decrease_speed()