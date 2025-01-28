import sys
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QLabel, QVBoxLayout, QWidget
import pyqtgraph as pg  # Install via `pip install pyqtgraph`


class RealTimeSignal():
    def __init__(self, speed_control):
        # Create a mouse tracking area
        self.canvas = MouseTrackingCanvas(self)

        # Set up PyQtGraph for real-time signal display
        self.draw_graph = pg.PlotWidget()
        self.draw_graph.setLabel("left", "Signal Amplitude")
        self.draw_graph.setLabel("bottom", "Time (ms)")
        # self.draw_graph.setYRange(-300, 300)

        self.filter_graph = pg.PlotWidget()
        self.filter_graph.setLabel("left", "Signal Amplitude")
        self.filter_graph.setLabel("bottom", "Time (ms)")
        # self.filter_graph.setYRange(-300, 300)
        
        # Initialize signal data
        self.signal_data = []
        # self.max_points = 500  # Maximum number of points to display

        # Timer for updating the graph
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)  # Update every 50ms
        
        self.speed_slider = speed_control
        self.speed_slider.setRange(50, 350)  # Speed range in milliseconds
        self.speed_slider.setValue(100)  # Default speed
        self.speed_slider.valueChanged.connect(self.update_speed)
        
    def update_graph(self):
        """Update the graph with the latest signal data."""
        if self.canvas.signal_data_y:
            self.signal_data.extend(self.canvas.signal_data_y)
            self.canvas.signal_data_y = []  # Clear the processed data

        # Keep the signal data size within the maximum number of points
        # self.signal_data = self.signal_data[-self.max_points :]
        # Adjust signal to start from the middle
        mid_y = self.draw_graph.height() / 2
        adjusted_signal = [point + mid_y for point in self.signal_data]
        # Update the graph
        self.draw_graph.plot(adjusted_signal, clear=True)
    def update_speed(self, value):
        """Update the timer speed based on slider value."""
        # self.speed_slider.setText(f"Speed: {value}ms")
        self.timer.setInterval(400-value)

class MouseTrackingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # self.setFixedSize(800, 200)
        # self.setMouseTracking(True)  # Enable mouse tracking
        self.signal_data_y = []

    def mouseMoveEvent(self, event):
        """Capture mouse movement and generate a signal."""
        # Use the y-coordinate as the signal (you can change to x if needed)
        amplitude = 2 * event.y() - self.height() / 3
        frequency = max(1, (event.x() - self.width() / 2) / (self.width() / 4))

        # Generate signal based on frequency
        signal_value = amplitude * frequency
        self.signal_data_y.append(signal_value)
    def paintEvent(self, event):
        """Draw the canvas border."""
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeSignal()
    window.show()
    sys.exit(app.exec_())
