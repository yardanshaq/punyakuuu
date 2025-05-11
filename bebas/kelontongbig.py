import tkinter as tk
import tkinter.simpledialog
from tkinter import messagebox

def kasir_kelontong_gui():
    # Daftar harga barang
    harga_barang = {
        'Gula Pasir': 12000, 
        'Beras 5kg': 70000,
        'Minyak Goreng 1L': 15000,
        'Telur (per butir)': 2500,
        'Susu UHT 1L': 15000,
        'Mie Instan': 3000
    }

    # Membuat jendela utama
    window = tk.Tk()
    window.title("Kasir Kelontong")

    # Menampilkan daftar barang
    tk.Label(window, text="Daftar Barang Kelontong", font=('Arial', 14, 'bold')).pack(pady=10)

    listbox_barang = tk.Listbox(window, width=40, height=10)
    for idx, (barang, harga) in enumerate(harga_barang.items(), 1):
        listbox_barang.insert(tk.END, f"{idx}. {barang} - Rp {harga:,.0f}")
    listbox_barang.pack(pady=10)

    # Input nama pembeli
    tk.Label(window, text="Masukkan Nama Pembeli:").pack()
    entry_nama_pembeli = tk.Entry(window)
    entry_nama_pembeli.pack(pady=5)

    # List untuk menyimpan barang yang dipilih
    daftar_belanja = []

    def tambah_barang():
        try:
            # Mengambil nomor barang yang dipilih
            pilihan_barang = listbox_barang.curselection()
            if not pilihan_barang:
                messagebox.showwarning("Peringatan", "Pilih barang terlebih dahulu!")
                return

            pilihan_barang = pilihan_barang[0]  # Mengambil item pertama yang dipilih
            barang_terpilih = list(harga_barang.keys())[pilihan_barang]
            harga_per_unit = harga_barang[barang_terpilih]

            # Menampilkan kotak input jumlah barang
            jumlah_barang_str = tk.simpledialog.askstring("Jumlah Barang", f"Masukkan jumlah {barang_terpilih} yang ingin dibeli:")
            if jumlah_barang_str:
                jumlah_barang = float(jumlah_barang_str.replace(',', '.'))
                daftar_belanja.append((barang_terpilih, harga_per_unit, jumlah_barang))

        except ValueError:
            messagebox.showerror("Error", "Jumlah barang tidak valid!")

    def tampilkan_struk():
        nama_pembeli = entry_nama_pembeli.get()
        if not nama_pembeli:
            messagebox.showwarning("Peringatan", "Masukkan nama pembeli terlebih dahulu!")
            return
        
        total_harga = 0
        struk = f"--- Struk Pembelian ---\nNama Pembeli: {nama_pembeli}\n\n"
        for barang, harga, jumlah in daftar_belanja:
            subtotal = harga * jumlah
            struk += f"{barang:<22} {jumlah:.2f} unit x Rp {harga:,.0f} = Rp {subtotal:,.0f}\n"
            total_harga += subtotal

        struk += f"\nTotal Harga: Rp {total_harga:,.0f}"
        messagebox.showinfo("Struk Pembelian", struk)

    # Tombol untuk menambahkan barang ke daftar belanja
    button_tambah = tk.Button(window, text="Tambah Barang", command=tambah_barang)
    button_tambah.pack(pady=5)

    # Tombol untuk menampilkan struk pembelian
    button_struk = tk.Button(window, text="Tampilkan Struk", command=tampilkan_struk)
    button_struk.pack(pady=10)

    # Menjalankan aplikasi
    window.mainloop()

# Memanggil fungsi kasir_kelontong_gui
kasir_kelontong_gui()
#yardanshaq