import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class StokObatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Stok Obat")
        self.root.geometry("1100x600")
        self.root.configure(bg='#ffffff')
        self.data_obat = []

        self.create_widgets()

    def create_widgets(self):
        # Frame input atas
        frame_input = tk.Frame(self.root, bg='#004080', padx=15, pady=15)
        frame_input.pack(fill='x')

        labels = [
            "Reg No", "Nama Obat", "Golongan", "Brand",
            "Expired (YYYY-MM-DD)", "Kemasan", "Jumlah", "Kode Obat",
            "Distributor", "Harga Beli", "Harga Grosir", "Harga Jual"
        ]

        self.entries = {}

        for i, label in enumerate(labels):
            row = i // 4
            col = i % 4
            lbl = tk.Label(frame_input, text=label, bg='#004080', fg='white', anchor='w')
            lbl.grid(row=row, column=col*2, sticky='w', padx=5, pady=5)
            ent = tk.Entry(frame_input, width=25)
            ent.grid(row=row, column=col*2 + 1, padx=5, pady=5)
            self.entries[label] = ent

        # Tombol aksi
        frame_btn = tk.Frame(self.root, bg='#ffffff', pady=10)
        frame_btn.pack()

        btn_tambah = tk.Button(frame_btn, text="Tambah Obat", bg="green", fg="white", width=15, command=self.tambah_obat)
        btn_hapus = tk.Button(frame_btn, text="Hapus Obat", bg="red", fg="white", width=15, command=self.hapus_obat)
        btn_bersih = tk.Button(frame_btn, text="Bersihkan Form", bg="blue", fg="white", width=15, command=self.bersihkan_form)

        btn_tambah.pack(side='left', padx=10)
        btn_hapus.pack(side='left', padx=10)
        btn_bersih.pack(side='left', padx=10)

        # Pencarian
        frame_cari = tk.Frame(self.root, pady=5, bg='#ffffff')
        frame_cari.pack()
        tk.Label(frame_cari, text="Cari Nama Obat:", bg='#ffffff').pack(side='left')
        self.search_var = tk.StringVar()
        tk.Entry(frame_cari, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(frame_cari, text="Cari", command=self.cari_obat).pack(side='left')

        # Tabel output
        frame_table = tk.Frame(self.root)
        frame_table.pack(fill='both', expand=True, padx=10, pady=10)

        columns = [
            "RegNo", "NamaObat", "Golongan", "Brand", "Expired",
            "Kemasan", "Jumlah", "KodeObat", "Distributor", "HargaBeli", "HargaGrosir"
        ]

        self.tree = ttk.Treeview(frame_table, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

    def tambah_obat(self):
        values = {k: v.get() for k, v in self.entries.items()}

        try:
            datetime.datetime.strptime(values["Expired (YYYY-MM-DD)"], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Format Salah", "Tanggal Expired harus format YYYY-MM-DD")
            return

        self.tree.insert('', 'end', values=(
            values["Reg No"], values["Nama Obat"], values["Golongan"], values["Brand"],
            values["Expired (YYYY-MM-DD)"], values["Kemasan"], values["Jumlah"],
            values["Kode Obat"], values["Distributor"], values["Harga Beli"], values["Harga Grosir"]
        ))

        self.bersihkan_form()

    def hapus_obat(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus")

    def bersihkan_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def cari_obat(self):
        keyword = self.search_var.get().lower()
        for item in self.tree.get_children():
            nama_obat = self.tree.item(item)['values'][1].lower()
            if keyword not in nama_obat:
                self.tree.detach(item)
            else:
                self.tree.reattach(item, '', 'end')

if __name__ == "__main__":
    root = tk.Tk()
    app = StokObatApp(root)
    root.mainloop()