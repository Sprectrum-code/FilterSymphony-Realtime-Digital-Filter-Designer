import sys
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen
from classes.signalViewer import SignalViewer
from classes.customSignal import CustomSignal
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QLabel, QVBoxLayout, QWidget
import pyqtgraph as pg  # Install via `pip install pyqtgraph`


class RealTimeSignal(QWidget):
    def __init__(self, speed_control, controller):
        super().__init__()       # Create a mouse tracking area
        self.canvas = MouseTrackingCanvas(self)
        
        # Set up PyQtGraph for real-time signal display
        self.draw_graph = None
        # self.draw_graph.setLabel("left", "Signal Amplitude")
        # self.draw_graph.setLabel("bottom", "Time (ms)")
        # self.draw_graph.setYRange(-300, 300)

        self.filter_graph = None
        # self.filter_graph.setLabel("left", "Signal Amplitude")
        # self.filter_graph.setLabel("bottom", "Time (ms)")
        # self.filter_graph.setYRange(-300, 300)
        
        # Initialize signal data
        self.signal_data = [[],[]]
        # self.max_points = 500  # Maximum number of points to display

        # Timer for updating the graph
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(60)  # Update every 50ms
        
        self.current_controller = controller 
        self.speed_slider = speed_control
        # self.speed_slider.setRange(50, 350)  # Speed range in milliseconds
        # self.speed_slider.setValue(50)  # Default speed
        # self.speed_slider.valueChanged.connect(self.update_speed)
        
    def update_graph(self):
        """Update the graph with the latest signal data."""
        self.current_signal = CustomSignal(self.signal_data[0] , self.signal_data[1])

        if self.canvas.signal_data_y:
            self.signal_data[1].extend(self.canvas.signal_data_y)
            self.signal_data[0].extend(self.canvas.signal_data_x)
            self.canvas.signal_data_y = []  # Clear the processed data
            self.canvas.signal_data_x = []
            
            self.current_controller.current_signal = self.current_signal.signal
            self.current_controller.set_current_signal()
            self.current_controller.pre_signal_viewer.play_timer()
            self.current_controller.post_signal_viewer.play_timer()
            # self.current_controller.replay_signal_viewers()
            self.current_controller.compute_new_filter(self.current_controller.designer_viewer.zeros_list,self.current_controller.designer_viewer.poles_list)
      
    def update_speed(self, value):
        """Update the timer speed based on slider value."""
        # self.speed_slider.setText(f"Speed: {value}ms")
        self.timer.setInterval(150)

class MouseTrackingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setMouseTracking(True)  # Enable mouse tracking
        self.mouse_position = None  # Store the current mouse position
        self.signal_data_y = []  # Store signal data (y-values)
        self.signal_data_x = []  # Store signal data (x-values)
        self.time_step = 0  # Time step for signal generation

        # Create a QTimer instance
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.generate_signal)

    def mouseMoveEvent(self, event):
        """Capture mouse movement and update the mouse position."""
        self.mouse_position = event.pos()  # Get the mouse position relative to the widget
        self.update()  # Trigger a repaint (optional, if you want to visualize the mouse position)

    def generate_signal(self):
        """Generate a signal based on the current mouse position."""
        if self.mouse_position is None:
            return  # Exit if no mouse position is available

        # Use the mouse position relative to the widget
        cursor_pos = self.mouse_position

        # Calculate amplitude based on the y-coordinate of the mouse
        amplitude = 2 * (self.height() / 2 - cursor_pos.y())

        # Update the time step based on the x-coordinate of the mouse
        self.time_step += 0.1 * min(1, (10 + cursor_pos.x()) / 1300)

        # Generate the signal value
        signal_value = amplitude

        # Print the signal values (for debugging)
        print(f"Time: {self.time_step}, Amplitude: {amplitude}")

        # Store the signal values
        self.signal_data_y.append(signal_value)
        self.signal_data_x.append(self.time_step)

    def toggle_timer(self, checked):
        """Start or stop the timer based on the checkbox state."""
        if checked:
            self.timer.start(50)  # Start the timer with a 50 ms interval
        else:
            self.timer.stop()  # Stop the timer

    def paintEvent(self, event):
        """Draw the canvas border and optionally the mouse position."""
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        # Optionally, draw a small circle at the mouse position
        if self.mouse_position:
            painter.setPen(QPen(Qt.red, 2))
            painter.drawEllipse(self.mouse_position, 5, 5)  # Draw a circle with radius 5


if __name__ == "__main__":
    app = QApplication([])
    window = MouseTrackingCanvas()
    window.show()
    app.exec_()