# Mesin Kasir Toko Kelontong
import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
from datetime import datetime

# Generate 100 barang contoh
def generate_barang():
    nama_barang = [
        "Indomie Goreng", "Indomie Soto", "Sabun Lifebuoy", "Sikat Gigi Pepsodent",
        "Odol Formula", "Teh Botol", "Kopi Kapal Api", "Gula Pasir", "Minyak Goreng Bimoli",
        "Beras Ramos", "Tepung Terigu", "Garam Dapur", "Air Mineral Aqua", "Rokok Sampoerna",
        "Rokok Gudang Garam", "Susu Dancow", "Kecap ABC", "Saus Sambal Indofood", "Sarden ABC",
        "Kornet Pronas", "Mie Sedap Ayam Bawang", "Susu Ultra", "Energen Coklat", "Chitato BBQ",
        "Beng-beng", "SilverQueen", "Kacang Garuda", "Permen Relaxa", "Tissue Paseo", "Masker Medis",
        "Obat Panadol", "Minyak Kayu Putih", "Hand Sanitizer", "Sabun Cuci Sunlight", "Baygon Spray",
        "Pasta Gigi Ciptadent", "Detergen Rinso", "Pewangi So Klin", "Kopi Good Day", "Teh Celup Sariwangi"
    ]
    barang = []
    for i in range(100):
        nama = random.choice(nama_barang)
        kode = f"BRG{str(i+1).zfill(4)}"
        barcode = f"{random.randint(100000000000,999999999999)}"
        harga = random.randint(1000, 25000)
        stok = random.randint(5, 100)
        barang.append({"kode": kode, "barcode": barcode, "nama": nama, "harga": harga, "stok": stok})
    return barang

class MesinKasir:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesin Kasir Toko Kelontong")
        self.root.geometry("1100x650")
        self.data_barang = generate_barang()
        self.keranjang = []
        self.create_widgets()

    def create_widgets(self):
        frame_atas = tk.Frame(self.root, bg='#003366', padx=15, pady=15)
        frame_atas.pack(fill='x')

        lbl_kode = tk.Label(frame_atas, text="Kode/Barcode:", bg='#003366', fg='white')
        lbl_kode.grid(row=0, column=0, sticky='w')
        self.ent_kode = tk.Entry(frame_atas, width=30)
        self.ent_kode.grid(row=0, column=1, padx=5)

        lbl_jumlah = tk.Label(frame_atas, text="Jumlah:", bg='#003366', fg='white')
        lbl_jumlah.grid(row=0, column=2, sticky='w')
        self.ent_jumlah = tk.Entry(frame_atas, width=10)
        self.ent_jumlah.insert(0, '1')
        self.ent_jumlah.grid(row=0, column=3, padx=5)

        btn_tambah = tk.Button(frame_atas, text="Tambah ke Keranjang", command=self.tambah_keranjang, bg='green', fg='white')
        btn_tambah.grid(row=0, column=4, padx=10)

        frame_table = tk.Frame(self.root)
        frame_table.pack(fill='both', expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_table, columns=("Kode", "Nama", "Harga", "Jumlah", "Total"), show='headings')
        for col in ["Kode", "Nama", "Harga", "Jumlah", "Total"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=150)
        self.tree.pack(fill='both', expand=True)

        frame_bawah = tk.Frame(self.root, bg='#f0f0f0', pady=10)
        frame_bawah.pack(fill='x')

        tk.Label(frame_bawah, text="Total Belanja:").grid(row=0, column=0, padx=5)
        self.label_total = tk.Label(frame_bawah, text="Rp 0", font=('Arial', 14, 'bold'))
        self.label_total.grid(row=0, column=1, padx=5)

        tk.Label(frame_bawah, text="Bayar:").grid(row=0, column=2, padx=5)
        self.ent_bayar = tk.Entry(frame_bawah, width=20)
        self.ent_bayar.grid(row=0, column=3, padx=5)

        tk.Label(frame_bawah, text="Kembalian:").grid(row=0, column=4, padx=5)
        self.label_kembali = tk.Label(frame_bawah, text="Rp 0")
        self.label_kembali.grid(row=0, column=5, padx=5)

        btn_bayar = tk.Button(frame_bawah, text="Proses Bayar", command=self.proses_bayar, bg='blue', fg='white')
        btn_bayar.grid(row=0, column=6, padx=10)

        btn_cetak = tk.Button(frame_bawah, text="Cetak Struk", command=self.cetak_struk, bg='orange', fg='white')
        btn_cetak.grid(row=0, column=7, padx=10)

    def cari_barang(self, kode):
        for item in self.data_barang:
            if item['kode'] == kode or item['barcode'] == kode:
                return item
        return None

    def tambah_keranjang(self):
        kode = self.ent_kode.get().strip()
        jumlah = int(self.ent_jumlah.get())
        barang = self.cari_barang(kode)
        if barang:
            total = barang['harga'] * jumlah
            self.keranjang.append({"kode": barang['kode'], "nama": barang['nama'], "harga": barang['harga'], "jumlah": jumlah, "total": total})
            self.tree.insert('', 'end', values=(barang['kode'], barang['nama'], f"Rp {barang['harga']}", jumlah, f"Rp {total}"))
            self.update_total()
            self.ent_kode.delete(0, tk.END)
            self.ent_jumlah.delete(0, tk.END)
            self.ent_jumlah.insert(0, '1')
        else:
            messagebox.showerror("Tidak Ditemukan", "Barang tidak ditemukan")

    def update_total(self):
        total = sum(item['total'] for item in self.keranjang)
        self.label_total.config(text=f"Rp {total}")

    def proses_bayar(self):
        try:
            bayar = int(self.ent_bayar.get())
            total = sum(item['total'] for item in self.keranjang)
            kembali = bayar - total
            if kembali < 0:
                messagebox.showwarning("Uang Kurang", "Uang yang dibayarkan kurang")
            else:
                self.label_kembali.config(text=f"Rp {kembali}")
        except ValueError:
            messagebox.showerror("Input Salah", "Masukkan nominal pembayaran dengan benar")

    def cetak_struk(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        nama_file = f"struk_{now}.txt"
        with open(nama_file, 'w') as f:
            f.write("STRUK PEMBELIAN\n")
            f.write("=======================\n")
            for item in self.keranjang:
                f.write(f"{item['nama']} x{item['jumlah']} - Rp {item['total']}\n")
            f.write("=======================\n")
            total = sum(i['total'] for i in self.keranjang)
            f.write(f"Total: Rp {total}\n")
            f.write(f"Dibayar: Rp {self.ent_bayar.get()}\n")
            f.write(f"Kembali: {self.label_kembali.cget('text')}\n")
        messagebox.showinfo("Struk Dicetak", f"Struk disimpan di {nama_file}")

if __name__ == '__main__':
    root = tk.Tk()
    app = MesinKasir(root)
    root.mainloop()