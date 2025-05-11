import sys
import json
import os
import urllib.parse
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QTextEdit, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

DATA_PATH = 'D:/punyaku/bebas/data_produk.json'

def load_barang():
    barang_dict = {}
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                barang_dict[item['kode']] = {
                    'nama': item['nama'],
                    'harga': int(item['harga'])
                }
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Gagal load data: {e}")
    return barang_dict

class KasirApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toko Harum Sari")
        self.showFullScreen()
        self.barang_data = load_barang()
        self.keranjang = []
        self.struk_terakhir = ""
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        font_bold = QFont('Segoe UI', 10, QFont.Bold)

        label_barang = QLabel("Kode/Nama:")
        self.input_barang = QLineEdit()
        self.input_barang.setPlaceholderText("Masukkan kode / nama barang")

        label_jumlah = QLabel("Jumlah:")
        self.input_jumlah = QLineEdit("1")

        self.tombol_tambah = QPushButton("Tambah")
        self.tombol_tambah.clicked.connect(self.tambah_barang)

        self.btn_daftar = QPushButton("Daftar Barang")
        self.btn_daftar.clicked.connect(self.tampilkan_daftar_barang)

        hbox_input = QHBoxLayout()
        hbox_input.addWidget(label_barang)
        hbox_input.addWidget(self.input_barang)
        hbox_input.addWidget(label_jumlah)
        hbox_input.addWidget(self.input_jumlah)
        hbox_input.addWidget(self.tombol_tambah)
        hbox_input.addWidget(self.btn_daftar)

        self.tabel = QTableWidget(0, 5)
        self.tabel.setHorizontalHeaderLabels(["Kode", "Nama", "Harga", "Jumlah", "Total"])
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabel.setAlternatingRowColors(True)

        self.label_total = QLabel("Total: Rp 0")
        self.label_total.setFont(font_bold)

        label_bayar = QLabel("Bayar:")
        self.input_bayar = QLineEdit()
        self.label_kembalian = QLabel("Kembalian: Rp 0")

        self.btn_bayar = QPushButton("Bayar")
        self.btn_bayar.clicked.connect(self.proses_bayar)

        self.btn_hapus = QPushButton("Hapus Barang")
        self.btn_hapus.clicked.connect(self.hapus_barang)

        self.btn_cetak = QPushButton("Cetak Struk")
        self.btn_cetak.clicked.connect(self.cetak_struk)

        self.btn_wa = QPushButton("Kirim WhatsApp")
        self.btn_wa.clicked.connect(self.kirim_wa)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_keranjang)

        hbox_footer = QHBoxLayout()
        hbox_footer.addWidget(self.label_total)
        hbox_footer.addWidget(label_bayar)
        hbox_footer.addWidget(self.input_bayar)
        hbox_footer.addWidget(self.label_kembalian)
        hbox_footer.addWidget(self.btn_bayar)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.btn_hapus)
        hbox_buttons.addWidget(self.btn_cetak)
        hbox_buttons.addWidget(self.btn_wa)
        hbox_buttons.addWidget(self.btn_reset)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_input)
        vbox.addWidget(self.tabel)
        vbox.addLayout(hbox_footer)
        vbox.addLayout(hbox_buttons)

        central_widget.setLayout(vbox)

        # Styling UI with CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f9;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #fff;
            }
            QTableWidget::item {
                padding: 8px;
                font-size: 12px;
            }
            QTableWidget::item:selected {
                background-color: #80c7a9;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #f9f9f9;
            }
            QTextEdit {
                background-color: #f9f9f9;
                font-size: 12px;
                padding: 5px;
            }
        """)

        # Set up event listeners for Enter key
        self.input_barang.returnPressed.connect(self.tambah_barang)
        self.input_bayar.returnPressed.connect(self.proses_bayar)

    def tambah_barang(self):
        keyword = self.input_barang.text().strip().lower()
        jumlah = self.input_jumlah.text().strip()
        if not keyword or not jumlah.isdigit():
            return
        jumlah = int(jumlah)
        barang_ditemukan = None
        for kode, info in self.barang_data.items():
            if keyword == kode.lower() or keyword in info['nama'].lower():
                barang_ditemukan = (kode, info)
                break
        if barang_ditemukan:
            kode, info = barang_ditemukan
            self.keranjang.append({
                "kode": kode, "nama": info['nama'], "harga": info['harga'], "jumlah": jumlah
            })
            self.update_tabel()
        self.input_barang.clear()
        self.input_jumlah.setText("1")

    def update_tabel(self):
        self.tabel.setRowCount(0)
        total_belanja = 0
        for item in self.keranjang:
            row = self.tabel.rowCount()
            self.tabel.insertRow(row)
            # Set items for the table without adding row numbers
            self.tabel.setItem(row, 0, QTableWidgetItem(item['kode']))
            self.tabel.setItem(row, 1, QTableWidgetItem(item['nama']))
            self.tabel.setItem(row, 2, QTableWidgetItem(f"Rp {item['harga']:,}"))
            self.tabel.setItem(row, 3, QTableWidgetItem(str(item['jumlah'])))
            total = item['harga'] * item['jumlah']
            self.tabel.setItem(row, 4, QTableWidgetItem(f"Rp {total:,}"))
            total_belanja += total
        self.label_total.setText(f"Total: Rp {total_belanja:,}")
        self.label_kembalian.setText("Kembalian: Rp 0")

    def proses_bayar(self):
        if not self.input_bayar.text().isdigit():
            QMessageBox.warning(self, "Salah Input", "Pembayaran tidak valid.")
            return
        bayar = int(self.input_bayar.text())
        total = sum(i['harga'] * i['jumlah'] for i in self.keranjang)
        if bayar < total:
            QMessageBox.warning(self, "Kurang", "Nominal bayar kurang.")
            return
        kembali = bayar - total
        self.label_kembalian.setText(f"Kembalian: Rp {kembali:,}")

    def hapus_barang(self):
        row = self.tabel.currentRow()
        if row >= 0:
            del self.keranjang[row]
            self.update_tabel()

    def reset_keranjang(self):
        self.keranjang.clear()
        self.struk_terakhir = ""
        self.input_bayar.clear()
        self.update_tabel()

    def cetak_struk(self):
        if not self.keranjang:
            QMessageBox.information(self, "Info", "Keranjang kosong.")
            return
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        total = sum(i['harga'] * i['jumlah'] for i in self.keranjang)
        bayar = int(self.input_bayar.text()) if self.input_bayar.text().isdigit() else total
        kembali = bayar - total
        lines = [
            "===== Toko Harum Sari =====",
            f"Waktu: {now}",
            "-----------------------------"
        ]
        for item in self.keranjang:
            lines.append(f"{item['nama']} x{item['jumlah']} @Rp{item['harga']:,} = Rp{item['harga']*item['jumlah']:,}")
        lines += [
            "-----------------------------",
            f"Total     : Rp{total:,}",
            f"Bayar     : Rp{bayar:,}",
            f"Kembalian : Rp{kembali:,}",
            "=============================",
            "Terima kasih telah berbelanja!"
        ]
        self.struk_terakhir = "\n".join(lines)

        dlg = QDialog(self)
        dlg.setWindowTitle("Struk Belanja")
        layout = QVBoxLayout(dlg)
        txt = QTextEdit()
        txt.setText(self.struk_terakhir)
        txt.setReadOnly(True)
        layout.addWidget(txt)
        dlg.resize(400, 400)
        dlg.exec_()

    def kirim_wa(self):
        if not self.struk_terakhir:
            QMessageBox.warning(self, "Tidak Ada Struk", "Struk belum dicetak.")
            return
        pesan = urllib.parse.quote(self.struk_terakhir)
        url = f"https://wa.me/?text={pesan}"
        webbrowser.open(url)
        self.reset_keranjang()

    def tampilkan_daftar_barang(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Daftar Barang")
        layout = QVBoxLayout(dlg)
        tabel = QTableWidget(0, 3)
        tabel.setHorizontalHeaderLabels(["Kode", "Nama", "Harga"])
        tabel.setEditTriggers(QTableWidget.NoEditTriggers)  # Disabling editing
        tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for kode, info in self.barang_data.items():
            row = tabel.rowCount()
            tabel.insertRow(row)
            # Remove adding row number here
            tabel.setItem(row, 0, QTableWidgetItem(kode))
            tabel.setItem(row, 1, QTableWidgetItem(info['nama']))
            tabel.setItem(row, 2, QTableWidgetItem(f"Rp {info['harga']:,}"))
        layout.addWidget(tabel)
        dlg.resize(500, 400)
        dlg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KasirApp()
    window.show()
    sys.exit(app.exec_())