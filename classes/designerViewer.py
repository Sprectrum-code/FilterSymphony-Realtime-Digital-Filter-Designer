import pyqtgraph as pg 
import numpy as np
from PyQt5 import QtCore
from classes.Viewer import Viewer
from classes.pole import Pole
from classes.zero import Zero
from enums.types import Type
from enums.modesEnum import Mode
from copy import deepcopy
class DesignerViewer(pg.PlotItem):
    def __init__(self):
        super().__init__()
        self.poles_list = []
        self.zeros_list = []
        self.current_mode = Mode.ADD
        self.current_type = Type.ZERO
        # self.setBackground((30, 41, 59))
        self.showGrid(x= True, y= True , alpha = 0.25)
        
        self.setAspectLocked(True)
        self.setAcceptDrops(True)
        self.plot_unit_circle()
        
        self.dragPoint = None
        self.dragIndex = -1
        self.conjIndex = -1
        self.dragOffset = 0
        self.plot_item_control = None
        
        #events
    def plot_unit_circle(self):
        theta = np.linspace(0, 2 * np.pi, 500)
        x = np.cos(theta)  
        y = np.sin(theta)  
        self.plot(x, y, pen=pg.mkPen('b', width=2), name="Unit Circle")
        
    def add_element(self,coordinates:tuple, conjugate:bool = True):
        if self.current_type == Type.POLE:
            new_pole = Pole(coordinates)
            self.addItem(new_pole)
            if conjugate:
                conj_coordinates = (coordinates[0], -coordinates[1])
                conj_pole = Pole(conj_coordinates)
                new_pole.conjugate = conj_pole
                conj_pole.conjugate = new_pole
                self.addItem(conj_pole)
            pole_tuple = (new_pole, new_pole.conjugate)
            self.poles_list.append(pole_tuple)
        else:
            new_zero = Zero(coordinates)
            self.addItem(new_zero)
            if conjugate:
                conj_coordinates = (coordinates[0], -coordinates[1])
                conj_zero = Zero(conj_coordinates)
                new_zero.conjugate = conj_zero
                conj_zero.conjugate = new_zero
                self.addItem(conj_zero)
            zero_tuple = (new_zero, new_zero.conjugate)
            self.zeros_list.append(zero_tuple)
            
        
    def mouseDoubleClickEvent(self,event):
        local_pos = self.vb.mapSceneToView(event.scenePos())
        x, y = local_pos.x(), local_pos.y()
        if self.current_mode == Mode.ADD:
            self.add_element((x,y))
        elif self.current_mode == Mode.DELETE:
            pass
        elif self.current_mode == Mode.REPLACE:
            pass
        elif self.current_mode == Mode.DRAG:
            pass
        
        print(f"Clicked at: x={x}, y={y}")
        
    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.RightButton:
            event.ignore()
            return
        else:
            # pos = event.buttonDownScenePos(QtCore.Qt.RightButton)
            local_pos = self.vb.mapSceneToView(event.scenePos())
            for i , item in enumerate(self.dataItems):
                if i != 0:
                    if abs(item.real - local_pos.x()) < 0.05 and abs(item.imaginary - local_pos.y()) < 0.05:
                        self.remove_item(item)
                        break
        
    def mouseDragEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton: # ignoring anything not the left button 
            event.ignore()
            return
        if event.isStart():
            pos = event.buttonDownScenePos()
            local_pos = self.vb.mapSceneToView(pos)
            for i, item in enumerate(self.dataItems):
                if i != 0:
                    if abs(item.real - local_pos.x()) < 0.05 and abs(item.imaginary - local_pos.y()) < 0.05:
                        self.dragPoint = item
                        self.dragIndex = i
                        self.dragOffset = item.pos() - local_pos
                        event.accept()
        elif event.isFinish(): # end of the dragging event 
            self.dragPoint = None
            self.dragIndex = -1
            return
        else: # this is the dragging itself
            if self.dragPoint is None: # we are not dragging a point 
                event.ignore()
                return
            else: # we are dragging a point
                local_pos = self.vb.mapSceneToView(event.scenePos())
                ###### here we must put the function that updates the points again
                data_list = self.listDataItems()
                data_list[self.dragIndex].real = local_pos.x()
                data_list[self.dragIndex].imaginary = local_pos.y()
                if data_list[self.dragIndex].conjugate:
                    data_list[self.dragIndex].conjugate.real = local_pos.x()
                    data_list[self.dragIndex].conjugate.imaginary = -local_pos.y()
                self.update()
                
    def remove_item(self, item):
        self.removeItem(item)
        if item.conjugate is not None:
            self.removeItem(item.conjugate)
        if isinstance(item, Zero):
            self.zeros_list.remove((item, item.conjugate))
        else:
            self.poles_list.remove((item, item.conjugate))
        self.update()
                
    def remove_all_zeros(self):
        for (item, conj_item) in self.zeros_list:
            if isinstance(item,Zero):
                self.removeItem(item)
                if conj_item:
                    self.removeItem(conj_item)
        self.zeros_list.clear()
        
    def remove_all_poles(self):
        for (item, conj_item) in self.poles_list:
            if isinstance(item,Pole):
                self.removeItem(item)
                if conj_item:
                    self.removeItem(conj_item)
        self.poles_list.clear()
                
    def remove_all(self):
        self.remove_all_zeros()
        self.remove_all_poles()
        
    def swap(self, mode_text):
        if mode_text == "Poles - Zeros":
            for (item, conj_item) in self.poles_list:
                new_zero_conj = None
                new_zero = Zero((item.real, item.imaginary))
                self.removeItem(item)
                self.addItem(new_zero)
                if conj_item:
                    new_zero_conj = Zero((conj_item.real, conj_item.imaginary))
                    new_zero.conjugate = new_zero_conj
                    new_zero_conj.conjugate = new_zero
                    self.removeItem(conj_item)
                    self.addItem(new_zero_conj)
                self.zeros_list.append((new_zero, new_zero_conj))
        else:
            for (item, conj_item) in self.zeros_list:
                new_pole_conj = None
                new_pole = Pole((item.real, item.imaginary))
                self.removeItem(item)
                self.addItem(new_pole)
                if conj_item:
                    new_pole_conj = Pole((conj_item.real, conj_item.imaginary))
                    new_pole.conjugate = new_pole_conj
                    new_pole_conj.conjugate = new_pole
                    self.removeItem(conj_item)
                    self.addItem(new_pole_conj)
                self.poles_list.append((new_pole, new_pole_conj))
        


        
