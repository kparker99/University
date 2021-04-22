# Algonquin University Class Enrollment Window

import pymysql

import class_enrollment
import stylesheets as s
import sql_functions as sql

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


# MYSQL CONNECTION #
####################
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()

# MAIN STUDENT WINDOW GUI AND FUNCTIONS #
#########################################
class MAIN_S(qtw.QWidget):
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
        self.banner = qtw.QLabel(self)
        self.banner.setStyleSheet("background-color: rgb(180, 145, 76);\n")
        self.banner.setGeometry(0, 0, 1400, 140)

        # PURPLE BANNER
        self.banner = qtw.QLabel(self)
        self.banner.setStyleSheet("background-color: rgb(57, 24, 71);\n")
        self.banner.setGeometry(0, 0, 1400, 90)

        # WELCOME
        self.banner = qtw.QLabel(name[1] + ", " + name[0], self)
        self.banner.setStyleSheet(("font: 18pt \"Cinzel\";\n"
                                   "background-color: transparent;\n"
                                   "color: white;"
                                    ))
        self.banner.setGeometry(30, 20, 500, 40)

        # LABELS
        self.enroll_b = qtw.QPushButton("ENROLL", self)
        self.enroll_b.setGeometry(120, 100, 125, 24)
        self.enroll_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                   "background-color: rgb(180, 145, 76);\n"
                                   "border-style: outset;\n"
                                   "color: white;"
                                    ))
        self.enroll_b.clicked.connect(self.enroll)

        self.profile_b = qtw.QPushButton("PROFILE", self)
        self.profile_b.setGeometry(300, 100, 125, 24)
        self.profile_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                    "background-color: rgb(180, 145, 76);\n"
                                    "border-style: outset;\n"
                                    "color: white;"
                                    ))
        self.profile_b.clicked.connect(self.profile)

        self.grades_b = qtw.QPushButton("GRADES", self)
        self.grades_b.setGeometry(480, 100, 125, 24)
        self.grades_b.setStyleSheet(("font: 14pt \"Montserrat SemiBold\";\n"
                                    "background-color: rgb(180, 145, 76);\n"
                                    "border-style: outset;\n"
                                    "color: white;"
                                    ))
        self.grades_b.clicked.connect(self.grades)

        self.grades_b = qtw.QPushButton("logout", self)
        self.grades_b.setGeometry(30, 50, 125, 24)
        self.grades_b.setStyleSheet(("font: 8pt \"Montserrat Regular\";\n"
                                     "background-color: transparent;\n"
                                     "border-style: outset;\n"
                                     "color: blue;"
                                     ))
        self.grades_b.clicked.connect(self.logout)

        # UNDERLINES
        self.e_uline = qtw.QLabel("", self)
        self.e_uline.setGeometry(133, 130, 98, 3)
        self.e_uline.setStyleSheet("background-color: white;")
        self.e_uline.hide()

        self.p_uline = qtw.QLabel("", self)
        self.p_uline.setGeometry(313, 130, 98, 3)
        self.p_uline.setStyleSheet("background-color: white;")
        self.p_uline.hide()

        self.g_uline = qtw.QLabel("", self)
        self.g_uline.setGeometry(493, 130, 98, 3)
        self.g_uline.setStyleSheet("background-color: white;")
        self.g_uline.hide()

        # TABLES
        self.e_table = qtw.QTableWidget(self)
        self.e_table.setGeometry(120, 200, 550, 160)
        self.e_table.setRowCount(0)
        self.e_table.setColumnCount(2)
        self.e_table.hide()

        self.p_table = qtw.QTableWidget(self)
        self.p_table.setGeometry(120, 200, 1000, 160)
        self.p_table.setRowCount(0)
        self.p_table.setColumnCount(8)
        self.p_table.hide()

        self.g_table = qtw.QTableWidget(self)
        self.g_table.setGeometry(120, 200, 550, 160)
        self.g_table.setRowCount(0)
        self.g_table.setColumnCount(4)
        self.g_table.hide()


# MAIN STUDENT WINDOW FUNCTIONS #
#################################

    # Creates tables for each "tab" (hides table from previously selected tab)
    def create_table(self):
        try:
            self.table.hide()                                # hides table if table was previously created
            self.table = qtw.QTableWidget(self)
            self.table.setStyleSheet("border: 0px;\n"
                                     "border-collapse: collapse;\n"
                                     "font: 9pt \"Montserrat Regular\";\n"
                                     )
            self.table.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
            self.table.setShowGrid(False)
            self.table.verticalHeader().setVisible(False)
            self.table.show()
        except AttributeError:                               # creates table if no table previously existed
            self.table = qtw.QTableWidget(self)
            self.table.setStyleSheet("border: 0px;\n"
                                     "border-collapse: collapse;\n"
                                     "font: 9pt \"Montserrat Regular\";\n"
                                     )
            self.table.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
            self.table.setShowGrid(False)
            self.table.verticalHeader().setVisible(False)
            self.table.show()

    # CREATE AND POPULATE TABLE FOR "GRADES" TAB
    def grades(self):
        self.e_uline.hide()
        self.p_uline.hide()
        self.g_uline.show()
        self.create_table()
        query = "SELECT o.course_name, c.instructor, g.test_date, g.grade \
                FROM university.person p \
                INNER JOIN university.grades g ON p.user_id = g.user_id \
                INNER JOIN university.class c ON g.class_id = c.class_id \
                INNER JOIN university.course o ON c.course_number = o.course_number \
                WHERE p.user_id=%s"
        result = c.execute(query, self.user)
        info = c.fetchall()
        self.table.setGeometry(120, 200, 800, 500)
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Class", "Instructor", "Test Date", "Grade"])
        for row_number, row_data in enumerate(info):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)


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
        self.table.setGeometry(120, 200, 1200, 160)
        self.table.setRowCount(0)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["First Name", "Last Name", "Address", "City", "State", "Date of Birth", "Phone #", "Email"])
        for row_number, row_data in enumerate(info):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.table.resizeColumnsToContents()

    # CREATE AND POPULATE TABLE FOR "ENROLL" TAB
    def enroll(self):
        self.e_uline.show()
        self.p_uline.hide()
        self.g_uline.hide()
        self.create_table()
        self.table.setGeometry(120, 200, 1100, 1160)
        info = sql.get_info_from_db("SELECT course_name, hours, department FROM university.course")
        print(info)
        self.table.setRowCount(8)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Course Name", "Credit Hours", "Department"])
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.table.setColumnWidth(0, 500)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 400)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(self.get_into_class)

    def logout(self):
        self.window().hide()

    def get_into_class(self, row, column):
        try:
            cell = self.table.item(row, column)
            course = cell.text()
            self.enroll = class_enrollment.ENROLL(course)
            self.enroll.show()
        except Exception:
            pass

if __name__ == '__main--':
    error_dialog = qtw.QErrorMessage()
    error_dialog.showMessage("Unauthorized Access. Please enter through main login page.")