# Algonquin University Teacher Main Window

import pymysql

import class_enrollment

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

# MYSQL CONNECTION #
####################
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()


# MAIN STUDENT WINDOW GUI AND FUNCTIONS #
#########################################
class MAIN_T(qtw.QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user
        query_statement = "SELECT f_name, l_name FROM university.person WHERE user_id=%s"
        db_query = c.execute(query_statement, self.user)
        name = c.fetchone()

        # MAIN STUDENT WINDOW GUI #
        ###########################
        # WINDOW SIZE/STYLE/ICON
        self.setWindowTitle("Welcome to Algonquin University")  # window title
        self.setGeometry(200, 100, 1400, 800)  # window size
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1400)
        self.setMinimumHeight(800)
        self.setMaximumWidth(1400)
        self.setMaximumHeight(800)
        self.setWindowIcon(qtg.QIcon('images\ALGONQUIN UNIVERSITY.png'))  # create AU window icon

        # GOLD BANNER
        self.banner = qtw.QLabel("Teacher site to be completed...", self)
        self.banner.setStyleSheet("background-color: rgb(180, 145, 76);\n")
        self.banner.setGeometry(0, 0, 1400, 140)

