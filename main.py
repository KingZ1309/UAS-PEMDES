import os
import sys
import uas
import users as User

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

basedir = os.path.dirname(__file__)

db = QSqlDatabase("QSQLITE")
db.setDatabaseName(os.path.join(basedir, "penjahit.sqlite"))
db.open()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.menu(), "Daftar Pesanan")
        self.tabs.addTab(self.pelanggan(), "Daftar Pelanggan")
        self.tabs.addTab(self.penjahit(), "Daftar Penjahit")
        self.setCentralWidget(self.tabs)
    
    def open_new_window(self):
        self.child_window = User.show_users()
        self.child_window.show()
    
    def menu(self):
        container = QWidget()
        layout_search = QHBoxLayout()
        btn = QPushButton("Buka Window Baru")
        btn.clicked.connect(self.open_new_window)
        self.track = QLineEdit()
        self.track.setPlaceholderText("Track name...")
        self.track.textChanged.connect(self.update_query)

        self.composer = QLineEdit()
        self.composer.setPlaceholderText("Artist name...")
        self.composer.textChanged.connect(self.update_query)

        self.album = QLineEdit()
        self.album.setPlaceholderText("Album name...")
        self.album.textChanged.connect(self.update_query)

        layout_search.addWidget(self.track)
        layout_search.addWidget(self.composer)
        layout_search.addWidget(self.album)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)
        layout_view.addWidget(btn)
        self.table = QTableView()

        layout_view.addWidget(self.table)

        container.setLayout(layout_view)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        self.query = QSqlQuery(db=db)

        self.query.prepare(
            """SELECT baju.panjang_lengan,baju.lingkar_pinggang, users.nama
            FROM baju JOIN users ON baju.id_user = users.id_user
            """
        )
        self.update_query()

        self.setMinimumSize(QSize(1024, 600))
        # self.setCentralWidget(container)
        # return container
        self.child_window = None
        return container
    
    def pelanggan(self):
        container = QWidget()
        layout_search = QHBoxLayout()

        self.track = QLineEdit()
        self.track.setPlaceholderText("Track name...")
        self.track.textChanged.connect(self.update_query)

        self.composer = QLineEdit()
        self.composer.setPlaceholderText("Artist name...")
        self.composer.textChanged.connect(self.update_query)

        self.album = QLineEdit()
        self.album.setPlaceholderText("Album name...")
        self.album.textChanged.connect(self.update_query)

        layout_search.addWidget(self.track)
        layout_search.addWidget(self.composer)
        layout_search.addWidget(self.album)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)

        self.table = QTableView()

        layout_view.addWidget(self.table)

        container.setLayout(layout_view)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        self.query = QSqlQuery(db=db)

        self.query.prepare(
            """SELECT * FROM users
            """
        )
        self.update_query()

        self.setMinimumSize(QSize(1024, 600))
        # self.setCentralWidget(container)
        # return container
        return container
    def penjahit(self):
        container = QWidget()
        layout_search = QHBoxLayout()

        self.track = QLineEdit()
        self.track.setPlaceholderText("Track name...")
        self.track.textChanged.connect(self.update_query)

        self.composer = QLineEdit()
        self.composer.setPlaceholderText("Artist name...")
        self.composer.textChanged.connect(self.update_query)

        self.album = QLineEdit()
        self.album.setPlaceholderText("Album name...")
        self.album.textChanged.connect(self.update_query)

        layout_search.addWidget(self.track)
        layout_search.addWidget(self.composer)
        layout_search.addWidget(self.album)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)

        self.table = QTableView()

        layout_view.addWidget(self.table)

        container.setLayout(layout_view)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        self.query = QSqlQuery(db=db)

        self.query.prepare(
            """SELECT * FROM penjahit
            """
        )
        self.update_query()

        self.setMinimumSize(QSize(1024, 600))
        # self.setCentralWidget(container)
        # return container
        return container

    def update_query(self, s=None):

        # Get the text values from the widgets.
        # track_name = self.track.text()
        # track_composer = self.composer.text()
        # album_title = self.album.text()

        # self.query.bindValue(":track_name", track_name)
        # self.query.bindValue(":track_composer", track_composer)
        # self.query.bindValue(":album_title", album_title)

        self.query.exec()
        self.model.setQuery(self.query)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
