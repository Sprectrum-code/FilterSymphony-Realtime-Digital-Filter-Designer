import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QVBoxLayout, QStackedWidget , QHBoxLayout , QFrame ,QSlider, QPushButton, QComboBox, QCheckBox, QFileDialog, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from helper_function.compile_qrc import compile_qrc
from classes.signalViewer import SignalViewer
from classes.controller import Controller
from classes.customSignal import CustomSignal
from classes.designerViewer import DesignerViewer 
from classes.digitalFiltersLibrary import DigitalFilters
from classes.allPassFiltersLibrary import allPassFiltersLibrary
from classes.filterCodeGenerator import FilterCodeGenerator
from classes.touch import MouseTrackingCanvas
from classes.touch import RealTimeSignal
from classes.realization import DigitalFilterRealization
import numpy as np
import pyqtgraph as pg
from enums.modesEnum import Mode
from enums.types import Type
from classes.Viewer import Viewer

# compile_qrc()
from icons_setup.compiledIcons import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Realtime Digital Filter Designer')
        self.setWindowIcon(QIcon('icons_setup\icons\logo.png'))
        
        # Initialize Program pages
        self.Pages = self.findChild(QStackedWidget, 'pages') 
    
        self.drawing_page = self.findChild(QWidget, 'drawingPage')
        self.drawing_page_index = self.Pages.indexOf(self.findChild(QWidget , 'drawingPage')) 

        self.all_pass_page = self.findChild(QWidget, 'allpassFilters')
        self.all_pass_page_index = self.Pages.indexOf(self.findChild(QWidget , 'allpassFilters')) 
    
        self.all_pass_page = self.findChild(QWidget, 'allpassFilters')
        self.all_pass_page_index = self.Pages.indexOf(self.findChild(QWidget , 'allpassFilters')) 

        self.home_page = self.findChild(QWidget,'homePage')
        self.home_page_index = self.Pages.indexOf(self.findChild(QWidget , 'homePage')) 
        
        # Initialize traverse_pages_buttons
        self.to_drawing_page_button = self.findChild(QPushButton , "signalDrawing")
        self.to_drawing_page_button.clicked.connect(self.go_to_drawing_page)
        
        self.to_realization_page_button = self.findChild(QPushButton,"filterRealization")
        self.to_realization_page_button.clicked.connect(self.go_to_realization_page)

        self.to_allpassfilters_page_button = self.findChild(QPushButton , "filters")
        self.to_allpassfilters_page_button.clicked.connect(self.go_to_all_pass_filters_page)
        
        self.to_home_page_from_draw_page = self.findChild(QPushButton, "backHome2")
        self.to_home_page_from_draw_page.clicked.connect(self.go_to_home_from_drawing)

        self.to_home_page_from_ap_button = self.findChild(QPushButton , "backHome3")
        self.to_home_page_from_ap_button.clicked.connect(self.go_to_main_page_from_ap)
        
        # self.to_home_page_from_signal_page_button = self.findChild(QPushButton , "backHome2")
        # self.to_home_page_from_signal_page_button.clicked.connect(self.go_to_main_page_from_signal

        # Initializing the signal viewer
        self.pre_signal_viewer = SignalViewer()
        self.post_signal_viewer = SignalViewer()
        
        # Initialize all pass page viewers
        self.ap_filter_phase_viewer = Viewer()
        self.ap_corrected_phase_viewer = Viewer()

        self.generator = FilterCodeGenerator()
        
        self.cCodeGenerator = self.findChild(QPushButton, "cCodeGenerator")
        self.cCodeGenerator.clicked.connect(self.download_c_code)
        
        # Initialize signal page viewers and frames will not be used
        self.signal_page_pre_viewer = SignalViewer()
        self.signal_page_post_viewer = SignalViewer()
        
        self.signal_page_pre_viewer_frame = self.findChild(QFrame , "frame_4")
        self.signal_page_pre_viewer_layout = QVBoxLayout()
        self.signal_page_pre_viewer_frame.setLayout(self.signal_page_pre_viewer_layout)
                
        self.signal_page_post_viewer_frame = self.findChild(QFrame , "frame_5")
        self.signal_page_post_viewer_layout = QVBoxLayout()
        self.signal_page_post_viewer_frame.setLayout(self.signal_page_post_viewer_layout)
        #modified by deeb to add the viewers into the drawing page
        
        
        # Initialize all pass page viewer frames
        self.ap_filter_phase_viewer_frame = self.findChild(QFrame , "frame_11")
        self.ap_filter_phase_viewer_layout = QVBoxLayout()
        self.ap_filter_phase_viewer_frame.setLayout(self.ap_filter_phase_viewer_layout)
        self.ap_filter_phase_viewer_layout.addWidget(self.ap_filter_phase_viewer)
        
        # Initialize all pass page viewer frames
        self.ap_corrected_phase_viewer_frame = self.findChild(QFrame , "frame_12")
        self.ap_corrected_phase_viewer_layout = QVBoxLayout()
        self.ap_corrected_phase_viewer_frame.setLayout(self.ap_corrected_phase_viewer_layout)
        self.ap_corrected_phase_viewer_layout.addWidget(self.ap_corrected_phase_viewer)
        
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
        x = np.linspace(0, 10 * np.pi, 10000)
        y = np.sin(2*np.pi*x)
        self.current_signal = CustomSignal(x , y)
        
        # Initialize the controller
        self.controller = Controller(self.pre_signal_viewer , self.post_signal_viewer, self.current_signal , self.ap_filter_phase_viewer , self.ap_corrected_phase_viewer ,  self.signal_page_pre_viewer , self.signal_page_post_viewer)
        
        # initialize the filter designer viewer
        self.designer_viewer = DesignerViewer(self.controller)
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.graphics_layout.setBackground((30, 41, 59))
        self.graphics_layout.addItem(self.designer_viewer)
        self.designer_frame = self.findChild(QFrame,"unitCircleFrame")
        self.designer_frame_layout = QVBoxLayout()
        self.designer_frame.setLayout(self.designer_frame_layout)
        self.designer_frame_layout.addWidget(self.graphics_layout)
        
        # Initialize Digital Filters Library
        self.digital_filters_library = DigitalFilters()
        
        # Initialize browse signal button
        self.browse_signal_button = self.findChild(QPushButton , "pushButton_11")
        self.browse_signal_button.clicked.connect(self.browse_signal)
        
        # Initialize play and pause buttons
        self.signal_viewer_play_pause_button = self.findChild(QPushButton , "playPause")
        self.signal_viewer_play_pause_button.clicked.connect(self.toggle_play_pause_signal_viewers)
        
        # Initialize the replay button
        self.replay_signal_viewers_button = self.findChild(QPushButton , "replay")
        self.replay_signal_viewers_button.clicked.connect(self.replay_signal_viewers)
        
        # initialize the zero pole combo box 
        self.add_element_combobox = self.findChild(QComboBox, "addComboBox")
        self.add_element_combobox.currentIndexChanged.connect(self.add_element_combobox_listener)
        
        # initialize the removing combobox 
        self.removal_combobox = self.findChild(QComboBox,"removeComboBox")
        # self.removal_combobox.currentIndexChanged.connect(self.remove_listener)
        
        self.removal_button = self.findChild(QPushButton, "pushButton_18")
        self.removal_button.clicked.connect(self.remove_listener)
        
        self.swap_combobox = self.findChild(QComboBox, "swapComboBox")
        self.swap_combobox.setDisabled(True)
        # self.swap_combobox.currentIndexChanged.connect(self.swap_listener)
        
        self.swap_button = self.findChild(QPushButton, "pushButton_27")
        self.swap_button.clicked.connect(self.swap_listener)
        
        self.conjugates_checkbox = self.findChild(QCheckBox, "addConjugates")
        self.conjugates_checkbox.setChecked(True)
        self.conjugates_checkbox.stateChanged.connect(self.conjugates_listener)
        
        # Initialize signal viewers speed modifiers
        self.signal_viewers_speed_slider = self.findChild(QSlider , "speedSlider")
        self.signal_viewers_speed_slider.setRange(10,100)
        self.signal_viewers_speed_slider.setValue(50)
        self.signal_viewers_speed_slider.sliderMoved.connect(self.modify_signal_viewers_speed)
        
        # Initialize signal page viewers speed modifiers
        self.signal_page_viewers_speed_slider = self.findChild(QSlider , "horizontalSlider")
        self.signal_page_viewers_speed_slider.setRange(10,100)
        self.signal_page_viewers_speed_slider.setValue(50)
        self.signal_page_viewers_speed_slider.sliderMoved.connect(self.modify_signal_page_viewers_speed)
        
        
        # undo_redo
        self.undo_button = self.findChild(QPushButton, "undo")
        self.undo_button.clicked.connect(self.designer_viewer.undo)
        self.redo_button = self.findChild(QPushButton, "redo")
        self.redo_button.clicked.connect(self.designer_viewer.redo)
        
        # controls initialization
        # self.add_zero_button = self.findChild(QPushButton, "addZero")
        # self.add_zero_button.clicked.connect(self.add_zero)
        # self.add_pole_button = self.findChild(QPushButton, "addPole")
        # self.add_pole_button.clicked.connect(self.add_pole)
        
        # Initialize digital filters buttons
        self.digital_filter_1_button = self.findChild(QPushButton , "pushButton_2")
        self.digital_filter_1_button.clicked.connect(self.get_digital_filter1_components)

        self.digital_filter_2_button = self.findChild(QPushButton , "pushButton_3")
        self.digital_filter_2_button.clicked.connect(self.get_digital_filter2_components)
        
        self.magnitude_viewer = Viewer()
        self.magnitude_signal_frame = self.findChild(QFrame, 'amplitudeFrame')
        self.magnitude_signal_frame_layout = QVBoxLayout()
        self.magnitude_signal_frame.setLayout(self.magnitude_signal_frame_layout)
        self.magnitude_signal_frame_layout.addWidget(self.magnitude_viewer)
        
        self.phase_viewer = Viewer()
        self.phase_signal_frame = self.findChild(QFrame, 'frequencyFrame')
        self.phase_signal_frame_layout = QVBoxLayout()
        self.phase_signal_frame.setLayout(self.phase_signal_frame_layout)
        self.phase_signal_frame_layout.addWidget(self.phase_viewer)
        
        self.controller.magnitude_viewer = self.magnitude_viewer
        self.controller.phase_viewer = self.phase_viewer
        self.controller.designer_viewer = self.designer_viewer
        
        self.export_button = self.findChild(QPushButton, 'save')
        self.export_button.clicked.connect(self.designer_viewer.export_current_filter)
        
        self.browse_filter_button = self.findChild(QPushButton, "browse")
        self.browse_filter_button.clicked.connect(self.browse_filter)
    
        self.digital_filter_3_button = self.findChild(QPushButton , "pushButton")
        self.digital_filter_3_button.clicked.connect(self.get_digital_filter3_components)

        self.digital_filter_4_button = self.findChild(QPushButton , "pushButton_5")
        self.digital_filter_4_button.clicked.connect(self.get_digital_filter4_components)

        self.digital_filter_5_button = self.findChild(QPushButton , "pushButton_6")
        self.digital_filter_5_button.clicked.connect(self.get_digital_filter5_components)

        self.digital_filter_6_button = self.findChild(QPushButton , "pushButton_4")
        self.digital_filter_6_button.clicked.connect(self.get_digital_filter6_components)

        self.digital_filter_7_button = self.findChild(QPushButton , "pushButton_9")
        self.digital_filter_7_button.clicked.connect(self.get_digital_filter7_components)

        self.digital_filter_8_button = self.findChild(QPushButton , "pushButton_8")
        self.digital_filter_8_button.clicked.connect(self.get_digital_filter8_components)

        self.digital_filter_9_button = self.findChild(QPushButton , "pushButton_7")
        self.digital_filter_9_button.clicked.connect(self.get_digital_filter9_components)

        self.digital_filter_10_button = self.findChild(QPushButton , "pushButton_10")
        self.digital_filter_10_button.clicked.connect(self.get_digital_filter10_components)
        
        self.all_pass_filters_library = allPassFiltersLibrary()
        
        self.custom_all_pass_combobox = self.findChild(QComboBox, "comboBox")
        self.custom_all_pass_input = self.findChild(QLineEdit, "lineEdit")
        
        self.add_custom_all_pass_button = self.findChild(QPushButton, "pushButton_26")
        self.add_custom_all_pass_button.clicked.connect(self.add_custom_all_pass_listener)
        
        self.apply_custom_all_pass_button = self.findChild(QPushButton, 'pushButton_28')
        self.apply_custom_all_pass_button.clicked.connect(self.apply_custom_all_pass)
        
        self.ap_filter1_button = self.findChild(QPushButton , "pushButton_21")
        self.ap_filter1_button.clicked.connect(self.apply_ap_filter_1)
    
        self.ap_filter2_button = self.findChild(QPushButton , "pushButton_16")
        self.ap_filter2_button.clicked.connect(self.apply_ap_filter_2)
    
        self.ap_filter3_button = self.findChild(QPushButton , "pushButton_22")
        self.ap_filter3_button.clicked.connect(self.apply_ap_filter_3)
    
        self.ap_filter4_button = self.findChild(QPushButton , "pushButton_17")
        self.ap_filter4_button.clicked.connect(self.apply_ap_filter_4)
    
        self.ap_filter5_button = self.findChild(QPushButton , "pushButton_23")
        self.ap_filter5_button.clicked.connect(self.apply_ap_filter_5)
        
        self.ap_filter6_button = self.findChild(QPushButton , "pushButton_20")
        self.ap_filter6_button.clicked.connect(self.apply_ap_filter_6)
    
        self.ap_filter7_button = self.findChild(QPushButton , "pushButton_24")
        self.ap_filter7_button.clicked.connect(self.apply_ap_filter_7)
    
        self.ap_filter8_button = self.findChild(QPushButton , "pushButton_15")
        self.ap_filter8_button.clicked.connect(self.apply_ap_filter_8)
    
        self.ap_filter9_button = self.findChild(QPushButton , "pushButton_25")
        self.ap_filter9_button.clicked.connect(self.apply_ap_filter_8)
    
        self.ap_filter10_button = self.findChild(QPushButton , "pushButton_19")
        self.ap_filter10_button.clicked.connect(self.apply_ap_filter_10)
    
        self.browse_signal_button = self.findChild(QPushButton, "pushButton_29")
        self.browse_signal_button.clicked.connect(self.browse_signal)

        #realization page
        self.cascade_form_frame = self.findChild(QFrame, "frame")
        self.direct_form_1_frame = self.findChild(QFrame, "frame_2")
        self.direct_form_2_frame = self.findChild(QFrame, "frame_3")
        
        self.print_cascade_button = self.findChild(QPushButton , "pushButton_14")
        self.print_form_1_button = self.findChild(QPushButton , "pushButton_12")
        self.print_form_2_button = self.findChild(QPushButton , "pushButton_13")
        
        self.direct_form_1_realization = DigitalFilterRealization(self.print_form_1_button, 
                                                                  self.direct_form_1_frame,
                                                                  "direct1")
        self.direct_form_2_realization = DigitalFilterRealization(self.print_form_2_button, 
                                                                  self.direct_form_2_frame,
                                                                  "direct2")
        self.cascade_form_realization = DigitalFilterRealization(self.print_cascade_button, 
                                                                  self.cascade_form_frame,
                                                                  "cascade")
        
 

        #draw page

        #Speed control
        self.draw_signal_speed_slider = self.findChild(QSlider, "horizontalSlider")
        self.draw_signal_tool = RealTimeSignal(self.draw_signal_speed_slider, self.controller)

        self.mouse_tracker_frame = self.findChild(QFrame, "frame_6")
        self.mouse_tracker_frame_layout = QVBoxLayout()
        self.mouse_tracker_frame.setLayout(self.mouse_tracker_frame_layout)
        self.mouse_tracker_frame_layout.addWidget(self.draw_signal_tool.canvas)
        #checkbox
        self.enable_drawing_checkbox = self.findChild(QCheckBox, "checkBox") 
        self.enable_drawing_checkbox.stateChanged.connect(self.turn_draw_mode)
    def add_custom_all_pass_listener(self):
        coef = float(self.custom_all_pass_input.text())
        self.all_pass_filters_library.make_custom_all_pass(coef)
        self.custom_all_pass_combobox.clear()
        for name in self.all_pass_filters_library.custom_filter_library.keys():
            self.custom_all_pass_combobox.addItem(name)
            
    def apply_custom_all_pass(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.custom_filter_library[self.custom_all_pass_combobox.currentText()])
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_1(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap1"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_2(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap2"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_3(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap3"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_4(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap4"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_5(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap5"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
        
    def apply_ap_filter_10(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap10"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_6(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap6"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_7(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap7"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_8(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap8"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    
    def apply_ap_filter_9(self):
        self.controller.handle_all_pass_zero_pole_list(self.all_pass_filters_library.get_filter("ap9"))
        self.controller.calculate_all_pass_filter_phase()
        self.controller.calculate_corrected_phase()
    # def apply_custom_all_pass(self):
    #     self.controller
    
    def get_digital_filter1_components(self):
        zeros , poles = self.digital_filters_library.butterworth_lowpass()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter2_components(self):
        zeros , poles = self.digital_filters_library.chebyshev1_lowpass()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter3_components(self):
        zeros , poles = self.digital_filters_library.chebyshev2_lowpass()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter4_components(self):
        zeros , poles = self.digital_filters_library.elliptic_lowpass()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter5_components(self):
        zeros , poles = self.digital_filters_library.bessel_lowpass()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter6_components(self):
        zeros , poles = self.digital_filters_library.notch_filter()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter7_components(self):
        zeros , poles = self.digital_filters_library.bandpass_filter()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter8_components(self):
        zeros , poles = self.digital_filters_library.highpass_filter()
        self.apply_digital_filter(zeros , poles)
    
    def get_digital_filter9_components(self):
        zeros , poles = self.digital_filters_library.bandstop_filter()
        zeros = sorted(zeros , key = lambda x: x[0])
        zeros = zeros[:4]
        current_mode = self.designer_viewer.current_mode
        current_type = self.designer_viewer.current_type
        current_conjugate_mode = self.designer_viewer.conjugate_mode
        
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.ZERO
        self.designer_viewer.conjugate_mode = True
        
        for zero in zeros:    
            self.designer_viewer.add_element(zero)
        self.designer_viewer.current_type = Type.POLE
        for pole in poles:
            self.designer_viewer.add_element(pole)

        self.designer_viewer.current_type = current_type
        self.designer_viewer.current_mode = current_mode
        self.designer_viewer.conjugate_mode = current_conjugate_mode    
    
    def get_digital_filter10_components(self):
        zeros , poles = self.digital_filters_library.gaussian_filter()
        self.apply_digital_filter(zeros , poles)
        
    def apply_digital_filter(self, zeros ,poles):
        zeros , poles = self.handle_zeros_and_poles_duplicates(zeros , poles)
        current_mode = self.designer_viewer.current_mode
        current_type = self.designer_viewer.current_type
        current_conjugate_mode = self.designer_viewer.conjugate_mode
        
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.ZERO
        self.designer_viewer.conjugate_mode = True
        
        for zero in zeros:    
            self.designer_viewer.add_element(zero)
        self.designer_viewer.current_type = Type.POLE
        for pole in poles:
            self.designer_viewer.add_element(pole)

        self.designer_viewer.current_type = current_type
        self.designer_viewer.current_mode = current_mode
        self.designer_viewer.conjugate_mode = current_conjugate_mode
        
    def handle_zeros_and_poles_duplicates(self , zeros , poles):
        zeros = sorted(zeros , key = lambda x: x[0])
        for idx , zero in enumerate(zeros):
            if (zeros[idx+1][0] == zeros[idx][0] and zeros[idx+1][1] == - zeros[idx][1]):
                zeros.pop(idx+1)
                idx = idx + 2
        poles = sorted(poles , key = lambda x: x[0])
        for idx , pole in enumerate(poles):
            if (poles[idx+1][0] == poles[idx][0] and poles[idx+1][1] == - poles[idx][1]):
                poles.pop(idx+1)
                idx = idx + 2
        return zeros , poles
        
    def toggle_play_pause_signal_viewers(self):
        self.controller.toggle_play_pause_signal_viewers(self.signal_viewer_play_pause_button)
    
    def replay_signal_viewers(self):
        self.controller.replay_signal_viewers()
        
    def modify_signal_viewers_speed(self , slider_speed_value):
        slider_speed_value = 110 - slider_speed_value
        self.controller.modify_signal_viewers_speed(slider_speed_value)
    
    def modify_signal_page_viewers_speed(self , slider_speed_value):
        slider_speed_value = 110 - slider_speed_value
        self.controller.modify_signal_page_viewers_speed(slider_speed_value)
        
    def add_element_combobox_listener(self):
        if self.add_element_combobox.currentText() == 'Zero':
            self.add_zero()
        else:
            self.add_pole()
    
    def add_zero(self):
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.ZERO
    def add_pole(self):
        self.designer_viewer.current_mode = Mode.ADD
        self.designer_viewer.current_type = Type.POLE
        
    def remove_listener(self):
        print(self.removal_combobox.currentText)
        if self.removal_combobox.currentText() == "Zeros":
            self.designer_viewer.remove_all_zeros()
            print("zero rem")
        elif self.removal_combobox.currentText() == "Poles":
            self.designer_viewer.remove_all_poles()
        else:
            self.designer_viewer.remove_all()
    
    def swap_listener(self):
        self.designer_viewer.swap(self.swap_combobox.currentText())
        
    def conjugates_listener(self):
        if self.conjugates_checkbox.isChecked():
            self.designer_viewer.conjugate_mode = True
        else:
            self.designer_viewer.conjugate_mode = False
    
    
    def browse_filter(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )

        if file_path:
            self.designer_viewer.import_filter(file_path)
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.")
               
    def go_to_all_pass_filters_page(self):
        page_index = self.Pages.indexOf(self.findChild(QWidget, 'allpassFilters'))
        if page_index != -1:
            self.Pages.setCurrentIndex(page_index)      
            # self.controller.calculate_all_pass_filter_phase()     
            self.controller.ap_corrected_phase_viewer.compute_phase(self.designer_viewer.poles_list , self.designer_viewer.zeros_list)

    def go_to_home_from_drawing(self):
        if self.home_page_index != -1:
            self.Pages.setCurrentIndex(self.home_page_index)
            self.pre_signal_viewer.setParent(None)
            self.post_signal_viewer.setParent(None)
            self.pre_signal_frame_layout.addWidget(self.pre_signal_viewer)
            self.post_signal_frame_layout.addWidget(self.post_signal_viewer)
        
            self.controller.toggle_play_pause_signal_viewers(self.signal_viewer_play_pause_button)
            self.controller.toggle_play_pause_signal_viewers(self.signal_viewer_play_pause_button)
            
    def go_to_drawing_page(self):
        if self.drawing_page_index != -1:
            self.Pages.setCurrentIndex(self.drawing_page_index) 
            
            self.pre_signal_viewer.setParent(None)
            self.post_signal_viewer.setParent(None)
            
            # Reuse the existing viewers from the home page
            self.signal_page_pre_viewer_layout.addWidget(self.pre_signal_viewer)
            self.signal_page_post_viewer_layout.addWidget(self.post_signal_viewer)
        
    
    def go_to_realization_page(self):
        page_index = self.Pages.indexOf(self.findChild(QWidget, 'realizationPage'))
        if page_index != -1:
            self.Pages.setCurrentIndex(page_index)      
        # we need to add functions that set the zeros and poles
        self.cascade_form_realization.draw_realization(self.designer_viewer.zeros_list, self.designer_viewer.poles_list)
        self.direct_form_1_realization.draw_realization(self.designer_viewer.zeros_list, self.designer_viewer.poles_list)
        self.direct_form_2_realization.draw_realization(self.designer_viewer.zeros_list, self.designer_viewer.poles_list)
        
    def go_to_main_page_from_ap(self):
        page_index = self.Pages.indexOf(self.findChild(QWidget, 'homePage'))
        if page_index != -1:
            self.Pages.setCurrentIndex(page_index)     
        # self.designer_viewer.zeros_list.extend(self.controller.original_all_pass_zeros_poles_list[1])
        if (self.controller.ap_filter_added):
            current_mode = self.designer_viewer.conjugate_mode
            current_type = self.designer_viewer.current_type
            self.designer_viewer.current_mode = False
            self.designer_viewer.current_type = Type.POLE
            self.designer_viewer.add_element((self.controller.original_all_pass_zeros_poles_list[0][0][0].real,self.controller.original_all_pass_zeros_poles_list[0][0][0].imaginary))
            self.designer_viewer.current_type = Type.ZERO
            self.designer_viewer.add_element((self.controller.original_all_pass_zeros_poles_list[1][0][0].real , self.controller.original_all_pass_zeros_poles_list[1][0][0].imaginary))
            self.designer_viewer.current_type = current_type
            self.designer_viewer.conjugate_mode = current_mode
            self.controller.compute_new_filter(self.designer_viewer.zeros_list,self.designer_viewer.poles_list)
            self.controller.compute_magnitude_and_phase()
            self.controller.all_pass_zeros_poles_list[0].clear()
            self.controller.all_pass_zeros_poles_list[1].clear()
            self.controller.original_all_pass_zeros_poles_list[0].clear()
            self.controller.original_all_pass_zeros_poles_list[1].clear()
            
    def download_c_code(self):
        self.generator.save_to_file(self.designer_viewer.poles_list, self.designer_viewer.zeros_list, "Filter.c")
        
    def turn_draw_mode(self):
        if self.enable_drawing_checkbox.isChecked():
            self.draw_signal_tool.canvas.toggle_timer(True)
            self.pre_signal_viewer.clear_viewer_content()
            self.post_signal_viewer.clear_viewer_content()
            # self.signal_page_pre_viewer.clear_viewer_content()
            # self.signal_page_post_viewer.clear_viewer_content()
            
        else:
            self.draw_signal_tool.canvas.toggle_timer(False)
        
    
    def browse_signal(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open CSV File", 
            "", 
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )

        if file_path:
            self.controller.browse_signal(file_path)
        else:
            QMessageBox.warning(self, "No File Selected", "Please select a valid CSV file.")   
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())