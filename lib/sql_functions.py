import pymysql
import os

host = os.environ.get('university_host')
user = os.environ.get('university_user')
password = os.environ.get('university_password')
db = os.environ.get('university_database')


def write(command, data):
    conn = pymysql.connect(host, user, password, db)
    c = conn.cursor()
    try:
        c.execute(command, data)
        conn.commit()
        conn.close()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))


def get(query, variable=None):
    conn = pymysql.connect(host, user, password, db)
    c = conn.cursor()
    try:
        c.execute(query, variable)
        info = c.fetchall()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        return info


def get_one(query, variable=None):
    conn = pymysql.connect(host, user, password, db)
    c = conn.cursor()
    try:
        c.execute(query, variable)
        info = c.fetchone()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    else:
        return info
