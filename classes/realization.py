import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter


class DigitalFilterRealization(QWidget):
    def __init__(self, print_button, frame, type):
        super().__init__()

        # Main layout
        self.central_widget = frame
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.realization_type = type
        self.zeros= [1,1,1,1,1]
        self.poles = [1,1,1]
        self.x_delays= []
        self.y_delays = []
        self.zeros_cascade = []
        self.poles_cascade = []
        # Create Graphics Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Add "Generate" button
        self.generate_button = QPushButton("Generate Filter Diagram")
        self.generate_button.clicked.connect(self.draw_cascaded_form)
        # self.layout.addWidget(self.generate_button)

        # Add "Save as PDF" button
        self.save_button =  QPushButton("Save as PDF")
        self.save_button.clicked.connect(self.save_as_pdf)
        self.layout.addWidget(self.save_button)

    def format_complex_number(self, num):
        """
        Format a complex number:
        - Remove the imaginary part if it's zero.
        - Round real and imaginary parts to two decimal places.
        """
        real_part = round(num.real, 2)
        imag_part = round(num.imag, 2)

        if imag_part == 0:
            return f"{real_part}"
        else:
            return f"{real_part} + {imag_part}j"

    def format_zeros_poles(self, zeros, poles):
        """
        Format the zeros and poles lists:
        - Remove imaginary part if zero.
        - Round to two decimal places.
        """
        self.zeros = [self.format_complex_number(z) for z in zeros]
        self.poles = [self.format_complex_number(p) for p in poles]

    def set_coefficients(self, zeros, poles):
        """
        Compute the numerator and denominator coefficients from zeros and poles.
        """
        # Extract zeros and poles from the lists
        zeros = [zero.real + 1j * zero.imaginary for (zero, _) in zeros]
        poles = [pole.real + 1j * pole.imaginary for (pole, _) in poles]

        # Compute numerator coefficients from zeros
        numerator_coeffs = np.poly(zeros)  # [b_M, b_{M-1}, ..., b_0]

        # Compute denominator coefficients from poles
        denominator_coeffs = np.poly(poles)  # [a_N, a_{N-1}, ..., a_0]

        # Normalize denominator coefficients so that a0 = 1
        denominator_coeffs = denominator_coeffs / denominator_coeffs[0]

        # Reverse coefficients to get them in ascending order of z^{-1}
        self.zeros = numerator_coeffs[::-1]  # [b0, b1, b2, ...]
        self.poles = denominator_coeffs[::-1]  # [a0, a1, a2, ...]

        self.format_zeros_poles(self.zeros, self.poles)

    import numpy as np

    def decompose_to_cascade(self, zeros, poles):
        """
        Decompose the filter into a cascade of second-order sections (SOS).
        Each section is a quadratic equation.
        """
        # Convert inputs to NumPy arrays and ensure they contain finite values
        zeros = np.asarray(zeros, dtype=complex)
        poles = np.asarray(poles, dtype=complex)

        # Check for non-finite values (e.g., NaN, Inf)
        if not np.all(np.isfinite(zeros)) or not np.all(np.isfinite(poles)):
            raise ValueError("Input zeros and poles must contain only finite values.")

        # Ensure the number of zeros and poles is even
        if len(zeros) % 2 != 0:
            zeros = np.append(zeros, 0)  # Add a zero if odd
        if len(poles) % 2 != 0:
            poles = np.append(poles, 0)  # Add a pole if odd

        # Pair zeros and poles into second-order sections
        sos = []
        for i in range(0, len(zeros), 2):
            zero_pair = zeros[i:i + 2]
            pole_pair = poles[i:i + 2]

            # Compute coefficients for the quadratic section
            b = np.poly(zero_pair)  # Numerator coefficients
            a = np.poly(pole_pair)  # Denominator coefficients

            # Normalize so that a[0] = 1
            a = a / a[0]

            # Append the section to the SOS list
            sos.append((b, a))

        return sos
    def draw_realization(self, zeros, poles):
            self.set_coefficients(zeros, poles)

            # Decompose into cascade form
            # sos = self.decompose_to_cascade(zeros, poles)
            # self.zeros_cascade = [section[0] for section in sos]  # Store cascade zeros
            # self.poles_cascade = [section[1] for section in sos]  # Store cascade poles

            if self.realization_type == "direct1":
                self.draw_direct_form_1()
            elif self.realization_type == "direct2":
                self.draw_direct_form_2()
            elif self.realization_type == "cascade":
                self.draw_cascaded_form()
    
            
    def draw_directform_2(self):
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.white)
        # Parameters
        box_width, box_height = 50, 30
        delay_distance = 100
        line_length = 50       
        input_text = self.scene.addText("x[n]")
        input_text.setPos(5, 140)
        self.add_line(10, (1+1)*delay_distance-25,0.5*delay_distance+10, (1+1)*delay_distance-25)
        input_text.setDefaultTextColor(Qt.blue)
        
        
        output_text = self.scene.addText("y[n]")
        output_text.setPos(4*delay_distance+35, 140)
        output_text.setDefaultTextColor(Qt.blue)

        # Connect to output
        self.add_line(3.5*delay_distance+25, (1+1)*delay_distance-25, 4*delay_distance+50, (1+1)*delay_distance-25)
        
        for i in range(1, max(len(self.zeros),len(self.poles))):
            if i == len(self.zeros):
                self.add_line(2*delay_distance+25, (i+1)*delay_distance-25,2*delay_distance+25, (i+2)*delay_distance-40)  ## vertical line connecting delays
            else:                 
                self.add_line(2*delay_distance+25, (i+1)*delay_distance-25,2*delay_distance+25, (i+2)*delay_distance-25)  ## vertical line c
            delay = self.add_block(2*delay_distance, (i+1)*delay_distance, f"z⁻{i}") ##delay blocks
            self.x_delays.append(delay)
            # self.add_line(0.5*delay_distance-5,(i+1)*100-25,delay_distance+25,(i+1)*100-25)
            
        for i in range(1,len(self.zeros)):
            self.add_line(3.5*delay_distance+40, (i+1)*100-10,3.5*delay_distance+40, (i+2)*100-40) #vertical lines connecting summation
            self.add_line(2*delay_distance+25,(i+1)*100-25,3.5*delay_distance+25,(i+1)*100-25,  text = f"{self.zeros[i-1]}")
            self.add_summation_circle(3.5*delay_distance+25, (i+1)*100-40)

        self.add_line(2*delay_distance+25,(i+2)*100-40, 3.5*delay_distance+40, (i+2)*100-40, text = f"{self.zeros[i]}")


        for i in range(1,len(self.poles)):
            self.add_line(0.5*delay_distance-5,(i+1)*100-25,2*delay_distance+25,(i+1)*100-25,text = f"{self.poles[i-1]}")
            self.add_line(0.5*delay_distance+10, (i+1)*100-10,0.5*delay_distance+10, (i+2)*100-25) #vertical line connectiong summation
            self.add_summation_circle(0.5*delay_distance-5, (i+1)*100-40)
            
        self.add_line(0.5*delay_distance+10,(i+2)*100-25,2*delay_distance+25, (i+2)*100-25,text = f"{self.poles[i]}")

        ## Handle if zeros not eqaul poles
    def draw_cascaded_form(self):
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.white)
        # Parameters
        box_width, box_height = 50, 30
        delay_distance = 100
        line_length = 50       
        input_text = self.scene.addText("x[n]")
        input_text.setPos(10, 160)
        self.add_line(0.5*delay_distance, (1+1)*delay_distance-25,delay_distance, (1+1)*delay_distance-25)
        input_text.setDefaultTextColor(Qt.white)
                     

        
        zeros_count = len(self.zeros)
        poles_count = len(self.poles)
        component_count = 1
        blocks_count = max(zeros_count, poles_count)
        while (blocks_count >=0):
            self.add_line(component_count*delay_distance, (1+1)*delay_distance-25, component_count*delay_distance + line_length, (1+1)*delay_distance-25)    
            self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25)
            self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25)
        

            if blocks_count >= 2:
                #first delay element
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, text= "z^-1")
                #second delay
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+2*line_length, text= "z^-1")
            if blocks_count<2:
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, text= "z^-1")
            blocks_count -= 2
            component_count +=2
            
        output_text = self.scene.addText("y[n]")
        output_text.setPos((component_count-1)*delay_distance + 2*line_length, 160)
        output_text.setDefaultTextColor(Qt.white)
        # Connect to output
        self.add_line((component_count-1)*delay_distance , (1+1)*delay_distance-25, (component_count-1)*delay_distance + 2*line_length, (1+1)*delay_distance-25)
        
        
        component_count = 1       
        while(zeros_count>0):
            if zeros_count>= 2:
               #zero coeffients b 1
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, text = f"{self.zeros[-zeros_count]}")
                self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25)
                
                #zero coeffients b 2
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + 3*line_length,(1+1)*delay_distance-25+2*line_length, text = f"{self.zeros[-zeros_count+1]}")
                self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length)

            if zeros_count< 2:
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, text = f"{self.zeros[-zeros_count]}")
                self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25)
              
            zeros_count -= 2
            component_count +=2
            
            pass
        
        component_count = 1       
        while(poles_count>0):
            if poles_count>= 2:
                #pole coeffients a 1
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length,component_count*delay_distance + line_length , (1+1)*delay_distance-25+line_length, text = f"{self.poles[-poles_count]}")
                self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + line_length, (1+1)*delay_distance-25)
                
                #pole coeffients a 2
                self.add_line(component_count*delay_distance + 2*line_length,(1+1)*delay_distance-25+2*line_length,component_count*delay_distance + line_length , (1+1)*delay_distance-25+2*line_length, text = f"{self.poles[-poles_count+1]}")
                self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + line_length, (1+1)*delay_distance-25+line_length)
            if poles_count<2:
                #pole coeffients a 1
                self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length,component_count*delay_distance + line_length , (1+1)*delay_distance-25+line_length, text = f"{self.poles[-poles_count]}")
                self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + line_length, (1+1)*delay_distance-25)
            self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 4*line_length, (1+1)*delay_distance-25)
  
            poles_count -= 2
            component_count +=2
        
        # while(zeros_count >= 2 and poles_count >= 2):
        #     self.add_line(component_count*delay_distance, (1+1)*delay_distance-25, component_count*delay_distance + line_length, (1+1)*delay_distance-25, text= "1")
            
        #     self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, text="2")
        #     self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25, text = "3")
        #     #first delay element
        #     self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, text= "z^-1")
        #     #second delay
        #     self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+2*line_length, text= "z^-1")
            
            # #pole coeffients a 1
            # self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length,component_count*delay_distance + line_length , (1+1)*delay_distance-25+line_length, text="4")
            # self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + line_length, (1+1)*delay_distance-25, text= "z^-1")

            #zero coeffients b 1
            # self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, text = "5")
            # self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25, text= "z^-1")
            
            # #pole coeffients a 2
            # self.add_line(component_count*delay_distance + 2*line_length,(1+1)*delay_distance-25+2*line_length,component_count*delay_distance + line_length , (1+1)*delay_distance-25+2*line_length)
            # self.add_line(component_count*delay_distance + line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + line_length, (1+1)*delay_distance-25+line_length)


            #zero coeffients b 2
            # self.add_line(component_count*delay_distance + 2*line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + 3*line_length,(1+1)*delay_distance-25+2*line_length)
            # self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+2*line_length, component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25+line_length)

            # self.add_line(component_count*delay_distance + 3*line_length, (1+1)*delay_distance-25, component_count*delay_distance + 4*line_length, (1+1)*delay_distance-25, text= "1")

            
            # component_count +=2
            # zeros_count -=2
            # poles_count -=2
            # print(f"poles: {poles_count}, zeros: {zeros_count}")
            
    def draw_direct_form_1(self):
        

        # Parameters
        box_width, box_height = 50, 30
        delay_distance = 100
        line_length = 50

        # Draw Input
        input_text = self.scene.addText("x[n]")
        input_text.setPos(10, 160)
        self.add_line(50, (1+1)*100-25,100+25, (1+1)*100-25)
        input_text.setDefaultTextColor(Qt.blue)
        input_text.setFont(self.font)

        # Output
        output_text = self.scene.addText("y[n]")
        output_text.setPos(750, 160)
        output_text.setDefaultTextColor(Qt.blue)
        input_text.setFont(self.font)

        # Connect to output
        self.add_line(600+25, (1+1)*100-25, 750, (1+1)*100-25)
        if len(self.zeros)> 0:
            for i in range(1, len(self.zeros)):
            # First Delay Block (z^-1)
                if i == len(self.zeros):
                    self.add_line(100+25, (i+1)*100-25,100+25, (i+2)*100-40)  ## vertical line connecting delays
                else:                 
                    self.add_line(100+25, (i+1)*100-25,100+25, (i+2)*100-25)  ## vertical line connecting delays

                self.add_line(100+25, (i+1)*100-25,300+25, (i+1)*100-25, text = f"{self.zeros[i-1]}") ## horizontal line connecting z and sum
                self.add_summation_circle(300+25, (i+1)*100-40)
                self.add_line(300+40, (i+1)*100-10,300+40, (i+2)*100-40) # vertical lines connecting summation

                x_delay = self.add_block(100, (i+1)*100, f"z⁻{i}")
            
                self.x_delays.append(x_delay)
            self.add_line(100+25,(i+2)*100-40, 300+40, (i+2)*100-40, f"{self.zeros[i]}")
            self.add_line(300+55, 200-25,400+25, 200-25)
        else:
            self.add_line(125, 200-25,300+55, 200-25)
            self.add_line(300+55, 200-25,400+25, 200-25)


        if len(self.poles)>0:
            for i in range(1, len(self.poles)):
            # First Delay Block (z^-1)
                if i == len(self.poles):
                    self.add_line(400+25, (i+1)*100-25,400+25, (i+2)*100-40)  ## vertical line connecting delays
                else:                 
                    self.add_line(400+25, (i+1)*100-25,400+25, (i+2)*100-25)  ## vertical line connecting delays

                self.add_line(400+25, (i+1)*100-25,400+25, (i+2)*100-25)
                self.add_line(400+25, (i+1)*100-25,600+25, (i+1)*100-25, text = f"{self.poles[i-1]}")
                self.add_summation_circle(410, (i+1)*100-40)
                self.add_line(600+25, (i+1)*100-22,600+25, (i+2)*100-22)

                y_delay = self.add_block(600, (i+1)*100, f"z⁻{i}")
            
                self.y_delays.append(y_delay)
            self.add_line(400+25,(i+2)*100-22, 600+25, (i+2)*100-22, f"{self.poles[i]}")
        else:
            self.add_line(400+25,(1+1)*100-25, 600+25, (1+1)*100-25)


    def add_block(self, x, y, text):
        """Add a block (e.g., z^-1)"""
        block = QGraphicsRectItem(x, y, 50, 30)
        block.setBrush(QBrush(Qt.lightGray))
        self.scene.addItem(block)
        
        block_text = self.scene.addText(text)
        block_text.setPos(x + 15, y + 5)
        print(block.y())
        block_text.setDefaultTextColor(Qt.black)
        return block

    def add_line(self, x1, y1, x2, y2, text=None):
        """Add a connecting line"""
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(QPen(Qt.black, 4))
        if text is not None:
            line_text = self.scene.addText(text)
            line_text.setPos((x1 + x2)//2, (y1 + y2)//2)
            line_text.setFont(self.text_font)

        self.scene.addItem(line)
    def add_summation_circle(self, x, y):
        """Add a summation circle"""
        summation = QGraphicsEllipseItem(x, y, 40, 40)
        summation.setPen(QPen(Qt.white, 5))
        summation.setBrush(QBrush(Qt.white))
        self.scene.addItem(summation)
        plus = self.scene.addText(" + ")
        plus.setPos(x + 10, y + 5)
        plus.setDefaultTextColor(Qt.black)

    def add_multiplier(self, x, y, text):
        """Add a multiplier block"""
        multiplier = QGraphicsRectItem(x, y, 50, 30)
        multiplier.setBrush(QBrush(Qt.lightGray))
        self.scene.addItem(multiplier)
        multiplier_text = self.scene.addText(text)
        multiplier_text.setPos(x + 15, y + 5)
        multiplier_text.setDefaultTextColor(Qt.black)

    def save_as_pdf(self):
        """Save the scene as a PDF"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save as PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
        )
        if file_path:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            # Render the scene to the printer
            painter = QPainter(printer)
            self.scene.render(painter)
            painter.end()
            print(f"Saved diagram as {file_path}")




 




if __name__ == "__main__":
    from PyQt5.QtGui import QPainter
    app = QApplication(sys.argv)
    window = DigitalFilterRealization()
    window.show()
    sys.exit(app.exec_())
