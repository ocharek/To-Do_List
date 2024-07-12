from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QGridLayout, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, Signal

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # Create items
        # Label
        lab1 = QLabel('List of things to do:')

        layout = QGridLayout()

        layout.addWidget(lab1, 0, 0)

        self.setLayout(layout)
        self.setWindowTitle('To-Do List')