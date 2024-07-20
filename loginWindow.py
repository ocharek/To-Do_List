import sys
from listWindow import ListWindow
import mysql
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
import database

conn = database.connect_to_db()
if conn:
    cursor = conn.cursor()

class LoginWidget(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.labLog = QLabel('Try to log in')
        layout.addWidget(self.labLog)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton('Go to Register', self)
        register_button.clicked.connect(self.switch_func)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def login(self):
        try:
            cursor.execute("SELECT * FROM uzytkownicy WHERE Login = %s AND Haslo = %s", (self.username.text(), self.password.text()))
            res = cursor.fetchall()
            if res:
                self.taskwin = ListWindow(f"{res[0][0]}")
                self.taskwin.show()

        except mysql.connector.Error as err:
            print("Login failed!")

class RegisterWidget(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        self.switch_func = switch_func
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.labReg = QLabel('Register yourself')
        layout.addWidget(self.labReg)

        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.exist = QLabel('Username already in use.')
        self.exist.setStyleSheet("color: red;")
        self.exist.setVisible(False)
        layout.addWidget(self.exist)

        self.win = QMessageBox()
        self.win.setWindowTitle("Success")
        self.win.setText("You can log in now!")
        self.win.setStandardButtons(QMessageBox.Ok)
        self.win.setGeometry(150, 200, 0, 0)

        register_button = QPushButton('Register', self)
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        login_button = QPushButton('Go to Login', self)
        login_button.clicked.connect(self.switch_func)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def register(self):
        try:
            cursor.execute("CALL DodajUzytkownika(%s, %s)", (self.username.text(), self.password.text()))
            self.exist.setVisible(False)
            self.switch_func()
            self.win.exec()

        except database.mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error code
                self.exist.setVisible(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamic Window Content')

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_widget = LoginWidget(self.switch_to_register)
        self.register_widget = RegisterWidget(self.switch_to_login)

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        self.stacked_widget.setCurrentWidget(self.login_widget)

    def switch_to_register(self):
        self.stacked_widget.setCurrentWidget(self.register_widget)

    def switch_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)
