from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from database.db_manager import DatabaseManager
from logic.validator import validate_input


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD NIM Genap")
        self.setGeometry(100, 100, 750, 520)

        self.db = DatabaseManager()
        self.selected_id = None

        self.init_ui()
        self.load_data()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        form = QFormLayout()

        self.judul = QLineEdit()
        self.sutradara = QLineEdit()

        self.tahun = QSpinBox()
        self.tahun.setRange(1900, 2100)

        self.durasi = QLineEdit()

        self.rating = QDoubleSpinBox()
        self.rating.setRange(1.0, 10.0)

        self.genre = QComboBox()
        self.genre.addItems(["Aksi", "Animasi", "Drama"])

        form.addRow("Judul Film", self.judul)
        form.addRow("Sutradara", self.sutradara)
        form.addRow("Tahun Rilis", self.tahun)
        form.addRow("Durasi", self.durasi)
        form.addRow("Rating", self.rating)
        form.addRow("Genre", self.genre)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()

        btn_simpan = QPushButton("Simpan")
        btn_simpan.clicked.connect(self.simpan)

        btn_hapus = QPushButton("Hapus")
        btn_hapus.clicked.connect(self.hapus)

        btn_clear = QPushButton("Bersihkan")
        btn_clear.clicked.connect(self.clear_form)

        btn_layout.addWidget(btn_simpan)
        btn_layout.addWidget(btn_hapus)
        btn_layout.addWidget(btn_clear)

        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Sutradara", "Tahun", "Durasi", "Rating", "Genre"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.clicked.connect(self.fill_form)

        layout.addWidget(self.table)
        central.setLayout(layout)

        self.statusBar().showMessage("Alya Dwi Pangesti - F1D02310104")

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Bantuan")

        about = QAction("Tentang", self)
        about.triggered.connect(self.show_about)

        help_menu.addAction(about)

        self.setStyleSheet("""
            QWidget { background-color: #ffe6f0; }
            QPushButton { background-color: #ff99cc; }
        """)

    def simpan(self):
        judul = self.judul.text().strip()
        sutradara = self.sutradara.text().strip()
        durasi = self.durasi.text().strip()

        valid, msg = validate_input(judul, sutradara, durasi)
        if not valid:
            QMessageBox.warning(self, "Error", msg)
            return

        data = (
            judul,
            sutradara,
            self.tahun.value(),
            int(durasi),
            self.rating.value(),
            self.genre.currentText()
        )

        self.db.tambah(data)
        self.load_data()
        self.clear_form()

    def load_data(self):
        data = self.db.ambil()
        self.table.setRowCount(0)

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, val in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(val)))

    def hapus(self):
        if not self.selected_id:
            return

        self.db.hapus(self.selected_id)
        self.load_data()
        self.clear_form()

    def fill_form(self):
        row = self.table.currentRow()
        self.selected_id = int(self.table.item(row, 0).text())

    def clear_form(self):
        self.judul.clear()
        self.sutradara.clear()
        self.durasi.clear()
        self.selected_id = None

    def show_about(self):
        QMessageBox.information(
            self,
            "Tentang",
            "Alya Dwi Pangesti - F1D02310104"
        )