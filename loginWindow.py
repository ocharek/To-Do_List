import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit

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
        print('Logging in with:', self.username.text(), self.password.text())


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

        register_button = QPushButton('Register', self)
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

        login_button = QPushButton('Go to Login', self)
        login_button.clicked.connect(self.switch_func)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def register(self):
        print('Registering with:', self.username.text(), self.password.text())


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
