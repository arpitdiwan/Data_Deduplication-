from PyQt5 import QtCore, QtGui, QtWidgets
from userprofile import Ui_userpofile
from client_core import auth


class Ui_MainWindow(object):

    def openUserProfile(self, un):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_userpofile(un)
        self.ui.setupUi(self.window)
        MainWindow.hide()
        self.window.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(668, 565)
        font = QtGui.QFont()
        font.setFamily("Product Sans")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 50, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Product Sans")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(36, 88, 601, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 120, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.username = QtWidgets.QLabel(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(160, 200, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.username.setFont(font)
        self.username.setObjectName("username")
        self.password = QtWidgets.QLabel(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(160, 250, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.username_fld = QtWidgets.QLineEdit(self.centralwidget)
        self.username_fld.setGeometry(QtCore.QRect(260, 200, 191, 22))
        self.username_fld.setObjectName("username_fld")
        self.password_fld = QtWidgets.QLineEdit(self.centralwidget)
        self.password_fld.setGeometry(QtCore.QRect(260, 250, 191, 22))
        self.password_fld.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_fld.setObjectName("password_fld")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(360, 300, 93, 28))
        self.login_btn.setObjectName("login_btn")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 350, 141, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(590, 480, 55, 16))
        self.label_6.setObjectName("label_6")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(40, 420, 601, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 170, 298, 19))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: red")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 668, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.login_btn.clicked.connect(self.user_login)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Client Application"))
        self.label_2.setText(_translate("MainWindow", "Enter login credentials"))
        self.username.setText(_translate("MainWindow", "Username:"))
        self.password.setText(_translate("MainWindow", "Password:"))
        self.login_btn.setText(_translate("MainWindow", "Login"))
        self.label_5.setText(_translate("MainWindow", "Forgot password?"))
        self.label_6.setText(_translate("MainWindow", "v:1.1.0"))
        self.label_3.setText(_translate("MainWindow", " "))

    def user_login(self):
        try:
            if len(self.username_fld.text()) == 0:
                self.label_3.setText("Please enter username and password")
            else:
                username = self.username_fld.text()
                password = self.password_fld.text()
                flag = auth(username, password)

                if flag == 1:
                    self.userwindow_op(username)
                else:
                    self.label_3.setText("Check Username ans Password")
        except Exception as e:
            print(e)

    def userwindow_op(self, uname):
        try:
            self.openUserProfile(uname)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
