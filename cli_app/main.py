# main.py
from auth import register, login
from gamification import add_achievement, view_profile, view_achievement

def main():
    print("=== LEVEL UP LIFE CLI ===")

    username = input("Username: ")
    password = input("Password: ")

    status, user = login(username, password)

    if not status:
        print("Login gagal:", user)
        return

    print("Login berhasil!")
    user_id = int(user["user_id"])

    while True:
        print("\nMenu:")
        print("1. Tambah Achievement")
        print("2. Lihat Profile")
        print("3. Lihat Achievement")
        print("4. Keluar")

        choice = input("Pilih: ")

        if choice == "1":
            text = input("Nama achievement: ")
            print("Difficulty: 1.Mudah 2.Sedang 3.Sulit 4.Sangat Sulit")
            diff = int(input("Pilih: "))
            print("Category: 1.Intellect 2.Creativity 3.Vitality 4.Dicipline 5.Social 6.Wealth")
            kat = int(input("Pilih: "))

            result = add_achievement(user_id, text, diff, kat)
            print(result["message"])

        elif choice == "2":
            profile = view_profile(user_id)
            print("\n--- PROFILE ---")
            for k, v in profile.items():
                print(f"{k}: {v}")

        elif choice == "3":
            name, ach = view_achievement(user_id)
            print(f"\n--- Achievement {name} ---")
            print(ach)

        elif choice == "4":
            print("Keluar dari aplikasi.")
            break

        else:
            print("Pilihan tidak valid")

if __name__ == "__main__":
    main()
