import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QVBoxLayout
from classes.signalViewer import SignalViewer
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Realtime Digital Filter Designer')
        
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        x = np.linspace(0, 100 * np.pi, 10000)
        viewer1 = SignalViewer()
        viewer1.current_signal = [x , np.sin(x)]
        viewer2 = SignalViewer()
        viewer2.current_signal = [x , np.sin(2*x)+2]
        layout.addWidget(viewer1)
        layout.addWidget(viewer2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())