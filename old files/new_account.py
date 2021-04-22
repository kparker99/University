# Algonquin University New Account Creation Window

import pymysql
import string

import stylesheets as s
import sql_functions as sql

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


# MYSQL CONNECTION
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()

# PREVENTS DUPLICATE USER_ID & ENTERS INTO MYSQL
def enter_user_id(un, pw1):
    counter = 1
    c.execute("SELECT user_id FROM university.login WHERE user_id=%s", (un))
    n = c.fetchone()
    while n != None:
        if not un[-1].isdigit():
            try:
                un = un + str(counter)
                sql.enter_into_db("INSERT INTO university.login (user_id, password) VALUES (%s,%s)", (un, pw1))
                # TODO: change code so it only tries to access the username, and does not try to enter information into the database
                return un
            except pymysql.Error as error:
                print(error.args)
                continue
        else:
            counter += 1
            un = un.rstrip(string.digits) + str(counter)
            c.execute("SELECT user_id FROM university.login WHERE user_id=%s", (un))
            n = c.fetchone()
    sql.enter_into_db("INSERT INTO university.login (user_id, password) VALUES (%s,%s)", (un, pw1))  # move this into the enter_into_db function
    email = un + '@au.edu'
    return email

# NEW ACCOUNT WINDOW CLASS
class NEW_ACCT(qtw.QWidget):
    def __init__(self):
        super().__init__()

# WINDOW SIZE/STYLE/ICON
        self.setWindowTitle("Create Account")
        self.setGeometry(300, 300, 1150, 500)
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1150)
        self.setMaximumWidth(1150)
        self.setMaximumHeight(500)
        self.setMinimumHeight(500)
        self.setWindowIcon(qtg.QIcon('images\ALGONQUIN UNIVERSITY.png'))

# PURPLE BANNER
        self.banner = qtw.QLabel(self)
        self.banner.setStyleSheet("background-color: rgb(57, 24, 71);\n")
        self.banner.setGeometry(0, 0, 1150, 50)

# "GOLD" CREATE ACCOUNT BUTTON
        self.login_b = qtw.QPushButton("Create Account", self)
        self.login_b.setGeometry(120, 390, 911, 41)
        self.login_b.setStyleSheet(s.large_button_style(self))
        self.login_b.clicked.connect(self.enter_into_db)

# "NEW ACCOUNT" BUTTON & UNDERLINE
        self.na_b = qtw.QLabel("New Account", self)
        self.na_b.setGeometry(120, 60, 120, 25)
        self.na_b.setStyleSheet("background-color: white;\n"
                                 "font: 10pt \"Montserrat SemiBold\";\n"
                                 "color: rgb(57, 24, 71);\n"
                                 "border-style: outset;\n")
        self.na_uline = qtw.QLabel("", self)
        self.na_uline.setGeometry(120, 90, 120, 2)
        self.na_uline.setStyleSheet("background-color: rgb(57, 24, 71);\n")


