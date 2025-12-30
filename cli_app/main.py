# main.py
from auth import register, login
from gamification import add_achievement, view_profile, view_achievement
from cli_utils import clear, divider, header

clear()

def main():
    while True:
        print("\n=== LEVEL UP LIFE CLI ===")
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
                print("Login gagal:", user)
                continue
            
            clear()

            print(f"Login berhasil! Selamat Datang {user["nama_user"]}")
            user_id = int(user["user_id"])
            
            # Menu utama setelah login
            while True:
                print("\n=== MENU UTAMA ===")
                print("1. Tambah Achievement")
                print("2. Lihat Profile")
                print("3. Lihat Achievement")
                print("4. Logout")
                divider()
                
                menu_choice = input("Pilih Menu (1-4): ")
                
                if menu_choice == "1":
                    clear()

                    text = input("Nama achievement: ")
                    print("Difficulty: 1.Mudah 2.Sedang 3.Sulit 4.Sangat Sulit")
                    diff = int(input("Pilih: "))
                    print("Category: 1.Intellect 2.Creativity 3.Vitality 4.Discipline 5.Social 6.Wealth")
                    kat = int(input("Pilih Kategori (1-6): "))
                    
                    clear()

                    result = add_achievement(user_id, text, diff, kat)
                    print(result["message"])
                    if result["status"]:
                        print(f"XP gained: {result['xp_gained']} ({result['attribute']})")
                
                elif menu_choice == "2":
                    clear()
                    profile = view_profile(user_id)
                    print("\n--- PROFILE ---")
                    for k, v in profile.items():
                        if k == "attributes":
                            print("\n=== ATTRIBUTES ===")
                            for attr_name, attr_info in v.items():
                                print(f"  {attr_name}: {attr_info}")
                        else:
                            print(f"{k}: {v}")
                    divider()
                elif menu_choice == "3":
                    clear()

                    name, ach = view_achievement(user_id)
                    print(f"\n--- Achievement {name} ---")
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