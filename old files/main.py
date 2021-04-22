# Algonquin University Main Student Window

import pymysql
import string

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


# MYSQL CONNECTION #
####################
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()


# MAIN LOGIN WINDOW CLASS FOR STUDENTS
class MAIN_S(QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user

        # WINDOW SIZE/STYLE/ICON
        self.setWindowTitle("Welcome to Algonquin University")  # window title
        self.setGeometry(200, 100, 1400, 800)  # window size
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.setWindowIcon(QIcon('images\ALGONQUIN UNIVERSITY.png'))  # create AU window icon

        # GOLD BANNER
        self.banner = QLabel(self)
        self.banner.setStyleSheet("background-color: rgb(180, 145, 76);\n")
        self.banner.setGeometry(0, 0, 1400, 150)

        # WELCOME
        self.banner = QLabel("Welcome " + self.user, self)
        self.banner.setStyleSheet(("font: 16pt \"Cinzel\";\n"
                                   "background-color: rgb(180, 145, 76);\n"
                                   "color: rgb(57, 24, 71);"))
        self.banner.setGeometry(30, 30, 300, 40)

        # LABELS
        self.enroll_b = QPushButton("ENROLL", self)
        self.enroll_b.setGeometry(120, 100, 125, 24)
        self.enroll_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                     "background-color: rgb(180, 145, 76);\n"
                                     "border-style: outset;\n"
                                     "color: white;"))
        self.enroll_b.clicked.connect(self.enroll)

        self.profile_b = QPushButton("PROFILE", self)
        self.profile_b.setGeometry(300, 100, 125, 24)
        self.profile_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                      "background-color: rgb(180, 145, 76);\n"
                                      "border-style: outset;\n"
                                      "color: white;"))
        self.profile_b.clicked.connect(self.profile)

        self.grades_b = QPushButton("GRADES", self)
        self.grades_b.setGeometry(480, 100, 125, 24)
        self.grades_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                     "background-color: rgb(180, 145, 76);\n"
                                     "border-style: outset;\n"
                                     "color: white;"))
        self.grades_b.clicked.connect(self.grades)

        # UNDERLINES
        self.e_uline = QLabel("", self)
        self.e_uline.setGeometry(133, 130, 98, 3)
        self.e_uline.setStyleSheet("background-color: white;\n")
        self.e_uline.hide()

        self.p_uline = QLabel("", self)
        self.p_uline.setGeometry(313, 130, 98, 3)
        self.p_uline.setStyleSheet("background-color: white;\n")
        self.p_uline.hide()

        self.g_uline = QLabel("", self)
        self.g_uline.setGeometry(493, 130, 98, 3)
        self.g_uline.setStyleSheet("background-color: white;\n")
        self.g_uline.hide()

        # TABLES
        self.e_table = QTableWidget(self)
        self.e_table.setGeometry(120, 200, 550, 160)
        self.e_table.setRowCount(0)
        self.e_table.setColumnCount(2)
        self.e_table.hide()

        self.p_table = QTableWidget(self)
        self.p_table.setGeometry(120, 200, 1000, 160)
        self.p_table.setRowCount(0)
        self.p_table.setColumnCount(8)
        self.p_table.hide()

        self.g_table = QTableWidget(self)
        self.g_table.setGeometry(120, 200, 550, 160)
        self.g_table.setRowCount(0)
        self.g_table.setColumnCount(4)
        self.g_table.hide()

    def create_table(self):
        try:
            self.table.hide()
            self.table = QTableWidget(self)
            self.table.setGeometry(120, 200, 550, 160)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.show()
        except AttributeError:
            self.table = QTableWidget(self)
            self.table.setGeometry(120, 200, 550, 160)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            self.table.show()

    # CREATE AND POPULATE TABLE FOR "GRADES" TAB
    def grades(self):
        self.e_uline.hide()
        self.p_uline.hide()
        self.g_uline.show()
        self.create_table()

        query = "SELECT o.comments, c.instructor, g.test_id, g.grade \
                FROM university.person p INNER JOIN university.grades g \
                ON p.person_id = g.person_id INNER JOIN university.class c \
                ON g.class_id = c.class_id INNER JOIN university.course o \
                ON c.course_id = o.course_id WHERE p.user_id=%s"
        result = c.execute(query, self.user)
        info = c.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setItem(0, 0, QTableWidgetItem("Class"))
        self.table.setItem(0, 1, QTableWidgetItem("Instructor"))
        self.table.setItem(0, 2, QTableWidgetItem("Test #"))
        self.table.setItem(0, 3, QTableWidgetItem("Grade"))
        for row_number, row_data in enumerate(info):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # CREATE AND POPULATE TABLE FOR "PROFILE" TAB
    def profile(self):
        self.e_uline.hide()
        self.p_uline.show()
        self.g_uline.hide()
        self.create_table()
        query = "SELECT f_name, l_name, address, city, state, dob, phone, email \
                FROM university.person \
                WHERE user_id=%s"
        result = c.execute(query, self.user)
        info = c.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(8)
        for row_number, row_data in enumerate(info):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # CREATE AND POPULATE TABLE FOR "ENROLL" TAB
    def enroll(self):
        self.e_uline.show()
        self.p_uline.hide()
        self.g_uline.hide()
        self.create_table()
        query = "SELECT name, comments FROM university.course"
        result = c.execute(query)
        info = c.fetchall()
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        for row_number, row_data in enumerate(info):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


app = QApplication(sys.argv)                                            # application object
window = MAIN_S()
window.show()

app.exec_()                                                             # execute application
sys.exit(0)                                                             # system exit