# WORDS ABOVE TEXT FIELDS

    # column 1
        self.lbl1 = qtw.QLabel("First Name", self)
        self.lbl1.setGeometry(120, 120, 191, 16)
        self.lbl1.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl2 = qtw.QLabel("Last Name", self)
        self.lbl2.setGeometry(120, 210, 191, 16)
        self.lbl2.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl3 = qtw.QLabel("Telephone Number", self)
        self.lbl3.setGeometry(120, 300, 205, 16)
        self.lbl3.setStyleSheet(s.text_label_stylesheet(self))

        self.opt = qtw.QLabel("*optional", self)
        self.opt.setGeometry(260, 300, 205, 16)
        self.opt.setStyleSheet(s.text_label_stylesheet(self))
    # column 2
        self.lbl4 = qtw.QLabel("Street Address", self)
        self.lbl4.setGeometry(450, 120, 191, 16)
        self.lbl4.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl5 = qtw.QLabel("City", self)
        self.lbl5.setGeometry(450, 210, 191, 16)
        self.lbl5.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl6 = qtw.QLabel("State", self)
        self.lbl6.setGeometry(450, 300, 191, 16)
        self.lbl6.setStyleSheet(s.text_label_stylesheet(self))
    # column 3
        self.lbl7 = qtw.QLabel("Date of Birth", self)
        self.lbl7.setGeometry(780, 120, 191, 16)
        self.lbl7.setStyleSheet(s.text_label_stylesheet(self))

        self.opt = qtw.QLabel("(yyyy-mm-dd)", self)
        self.opt.setGeometry(880, 120, 100, 16)
        self.opt.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl8 = qtw.QLabel("Enter Password", self)
        self.lbl8.setGeometry(780, 210, 191, 16)
        self.lbl8.setStyleSheet(s.text_label_stylesheet(self))

        self.lbl9 = qtw.QLabel("Confirm Password", self)
        self.lbl9.setGeometry(780, 300, 191, 16)
        self.lbl9.setStyleSheet(s.text_label_stylesheet(self))

    # TODO: Make it so you can only enter letters in f_name and l_name; put password requirements
    # TODO: create function to make 9 text fields

    ### TEXT FIELDS
    # column 1
        self.f_name = qtw.QLineEdit("Kyle", self)
        self.f_name.setGeometry(120, 140, 250, 31)
        self.f_name.setStyleSheet(s.line_edit_stylesheet(self))

        self.l_name = qtw.QLineEdit("Parker", self)
        self.l_name.setGeometry(120, 230, 250, 31)
        self.l_name.setStyleSheet(s.line_edit_stylesheet(self))

        self.phone = qtw.QLineEdit("", self)
        self.phone.setGeometry(120, 320, 250, 31)
        self.phone.setStyleSheet(s.line_edit_stylesheet(self))
        self.phone.setInputMask("999-999-9999")
    # column 2
        self.street = qtw.QLineEdit("123 Main St", self)
        self.street.setGeometry(450, 140, 250, 31)
        self.street.setStyleSheet(s.line_edit_stylesheet(self))

        self.city = qtw.QLineEdit("Algonquin", self)
        self.city.setGeometry(450, 230, 250, 31)
        self.city.setStyleSheet(s.line_edit_stylesheet(self))

        self.state = qtw.QLineEdit("IL", self)
        self.state.setGeometry(450, 320, 250, 31)
        self.state.setStyleSheet(s.line_edit_stylesheet(self))
        self.state.setInputMask("AA")
    # column 3
        self.dob = qtw.QLineEdit("1991-01-01", self)
        self.dob.setGeometry(780, 140, 250, 31)
        self.dob.setStyleSheet(s.line_edit_stylesheet(self))
        self.dob.setInputMask("9999-99-99")

        self.pw1 = qtw.QLineEdit("123", self)
        self.pw1.setGeometry(780, 230, 250, 31)
        self.pw1.setStyleSheet(s.line_edit_stylesheet(self))
        self.pw1.setEchoMode(qtw.QLineEdit.Password)

        self.pw2 = qtw.QLineEdit("123", self)
        self.pw2.setGeometry(780, 320, 250, 31)
        self.pw2.setStyleSheet(s.line_edit_stylesheet(self))
        self.pw2.setEchoMode(qtw.QLineEdit.Password)

# POP UP WINDOW FEATURE
    def pop_up_message(self, title, message):
        m = qtw.QMessageBox()
        m.setWindowTitle(title)
        m.setText(message)
        m.exec_()

# ENTER FIELDS INTO SQL DB
    def enter_into_db(self):
        """enters new account into mysql database"""
        f_name = self.f_name.text()
        l_name = self.l_name.text()
        street = self.street.text()
        city = self.city.text()
        state = self.state.text()
        dob = self.dob.text()
        phone = self.phone.text()
        pw1 = self.pw1.text()
        pw2 = self.pw2.text()
        possible_username_unformatted = f_name[0] + l_name
        possible_username = possible_username_unformatted.lower()

        # test both password fields match
        if pw1 == pw2:
            email = enter_user_id(possible_username, pw1)
            username = email[:-7]
            sql.enter_into_db("INSERT INTO university.person (role_id, user_id, f_name, l_name, address, city, state, dob, email, phone) \
                              VALUES (1,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (username, f_name, l_name, street, city, state, dob, email, phone))
#TODO: find a way to catch error if someone is trying to enter an invalid entry (possibly put it in the entry requirements for each field
            self.pop_up_message("Confirmation", "Account created successfully" + "\n" + "Your username is: " + username)
            self.close()
        else:
            self.pop_up_message("Error", "Passwords do not match")

