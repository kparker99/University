import pymysql

def enter_into_db(command, data):
    conn = pymysql.connect(host='[redacted]', user='[redacted]', password='[redacted]', db='[redacted]')
    c = conn.cursor()
    try:
        c.execute(command, data)
        conn.commit()
        conn.close()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))


def get_info_from_db(query, variable = None):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
    c = conn.cursor()
    try:
        result = c.execute(query, variable)
        info = c.fetchall()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    return info

def get_one_info_from_db(query, variable = None):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='8Jk$4*j!M.3f', db='University')
    c = conn.cursor()
    try:
        result = c.execute(query, variable)
        info = c.fetchone()
    except pymysql.Error as e:
        return print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    return info

