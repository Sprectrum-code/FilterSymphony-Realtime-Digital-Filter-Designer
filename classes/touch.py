import sys
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QLabel, QVBoxLayout, QWidget
import pyqtgraph as pg  # Install via `pip install pyqtgraph`


class RealTimeSignalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Signal Generator")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Create a display label for instructions
        self.instruction_label = QLabel("Move your mouse in the box below to generate a signal!")
        layout.addWidget(self.instruction_label)

        # Create a mouse tracking area
        self.canvas = MouseTrackingCanvas(self)
        layout.addWidget(self.canvas)

        # Set up PyQtGraph for real-time signal display
        self.graph = pg.PlotWidget()
        self.graph.setLabel("left", "Signal Amplitude")
        self.graph.setLabel("bottom", "Time (ms)")
        self.graph.setYRange(-300, 300)
        layout.addWidget(self.graph)

        # Initialize signal data
        self.signal_data = []
        self.max_points = 500  # Maximum number of points to display

        # Timer for updating the graph
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(50)  # Update every 50ms

    def update_graph(self):
        """Update the graph with the latest signal data."""
        if self.canvas.signal_data:
            self.signal_data.extend(self.canvas.signal_data)
            self.canvas.signal_data = []  # Clear the processed data

        # Keep the signal data size within the maximum number of points
        self.signal_data = self.signal_data[-self.max_points :]

        # Update the graph
        self.graph.plot(self.signal_data, clear=True)


class MouseTrackingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 200)
        self.setMouseTracking(True)  # Enable mouse tracking
        self.signal_data = []

    def mouseMoveEvent(self, event):
        """Capture mouse movement and generate a signal."""
        # Use the y-coordinate as the signal (you can change to x if needed)
        signal_value = event.y() - self.height() / 2
        self.signal_data.append(signal_value)

    def paintEvent(self, event):
        """Draw the canvas border."""
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeSignalApp()
    window.show()
    sys.exit(app.exec_())
