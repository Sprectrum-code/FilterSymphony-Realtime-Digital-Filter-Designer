import pyqtgraph as pg 
import numpy as np
from PyQt5 import QtCore
from classes.Viewer import Viewer
from classes.pole import Pole
from classes.zero import Zero
from enums.types import Type
from enums.modesEnum import Mode
from copy import deepcopy
import pandas as pd
class DesignerViewer(pg.PlotItem):
    def __init__(self , controller):
        super().__init__()
        self.poles_list = []
        self.zeros_list = []
        self.current_mode = Mode.ADD
        self.current_type = Type.ZERO
        self.conjugate_mode = True
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
        
        self.controller = controller
        
        self.undo_stack = [([],[])]
        self.redo_stack = []
        #events
    def plot_unit_circle(self):
        theta = np.linspace(0, 2 * np.pi, 500)
        x = np.cos(theta)  
        y = np.sin(theta)  
        self.plot(x, y, pen=pg.mkPen('b', width=2), name="Unit Circle")
        
    def push_in_undo_stack(self):
        print("pushed")
        new_zeros_list = []
        new_poles_list = []
        for (zero, conj) in self.zeros_list:
            new_zero = Zero((zero.real, zero.imaginary))
            if conj:
                new_conj = Zero((conj.real, conj.imaginary))
                new_conj.conjugate = new_zero
                new_zero.conjugate = new_conj
            new_zeros_list.append((new_zero, new_zero.conjugate))
        for (pole, conj) in self.poles_list:
            new_pole = Pole((pole.real, pole.imaginary))
            if conj:
                new_conj = Pole((conj.real, conj.imaginary))
                new_conj.conjugate = new_pole
                new_pole.conjugate = new_conj
            new_poles_list.append((new_pole, new_pole.conjugate))
        self.undo_stack.append((new_poles_list, new_zeros_list))
        
        
        
    def undo(self):
        circle = self.dataItems[0]
        if len(self.undo_stack) <= 1:
            self.clear()
            self.addItem(circle)
            # self.zeros_list.clear()
            # self.poles_list.clear()
        
        else:
            redoed_state = self.undo_stack.pop(-1)
            print("inundo")
            last_state = self.undo_stack[-1]
            # self.redo_stack.append(last_state)
            another_poles_list, another_zeros_list = [x for x in last_state[0]], [x for x in last_state[1]]
            self.poles_list, self.zeros_list = another_poles_list, another_zeros_list
            another_poles_list_redoed, another_zeros_list_redoed = [x for x in redoed_state[0]], [x for x in redoed_state[1]]
            # self.poles_list, self.zeros_list = another_poles_list, another_zeros_list
            
            
            self.redo_stack.append((another_poles_list_redoed, another_zeros_list_redoed))
            # self.redo_stack.append((another_poles_list, another_zeros_list))
            self.clear()
            self.addItem(circle)
            for (pole,conj_pole) in self.poles_list:
                self.addItem(pole)
                if conj_pole:
                    self.addItem(conj_pole)
            for (zero,conj_zero) in self.zeros_list:
                self.addItem(zero)
                if conj_zero:
                    self.addItem(conj_zero)
            self.update()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        
    def redo(self):
        if len(self.redo_stack):
            circle = self.dataItems[0]
            last_state = self.redo_stack.pop(-1)
            another_poles_list, another_zeros_list = [x for x in last_state[0]], [x for x in last_state[1]]
            self.poles_list, self.zeros_list = another_poles_list, another_zeros_list
            self.clear()
            self.addItem(circle)
            for (pole,conj_pole) in self.poles_list:
                self.addItem(pole)
                if conj_pole:
                    self.addItem(conj_pole)
            for (zero,conj_zero) in self.zeros_list:
                self.addItem(zero)
                if conj_zero:
                    self.addItem(conj_zero)
            self.update()
            self.push_in_undo_stack()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        
        
    def add_element(self,coordinates:tuple, conjugate:bool = True):
        if self.current_type == Type.POLE:
            new_pole = Pole(coordinates)
            self.addItem(new_pole)
            if self.conjugate_mode:
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
            if self.conjugate_mode:
                conj_coordinates = (coordinates[0], -coordinates[1])
                conj_zero = Zero(conj_coordinates)
                new_zero.conjugate = conj_zero
                conj_zero.conjugate = new_zero
                self.addItem(conj_zero)
            zero_tuple = (new_zero, new_zero.conjugate)
            self.zeros_list.append(zero_tuple)
        # self.undo_stack.append((deepcopy(self.poles_list),deepcopy(self.zeros_list), deepcopy(self.dataItems)))
        self.redo_stack.clear()
        self.push_in_undo_stack()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        
    def mouseDoubleClickEvent(self,event):
        local_pos = self.vb.mapSceneToView(event.scenePos())
        x, y = local_pos.x(), local_pos.y()
        if self.current_mode == Mode.ADD:
            self.add_element((x,y))
            # self.push_in_undo_stack()
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
            # self.undo_stack.append((self.poles_list, self.zeros_list, self.dataItems))
            self.redo_stack.clear()
            self.push_in_undo_stack()
            print("app")
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
                self.controller.compute_new_filter(self.zeros_list, self.poles_list)
                self.update()
                # print("appended")
    
    def remove_item(self, item):
        self.removeItem(item)
        if item.conjugate is not None:
            self.removeItem(item.conjugate)
        if isinstance(item, Zero):
            self.zeros_list.remove((item, item.conjugate))
        else:
            self.poles_list.remove((item, item.conjugate))
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        self.update()
        self.redo_stack.clear()
        self.push_in_undo_stack()
        
        # self.undo_stack.append((deepcopy(self.poles_list), deepcopy(self.zeros_list), deepcopy(self.dataItems)))
                
    def remove_all_zeros(self):
        for (item, conj_item) in self.zeros_list:
            if isinstance(item,Zero):
                self.removeItem(item)
                if conj_item:
                    self.removeItem(conj_item)
        self.zeros_list.clear()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        # self.undo_stack.append((deepcopy(self.poles_list), deepcopy(self.zeros_list), deepcopy(self.dataItems)))
        self.push_in_undo_stack()
        self.redo_stack.clear()

    def remove_all_poles(self):
        for (item, conj_item) in self.poles_list:
            if isinstance(item,Pole):
                self.removeItem(item)
                if conj_item:
                    self.removeItem(conj_item)
        self.poles_list.clear()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        # self.undo_stack.append((deepcopy(self.poles_list), deepcopy(self.zeros_list), deepcopy(self.dataItems)))
        self.push_in_undo_stack()
        self.redo_stack.clear()
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
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        # self.undo_stack.append((deepcopy(self.poles_list), deepcopy(self.zeros_list), deepcopy(self.dataItems)))
        self.redo_stack.clear()
        self.push_in_undo_stack()
        
    def export_current_filter(self):
        real_zeros_list, imaginary_zeros_list, real_poles_list, imaginary_poles_list, zero_conj_list, pole_conj_list = [],[],[],[],[],[]
        for (zero, conj_zero) in self.zeros_list:
            real_zeros_list.append(zero.real)
            imaginary_zeros_list.append(zero.imaginary)
            if conj_zero:
                zero_conj_list.append('True')
            else:
                zero_conj_list.append('False')
        for (pole, conj_pole) in self.poles_list:
            real_poles_list.append(pole.real)
            imaginary_poles_list.append(pole.imaginary)
            if conj_pole:
                pole_conj_list.append('True')
            else:
                pole_conj_list.append('False')
        diff = abs(len(real_zeros_list) - len(real_poles_list))
        if diff > 0:
            if len(real_zeros_list) > len(real_poles_list):
                for _ in range(diff):
                    real_poles_list.append(None)
                    imaginary_poles_list.append(None)
                    pole_conj_list.append(None)
            else:
                for _ in range(diff):
                    real_zeros_list.append(None)
                    imaginary_zeros_list.append(None)
                    zero_conj_list.append(None)
        filter_data = { 'zero_real':real_zeros_list,
                        'zero_imaginary':imaginary_zeros_list,
                        'zero_has_conj':zero_conj_list,
                        'pole_real':real_poles_list,
                        'pole_imaginary':imaginary_poles_list,
                        'pole_has_conj':pole_conj_list}
        df = pd.DataFrame(filter_data)
        df.to_csv("exported_filter.csv", index=False)
        
    def import_filter(self, file_path):
        filter_df = pd.read_csv(file_path)
        for _, row in filter_df.iterrows():
            if pd.notnull(row['zero_real']) and pd.notnull(row['zero_imaginary']):
                zero = Zero((row['zero_real'], row['zero_imaginary']))
                self.addItem(zero)
                if row['zero_has_conj'] == True: 
                    print("iam conj")
                    conj_zero = Zero((row['zero_real'], -row['zero_imaginary']))
                    zero.conjugate = conj_zero
                    conj_zero.conjugate = zero
                    self.addItem(conj_zero)
                data_element = (zero, zero.conjugate)
                self.zeros_list.append(data_element)
            if pd.notnull(row['pole_real']) and pd.notnull(row['pole_imaginary']):
                pole = Pole((row['pole_real'], row['pole_imaginary']))
                self.addItem(pole)
                if row['pole_has_conj'] == True: 
                    conj_pole = Pole((row['pole_real'], -row['pole_imaginary']))
                    pole.conjugate = conj_pole
                    conj_pole.conjugate = pole
                    self.addItem(conj_pole)
                data_element = (pole, pole.conjugate)
                self.poles_list.append(data_element)
        self.update()
        self.controller.compute_new_filter(self.zeros_list, self.poles_list)
        self.redo_stack.clear()
        self.push_in_undo_stack()


        
