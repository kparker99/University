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
        self.ui.l_login_btn.clicked.connect(self._login)
        self.ui.l_newaccount_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.l_newaccount_btn.clicked.connect(self._center_window)

        # page 1 (new_account_page)
        self.ui.n_firstname_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_lastname_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_address_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_city_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_state_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_phone_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_enterpassword_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_confirmpassword_field.textChanged.connect(self._are_fields_empty)
        self.ui.n_createaccount_btn.clicked.connect(self._create_account)
        self.ui.n_back_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # page 2 (student_page)
        self.ui.s_profile_btn.clicked.connect(self.s_profile_profile_data)
        self.ui.s_classes_btn.clicked.connect(self.s_enroll_course_data)
        self.ui.s_courseenroll_enroll_btn.clicked.connect(self.s_courseenroll_enroll_in_class)
        self.ui.s_grades_btn.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(3))
        self.ui.s_grades_btn.clicked.connect(self.s_classgrades_test_grade_data)
        self.ui.s_classgrades_class_drop.activated.connect(self.s_classgrades_test_grade_data)
        self.ui.s_logout_btn.clicked.connect(self._logout)
        self.ui.s_courseenroll_close_btn.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.s_enroll_enroll_table.cellClicked.connect(self.s_courseenroll_class_data)

        # page 3 (teacher_page)
        self.ui.t_profile_btn.clicked.connect(self.t_profile_profile_data)
        self.ui.t_classes_btn.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(1))
        self.ui.t_classes_btn.clicked.connect(self.t_grades_grade_data)
        self.ui.t_logout_btn.clicked.connect(self._logout)
        self.ui.t_grades_class_drop.activated.connect(self.t_grades_grade_data)
        self.ui.t_grades_addgrade.clicked.connect(lambda: self.ui.stackedWidget_3.setCurrentIndex(2))
    # END BUTTONS


    # VALIDATORS FOR FIELDS IN NEW_ACCOUNT_PAGE HERE
        # state lineedit
        state_regex = qtc.QRegExp("[a-zA-Z][a-zA-Z]")

        state_validator = qtg.QRegExpValidator(state_regex, self.ui.n_state_field)
        self.ui.n_state_field.setValidator(state_validator)

        # first name, last name, city lineedits
        name_regex = qtc.QRegExp("([a-zA-Z-_]+ )+")

        first_name_validator = qtg.QRegExpValidator(name_regex, self.ui.n_firstname_field)
        self.ui.n_firstname_field.setValidator(first_name_validator)
        last_name_validator = qtg.QRegExpValidator(name_regex, self.ui.n_lastname_field)
        self.ui.n_lastname_field.setValidator(last_name_validator)
        city_validator = qtg.QRegExpValidator(name_regex, self.ui.n_city_field)
        self.ui.n_city_field.setValidator(city_validator)
    # END VALIDATORS

    def _message(self, title, text):
        '''create message box'''
        message = qtw.QMessageBox()
        message.setWindowTitle(title)
        message.setText(text)
        message.exec()

    def _center_window(self):
        '''centers the window to user's screen by centering stackedWidget to center of screen'''
        screen = app.primaryScreen()
        rect = self.ui.stackedWidget.geometry()
        cp = screen.availableGeometry().center()
        rect.moveCenter(cp)
        self.move(rect.topLeft())

    def _login(self):
        '''logs into main window based on role (student, teacher, admin)'''
        if self.ui.l_username_field.text() and self.ui.l_password_field.text():
            username = self.ui.l_username_field.text()
            password = self.ui.l_password_field.text()
        else:
            return self._message("Missing Information", "Please enter a username and password")
        info = sql.get_info_from_db("SELECT * FROM university.login WHERE user_id=%s AND password=%s", (username, password))
        if info != ():
            query = sql.get_info_from_db("SELECT role_id, f_name, l_name FROM university.person WHERE user_id=%s", username)
            role, first, last = query[0]
            if role == 1:
                self.ui.stackedWidget.setCurrentIndex(2)
                self.ui.stackedWidget_2.setCurrentIndex(0)
                self.ui.s_userwelcome_field.setText("{} {}".format(first, last))
                self.s_classgrades_enrolled_classes(username)
                self.s_profile_profile_data()
                self.showMaximized()
                return username
            elif role == 2:
                self.ui.stackedWidget.setCurrentIndex(3)
                self.ui.stackedWidget_3.setCurrentIndex(0)
                self.ui.t_userwelcome_field.setText("{} {}".format(first, last))
                self.t_grades_teacher_classes(username)
                self.s_profile_profile_data_teacher()
                self.showMaximized()
                return username
            elif role == 3:
                print('admin')
        else:
            return self._message("Invalid Username/Password", "No Such Username/Password")

    def _logout(self):
        '''goes to login_page and clears username and password fields'''
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.l_username_field.clear()
        self.ui.l_password_field.clear()

    def _create_email(self, username):
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

    def _are_fields_empty(self):
        '''changes create_account button to gold when all required fields are filled in'''
        if self.ui.n_firstname_field.text() and \
           self.ui.n_lastname_field.text() and \
           self.ui.n_dob_field.text() and \
           self.ui.n_address_field.text() and \
           self.ui.n_city_field.text() and \
           self.ui.n_state_field.text() and \
           self.ui.n_phone_field.text() and \
           self.ui.n_enterpassword_field.text() and \
           self.ui.n_confirmpassword_field.text():
                self.ui.n_createaccount_btn.setStyleSheet("background-color: rgb(180, 145, 76);\n"
                                                            "font: 12pt \"Montserrat SemiBold\";\n"
                                                            "color: white;\n"
                                                            "border-style: outset;\n"
                                                            "border-width: 0px;\n"
                                                            )
        else:
            pass

    def _create_account(self):
        '''takes user input in new account window and creates account with unique username'''
        if self.ui.n_firstname_field.text() and \
           self.ui.n_lastname_field.text() and \
           self.ui.n_dob_field.text() and \
           self.ui.n_address_field.text() and \
           self.ui.n_city_field.text() and \
           self.ui.n_state_field.text() and \
           self.ui.n_phone_field.text() and \
           self.ui.n_enterpassword_field.text() and \
           self.ui.n_confirmpassword_field.text():
                first_name, last_name, dob, address, city, state, phone, password, confirm_password = \
                self.ui.n_firstname_field.text(), self.ui.n_lastname_field.text(), self.ui.n_dob_field.text(), \
                self.ui.n_address_field.text(), self.ui.n_city_field.text(), self.ui.n_state_field.text(), \
                self.ui.n_phone_field.text(), self.ui.n_enterpassword_field.text(), self.ui.n_confirmpassword_field.text()
        else:
            return self._message("Missing new account data", "Not all fields completed correctly")
        if password == confirm_password:
            # next 3 lines create unique email and username using create_email function
            possible_email_unformatted = first_name[0] + last_name
            possible_email = possible_email_unformatted.lower()
            email, username = self._create_email(possible_email)    # create unique email and username from create_email function
            sql.enter_into_db("INSERT INTO university.login (user_id, password) VALUES (%s,%s)", (username, password))
            sql.enter_into_db("INSERT INTO university.person (role_id, user_id, f_name, l_name, address, city, state, dob, email, phone) \
                               VALUES (1,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               (username, first_name, last_name, address, city, state, dob, email, phone))
            self._message("New User Created", "your username is " + username)
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            return self._message("Password Invalid", "Error Passwords do not match")

    def s_classgrades_enrolled_classes(self, username):
        '''gets a list of classes student is enrolled in upon login'''
        class_list = []
        table_info = sql.get_info_from_db("SELECT class_id \
                                          FROM university.enrolled \
                                          WHERE user_id=%s", username)
        for tuple in table_info:
            class_list = class_list + list(tuple)
        self.ui.s_classgrades_class_drop.addItems(class_list)
        return class_list

    def s_profile_profile_data(self):
        '''populates student users info from sql db onto table'''
        self.ui.stackedWidget_2.setCurrentIndex(0)
        username = self.ui.l_username_field.text()
        info = sql.get_info_from_db("SELECT f_name, l_name, address, city, state, dob, phone, email \
                                    FROM university.person WHERE user_id=%s", username)
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.s_profile_profile_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.s_profile_profile_table.resizeColumnsToContents()

#TODO: Edit profile
    #def edit_profile(self):
       # pass

    def s_enroll_course_data(self):
        '''populates general course information for student to view'''
        self.ui.stackedWidget_2.setCurrentIndex(1)
        info = sql.get_info_from_db("SELECT course_name, hours, department FROM university.course")
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.s_enroll_enroll_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.s_enroll_enroll_table.resizeColumnsToContents()

    def s_courseenroll_class_data(self, row):
        '''populates specific classes available to enroll in selected general course'''
        self.ui.stackedWidget_2.setCurrentIndex(2)
        course = self.ui.s_enroll_enroll_table.item(row, 0).text()
        self.ui.s_courseenroll_coursename_field.setText(course)
        info = sql.get_info_from_db("SELECT hours, course_description FROM university.course WHERE course_name = %s", course)
        hours, course_description = info[0]
        self.ui.s_courseenroll_credits_field.setText(str(hours))
        self.ui.s_courseenroll_coursedesc_field.setText(course_description)
        self.ui.s_profile_profile_table.resizeColumnsToContents()
        table_info = sql.get_info_from_db("SELECT c.start_date, c.end_date, c.room, c.instructor, o.course_number \
                                          FROM university.class c \
                                          JOIN university.course o ON c.course_number = o.course_number \
                                          WHERE o.course_name=%s \
                                          AND c.start_date>%s", [course, datetime.date.today()])
        self.ui.s_courseenroll_classes_table.setRowCount(len(table_info))
        for row_number, row_data in enumerate(table_info):
            for column_number, data in enumerate(row_data):
                self.ui.s_courseenroll_classes_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

    def s_courseenroll_enroll_in_class(self):
        row = self.ui.s_courseenroll_classes_table.currentRow()
        username = self.ui.l_username_field.text()
        start = self.ui.s_courseenroll_classes_table.item(row, 0).text()
        course = self.ui.s_courseenroll_classes_table.item(row, 4).text()
        query = sql.get_one_info_from_db("SELECT class_id FROM university.class \
                                          WHERE course_number=%s AND start_date=%s", (course, start))
        course_number = query[0]
        query = sql.get_info_from_db("SELECT role_id FROM university.enrolled WHERE user_id=%s AND class_id=%s",
                                     (username, course_number))
        if query == ():
            sql.enter_into_db("INSERT INTO university.enrolled (user_id, class_id, role_id) VALUES (%s,%s,1)",
                              (username, course_number))
            self.ui.s_classgrades_class_drop.clear()
            self.s_classgrades_enrolled_classes(username)
            self._message("Student Enrolled", "You are enrolled in " + course)
        else:
            self._message("Enrollment Error", "You are already enrolled in this class")

    def s_classgrades_test_grade_data(self):
        '''obtains test grades for student and determines course overall grade'''
        self.ui.s_classgrades_grades_table.clearContents()
        course = self.ui.s_classgrades_class_drop.currentText()
        username = self.ui.l_username_field.text()
        info = sql.get_info_from_db("SELECT test_date, grade FROM university.grades WHERE user_id=%s AND class_id=%s", (username, course))
        if info == ():
            self.ui.s_classgrades_totalgrade_field.setText("No grade available")
        else:
            lis = []
            for x in range(len(info)):
                lis.append(info[x][1])
                avg = sum(lis)/len(lis)
            self.ui.s_classgrades_totalgrade_field.setText("Class Grade: {:.2f}%".format(avg))
            for row_number, row_data in enumerate(info):
                for column_number, data in enumerate(row_data):
                    self.ui.s_classgrades_grades_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

    def t_profile_profile_data(self):
        '''populates teacher users info from sql db onto table'''
        self.ui.stackedWidget_3.setCurrentIndex(0)
        username = self.ui.l_username_field.text()
        info = sql.get_info_from_db("SELECT f_name, l_name, address, city, state, dob, phone, email \
                                    FROM university.person WHERE user_id=%s", username)
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.t_profile_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))
        self.ui.t_profile_table.resizeColumnsToContents()

    def t_grades_teacher_classes(self, username):
        '''gets a list of classes teacher is instructor of upon login'''
        class_list = []
        table_info = sql.get_info_from_db("SELECT c.class_id \
                                          FROM university.class c \
                                          JOIN university.person p ON c.instructor = p.user_id \
                                          WHERE p.user_id=%s", username)
        for tuple in table_info:
            class_list = class_list + list(tuple)
        self.ui.t_grades_class_drop.addItems(class_list)
        return class_list

    def t_grades_grade_data(self):
        '''obtains test grades for each teacher's class and displays message if there are no test grades for the class'''
        self.ui.t_grades_allgrades_table.clearContents()
        self.ui.t_grades_nogrades_label.clear()
        course = self.ui.t_grades_class_drop.currentText()
        info = sql.get_info_from_db("SELECT user_id, test_number, test_date, grade FROM university.grades WHERE class_id=%s", (course))
        if info == ():
            self.ui.t_grades_nogrades_label.setText("No test grades available")
        for row_number, row_data in enumerate(info):
            for column_number, data in enumerate(row_data):
                self.ui.t_grades_allgrades_table.setItem(row_number, column_number, qtw.QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = qtw.QApplication([])
    window = GUI_Window()

    qr = window.frameGeometry()
    cp = qtw.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

    window.show()
    app.exec_()