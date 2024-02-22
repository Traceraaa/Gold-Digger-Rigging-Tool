import sys
from PySide2.QtWidgets import QWidget, QLineEdit
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication



class SimpleUI(QWidget):
    def __init__(self, parent=None):
        super(SimpleUI, self).__init__(parent)

        # Load the created UI widget .ui file from Qt Designer
        loader = QUiLoader()

        self.widget = loader.load("E:/Unreal_Projects/UnrealPy/UE_IDE/QtGui/Renamer.ui")


        # Check if the widget was loaded successfully
        if self.widget is not None:
            self.widget.setParent(self)
        else:
            print("Failed to load UI file")

        # Set the UI geometry (if UI is not centered/visible)
        self.widget.setGeometry(0, 0, self.widget.width(),self.widget.height())

        # Find the interactino element (XML structure)
        self.text_l = self.widget.findChild(QLineEdit)





app = None
if not QApplication.instance():
    app = QApplication(sys.argv)

main_window = SimpleUI()
main_window.show()