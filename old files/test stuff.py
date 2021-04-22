from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
import pymysql

# user = self.user_box.text()
# pw = self.pw_box.text()
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='8Jk$4*j!M.3f',
    db='University'
)

c = conn.cursor()
user = input("enter username: ")
pw = input("enter password: ")

try:
    c.execute("SELECT * FROM login WHERE person_id={} AND password={}".format(user, pw))
except:
    print('please enter valid username/password')

c.execute("SELECT p.f_name FROM person p JOIN login l USING (person_id) WHERE p.person_id={}".format(user))
name = c.fetchone()
print("Welcome to the database", name[0])

d = input("What class would you like to look up: ")
cmd = d.lower()

c.execute("SELECT cl.year, cl.semester, cl.room, cl.instructor FROM course co JOIN class cl USING (course_id) WHERE co.comments='{}'".format(cmd))
res = c.fetchall()
for tuple in res:
    print("Year:", tuple[0],\
          "Semester:", tuple[1],\
          "Room:", tuple[2],\
          "Instructor:", tuple[3])