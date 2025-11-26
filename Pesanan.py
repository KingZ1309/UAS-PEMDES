from TambahPesanan import FormPesanan
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
basedir = os.path.dirname(__file__)

import sqlite3
import sys
class show_pesanan(QMainWindow, FormPesanan):
    data_added = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.parent_window = parent
        conn = sqlite3.connect("penjahit.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT id_user, nama FROM users")
        self.comboBox.clear()
        for row in cur.fetchall():
            id_user, nama = row
            self.comboBox.addItem(nama, id_user)
        
        cur.execute("SELECT id_penjahit, nama_penjahit FROM penjahit")
        self.comboBox_2.clear()
        for row in cur.fetchall():
            id_penjahit, nama = row
            self.comboBox_2.addItem(nama, id_penjahit)
        conn.close()
        
        self.pushButton.clicked.connect(self.tambahPesanan)
    def tambahPesanan(self):
        panjang_lengan = self.panjang_lengan.text()
        lingkar_pinggang = self.lingkar_pinggang.text()
        lingkar_dada = self.lingkar_dada.text()
        lebar_bahu = self.lebar_bahu.text()
        lingkar_pinggul = self.lingkar_pinggul.text()
        panjang_baju = self.panjang_baju.text()
        
        harga = self.spinBox.text()
        
        ambil = self.dateEdit.date().toString("yyyy-M-d")
        
        userid = self.comboBox.currentData()
        penjahitid = self.comboBox_2.currentData()
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
        db.open()
        self.query = QSqlQuery(db=db)
        self.query.prepare("""
            INSERT INTO baju 
                (id_user, id_penjahit, panjang_lengan, lingkar_pinggang, lingkar_dada,
                lebar_bahu, lingkar_pinggul, panjang_baju, tanggal_pesan,
                tanggal_ambil, harga)
                VALUES
                (:userID, :id_penjahit, :panjang_lengan, :lingkar_pinggang, :lingkar_dada,
                :lebar_bahu, :lingkar_pinggul, :panjang_baju, DATE('now'),
                :tanggal_ambil, :harga)
        """)

        self.query.bindValue(":userID", userid)
        self.query.bindValue(":id_penjahit", penjahitid)
        self.query.bindValue(":panjang_lengan", panjang_lengan)
        self.query.bindValue(":lingkar_pinggang", lingkar_pinggang)
        self.query.bindValue(":lingkar_dada", lingkar_dada)
        self.query.bindValue(":lebar_bahu", lebar_bahu)
        self.query.bindValue(":lingkar_pinggul", lingkar_pinggul)
        self.query.bindValue(":panjang_baju", panjang_baju)
        self.query.bindValue(":tanggal_ambil", ambil)
        self.query.bindValue(":harga", harga)

        self.query.exec()
        # if self.parent_window:
        self.data_added.emit()
        self.close()
        
        
