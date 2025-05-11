def kasir_bbm():

    # daftar harga per liter untuk setiap jenis BBM
    harga_pertalite = 10000
    harga_pertamax = 12500
    harga_solar = 6800
    harga_pertamax_turbo = 15000

    # menampilkan pilihan jenis BBM
    print("|---------------------------------------|")
    print("|           Pilihan Jenis BBM           |")
    print("|---------------------------------------|")
    print("|1. Pertalite       (Rp 10.000 /liter)  |")
    print("|2. Pertamax        (Rp 12.500 /liter)  |")
    print("|3. Solar           (Rp 6.800  /liter)  |")
    print("|4. Pertamax Turbo  (Rp 15.000 /liter)  |")
    print("|---------------------------------------|\n")
    
    # meminta input nama pembeli
    nama_pembeli = input("Masukkan nama pembeli: ")
    
    # meminta input pilihan jenis BBM
    pilihan = input("Masukkan pilihan (1/2/3/4): ")

    # meminta input jumlah liter dan mengganti koma dengan titik
    jumlah_liter_str = input("Masukkan jumlah liter: ")
    jumlah_liter_str = jumlah_liter_str.replace(',', '.')  # mengganti koma dengan titik

    try:
        jumlah_liter = float(jumlah_liter_str)  # konversi ke float
    except ValueError:
        print("Input jumlah liter tidak valid!")
        return

    # menghitung total harga berdasarkan pilihan jenis BBM
    if pilihan == "1":
        jenis_bbm = "Pertalite"
        harga_per_liter = harga_pertalite
    elif pilihan == "2":
        jenis_bbm = "Pertamax"
        harga_per_liter = harga_pertamax
    elif pilihan == "3":
        jenis_bbm = "Solar"
        harga_per_liter = harga_solar
    elif pilihan == "4":
        jenis_bbm = "Pertamax Turbo"
        harga_per_liter = harga_pertamax_turbo
    else:
        print("Pilihan tidak valid.")
        return

    total_harga = harga_per_liter * jumlah_liter

    # menampilkan struk pembelian
    print("\n--- Struk Pembelian ---")
    print(f"Nama Pembeli: {nama_pembeli}")
    print(f"Jenis BBM: {jenis_bbm}")
    print(f"Harga per Liter: Rp {harga_per_liter:,.0f}")
    print(f"Jumlah Liter: {jumlah_liter:.2f} liter")
    print(f"Total Harga: Rp {total_harga:,.0f}")
    print("-----------------------")

# memanggil fungsi kasir_bbm
kasir_bbm()
#yardanshaq