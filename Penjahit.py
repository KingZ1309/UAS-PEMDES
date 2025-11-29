from tambahPenjahit import Ui_Dialog as formPenjahit
from PyQt6.QtCore import QSize, Qt,pyqtSignal
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
import os
import sqlite3
import sys

basedir = os.path.dirname(__file__)


class form_tambah(QMainWindow, formPenjahit):
    data_added = pyqtSignal()
    data_tambah = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.parent_window = parent
        
        self.tambahPenjahitBtn.clicked.connect(self.tambahPenjahit)
    
    def tambahPenjahit(self):
        nama = self.tambahNamaPenjahit.text()
        telp = self.tambahTelpPenjahit.text()
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
        db.open()
        self.query = QSqlQuery(db=db)
        self.query.prepare("""
            INSERT INTO penjahit (nama_penjahit, telp_penjahit)  
            VALUES(:nama,:telp);
        """)
        self.query.bindValue(':nama',nama)
        self.query.bindValue(':telp',telp)
        self.query.exec()
        self.data_tambah.emit()
        self.close()