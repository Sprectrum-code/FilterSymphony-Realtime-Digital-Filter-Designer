import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QVBoxLayout ,QFrame , QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from classes.signalViewer import SignalViewer
from classes.controller import Controller
from classes.customSignal import CustomSignal
from classes.designerViewer import DesignerViewer 
import numpy as np
import pyqtgraph as pg
from enums.modesEnum import Mode
from enums.types import Type

compile_qrc()
from icons_setup.compiledIcons import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Realtime Digital Filter Designer')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
        
        # Initializing the signal viewer
        self.pre_signal_viewer = SignalViewer()
        self.post_signal_viewer = SignalViewer()
        
        # Initializing the pre-signal frame
        self.pre_signal_frame = self.findChild(QFrame, 'presignalFrame')
        self.pre_signal_frame_layout = QVBoxLayout()
        self.pre_signal_frame.setLayout(self.pre_signal_frame_layout)
        self.pre_signal_frame_layout.addWidget(self.pre_signal_viewer)
        
        # Initializing the post-signal viewer
        self.post_signal_frame = self.findChild(QFrame, 'postsignalFrame')
        self.post_signal_frame_layout = QVBoxLayout()
        self.post_signal_frame.setLayout(self.post_signal_frame_layout)
        self.post_signal_frame_layout.addWidget(self.post_signal_viewer)
        
        # Initialize the signal
        x = np.linspace(0, 10 * np.pi, 1000)
        y = np.sin(x)
        self.current_signal = CustomSignal(x , y)
        
        # initialize the filter designer viewer
        self.designer_viewer = DesignerViewer()
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.graphics_layout.setBackground((30, 41, 59))
        self.graphics_layout.addItem(self.designer_viewer)
        self.designer_frame = self.findChild(QFrame,"unitCircleFrame")
        self.designer_frame_layout = QVBoxLayout()
        self.designer_frame.setLayout(self.designer_frame_layout)
        self.designer_frame_layout.addWidget(self.graphics_layout)
        
        # Initialize the controller
        self.controller = Controller(self.pre_signal_viewer , self.post_signal_viewer, self.current_signal)
        
        # Initialize play and pause buttons
        self.signal_viewer_play_pause_button = self.findChild(QPushButton , "playPause")
        self.signal_viewer_play_pause_button.clicked.connect(self.toggle_play_pause_signal_viewers)
        
        # Initialize the replay button
        self.replay_signal_viewers_button = self.findChild(QPushButton , "replay")
        self.replay_signal_viewers_button.clicked.connect(self.replay_signal_viewers)
        
        # Initialize signal viewers speed modifiers
        self.speed_up_signal_viewer_button = self.findChild(QPushButton , "speedUp")
        self.speed_up_signal_viewer_button.clicked.connect(self.speed_up_signal_viewers)
        
        self.speed_down_signal_viewer_button = self.findChild(QPushButton , "speedDown")
        self.speed_down_signal_viewer_button.clicked.connect(self.speed_down_signal_viewers)
        
        # controls initialization
        self.add_zero_button = self.findChild(QPushButton, "addZero")
        self.add_zero_button.clicked.connect(self.add_zero)
        self.add_pole_button = self.findChild(QPushButton, "addPole")
        self.add_pole_button.clicked.connect(self.add_pole)
        
    def toggle_play_pause_signal_viewers(self):
        self.controller.toggle_play_pause_signal_viewers(self.signal_viewer_play_pause_button)
    
    def replay_signal_viewers(self):
        self.controller.replay_signal_viewers()
        
    def speed_up_signal_viewers(self):
        self.controller.speed_up_signal_viewers()
    
    def speed_down_signal_viewers(self):
        self.controller.speed_down_signal_viewers()
    
    def add_zero(self):
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.ZERO
    def add_pole(self):
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.POLE
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())