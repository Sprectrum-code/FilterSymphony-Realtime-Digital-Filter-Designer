import sys
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem,
    QGraphicsTextItem, QGraphicsEllipseItem, QMainWindow, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF


class DirectForm1Realization(QMainWindow):
    def __init__(self, numerator_coeffs, denominator_coeffs):
        super().__init__()

        # Coefficients
        self.numerator_coeffs = numerator_coeffs  # [b0, b1, b2, ...]
        self.denominator_coeffs = denominator_coeffs  # [a0, a1, a2, ...]

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create Graphics Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Draw the Direct Form I realization
        self.draw_direct_form_1()

    def draw_direct_form_1(self):
        """Draw the Direct Form I realization of the digital filter."""
        # Parameters
        box_width, box_height = 50, 30
        delay_distance = 100
        line_length = 50
        y_offset = 100

        # Draw input
        input_text = self.scene.addText("x[n]")
        input_text.setPos(10, y_offset)
        input_text.setDefaultTextColor(Qt.black)

        # Draw input line
        self.add_line(50, y_offset, 150, y_offset)

        # Draw input delays and multipliers
        x_pos = 150
        for i, b in enumerate(self.numerator_coeffs):
            # Draw delay block
            self.add_delay_block(x_pos, y_offset, f"z⁻{i + 1}")
            x_pos += delay_distance

            # Draw multiplier
            self.add_multiplier(x_pos, y_offset, f"b{i}")
            x_pos += delay_distance

            # Draw line to next block
            self.add_line(x_pos, y_offset, x_pos + line_length, y_offset)
            x_pos += line_length

        # Draw output side
        x_pos = 150
        y_offset += 100  # Move down for output side

        # Draw output line
        self.add_line(50, y_offset, 150, y_offset)

        # Draw output delays and multipliers
        for i, a in enumerate(self.denominator_coeffs[1:], start=1):  # Skip a0 (always 1)
            # Draw delay block
            self.add_delay_block(x_pos, y_offset, f"z⁻{i}")
            x_pos += delay_distance

            # Draw multiplier
            self.add_multiplier(x_pos, y_offset, f"a{i}")
            x_pos += delay_distance

            # Draw line to next block
            self.add_line(x_pos, y_offset, x_pos + line_length, y_offset)
            x_pos += line_length

        # Draw output
        output_text = self.scene.addText("y[n]")
        output_text.setPos(x_pos, y_offset)
        output_text.setDefaultTextColor(Qt.black)

    def add_line(self, x1, y1, x2, y2, text=None):
        """Add a connecting line with optional text."""
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(QPen(Qt.black, 2))
        self.scene.addItem(line)

        if text is not None:
            text_item = self.scene.addText(text)
            text_item.setDefaultTextColor(Qt.black)
            text_item.setPos((x1 + x2) // 2, (y1 + y2) // 2)

    def add_delay_block(self, x, y, label):
        """Add a delay block with a label."""
        block = QGraphicsRectItem(x, y, 50, 30)
        block.setBrush(QBrush(Qt.lightGray))
        self.scene.addItem(block)

        text = self.scene.addText(label)
        text.setPos(x + 10, y + 5)
        text.setDefaultTextColor(Qt.black)

    def add_multiplier(self, x, y, label):
        """Add a multiplier with a label."""
        multiplier = QGraphicsEllipseItem(x, y, 30, 30)
        multiplier.setBrush(QBrush(Qt.lightGray))
        self.scene.addItem(multiplier)

        text = self.scene.addText(label)
        text.setPos(x + 5, y + 5)
        text.setDefaultTextColor(Qt.black)


if __name__ == "__main__":
    # Example coefficients
    numerator_coeffs = [1, -1.5, 0.7]  # b0, b1, b2
    denominator_coeffs = [1, -1.2, 0.5]  # a0, a1, a2

    app = QApplication(sys.argv)
    window = DirectForm1Realization(numerator_coeffs, denominator_coeffs)
    window.setGeometry(100, 100, 800, 400)
    window.show()
    sys.exit(app.exec_())