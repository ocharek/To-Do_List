from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QGridLayout, QMessageBox, QCheckBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, Signal
import database

conn = database.connect_to_db()
if conn:
    cursor = conn.cursor()

class ListWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        self.initUI(id)
    def initUI(self, id):
        # Create items
        # Label
        layout = QGridLayout()

        lab1 = QLabel('List of things to do:')
        layout.addWidget(lab1)
        self.tasks = database.select_all_tasks(conn, id)
        for task in self.tasks:
            if task[2] == 1:
                lab = QLabel(f"• {task[1]}")
                lab.setStyleSheet("color: rgba(255, 255, 255, 100)")
            else:
                lab = QLabel(f"• {task[1]}")

            layout.addWidget(lab)

        self.setLayout(layout)
        self.setWindowTitle('To-Do List')