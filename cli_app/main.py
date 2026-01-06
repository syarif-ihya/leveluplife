# main.py
from auth import register, login
from gamification import (
    add_achievement, 
    view_profile, 
    view_achievement,
    view_achievement_sorted, 
    search_achievement,      
    DIFFICULTY_LEVELS,      
    ATTRIBUTE_TYPES      
)
from cli_utils import clear, divider, header, progress_bar

clear()

def main():
    while True:
        header("LEVEL UP LIFE CLI")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        divider()

        choice = input("Pilih Menu (1-3): ")
        
        if choice == "1":
            # Login
            username = input("Username: ")
            password = input("Password: ")
            
            status, user = login(username, password)

            if not status:
                clear()
                print("Login gagal:", user)
                continue
            
            clear()

            print(f"Login berhasil! Selamat Datang {user['nama_user']}")
            user_id = int(user["user_id"])
            
            # Menu utama setelah login
            while True:
                print("\n============== MENU UTAMA ==============")
                print("1. Tambah Achievement")
                print("2. Lihat Profile")
                print("3. Lihat Achievement")
                print("4. Logout")
                divider()
                
                menu_choice = input("Pilih Menu (1-4): ")
                
                if menu_choice == "1":
                    clear()
                    
                    while True:
                        print(f"\n----------- Tambah Achievement -----------")
                        text = input("Nama achievement: ")
                        if text.strip(): 
                            break
                        clear()
                        print("Teks achievement tidak boleh kosong!")
                    
                    # MODIFIKASI: tampilkan dari tuple
                    while True:
                        print(f"\nDifficulty:")
                        for i, level in enumerate(DIFFICULTY_LEVELS, 1):
                            print(f"  {i}. {level}")
                        diff = input("Pilih (1-4): ")
                        
                        if not diff.strip():
                            print("Tingkat kesulitan tidak boleh kosong!")
                            continue
                        if not diff.isdigit(): 
                            print("Input harus berupa angka!")
                            continue
                        
                        diff = int(diff)

                        if diff not in range(1, len(DIFFICULTY_LEVELS) + 1):
                            print("Tingkat kesulitan tidak valid")
                            continue
                        break

                    # MODIFIKASI: tampilkan dari tuple
                    while True:
                        print(f"\nCategory:")
                        for i, attr in enumerate(ATTRIBUTE_TYPES, 1):
                            print(f"  {i}. {attr}")
                        kat = input("Pilih Kategori (1-6): ")
                        
                        if not kat.strip():
                            print("Kategori tidak boleh kosong!")
                            continue
                        if not kat.isdigit():
                            print("Input harus berupa angka!")
                            continue
                        
                        kat = int(kat)

                        if kat not in range(1, len(ATTRIBUTE_TYPES) + 1):
                            print("Kategori tidak valid")
                            continue
                        break
                    
                    clear()

                    result = add_achievement(user_id, text, diff, kat)

                    if not result["status"]:
                        print(f"\n{result['message']}")
                    else:
                        print(f"\n{result['message']}")
                        print(f"XP gained: {result['xp_gained']} ({result['attribute']})")
                        divider()

                elif menu_choice == "2":
                    clear()
                    profile = view_profile(user_id)
                    
                    header("PROFILE")
                    print(f"Nama         : {profile['nama']}")
                    print(f"Level        : {profile['level']}")
                    print(f"Progress     : {profile['progress_to_next']}")
                    print(f"Achievements : {profile['total_achievements']}")
                    
                    
                    print("\n============== ATTRIBUTES ==============")
                    for attr_name, attr_info in profile["attributes"].items():
                        level = attr_info["level"]
                        xp = attr_info["xp"]
                        xp_needed = attr_info["xp_needed"]
                        
                        bar = progress_bar(xp, xp_needed, width=20)
                        
                        print(f"\n{attr_name:<12} Lv.{level}")
                        print(f"  {bar} {xp}/{xp_needed} XP")
                    
                    divider()

                elif menu_choice == "3":
                    # MODIFIKASI BESAR: Menu achievement dengan sorting & searching
                    clear()
                    
                    print("\n======== ACHIEVEMENT MENU ========")
                    print("1. Lihat Semua Achievement")
                    print("2. Urutkan Achievement (Sort)")
                    print("3. Cari Achievement (Search)")
                    print("4. Kembali")
                    divider()
                    
                    ach_choice = input("Pilih (1-4): ")
                    
                    if ach_choice == "1":
                        # Lihat semua achievement (default)
                        clear()
                        name, ach = view_achievement(user_id)
                        print(f"\n--------- Achievement {name} ---------")
                        if len(ach) > 0:
                            print(ach.to_string())
                        else:
                            print("Belum ada achievement.")
                    
                    elif ach_choice == "2":
                        # SORTING ACHIEVEMENT
                        clear()
                        print("\n======== SORT ACHIEVEMENT ========")
                        print("1. Urutkan berdasarkan Tanggal (Terbaru)")
                        print("2. Urutkan berdasarkan Tanggal (Terlama)")
                        print("3. Urutkan berdasarkan Difficulty (Mudah-Sulit)")
                        print("4. Urutkan berdasarkan Difficulty (Sulit-Mudah)")
                        print("5. Urutkan berdasarkan Category (A-Z)")
                        divider()
                        
                        sort_choice = input("Pilih (1-5): ")
                        
                        sort_config = {
                            '1': ('datetime', True),   # Terbaru dulu
                            '2': ('datetime', False),  # Terlama dulu
                            '3': ('difficulty', False), # Mudah ke Sulit
                            '4': ('difficulty', True),  # Sulit ke Mudah
                            '5': ('category', False)   # A-Z
                        }
                        
                        if sort_choice in sort_config:
                            sort_by, reverse = sort_config[sort_choice]
                            clear()
                            name, ach = view_achievement_sorted(user_id, sort_by=sort_by, reverse=reverse)
                            
                            sort_labels = {
                                '1': 'Tanggal (Terbaru)',
                                '2': 'Tanggal (Terlama)',
                                '3': 'Difficulty (Mudah-Sulit)',
                                '4': 'Difficulty (Sulit-Mudah)',
                                '5': 'Category (A-Z)'
                            }
                            
                            print(f"\n--- Achievement {name} ({sort_labels[sort_choice]}) ---")
                            if len(ach) > 0:
                                print(ach.to_string())
                            else:
                                print("Belum ada achievement.")
                        else:
                            clear()
                            print("Pilihan tidak valid!")
                    
                    elif ach_choice == "3":
                        # SEARCHING ACHIEVEMENT
                        clear()
                        print("\n======== SEARCH ACHIEVEMENT ========")
                        keyword = input("Masukkan keyword (nama/kategori): ")
                        
                        if keyword.strip():
                            name, ach, found = search_achievement(user_id, keyword)
                            clear()
                            print(f"\n--- Hasil Pencarian '{keyword}' ---")
                            if found:
                                print(f"Ditemukan {len(ach)} achievement:")
                                print(ach.to_string())
                            else:
                                print("Tidak ada achievement yang cocok.")
                        else:
                            clear()
                            print("Keyword tidak boleh kosong!")
                    
                    elif ach_choice == "4":
                        clear()
                    else:
                        clear()
                        print("Pilihan tidak valid!")
                
                elif menu_choice == "4":
                    clear()

                    print("Logout berhasil.")
                    break
                
                else:
                    clear()
                    
                    print("Pilihan tidak valid")
        
        elif choice == "2":
            # Register
            username = input("Masukan Username: ")
            email = input("Masukan Email: ")
            password = input("Masukan Password: ")

            status, message = register(username, password, email)
            
            clear()

            if status:
                print("Registrasi berhasil! Silakan login.")
            else:
                print("Registrasi gagal:", message)
        
        elif choice == "3":
            print("Terima kasih telah menggunakan Level Up Life!")
            break
        
        else:
            clear()

            print("Pilihan tidak valid")

if __name__ == "__main__":
    main()