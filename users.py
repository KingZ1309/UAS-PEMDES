from detailPelanggan import Ui_Dialog as detail
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
import sys
basedir = os.path.dirname(__file__)

class show_users(QMainWindow, detail):
    data_edit = pyqtSignal()
    recno = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('penjahit.sqlite')
        self.db.open()

        self.model = QSqlQueryModel(self)
        self.model.setQuery("select * from users")
        self.record = self.model.record(0)
        self.lineEdit.setText(str(self.record.value("nama")))
        self.lineEdit_2.setText(str(self.record.value("telp")))
        self.textEdit.setText(str(self.record.value("alamat")))
        self.pushButton_4.clicked.connect(self.dispFirst)
        self.pushButton.clicked.connect(self.dispPrevious)
        self.pushButton_2.clicked.connect(self.dispNext)
        self.pushButton_3.clicked.connect(self.dispLast)
        self.pushButton_5.clicked.connect(self.edit)
        
    def displayRec(self):
        self.record=self.model.record(show_users.recno)
        self.lineEdit.setText(str(self.record.value("nama")))
        self.lineEdit_2.setText(str(self.record.value("telp")))
        self.textEdit.setText(str(self.record.value("alamat"))) 
    def dispFirst(self):
        show_users.recno = 0
        self.displayRec()
    def dispPrevious(self):
        show_users.recno -= 1
        if show_users.recno < 0:
            show_users.recno = 0
        self.displayRec()
    def dispLast(self):
        show_users.recno = self.model.rowCount()-1
        self.displayRec()
    def dispNext(self): 
        show_users.recno += 1
        if show_users.recno > self.model.rowCount()-1:
            show_users.recno = self.model.rowCount()-1
        self.displayRec()
    
    def edit(self):
        userid = self.record.value("id_user")
        nama = self.lineEdit.text()
        telp = self.lineEdit_2.text()
        alamat = self.textEdit.toPlainText()
        
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
        db.open()
        self.query = QSqlQuery(db=db)
        self.query.prepare("""
            UPDATE users  
            SET nama = :nama, telp = :telp, alamat = :alamat
            WHERE id_user = :id;
        """)
        self.query.bindValue(':nama',nama)
        self.query.bindValue(':telp',telp)
        self.query.bindValue(':alamat',alamat)
        self.query.bindValue(':id',userid)
        self.query.exec()
        self.data_edit.emit()
        self.close()
