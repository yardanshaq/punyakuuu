
import tkinter as tk
from tkinter import ttk, messagebox

class KasirApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesin Kasir Toko Kelontong")
        self.root.geometry("1000x600")
        self.root.configure(bg='white')
        self.cart = []

        self.barang = {
            "BRG0001": {"nama": "Beras 5Kg", "harga": 60000},
            "BRG0002": {"nama": "Minyak Goreng 2L", "harga": 28000},
            "BRG0003": {"nama": "Gula Pasir 1Kg", "harga": 14000},
            "BRG0004": {"nama": "Indomie Goreng", "harga": 3000},
            "BRG0005": {"nama": "Kopi Sachet", "harga": 1500},
        }

        self.total_belanja = 0
        self.create_widgets()

    def create_widgets(self):
        frame_top = tk.Frame(self.root, bg='#003366')
        frame_top.pack(side=tk.TOP, fill=tk.X)

        tk.Label(frame_top, text="Kode/Barcode:", bg='#003366', fg='white').pack(side=tk.LEFT, padx=10, pady=10)
        self.kode_entry = tk.Entry(frame_top)
        self.kode_entry.pack(side=tk.LEFT, padx=5)
        self.kode_entry.focus()

        tk.Label(frame_top, text="Jumlah:", bg='#003366', fg='white').pack(side=tk.LEFT)
        self.jumlah_entry = tk.Entry(frame_top, width=5)
        self.jumlah_entry.insert(0, "1")
        self.jumlah_entry.pack(side=tk.LEFT, padx=5)

        tambah_btn = tk.Button(frame_top, text="Tambah ke Keranjang", command=self.tambah_keranjang, bg='green', fg='white')
        tambah_btn.pack(side=tk.LEFT, padx=10)

        frame_table = tk.Frame(self.root)
        frame_table.pack(fill='both', expand=True, padx=10, pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#f9f9f9",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#f9f9f9")
        style.map('Treeview', background=[('selected', '#347083')])

        self.tree = ttk.Treeview(frame_table, columns=("Kode", "Nama", "Harga", "Jumlah", "Total"), show='headings')
        for col in ("Kode", "Nama", "Harga", "Jumlah", "Total"):
            self.tree.heading(col, text=col)
        self.tree.column("Kode", anchor='center', width=120)
        self.tree.column("Nama", anchor='w', width=250)
        self.tree.column("Harga", anchor='center', width=100)
        self.tree.column("Jumlah", anchor='center', width=80)
        self.tree.column("Total", anchor='center', width=100)
        self.tree.pack(fill='both', expand=True)

        frame_bottom = tk.Frame(self.root, bg='white')
        frame_bottom.pack(fill=tk.X, pady=10)

        self.total_label = tk.Label(frame_bottom, text="Total Belanja: Rp 0", font=('Arial', 12, 'bold'), bg='white')
        self.total_label.pack(side=tk.LEFT, padx=10)

        tk.Label(frame_bottom, text="Bayar:", bg='white').pack(side=tk.LEFT)
        self.bayar_entry = tk.Entry(frame_bottom, width=10)
        self.bayar_entry.pack(side=tk.LEFT, padx=5)

        self.kembali_label = tk.Label(frame_bottom, text="Kembalian: Rp 0", bg='white')
        self.kembali_label.pack(side=tk.LEFT, padx=10)

        proses_btn = tk.Button(frame_bottom, text="Proses Bayar", bg='blue', fg='white', command=self.proses_bayar)
        proses_btn.pack(side=tk.RIGHT, padx=10)

        cetak_btn = tk.Button(frame_bottom, text="Cetak Struk", bg='orange', command=self.cetak_struk)
        cetak_btn.pack(side=tk.RIGHT, padx=5)

    def tambah_keranjang(self):
        kode = self.kode_entry.get().upper()
        try:
            jumlah = int(self.jumlah_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return

        if kode in self.barang:
            data = self.barang[kode]
            total = data['harga'] * jumlah
            self.cart.append((kode, data['nama'], data['harga'], jumlah, total))
            self.tree.insert('', 'end', values=(kode, data['nama'], f"Rp {data['harga']}", jumlah, f"Rp {total}"))
            self.update_total()
        else:
            messagebox.showerror("Error", "Kode barang tidak ditemukan.")

    def update_total(self):
        self.total_belanja = sum(item[4] for item in self.cart)
        self.total_label.config(text=f"Total Belanja: Rp {self.total_belanja}")

    def proses_bayar(self):
        try:
            bayar = int(self.bayar_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Masukkan nominal pembayaran yang valid.")
            return

        if bayar < self.total_belanja:
            messagebox.showwarning("Kurang", "Uang bayar kurang.")
        else:
            kembalian = bayar - self.total_belanja
            self.kembali_label.config(text=f"Kembalian: Rp {kembalian}")

    def cetak_struk(self):
        if not self.cart:
            messagebox.showinfo("Info", "Keranjang masih kosong.")
            return
        print("=== STRUK BELANJA ===")
        for item in self.cart:
            print(f"{item[1]} x{item[3]} = Rp {item[4]}")
        print(f"Total: Rp {self.total_belanja}")
        print("=====================")

if __name__ == "__main__":
    root = tk.Tk()
    app = KasirApp(root)
    root.mainloop()
