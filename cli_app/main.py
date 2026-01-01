# main.py
from auth import register, login
from gamification import add_achievement, view_profile, view_achievement
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

            print(f"Login berhasil! Selamat Datang {user["nama_user"]}")
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
                    

                    while True:
                        print("\nDifficulty: 1.Mudah 2.Sedang 3.Sulit 4.Sangat Sulit")
                        diff = input("Pilih (1-4): ")
                        if not diff.strip():
                            print("Tingkat kesulitan tidak boleh kosong!")
                            continue
                        if not diff.isdigit(): 
                            print("Input harus berupa angka!")
                            continue
                        
                        diff = int(diff)

                        if diff not in range(1,5):
                            print("Tingkat kesulitan tidak valid")
                            continue
                        break

                    while True:
                        print("\nCategory: 1.Intellect 2.Creativity 3.Vitality 4.Discipline 5.Social 6.Wealth")
                        kat = input("Pilih Kategori (1-6): ")
                        if not kat.strip():
                            print("Kategori tidak boleh kosong!")
                            continue
                        if not kat.isdigit():
                            print("Input harus berupa angka!")
                            continue
                        
                        kat = int(kat)

                        if kat not in range(1,7):
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
                    clear()

                    name, ach = view_achievement(user_id)
                    print(f"\n--------- Achievement {name} ---------")
                    if len(ach) > 0:
                        print(ach.to_string())
                    else:
                        print("Belum ada achievement.")
                
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
            password = input("Masukan Password: ")
            email = input("Masukan Email: ")

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