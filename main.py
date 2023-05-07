from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.Qtci import *
from PyQt5.QtGui import *
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        ##body

        self.setWindowTitle("PyQt5 editor")
        self.resize(1300, 900)

        self.setStyleSheet(open("./src/css/style.css", "r").read())

        ##alternative consolel
        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(16)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()


        self.show()

    def set_up_menu(self):
        pass

    def set_up_body(self):
        pass    

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
       

