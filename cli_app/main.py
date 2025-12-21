# main.py
from auth import register, login
from gamification import add_achievement, view_profile, view_achievement, process_achievement

def main():
    print("=== LEVEL UP LIFE CLI ===")
    print("Apakah sudah punya akun?")
    print("1. Sudah (Login)")
    print("2. Belum (Register)")

    pilihan = input("Pilih: ")

    if pilihan == "1":
        username = input("Username: ")
        password = input("Password: ")

        status, user = login(username, password)
        if not status:
            print("Login gagal! Periksa username atau password.")
            return

    elif pilihan == "2":
        username = input("Username baru: ")
        password = input("Password: ")

        status, msg = register(username, password)
        print(msg)
        if not status:
            return

        status, user = login(username, password)

    else:
        print("Pilihan tidak valid")
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

            try:
                print("\nDifficulty:")
                print("1. Mudah")
                print("2. Sedang")
                print("3. Sulit")
                print("4. Sangat Sulit")
                diff = int(input("Pilih (1-4): "))

                print("\nCategory:")
                print("1. Intellect")
                print("2. Creativity")
                print("3. Vitality")
                print("4. Dicipline")
                print("5. Social")
                print("6. Wealth")
                kat = int(input("Pilih (1-6): "))

            except ValueError:
                print("Input harus berupa angka!")
                continue

            if diff not in [1, 2, 3, 4]:
                print("Pilihan difficulty tidak valid!")
                continue

            if kat not in [1, 2, 3, 4, 5, 6]:
                print("Pilihan category tidak valid!")
                continue

            result = add_achievement(user_id, text, diff, kat)
            if not result["status"]:
                print(result["message"])
                continue

            process_achievement(user_id, diff)
            print(result["message"])

        elif choice == "2":
            profile = view_profile(user_id)
            print("\n--- PROFILE ---")
            for k, v in profile.items():
                print(f"{k}: {v}")

        elif choice == "3":
            name, ach = view_achievement(user_id)
            print(f"\n--- Achievement {name} ---")
            if ach is None:
                print("Belum ada achievement.")
            else:
                print(ach)

        elif choice == "4":
            print("Keluar dari aplikasi.")
            break

        else:
            print("Pilihan tidak valid")

if __name__ == "__main__":
    main()
