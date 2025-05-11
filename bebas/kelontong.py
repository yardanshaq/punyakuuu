def kasir_kelontong():
    # Daftar harga barang
    harga_barang = {
        'Gula Pasir': 12000, 
        'Beras 5kg': 70000,
        'Minyak Goreng 1L': 15000,
        'Telur (per butir)': 2500,
        'Susu UHT 1L': 15000,
        'Mie Instan': 3000
    }

    # Menampilkan daftar barang dan harga dengan pemformatan yang rapi
    print("|------------------------------------------------|")
    print("|             Daftar Barang Kelontong            |")
    print("|------------------------------------------------|")
    print("| No | Nama Barang            | Harga per Unit   |")
    print("|----|------------------------|------------------|")
    for idx, (barang, harga) in enumerate(harga_barang.items(), 1):
        print(f"| {idx:<2} | {barang:<22} | Rp {harga:>13,} |")
    print("|------------------------------------------------|\n")

    # Meminta input nama pembeli
    nama_pembeli = input("Masukkan nama pembeli: ")
    
    # Membuat list untuk menyimpan barang yang dipilih
    daftar_belanja = []

    while True:
        try:
            # Meminta input nomor barang yang ingin dibeli (dengan banyak pilihan)
            pilihan_barang = input(f"Masukkan nomor barang yang ingin dibeli (pisahkan dengan koma, misal: 1, 2, 3), atau 0 untuk selesai: ")

            if pilihan_barang == '0':
                break  # Keluar dari loop jika pelanggan sudah selesai belanja

            # Mengonversi input menjadi list nomor yang dipilih
            pilihan_list = [int(p.strip()) for p in pilihan_barang.split(',')]

            for pilihan in pilihan_list:
                if 1 <= pilihan <= len(harga_barang):
                    # Menampilkan barang yang dipilih
                    barang_terpilih = list(harga_barang.keys())[pilihan - 1]
                    harga_per_unit = harga_barang[barang_terpilih]

                    # Meminta jumlah barang yang ingin dibeli (dengan titik atau koma)
                    jumlah_barang_str = input(f"Masukkan jumlah {barang_terpilih} yang ingin dibeli: ")
                    jumlah_barang_str = jumlah_barang_str.replace(',', '.')
                    jumlah_barang = float(jumlah_barang_str)

                    # Menambahkan barang dan jumlahnya ke dalam daftar belanja
                    daftar_belanja.append((barang_terpilih, harga_per_unit, jumlah_barang))
                else:
                    print(f"Pilihan {pilihan} tidak valid, coba lagi.")

        except ValueError:
            print("Input tidak valid, coba lagi.")

    # Menghitung total harga
    total_harga = 0
    print("\n--- Struk Pembelian ---")
    print(f"Nama Pembeli: {nama_pembeli}")
    for barang, harga, jumlah in daftar_belanja:
        subtotal = harga * jumlah
        print(f"{barang:<22} {jumlah:.2f} unit x Rp {harga:,.0f} = Rp {subtotal:,.0f}")
        total_harga += subtotal

    print(f"Total Harga: Rp {total_harga:,.0f}")
    print("-----------------------")

# Memanggil fungsi kasir_kelontong
kasir_kelontong()
#yardanshaq