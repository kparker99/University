from PyQt5 import QtWidgets as qtw
from lib.main import GUI_Window


if __name__ == '__main__':
    app = qtw.QApplication([])
    window = GUI_Window()

    qr = window.frameGeometry()
    cp = qtw.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

    window.show()
    app.exec_()
