from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QProcess
# from mainwindow import Ui_MainWindow


import sys
sys.path.insert(0, '/home/viv/GitHub/Facial Recognition/Main/Adding and Upgrading/')
sys.path.insert(0, '/home/viv/GitHub/Facial Recognition//Main/Facial_Detection/')


from  Adding_Upgrading import UPAD
from Removing import remove
from Train_Scan import Scan
import os



class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'Admin' and
            self.textPass.text() == 'Password'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Not an Admin')

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        btn1 = QPushButton("Remove 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Live Feed  2", self)
        btn2.move(150, 50)

        btn3 = QPushButton("Update ", self)
        btn3.move(270, 50)

        btn1.clicked.connect(self.remover)
        btn2.clicked.connect(self.livefeed)
        btn3.clicked.connect(self.buttonClicked)


       # btn3.clicked.connect(self.buttonClicked) # +++

        self.statusBar()
    def remover(self):
        remove()

    def livefeed(self):
        Scan()



    def buttonClicked(self):
        UPAD()




        #self.btn3.clicked.connect(lambda :self.close())

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Example()
        window.show()
        sys.exit(app.exec_())

