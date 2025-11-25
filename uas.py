import sqlite3
connection = sqlite3.connect('penjahit.sqlite')
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("""CREATE TABLE users (id_user INTEGER PRIMARY KEY AUTOINCREMENT
UNIQUE NOT NULL, nama TEXT, alamat TEXT NOT NULL,telp TEXT NOT NULL)""")
cursor.execute("DROP TABLE IF EXISTS baju;")
cursor.execute("DROP TABLE IF EXISTS penjahit;")
cursor.execute("DROP TABLE IF EXISTS detail_transaksi;")
cursor.execute("""CREATE TABLE penjahit (id_penjahit INTEGER PRIMARY KEY AUTOINCREMENT, nama_penjahit TEXT NOT NULL,telp_penjahit TEXT NOT NULL)""")
cursor.execute("""CREATE TABLE baju(
    id_baju INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    id_user INTEGER, 
    id_penjahit INTEGER,
    panjang_lengan DECIMAL(10,2) NOT NULL,
    lingkar_pinggang DECIMAL(10,2) NOT NULL,
    lingkar_dada DECIMAL(10,2) NOT NULL,
    lebar_bahu DECIMAL(10,2) NOT NULL, 
    lingkar_pinggul DECIMAL(10,2) NOT NULL,
    panjang_baju DECIMAL(10,2) NOT NULL,
    FOREIGN KEY(id_user) REFERENCES users(id_user),
    FOREIGN KEY(id_penjahit) REFERENCES penjahit(id_penjahit)
    )""")
cursor.execute("""
               CREATE TABLE detail_transaksi(
                   id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                   tanggal_pesan DATE,
                   tanggal_ambil DATE,
                   harga INTEGER,
                   id_baju INTEGER,
                   FOREIGN KEY(id_baju) REFERENCES baju(id_baju)
               )
            """)
cursor.execute("""INSERT INTO users (nama, alamat,telp) VALUES 
               ('rizal','jalan pegangsaan timur, jakarta selatan','0894258771'),
               ('rani','jalan basuki rahmat, lamongan','0834258421'),
               ('hanna','jalan patimura, Tuban','0853258771'),
               ('rizki','jalan diponegoro, semarang','0893428047'),
               ('yoga','jalan vetran, pamekasan','0834258772')
               """)
cursor.execute("""INSERT INTO penjahit (nama_penjahit,telp_penjahit) VALUES 
               ('zainal','0894258791'),
               ('isa','0834253421'),
               ('ali','0853298771'),
               ('rafi','0893428447'),
               ('ali muslim','0834256772')
               """)
cursor.execute("""INSERT INTO baju (id_user,id_penjahit,panjang_lengan,lingkar_pinggang,lingkar_dada,lebar_bahu,lingkar_pinggul,panjang_baju) VALUES 
               ('1','1','72','80','90','55','75','102'),
               ('2','1','79','76','98','64','77','98'),
               ('3','1','75','87','88','70','85','99'),
               ('4','2','70','79','89','61','80','100'),
               ('5','2','67','86','99','65','90','90')
               """)
cursor.execute("""INSERT INTO detail_transaksi (tanggal_pesan,tanggal_ambil,harga,id_baju) VALUES 
               ('2025-10-11','2025-10-12',200000,1),
               ('2025-10-11','2025-10-12',240000,2),
               ('2025-10-11','2025-10-12',250000,3),
               ('2025-10-11','2025-10-12',260000,4),
               ('2025-10-11','2025-10-12',270000,5)
               """)
connection.commit()
connection.close()