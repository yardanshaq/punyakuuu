from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import json, os, urllib.parse, webbrowser

# Load data produk dari file JSON
with open(r'D:\punyaku\bebas\data_produk.json', 'r') as f:
    produk_list = json.load(f)

# Konversi ke dict untuk akses cepat
produk_dict = {p["kode"]: p for p in produk_list}
produk_dict.update({p["nama"].lower(): p for p in produk_list})

# Inisialisasi window
root = Tk()
root.title("Toko Harum Sari")
root.attributes('-fullscreen', True)
#root.state('zoomed')
root.configure(bg="white")

cart = []
struk_terakhir = ""

# Fungsi update tampilan keranjang
def update_keranjang():
    for row in tree.get_children():
        tree.delete(row)
    total = 0
    for item in cart:
        total += item['total']
        tree.insert('', END, values=(item['kode'], item['nama'], item['harga'], item['jumlah'], item['total']))
    label_total.config(text=f"Rp {total:,}")
    entry_bayar.delete(0, END)
    label_kembalian.config(text="Rp 0")

# Fungsi tambah item ke keranjang
def tambah_ke_keranjang():
    kode = entry_kode.get().strip()
    jumlah = entry_jumlah.get().strip()

    if not jumlah.isdigit():
        messagebox.showwarning("Input Salah", "Pembayaran tidak sah!")
        return
    jumlah = int(jumlah)

    # Cari produk berdasarkan nama (caseless) yang mengandung string kode
    produk = None
    for p in produk_list:
        if kode.lower() in p["nama"].lower():
            produk = p
            break
    
    if not produk:
        messagebox.showerror("Tidak Ditemukan", "Barang tidak ditemukan!")
        return

    item = {
        "kode": produk["kode"],
        "nama": produk["nama"],
        "harga": produk["harga"],
        "jumlah": jumlah,
        "total": produk["harga"] * jumlah
    }
    cart.append(item)
    update_keranjang()
    entry_kode.delete(0, END)
    entry_jumlah.delete(0, END)
    entry_jumlah.insert(0, "1")


# Fungsi hapus item dari keranjang
def hapus_barang():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Pilih Item", "Pilih item yang ingin dihapus!")
        return
    for sel in selected:
        values = tree.item(sel, 'values')
        kode = values[0]
        for i, item in enumerate(cart):
            if item['kode'] == kode:
                del cart[i]
                break
    update_keranjang()

# Fungsi tampilkan daftar barang
def tampilkan_daftar_barang():
    daftar_window = Toplevel(root)
    daftar_window.title("Daftar Barang")
    daftar_window.geometry("700x400")

    style = ttk.Style(daftar_window)
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=28, background="#f5f5f5", fieldbackground="#f5f5f5")
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="#004080", foreground="white")

    tree_daftar = ttk.Treeview(daftar_window, columns=("Kode", "Nama", "Harga"), show="headings")
    tree_daftar.heading("Kode", text="Kode")
    tree_daftar.heading("Nama", text="Nama Barang")
    tree_daftar.heading("Harga", text="Harga")
    tree_daftar.column("Kode", anchor=CENTER, width=100)
    tree_daftar.column("Nama", anchor=W, width=400)
    tree_daftar.column("Harga", anchor=E, width=150)
    tree_daftar.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for p in produk_list:
        tree_daftar.insert('', END, values=(p["kode"], p["nama"], f"Rp {int(p['harga']):,}"))

# Fungsi proses pembayaran
def proses_bayar():
    total = sum(item['total'] for item in cart)
    bayar = entry_bayar.get().strip()
    if not bayar.isdigit():
        messagebox.showwarning("Input Salah", "Nominal bayar harus angka!")
        return
    bayar = int(bayar)
    if bayar < total:
        messagebox.showwarning("Uang Kurang", "Nominal bayar kurang!")
        return
    kembali = bayar - total
    label_kembalian.config(text=f"Rp {kembali:,}")

