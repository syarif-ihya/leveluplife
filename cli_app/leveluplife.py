# Sistem pencatatan pencapaian sederhana

def tampilkan_menu():
    print("\n=== SISTEM PENCAPAIAN ===")
    print("1. Tambahkan pencapaian")
    print("2. Lihat semua pencapaian")
    print("3. Keluar")

def main():
    pencapaian_list = []  # menyimpan semua pencapaian
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-3): ")

        if pilihan == "1":
            teks = input("Masukkan pencapaianmu: ")
            pencapaian_list.append(teks)
            print(f"✅ Pencapaian '{teks}' berhasil ditambahkan!")
        elif pilihan == "2":
            if pencapaian_list == []:
                print("📭 Belum ada pencapaian yang tercatat.")
            else:
                print("\n=== DAFTAR PENCAPAIAN ===")
                for i in range(len(pencapaian_list)):
                    p = pencapaian_list[i]
                    print(f"{i+1}. {p}")
        elif pilihan == "3":
            print("👋 Terima kasih! Sampai jumpa lagi.")
            break
        else:
            print("❌ Pilihan tidak valid, coba lagi!")

if __name__ == "__main__":
    main()
else:
    print(__name__)

# Setiap file python itu ada variabel __name__ yang kegunaanya sebagai status atau identitas dari file yang sedang dijalankan (sepengatuanku dari penjelasan chatgpt)
# intinya setiap file bakal mengoreksi __name__, jika dijalankan langsung maka __name__ == __main__
# tapi kalo dijalanin via import maka __name__ nya bukan main tapi sesuai nama file itu sendiri