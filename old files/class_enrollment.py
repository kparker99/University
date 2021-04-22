# Algonquin University Class Enrollment Window

import pymysql
import datetime

import stylesheets as s
import sql_functions as sql

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


# MYSQL CONNECTION #
####################
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()

date = datetime.date.today()

# NEW ACCOUNT WINDOW CLASS #
############################
class ENROLL(qtw.QWidget):


    def __init__(self, course):
        super().__init__()

        self.course = course        # Variable of course selected in "main" page

        # QUERY FOR CREDIT HOURS
        ch_query = "SELECT hours FROM university.course WHERE course_name = %s"
        ch_result = c.execute(ch_query, self.course)
        ch_tuple = c.fetchone()
        hours = ch_tuple[0]

        # QUERY FOR COURSE DESCRIPTION

        cd_query = "SELECT course_description FROM university.course WHERE course_name = %s"
        cd_result = c.execute(cd_query, self.course)
        cd_tuple = c.fetchone()
        # TODO: make house, course description part of the same tuple or part of a dictionary for later use??
        course_description = cd_tuple[0]

        # WINDOW SIZE/STYLE/ICON
        self.setWindowTitle("Class Enrollment")  # window title
        self.setGeometry(100, 100, 1100, 750)  # window size
        self.setStyleSheet("background-color: white")
        self.setMinimumWidth(1100)
        self.setMaximumWidth(1100)
        self.setMaximumHeight(750)
        self.setMinimumHeight(750)
        self.setWindowIcon(qtg.QIcon('images\ALGONQUIN UNIVERSITY.png'))  # create AU window icon

        # PURPLE BANNER
        self.banner = qtw.QLabel(self)
        self.banner.setStyleSheet("background-color: rgb(57, 24, 71);\n")
        self.banner.setGeometry(0, 0, 1150, 50)

        # ENROLL & CLOSE BUTTONS
        self.enroll_b = qtw.QPushButton("Enroll", self)
        self.enroll_b.setGeometry(100, 650, 250, 40)
        self.enroll_b.setStyleSheet(s.large_button_style(self))
        # TODO: add class to user's file

        self.close_b = qtw.QPushButton("Close", self)
        self.close_b.setGeometry(750, 650, 250, 40)
        self.close_b.setStyleSheet(s.large_button_style(self))
        self.close_b.clicked.connect(self.window().hide)

        # COURSE TITLE
        self.course_name = qtw.QLabel(self.course, self)
        self.course_name.setGeometry(100, 100, 900, 40)
        self.course_name.setStyleSheet(s.large_header_text_style(self))

        # "CREDIT HOURS" LABEL
        self.credit_l = qtw.QLabel("Credit Hours: ", self)
        self.credit_l.setGeometry(100, 160, 161, 16)
        self.credit_l.setStyleSheet(s.small_header_text_style(self))

        # CREDIT HOURS (filled in by MYSQL)
        self.hrs = qtw.QLabel(str(hours), self)
        self.hrs.setGeometry(240, 160, 75, 16)
        self.hrs.setStyleSheet(s.body_text_style(self))

        # "COURSE DESCRIPTION" LABEL
        self.c_description_l = qtw.QLabel("Course Description", self)
        self.c_description_l.setGeometry(100, 220, 250, 25)
        self.c_description_l.setStyleSheet(s.small_header_text_style(self))

        # COURSE DESCRIPTION TEXT
        self.c_description_t = qtw.QLabel(course_description, self)
        self.c_description_t.setGeometry(100, 250, 900, 140)
        self.c_description_t.setStyleSheet(s.body_text_style(self))
        self.c_description_t.setWordWrap(True)
        self.c_description_t.setAlignment(qtc.Qt.AlignTop)

        # TODO: AVAILABLE CLASSES TABLE
        # TODO: check present date and only allow classes to show that are past date
        table_info = sql.get_info_from_db("SELECT c.start_date, c.end_date, c.room, c.instructor, o.course_number \
                                          FROM university.class c \
                                          JOIN university.course o ON c.course_number = o.course_number \
                                          WHERE o.course_name=%s \
                                          AND c.start_date>%s", [self.course, date])
        h_font = qtg.QFont()
        h_font.setBold(True)
        self.class_table = qtw.QTableWidget(self)
        self.class_table.setStyleSheet("border: 0px;\n"
                                       "border-collapse: collapse;\n"
                                       "font: 10pt \"Montserrat Regular\";\n"
                                        )
        self.class_table.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustToContents)
        self.class_table.setShowGrid(False)
        self.class_table.verticalHeader().setVisible(False)
        self.class_table.setGeometry(100, 420, 900, 200)
        self.class_table.setRowCount(0)
        self.class_table.setColumnCount(5)
        self.class_table.setHorizontalHeaderLabels(["Start Date" + "\n", "End Date", "Room #", "Instructor", "Course Number"])
        self.class_table.horizontalHeaderItem(0).setTextAlignment(qtc.Qt.AlignLeft)
        self.class_table.horizontalHeaderItem(0).setFont(h_font)
        self.class_table.horizontalHeaderItem(1).setTextAlignment(qtc.Qt.AlignLeft)
        self.class_table.horizontalHeaderItem(1).setFont(h_font)
        self.class_table.horizontalHeaderItem(2).setTextAlignment(qtc.Qt.AlignLeft)
        self.class_table.horizontalHeaderItem(2).setFont(h_font)
        self.class_table.horizontalHeaderItem(3).setTextAlignment(qtc.Qt.AlignLeft)
        self.class_table.horizontalHeaderItem(3).setFont(h_font)
        self.class_table.horizontalHeaderItem(4).setTextAlignment(qtc.Qt.AlignLeft)
        self.class_table.horizontalHeaderItem(4).setFont(h_font)
        for row_number, row_data in enumerate(table_info):
            self.class_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.class_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.class_table.setColumnWidth(0, 200)
        self.class_table.setColumnWidth(1, 200)
        self.class_table.setColumnWidth(2, 170)
        self.class_table.setColumnWidth(4, 200)
        self.class_table.setColumnWidth(5, 200)
        self.class_table.setSortingEnabled(True)
        self.class_table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)