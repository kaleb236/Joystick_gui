import sys
import math
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from joystick import Ui_MainWindow

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

class ui_windows(QMainWindow):
    def __init__(self):
        super(ui_windows, self).__init__()
        self.ui = Ui_MainWindow()
        self.mouse_tracking = False
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.print_mouse_position)
        self.ui.joystick_btn.setDisabled(True)
        self.linear_vel = 0.5
        self.angular_vel = 1
        self.lin_vel = 0
        self.ang_vel = 0
        self.X1, self.Y1 = self.ui.joystick_btn.geometry().x(), self.ui.joystick_btn.geometry().y()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.timer.start(1)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.ui.joystick_btn.move(self.X1, self.Y1)
            self.ang_vel, self.lin_vel = 0.00, 0.00
            print(-round(self.lin_vel, 2), round(self.ang_vel, 2))
            self.timer.stop()
        
    def print_mouse_position(self):
        mouse_pos = self.mapFromGlobal(self.cursor().pos())
        button_geo = self.ui.joystick_btn.geometry()
        limit_geo = self.ui.joy_frame.geometry()
        cx = limit_geo.x() + limit_geo.width()/2
        cy = limit_geo.y() + limit_geo.height()/2
        d = math.sqrt((mouse_pos.x() - cx)**2 + (mouse_pos.y() - cy)**2)
        if d <= limit_geo.height()/2:
            x = int(mouse_pos.x()-button_geo.width()/2)
            y = int(mouse_pos.y()-button_geo.height()/2)
            # if x + button_geo.width() >= limit_geo.x() + limit_geo.width():
            #     x = limit_geo.x() + limit_geo.width() - button_geo.width() 
            # elif x <= limit_geo.x():
            #     x = limit_geo.x()
            # if y + button_geo.height() >= limit_geo.y() + limit_geo.height():
            #     y = limit_geo.y() + limit_geo.height() - button_geo.height() 
            # elif y <= limit_geo.y():
            #     y = limit_geo.y()
            max_linear_vel = limit_geo.x() + limit_geo.width() - cx
            max_angular_vel = limit_geo.y() + limit_geo.height() - cy
            self.ang_vel = ((x + button_geo.width()/2) - cx) * self.angular_vel / max_linear_vel
            self.lin_vel = ((y + button_geo.height()/2) - cy) * self.linear_vel / max_angular_vel
            print(-round(self.lin_vel, 2), round(self.ang_vel, 2))
            self.ui.joystick_btn.move(x, y)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ui_windows()

    win.show()
    sys.exit(app.exec_())