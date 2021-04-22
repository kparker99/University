# Algonquin University Login Window

import sys
import pymysql

import new_account
import main_student
import main_teacher
import main_admin
import stylesheets as s
import sql_functions as sql

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# MYSQL CONNECTION
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()

class LOGIN(qtw.QWidget):
    def __init__(self):
        super().__init__()
        """creates GUI using pyqt5"""

        # WINDOW SIZE/STYLE/ICON
        self.setWindowTitle("Welcome to Algonquin University")          # window title
        self.setGeometry(400, 400, 1000, 500)                               # window size
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1000)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(500)
        self.setMinimumHeight(500)
        self.setWindowIcon(qtg.QIcon('images\ALGONQUIN UNIVERSITY.png'))    # create AU window icon

        # AU LOGO
        self.au_img = qtw.QLabel(self)
        pixmap = qtg.QPixmap("images\ALGONQUIN UNIVERSITY.png")
        self.au_img.setPixmap(pixmap)
        self.au_img.setGeometry(500, 0, 500, 500)

        # "GOLD" LOGIN BUTTON
        self.login_b = qtw.QPushButton("Login", self, clicked=self.login)
        self.login_b.setGeometry(120, 300, 251, 41)
        self.login_b.setStyleSheet(s.large_button_style(self))

        # CREATE "LOGIN" LABEL & UNDERLINE
        self.l_lbl = qtw.QLabel("Login", self)
        self.l_lbl.setGeometry(120, 60, 50, 25)
        self.l_lbl.setStyleSheet("background-color: white;\n"
                                 "font: 10pt \"Montserrat SemiBold\";\n"
                                 "color: rgb(57, 24, 71);\n"
                                 "border-style: outset;\n"
                                 )
        self.l_uline = qtw.QLabel("", self)
        self.l_uline.setGeometry(120, 90, 50, 2)
        self.l_uline.setStyleSheet("background-color: rgb(57, 24, 71);\n")

        # "NEW ACCOUNT" BUTTON & UNDERLINE
        self.na_b = qtw.QPushButton("New Account", self, clicked = self.create_new_account)
        self.na_b.setGeometry(248, 60, 120, 25)
        self.na_b.setStyleSheet("background-color: white;\n"
                                "font: 10pt \"Montserrat Regular\";\n"
                                "color: rgb(57, 24, 71);\n"
                                "border-style: outset;\n"
                                )
        self.na_uline = qtw.QLabel("", self)
        self.na_uline.setGeometry(248, 90, 120, 1)
        self.na_uline.setStyleSheet("background-color: rgb(57, 24, 71);\n")

        # "USERNAME" & "PASSWORD" WORDS ABOVE TEXT FIELDS
        self.un_lbl = qtw.QLabel("Username", self)
        self.un_lbl.setGeometry(120, 120, 191, 16)
        self.un_lbl.setStyleSheet(s.text_label_stylesheet(self))

        self.pw_lbl = qtw.QLabel("Password", self)
        self.pw_lbl.setGeometry(120, 210, 191, 16)
        self.pw_lbl.setStyleSheet(s.text_label_stylesheet(self))

        # USERNAME FIELD
        self.un_f = qtw.QLineEdit("kparker", self)
        self.un_f.setGeometry(120, 140, 250, 31)
        self.un_f.setStyleSheet(s.line_edit_stylesheet(self))
        self.un_f.setPlaceholderText("Username")

        # PASSWORD FIELD
        self.pw_f = qtw.QLineEdit("1234", self)
        self.pw_f.setGeometry(120, 230, 250, 31)
        self.pw_f.setStyleSheet(s.line_edit_stylesheet(self))
        self.pw_f.setEchoMode(qtw.QLineEdit.Password)
        self.pw_f.setPlaceholderText("Password")


    # LOGIN WINDOW FUNCTIONS #
    ##########################
    def create_new_account(self):
        """Opens "New Account window"""
        self.window = new_account.NEW_ACCT()
        self.window.show()

    def pop_up_message(self, title, message):
        """creates pop up message w/ custom title and message"""
        pop_up = qtw.QMessageBox()
        pop_up.setWindowTitle(title)
        pop_up.setText(message)
        pop_up.exec_()

    def login(self):
        """log into the application if username and password match existing record"""
        un = self.un_f.text()
        pw = self.pw_f.text()
        info = sql.get_info_from_db("SELECT * FROM university.login WHERE user_id=%s AND password=%s", (un,pw))
        # query = "SELECT * FROM university.login WHERE user_id=%s AND password=%s"
        # data=c.execute(query, (un, pw))
        if info != None:
            query = sql.get_info_from_db("SELECT role_id FROM university.person WHERE user_id=%s", un)
            role = query[0][0]
            if role == 1:
                self.window = main_student.MAIN_S(un)
                self.window.show()
            elif role == 2:
                self.window = main_teacher.MAIN_T(un)
                self.window.show()
            elif role == 3:
                self.window = main_admin.MAIN_A(un)
                self.window.show()
            else:
                self.pop_up_message("Error", "No database privileges: Please contact IT administrator")
        else:
            self.pop_up_message("Access Denied", "Username/Password Incorrect")


# APPLICATION EXECUTION #
#########################
app = qtw.QApplication(sys.argv)                                        # application object
window = LOGIN()                                                        # makes login class an object
window.show()                                                           # shows login class object

app.exec_()                                                             # execute application
sys.exit(0)                                                             # system exit
