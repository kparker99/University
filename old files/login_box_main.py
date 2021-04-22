import sys
import pymysql

import new_account

from login_box import Ui_Form
from new_account_gui import Ui_Form as na_form

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg


# MYSQL DB CONNECTION #
#######################
conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
c = conn.cursor()

# LOGIN WINDOW FUNCTIONALITY #
##############################
class login_window(qtw.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        # References QWidget parent object
        super().__init__(*args, **kwargs)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.login_b.clicked.connect(self.login)
        self.ui.na_b.clicked.connect(self.new_account)
        self.ui.un_f.textChanged.connect(self.set_button_text)

        self.show()

    def set_button_text(self, text):
        if text:
            self.login_b.setText(f'Log In {text}')
        else:
            self.login_b.setText('Log in')

    # OPENS NEW ACCOUNT WINDOW
    def new_account(self):
        print('trying')
        print('instanced')
        # self.window.setupUi(na_form)
        print('setup')

    # CHECK FOR CORRECT LOGIN INFO / OPEN MAIN WINDOW
    def login(self):
        un = self.ui.un_f.text()
        pw = self.ui.pw_f.text()

        query = "SELECT * FROM university.login WHERE user_id=%s AND password=%s"
        data = c.execute(query, (un, pw))
        if (len(c.fetchall())>0):
            self.window = na_form()
            self.window.show()
        else:
            qtw.QMessageBox.critical(self, "Error", "Invalid username/password")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    widget = login_window()
    sys.exit(app.exec_())