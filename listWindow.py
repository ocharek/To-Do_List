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
        self.layout = QGridLayout()
        # Setting maximum size
        self.setMaximumHeight(200)
        self.setMinimumWidth(210)
        self.setMaximumWidth(210)

        self.load_tasks(self.layout)

        self.setLayout(self.layout)
        self.setWindowTitle('To-Do List')

    def load_tasks(self, layout):
        lab1 = QLabel('List of things to do:')
        self.layout.addWidget(lab1, 0, 0, 1, 3)
        conn = database.connect_to_db()

        self.x = 1
        self.tasks = database.select_all_tasks(conn, self.id)
        for task in self.tasks:
            lab = QLabel(f"• {task[1]}")
            lab.setWordWrap(True)
            chkb = QCheckBox()
            deltask = QPushButton('X')
            deltask.setFixedSize(14, 14)
            if task[2] == 1:
                lab.setStyleSheet("color: rgba(255, 255, 255, 100); text-decoration: line-through")
                chkb.setChecked(True)
            layout.addWidget(lab, self.x, 0)
            layout.addWidget(chkb, self.x, 1)
            layout.addWidget(deltask, self.x, 2)

            chkb.stateChanged.connect(lambda state, t=task, l=lab: self.checkt(t, l, state))
            deltask.clicked.connect(lambda _, t=task: self.delete_task(t))

            self.x += 1

        self.add = QTextEdit()
        self.add.setFixedSize(140, 42)
        self.addbtn = QPushButton('Add')
        self.addbtn.setFixedSize(40, 22)
        self.addbtn.clicked.connect(self.add_task)

        self.limit = QLabel('Limit of tasks reached! (8)')
        self.limit.setVisible(False)
        self.limit.setStyleSheet("color: red;")

        self.layout.addWidget(self.limit, self.x, 0, 1, 3)
        self.layout.addWidget(self.add, self.x + 1, 0)
        self.layout.addWidget(self.addbtn, self.x + 1, 1, 1, 2)
        # layout.setRowStretch(self.x, 1)
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
            if len(database.select_all_tasks(conn, self.id)) < 8:
                try:
                    database.add_task(conn, self.id, task)
                    print('Task added successfully')
                    self.clear_layout()  # Clear the layout
                    self.load_tasks(self.layout)  # Reinitialize the layout
                except database.mysql.connector.Error as err:
                    print(f"Error: {err.msg}")
            else:
                self.limit.setVisible(True)
        else:
            print("Task cannot be empty")
        database.close_connection(conn)

    def delete_task(self, task):
        # zrobic skalalnosc po usunieciu zadan
        conn = database.connect_to_db()
        try:
            database.delete_task(conn, task[0], self.id)  # Assuming task[0] is the task ID
            print('Task deleted successfully')
            self.clear_layout()  # Clear the layout
            self.load_tasks(self.layout)  # Reload tasks to refresh the UI
        except database.mysql.connector.Error as err:
            print(f"Error: {err.msg}")
        finally:
            database.close_connection(conn)

    def checkt(self, task, label, state):
        conn = database.connect_to_db()
        try:
            new_status = 1 if state == 2 else 0
            database.check_task(conn, task[0], new_status, self.id)  # Assuming task[0] is the task ID
            print('Task status updated successfully')
            if new_status == 1:
                label.setStyleSheet("text-decoration: line-through; color: rgba(255, 255, 255, 100);")
            else:
                label.setStyleSheet("")
        except database.mysql.connector.Error as err:
            print(f"Error: {err.msg}")
        finally:
            database.close_connection(conn)
