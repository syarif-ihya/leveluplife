import csv

USER_DATA = "cli_app/data/user.csv"

def read_users():
    with open(USER_DATA, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_users(users):
    with open(USER_DATA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["user_id", "nama_user", "password", "level", "total_xp"]
        )
        writer.writeheader()
        writer.writerows(users)


def register(username, password):
    users = read_users()

    for u in users:
        if u["nama_user"] == username:
            return False, "Username sudah ada"

    new_id = max(int(u["user_id"]) for u in users) + 1 if users else 1

    new_user = {
        "user_id": new_id,
        "nama_user": username,
        "password": password,
        "level": 1,
        "total_xp": 0
    }

    users.append(new_user)
    write_users(users)

    return True, "Registrasi berhasil"

def login(username, password):
    users = read_users()

    for u in users:
        if u["nama_user"] == username and u["password"] == password:
            return True, u

    return False, "Username atau password salah"
