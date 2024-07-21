from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, QGridLayout, QMessageBox, QCheckBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, Signal
import database

class ListWindow(QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.initUI()
    def initUI(self):
        # Create items
        # Label
        self.layout = QGridLayout()

        self.load_tasks(self.layout)

        self.setLayout(self.layout)
        self.setWindowTitle('To-Do List')

    def load_tasks(self, layout):
        lab1 = QLabel('List of things to do:')
        self.layout.addWidget(lab1, 0, 0, 1, 2)
        conn = database.connect_to_db()
        self.x = 1
        self.tasks = database.select_all_tasks(conn, self.id)
        for task in self.tasks:
            lab = QLabel(f"• {task[1]}")
            chkb = QCheckBox()
            if task[2] == 1:
                lab.setStyleSheet("color: rgba(255, 255, 255, 100)")
                chkb.setChecked(True)
            layout.addWidget(lab, self.x, 0)
            layout.addWidget(chkb, self.x, 1)
            self.x += 1
        self.add = QTextEdit()
        self.add.setFixedSize(140, 42)
        self.addbtn = QPushButton('Add')
        self.addbtn.setFixedSize(40, 22)
        self.addbtn.clicked.connect(self.add_task)

        self.layout.addWidget(self.add, self.x, 0)
        self.layout.addWidget(self.addbtn, self.x, 1)
        database.close_connection(conn)

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
    def add_task(self):
        conn = database.connect_to_db()
        task = self.add.toPlainText().strip()
        if task:  # Ensure the task is not empty
            try:
                database.add_task(conn, self.id, task)
                print('Task added successfully')
                self.clear_layout()  # Clear the layout
                self.load_tasks(self.layout)  # Reinitialize the layout
            except database.mysql.connector.Error as err:
                print(f"Error: {err.msg}")
        else:
            print("Task cannot be empty")
        database.close_connection(conn)