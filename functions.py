import datetime
import re
import string

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from design import Ui_MainWindow
import sql_functions as sql


class GUI_Window(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # center login page and show
        screen = app.primaryScreen()
        rect = self.ui.stackedWidget.geometry()
        cp = screen.availableGeometry().center()
        rect.moveCenter(cp)
        self.move(rect.topLeft())
        self.ui.stackedWidget.setCurrentIndex(0)


    # BUTTON FUNCTIONALITY BELOW
        # page 0 (login_page)
        self.ui.login_button.clicked.connect(self.login)
        self.ui.new_account_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.new_account_button.clicked.connect(self.center_window)

        # page 1 (new_account_page)
        self.ui.first_name_field.textChanged.connect(self.are_fields_empty)
        self.ui.last_name_field.textChanged.connect(self.are_fields_empty)
        self.ui.address_field.textChanged.connect(self.are_fields_empty)
        self.ui.city_field.textChanged.connect(self.are_fields_empty)
        self.ui.state_field.textChanged.connect(self.are_fields_empty)
        self.ui.phone_field.textChanged.connect(self.are_fields_empty)
        self.ui.enter_password_field.textChanged.connect(self.are_fields_empty)
        self.ui.confirm_password_field.textChanged.connect(self.are_fields_empty)
        self.ui.create_account_button.clicked.connect(self.create_account)
        self.ui.back_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # page 2 (student_page)
        # self.ui.profile_button.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(3))  # TODO: fix so it shows profile page
        self.ui.profile_button.clicked.connect(self.get_profile_data)
        self.ui.classes_button.clicked.connect(self.get_course_data)
        self.ui.enroll_button.clicked.connect(self.enroll)
        self.ui.grades_button.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(3))
        self.ui.class_grades_table.clicked.connect(self.get_test_grades)
        self.ui.logout_button.clicked.connect(self.logout)
        self.ui.close_button.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.enroll_table.cellClicked.connect(self.get_class_data)

        # page 3 (teacher_page)
        self.ui.profile_button_2.clicked.connect(self.get_profile_data_teacher)
        self.ui.classes_button_2.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(1))
        self.ui.logout_button_2.clicked.connect(self.logout)
        self.ui.student_class_dropdown.activated.connect(self.get_class_grades)
        self.ui.add_grade.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(2))
    # END BUTTONS


    # VALIDATORS FOR FIELDS IN NEW_ACCOUNT_PAGE HERE
        # state lineedit
        state_regex = qtc.QRegExp("[a-zA-Z][a-zA-Z]")

        state_validator = qtg.QRegExpValidator(state_regex, self.ui.state_field)
        self.ui.state_field.setValidator(state_validator)

        # first name, last name, city lineedits
        name_regex = qtc.QRegExp("([a-zA-Z-_]+ )+")

        first_name_validator = qtg.QRegExpValidator(name_regex, self.ui.first_name_field)
        self.ui.first_name_field.setValidator(first_name_validator)
        last_name_validator = qtg.QRegExpValidator(name_regex, self.ui.last_name_field)
        self.ui.last_name_field.setValidator(last_name_validator)
        city_validator = qtg.QRegExpValidator(name_regex, self.ui.city_field)
        self.ui.city_field.setValidator(city_validator)
    # END VALIDATORS

    def message(self, title, text):
        '''create message box'''
        message = qtw.QMessageBox()
        message.setWindowTitle(title)
        message.setText(text)
        message.exec()

    def center_window(self):
        '''centers the window to user's screen by centering stackedWidget to center of screen'''
        screen = app.primaryScreen()
        rect = self.ui.stackedWidget.geometry()
        cp = screen.availableGeometry().center()
        rect.moveCenter(cp)
        self.move(rect.topLeft())

    def login(self):
        '''logs into main window based on role (student, teacher, admin)'''
        if self.ui.username_field.text() and self.ui.password_field.text():
            username = self.ui.username_field.text()
            password = self.ui.password_field.text()
        else:
            return self.message("Missing Information", "Please enter a username and password")
        info = sql.get_info_from_db("SELECT * FROM university.login WHERE user_id=%s AND password=%s", (username, password))
        if info != ():
            query = sql.get_info_from_db("SELECT role_id, f_name, l_name FROM university.person WHERE user_id=%s", username)
            role, first, last = query[0]
            if role == 1:
                self.ui.stackedWidget.setCurrentIndex(2)
                self.ui.stackedWidget_2.setCurrentIndex(0)
                self.ui.user_welcome.setText("{} {}".format(first, last))
                self.get_student_classes(username)
                self.get_profile_data()
                self.showMaximized()
                return username
            elif role == 2:
                self.ui.stackedWidget.setCurrentIndex(3)
                self.ui.stackedWidget_3.setCurrentIndex(0)
                self.ui.user_welcome_2.setText("{} {}".format(first, last))
                self.get_teacher_classes(username)
                self.get_profile_data_teacher()
                self.showMaximized()
                return username
            elif role == 3:
                print('admin')
        else:
            return self.message("Invalid Username/Password", "No Such Username/Password")

    def logout(self):
        '''goes to login_page and clears username and password fields'''
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.username_field.clear()
        self.ui.password_field.clear()

    def create_email(self, username):
        '''checks database to create unique email and username for user'''
        counter = 1
        n = sql.get_one_info_from_db("SELECT user_id FROM university.login WHERE user_id=%s", (username))
        while n != None:
            if not username[-1].isdigit():
                username = username + str(counter)
                n = sql.get_one_info_from_db("SELECT user_id FROM university.login WHERE user_id=%s", (username))
            else:
                counter += 1
                username = username.rstrip(string.digits) + str(counter)
                n = sql.get_one_info_from_db("SELECT user_id FROM university.login WHERE user_id=%s", (username))
        email = username + '@au.edu'
        search = re.search(r"(\w+)", email)
        username = search[0]
        return email, username

    def are_fields_empty(self):
        '''changes create_account button to gold when all required fields are filled in'''
        if self.ui.first_name_field.text() and \
           self.ui.last_name_field.text() and \
           self.ui.dob_field.text() and \
           self.ui.address_field.text() and \
           self.ui.city_field.text() and \
           self.ui.state_field.text() and \
           self.ui.phone_field.text() and \
           self.ui.enter_password_field.text() and \
           self.ui.confirm_password_field.text():
                self.ui.create_account_button.setStyleSheet("background-color: rgb(180, 145, 76);\n"
                                                            "font: 12pt \"Montserrat SemiBold\";\n"
                                                            "color: white;\n"
                                                            "border-style: outset;\n"
                                                            "border-width: 0px;\n"
                                                            )
        else:
            pass

    def create_account(self):
        '''takes user input in new account window and creates account with unique username'''
        if self.ui.first_name_field.text() and \
           self.ui.last_name_field.text() and \
           self.ui.dob_field.text() and \
           self.ui.address_field.text() and \
           self.ui.city_field.text() and \
           self.ui.state_field.text() and \
           self.ui.phone_field.text() and \
           self.ui.enter_password_field.text() and \
           self.ui.confirm_password_field.text():
                first_name, last_name, dob, address, city, state, phone, password, confirm_password = \
                self.ui.first_name_field.text(), self.ui.last_name_field.text(), self.ui.dob_field.text(), \
                self.ui.address_field.text(), self.ui.city_field.text(), self.ui.state_field.text(), \
                self.ui.phone_field.text(), self.ui.enter_password_field.text(), self.ui.confirm_password_field.text()
        else:
            return self.message("Missing new account data", "Not all fields completed correctly")
        if password == confirm_password:
            # next 3 lines create unique email and username using create_email function
            possible_email_unformatted = first_name[0] + last_name
            possible_email = possible_email_unformatted.lower()
            email, username = self.create_email(possible_email)    # create unique email and username from create_email function
            sql.enter_into_db("INSERT INTO university.login (user_id, password) VALUES (%s,%s)", (username, password))
            sql.enter_into_db("INSERT INTO university.person (role_id, user_id, f_name, l_name, address, city, state, dob, email, phone) \
                               VALUES (1,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               (username, first_name, last_name, address, city, state, dob, email, phone))
            self.message("New User Created", "your username is " + username)
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            return self.message("Password Invalid", "Error Passwords do not match")

    def get_student_classes(self, username):
        '''gets a list of classes student is enrolled in upon login'''
        class_list = []
        table_info = sql.get_info_from_db("SELECT class_id \
                                          FROM university.enrolled \
                                          WHERE user_id=%s", username)
        for tuple in table_info:
            class_list = class_list + list(tuple)
        self.ui.student_class_dropdown.addItems(class_list)
        return class_list

    def get_profile_data(self):
        '''populates student users info from sql db onto table'''
        self.ui.stackedWidget_2.setCurrentIndex(0)
        username = self.ui.username_field.text()
        info = sql.get_info_from_db("SELECT f_name, l_name, address, city, state, dob, phone, email \
                                    FROM university.person WHERE user_id=%s", username)
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.profile_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.profile_table.resizeColumnsToContents()

    def edit_profile(self):
        pass

    def get_course_data(self):
        '''populates general course information for student to view'''
        self.ui.stackedWidget_2.setCurrentIndex(1)
        info = sql.get_info_from_db("SELECT course_name, hours, department FROM university.course")
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.enroll_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.enroll_table.resizeColumnsToContents()

    def get_class_data(self, row):
        '''populates specific classes available to enroll in selected general course'''
        self.ui.stackedWidget_2.setCurrentIndex(2)
        course = self.ui.enroll_table.item(row, 0).text()
        self.ui.course_name.setText(course)
        info = sql.get_info_from_db("SELECT hours, course_description FROM university.course WHERE course_name = %s", course)
        hours, course_description = info[0]
        self.ui.credits.setText(str(hours))
        self.ui.course_description.setText(course_description)
        self.ui.profile_table.resizeColumnsToContents()
        table_info = sql.get_info_from_db("SELECT c.start_date, c.end_date, c.room, c.instructor, o.course_number \
                                          FROM university.class c \
                                          JOIN university.course o ON c.course_number = o.course_number \
                                          WHERE o.course_name=%s \
                                          AND c.start_date>%s", [course, datetime.date.today()])
        self.ui.classes_table.setRowCount(len(table_info))
        for row_number, row_data in enumerate(table_info):
            for column_number, data in enumerate(row_data):
                self.ui.classes_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

    def enroll(self):
        row = self.ui.classes_table.currentRow()
        username = self.ui.username_field.text()
        start = self.ui.classes_table.item(row, 0).text()
        course = self.ui.classes_table.item(row, 4).text()
        query = sql.get_one_info_from_db("SELECT class_id FROM university.class \
                                          WHERE course_number=%s AND start_date=%s", (course, start))
        course_number = query[0]
        query = sql.get_info_from_db("SELECT role_id FROM university.enrolled WHERE user_id=%s AND class_id=%s",
                                     (username, course_number))
        if query == ():
            sql.enter_into_db("INSERT INTO university.enrolled (user_id, class_id, role_id) VALUES (%s,%s,1)",
                              (username, course_number))
            self.ui.student_class_dropdown.clear()
            self.get_student_classes(username)
            self.message("Student Enrolled", "You are enrolled in " + course)
        else:
            self.message("Enrollment Error", "You are already enrolled in this class")

    def get_test_grades(self):
        self.ui.class_grades_table.clearContents()
        course = self.ui.student_class_dropdown.currentText()
        username = self.ui.username_field.text()
        info = sql.get_info_from_db("SELECT test_date, grade FROM university.grades WHERE user_id=%s AND class_id=%s", (username, course))
        if info == ():
            self.ui.total_grade.setText("No grade available")
        else:
            lis = []
            for x in range(len(info)):
                lis.append(info[x][1])
                avg = sum(lis)/len(lis)
            self.ui.total_grade.setText("Class Grade: {:.2f}%".format(avg))
            for row_number, row_data in enumerate(info):
                for column_number, data in enumerate(row_data):
                    self.ui.class_grades_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

    def get_profile_data_teacher(self):
        '''populates teacher users info from sql db onto table'''
        self.ui.stackedWidget_3.setCurrentIndex(0)
        username = self.ui.username_field.text()
        info = sql.get_info_from_db("SELECT f_name, l_name, address, city, state, dob, phone, email \
                                    FROM university.person WHERE user_id=%s", username)
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.profile_table_teacher.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.profile_table_teacher.resizeColumnsToContents()

    def get_teacher_classes(self, username):
        '''gets a list of classes teacher is instructor of upon login'''
        class_list = []
        table_info = sql.get_info_from_db("SELECT c.class_id \
                                          FROM university.class c \
                                          JOIN university.person p ON c.instructor = p.user_id \
                                          WHERE p.user_id=%s", username)
        for tuple in table_info:
            class_list = class_list + list(tuple)
        self.ui.class_dropdown.addItems(class_list)
        return class_list

    def get_class_grades(self):
        self.ui.all_grades_table.clearContents()
        course = self.ui.class_dropdown.currentText()
        info = sql.get_info_from_db("SELECT SELECT user_id, test_number, test_date, grade FROM university.grades WHERE class_id=%s", (course))
        if info == ():
            self.ui.total_grade.setText("No grade available")
        else:
            lis = []
            for x in range(len(info)):
                lis.append(info[x][1])
                avg = sum(lis)/len(lis)
            self.ui.total_grade.setText("Class Grade: {:.2f}%".format(avg))
            for row_number, row_data in enumerate(info):
                for column_number, data in enumerate(row_data):
                    self.ui.class_grades_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = qtw.QApplication([])
    window = GUI_Window()

    qr = window.frameGeometry()
    cp = qtw.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

    window.show()
    app.exec_()