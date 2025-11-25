
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QTableView,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QLabel,
    QPushButton
    
)
class show_users(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Baru")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah window baru!"))
        self.setLayout(layout)
        self.resize(300, 150)