# Fungsi cetak struk
def cetak_struk():
    global struk_terakhir
    if not cart:
        messagebox.showwarning("Kosong", "Keranjang belanja kosong!")
        return

    total = sum(item['total'] for item in cart)
    bayar_str = entry_bayar.get().strip()
    if not bayar_str.isdigit():
        messagebox.showwarning("Input Salah", "Nominal bayar harus angka!")
        return
    bayar = int(bayar_str)
    kembali = bayar - total

    now = datetime.now()
    waktu = now.strftime("%d-%m-%Y %H:%M:%S")
    struk_lines = [
        "===== Toko Harum Sari =====",
        f"Waktu: {waktu}",
        "-----------------------------",
    ]

    for item in cart:
        struk_lines.append(f"{item['nama']} x{item['jumlah']} @Rp{item['harga']:,} = Rp{item['total']:,}")

    struk_lines += [
        "-----------------------------",
        f"Total      : Rp{total:,}",
        f"Bayar      : Rp{bayar:,}",
        f"Kembalian  : Rp{kembali:,}",
        "=============================",
        "Terima kasih telah berbelanja!"
    ]

    struk_terakhir = "\n".join(struk_lines)

    with open("struk_belanja.txt", "w", encoding="utf-8") as f:
        f.write(struk_terakhir)

    struk_window = Toplevel(root)
    struk_window.title("Struk Belanja")
    struk_box = Text(struk_window, width=60, height=20, font=("Courier", 12))
    struk_box.pack(padx=10, pady=10)
    struk_box.insert(END, struk_terakhir)
    struk_box.config(state=DISABLED)

# Fungsi kirim struk ke WhatsApp Web
def kirim_ke_whatsapp():
    global struk_terakhir
    if not struk_terakhir:
        messagebox.showwarning("Tidak Ada Struk", "Belum ada struk untuk dikirim.")
        return
    pesan = urllib.parse.quote(struk_terakhir)
    url = f"https://wa.me/?text={pesan}"
    webbrowser.open(url)
    reset_transaksi()

def reset_transaksi():
    cart.clear()
    struk_terakhir = ""
    update_keranjang()
    label_kembalian.config(text="Rp 0")
    entry_bayar.delete(0, END)


# UI Atas
frame_top = Frame(root, bg="#003366", pady=10)
frame_top.pack(fill=X)

Label(frame_top, text="Kode/Nama Barang:", bg="#003366", fg="white", font=("Arial", 11)).pack(side=LEFT, padx=5)
entry_kode = Entry(frame_top, width=30, font=("Arial", 11))
entry_kode.pack(side=LEFT, padx=5)
entry_kode.bind("<Return>", lambda event: tambah_ke_keranjang())

Label(frame_top, text="Jumlah:", bg="#003366", fg="white", font=("Arial", 11)).pack(side=LEFT)
entry_jumlah = Entry(frame_top, width=5, font=("Arial", 11))
entry_jumlah.insert(0, "1")
entry_jumlah.pack(side=LEFT, padx=5)
entry_jumlah.bind("<Return>", lambda event: tambah_ke_keranjang())

Button(frame_top, text="Tambah", bg="green", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5, command=tambah_ke_keranjang).pack(side=LEFT, padx=5)
Button(frame_top, text="Hapus Barang", bg="red", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5, command=hapus_barang).pack(side=LEFT, padx=5)
Button(frame_top, text="Daftar Barang", bg="#004080", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5, command=tampilkan_daftar_barang).pack(side=LEFT, padx=5)

# Treeview keranjang
cols = ("Kode", "Nama", "Harga", "Jumlah", "Total")
tree = ttk.Treeview(root, columns=cols, show="headings", height=20)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, stretch=True)
tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Footer: Total dan Bayar
frame_footer = Frame(root, bg="white", pady=10)
frame_footer.pack(fill=X)

Label(frame_footer, text="Total:", bg="white", font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
label_total = Label(frame_footer, text="Rp 0", bg="white", fg="black", font=("Arial", 12, "bold"))
label_total.pack(side=LEFT)

Label(frame_footer, text="    Bayar:", bg="white", font=("Arial", 11)).pack(side=LEFT)
entry_bayar = Entry(frame_footer, width=15, font=("Arial", 11))
entry_bayar.pack(side=LEFT)

Label(frame_footer, text="    Kembalian:", bg="white", font=("Arial", 11)).pack(side=LEFT)
label_kembalian = Label(frame_footer, text="Rp 0", bg="white", font=("Arial", 11))
label_kembalian.pack(side=LEFT)

Button(frame_footer, text="Bayar", bg="blue", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5, command=proses_bayar).pack(side=LEFT, padx=10)
Button(frame_footer, text="Cetak Struk", bg="orange", fg="black", font=("Arial", 11, "bold"), padx=10, pady=5, command=cetak_struk).pack(side=LEFT)
Button(frame_footer, text="Kirim ke WA", bg="#25D366", fg="white", font=("Arial", 11, "bold"), padx=10, pady=5, command=kirim_ke_whatsapp).pack(side=LEFT, padx=5)

# Style Treeview
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

root.mainloop()
#yardanshaq