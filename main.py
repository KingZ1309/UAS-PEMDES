import os
import sys
import uas
import users as User
from Pesanan import show_pesanan
from PyQt6.QtCore import QSize, Qt,pyqtSignal
       
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
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
    QPushButton,
    QGridLayout
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        basedir = os.path.dirname(__file__)

        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
        self.db.open()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.menu(), "Daftar Pesanan")
        self.tabs.addTab(self.pelanggan(), "Daftar Pelanggan")
        self.tabs.addTab(self.penjahit(), "Daftar Penjahit")
        self.setCentralWidget(self.tabs)
    
    def open_new_window(self):
        self.child_window = User.show_users()
        self.child_window.data_edit.connect(self.update_list_pelanggan)
        self.child_window.show()
    
    def tambahPelangganForm(self):
        self.child_window=User.tambahUser()
        self.child_window.data_tambah.connect(self.update_list_pelanggan)
        self.child_window.show()    
        
    
    def menu(self):
        container = QWidget()
        layout_search = QHBoxLayout()
        
        self.nama_pelanggan = QLineEdit()
        self.nama_pelanggan.setPlaceholderText("Nama Pelanggan")
        self.nama_pelanggan.textChanged.connect(self.update_query)

        self.nama_penjahit = QLineEdit()
        self.nama_penjahit.setPlaceholderText("Nama Penjahit")
        self.nama_penjahit.textChanged.connect(self.update_query)


        layout_search.addWidget(self.nama_pelanggan)
        layout_search.addWidget(self.nama_penjahit)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)
        tambah = QPushButton("Tambah Pesanan")
        tambah.clicked.connect(self.tambahPesananForm)
        layout_view.addWidget(tambah)
        self.table = QTableView()

        layout_view.addWidget(self.table)

        container.setLayout(layout_view)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        self.update_query()
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Panjang Lengan")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Lingkar Pinggang")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Lingkar Dada")
        self.model.setHeaderData(5, Qt.Orientation.Horizontal, "Lebar Bahu")
        self.model.setHeaderData(6, Qt.Orientation.Horizontal, "Lingkar Pinggul")
        self.model.setHeaderData(7, Qt.Orientation.Horizontal, "Panjang Baju")
        self.model.setHeaderData(8, Qt.Orientation.Horizontal, "Tanggal Pesan")
        self.model.setHeaderData(9, Qt.Orientation.Horizontal, "Tanggal Ambil")
        self.model.setHeaderData(10, Qt.Orientation.Horizontal, "Harga")
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "Nama Pelanggan")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "Nama Penjahit")

        self.setMinimumSize(QSize(1024, 600))
        return container
    
    def tambahPesananForm(self):
        self.pesanan_window = show_pesanan(parent=self)
        self.pesanan_window.data_added.connect(self.update_query)
        self.pesanan_window.data_tambah.connect(self.pesanan_window.update_option)

        self.pesanan_window.show()

        
    def update_query(self):
        nama_pelanggan = self.nama_pelanggan.text()
        nama_penjahit = self.nama_penjahit.text()
        self.sql = QSqlQuery(db=self.db)
        
        self.sql.prepare( """
            SELECT users.nama, penjahit.nama_penjahit,baju.panjang_lengan, baju.lingkar_pinggang, baju.lingkar_dada,
                baju.lebar_bahu, baju.lingkar_pinggul, baju.panjang_baju, baju.tanggal_pesan,
                baju.tanggal_ambil, baju.harga 
            FROM baju JOIN users ON baju.id_user = users.id_user JOIN penjahit ON baju.id_penjahit = penjahit.id_penjahit
            WHERE users.nama LIKE '%'|| :nama_pelanggan|| '%' AND penjahit.nama_penjahit LIKE '%'|| :penjahit ||'%'
        """)
        self.sql.bindValue(":nama_pelanggan", nama_pelanggan)
        self.sql.bindValue(":penjahit", nama_penjahit)
        self.sql.exec()
        self.model.setQuery(self.sql)

    def pelanggan(self):
        container = QWidget()
        layout_search = QHBoxLayout()
        layout_view = QVBoxLayout()
        layout = QGridLayout()
        btn = QPushButton("Detail Pelanggan")
        tambah = QPushButton("Tambah Pelanggan")
        layout.addWidget(btn,0,0)
        layout.addWidget(tambah,0,1)
        layout_view.addLayout(layout)
        btn.clicked.connect(self.open_new_window)
        tambah.clicked.connect(self.tambahPelangganForm)

        self.track = QLineEdit()
        self.track.setPlaceholderText("Track name...")
        layout_view.addWidget(self.track)
        self.track.textChanged.connect(self.update_query)

        basedir = os.path.dirname(__file__)

        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
        self.db.open()
        self.table_pelanggan = QTableView()
        self.model_pelanggan = QSqlTableModel(db=self.db)
        self.model_pelanggan.setTable("users")
        self.update_list_pelanggan()
        self.table_pelanggan.setModel(self.model_pelanggan)
        layout_view.addWidget(self.table_pelanggan)

        container.setLayout(layout_view)
        self.setCentralWidget(container)
        self.child_window = None
        return container
    
    def update_list_pelanggan(self):
        self.model_pelanggan.select()
    
    def penjahit(self):
        container = QWidget()
        layout_search = QHBoxLayout()
        self.nama_penjahit = QLineEdit()
        self.nama_penjahit.setPlaceholderText("Nama Penjahit")
        self.nama_penjahit.textChanged.connect(self.update_query)
        self.telp_penjahit = QLineEdit()
        self.telp_penjahit.setPlaceholderText("No Telp Penjahit")
        self.telp_penjahit.textChanged.connect(self.update_query)
        layout_search.addWidget(self.nama_penjahit)
        layout_search.addWidget(self.telp_penjahit)
        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)
        tambah = QPushButton("Tambah Penjahit")
        layout_view.addWidget(tambah)
        self.table_penjahit = QTableView()
        layout_view.addWidget(self.table_penjahit)

        container.setLayout(layout_view)

        self.model_penjahit = QSqlQueryModel()
        self.table_penjahit.setModel(self.model_penjahit)

        self.query_penjahit = QSqlQuery(db=self.db)

        self.query_penjahit.prepare(
            """SELECT *
            FROM penjahit
            """
        )
        self.query_penjahit.exec()
        self.model_penjahit.setQuery(self.query_penjahit)

        self.setMinimumSize(QSize(1024, 600))
        return container

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
