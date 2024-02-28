import sys
import os

# from .Arm_Rig import ArmRigFunctions
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QLabel, QSlider, QPushButton
from PySide2.QtCore import QSize, Qt

#
# module_dir = "E:/MayaTools/Gold-Digger-Rigging-Tool/"
# sys.path.append(module_dir)

class RiggingToolMain(QMainWindow):
    def __init__(self, parent=None):
        super(RiggingToolMain, self).__init__(parent)
        self.setWindowTitle("Quick Rigging Tool")
        self.setFixedSize(QSize(450, 580))

        # self._armrig = ArmRigFunctions.instance()

        # Load the created UI widget .ui file from Qt Designer
        loader = QUiLoader()

        self.ui_file_path = "E:/MayaTools/Gold-Digger-Rigging-Tool/ui_files/rigging_tool.ui"
        # load ui file
        self.widget = loader.load(self.ui_file_path)

        # Check if the widget was loaded successfully
        if self.widget is not None:
            self.widget.setParent(self)
        else:
            print("Failed to load UI file")

        # Set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(), self.widget.height())

        # Find the interaction element (XML structure)
        self.label_arm_pieces = self.widget.findChild(QLabel, "l_arm_pieces_value")
        self.slider_arm_pieces = self.findChild(QSlider, "horizontalSlider")
        self.btn_initialize = self.findChild(QPushButton, "btn_initialize")
        self.btn_initialize.setCheckable(True)

        # signal
        self.slider_arm_pieces.valueChanged.connect(self.set_arm_piece_value)
        self.btn_initialize.clicked.connect(self.initialize_arm)

    """
    Codes goes here
    """

    # Start of slots
    def set_arm_piece_value(self, value):
        self.label_arm_pieces.setText(str(value))

    def initialize_arm(self):
        self.btn_initialize.setEnabled(False)
        self.slider_arm_pieces.setEnabled(False)
        # TODO import arm rig functions initialize()


    def close_window(self):
        """
        Close window
        """
        print("close windows")
        self.destroy()





def open_window():

    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if "RiggingToolMainWindow" in win.objectName():
                win.destroy()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    RiggingToolMain.window = RiggingToolMain(parent=mayaMainWindow)
    RiggingToolMain.window.setObjectName("RiggingToolMainWindow")
    RiggingToolMain.window.setWindowTitle(" GD Rigging Tool")
    RiggingToolMain.window.show()



    # app = None
    #
    # if not QApplication.instance():
    #     app = QApplication(sys.argv)
    #
    # main_window = RiggingToolMain()
    # main_window.show()
