import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("film.db")
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS film (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT NOT NULL,
                sutradara TEXT NOT NULL,
                tahun INTEGER,
                durasi INTEGER,
                rating REAL,
                genre TEXT
            )
        """)

    def tambah(self, data):
        self.conn.execute("""
            INSERT INTO film (judul, sutradara, tahun, durasi, rating, genre)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        self.conn.commit()

    def ambil(self):
        return self.conn.execute("SELECT * FROM film").fetchall()

    def hapus(self, id):
        self.conn.execute("DELETE FROM film WHERE id=?", (id,))
        self.conn.commit()