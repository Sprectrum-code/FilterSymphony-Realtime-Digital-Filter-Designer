import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from icons_setup.compiledIcons import *
from classes.signalViewer import SignalViewer
import numpy as np

compile_qrc()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Realtime Digital Filter Designer')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())