import sys
import pymysql

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# LOGIN WINDOW FUNCTIONALITY #
##############################
class login_window(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        # References QWidget parent object
        super().__init__(*args, **kwargs)

        # START OF GUI CODE #
        #####################

        # Window settings
        self.setWindowTitle("Welcome to Algonquin University")          # window title
        self.setGeometry(400, 400, 1000, 500)                               # window size
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1000)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(500)
        self.setMinimumHeight(500)
        # Window Icon
        self.setWindowIcon(qtg.QIcon('images\ALGONQUIN UNIVERSITY.png'))

        # AU right side image
        au_img = qtw.QLabel(self)
        pixmap = qtg.QPixmap("images\ALGONQUIN UNIVERSITY.png")
        au_img.setPixmap(pixmap)
        au_img.setGeometry(500, 0, 500, 500)

        # Login button
        self.login_b = qtw.QPushButton("Login", self)
        self.login_b.setGeometry(120, 300, 251, 41)
        self.login_b.setStyleSheet(("background-color: rgb(180, 145, 76);\n"
                                    "font: 12pt \"Montserrat SemiBold\";\n"
                                    "color: white;\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius: 5px;"))
        # self.login_b.clicked.connect(self.login)

        # "Login" label and underline
        l_lbl = qtw.QLabel("Login", self)
        l_lbl.setGeometry(120, 60, 50, 25)
        l_lbl.setStyleSheet("background-color: white;\n"
                                 "font: 10pt \"Montserrat SemiBold\";\n"
                                 "color: rgb(57, 24, 71);\n"
                                 "border-style: outset;\n")
        l_uline = qtw.QLabel("", self)
        l_uline.setGeometry(120, 90, 50, 2)
        l_uline.setStyleSheet("background-color: rgb(57, 24, 71);\n")

        # "New Account" label and underline
        na_b = qtw.QPushButton("New Account", self)
        na_b.setGeometry(248, 60, 120, 25)
        na_b.setStyleSheet("background-color: white;\n"
                                "font: 10pt \"Montserrat\";\n"
                                "color: rgb(57, 24, 71);\n"
                                "border-style: outset;\n")
        na_uline = qtw.QLabel("", self)
        na_uline.setGeometry(248, 90, 120, 1)
        na_uline.setStyleSheet("background-color: rgb(57, 24, 71);\n")
        # na_b.clicked.connect(self.open)

        # END OF GUI CODE #
        ###################
        self.show()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    widget = login_window()
    sys.exit(app.exec_())