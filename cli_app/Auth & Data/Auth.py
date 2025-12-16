from csv_handler import read_csv, write_csv

USER_DATA = "cli_app_test_train/Auth & Data/users.csv"

def register(username, password):
    users = read_csv(USER_DATA)

    for u in users:
        if any (u["username"] == username):
            return False, "Username Sudah Ada"  
    
    new_user = {
        "id" : str(len(users) + 1),
        "username" : username,
        "password": password,
        "xp": "0",
        "level": "1"
    }

    users.append(new_user)
    write_csv(USER_DATA, users[0].keys(), users)

    return True, "Registrasi Berhasil"

def login(username, password):
    users = read_csv(USER_DATA)

    for u in users:
        if u["username"] == username and u["password"] == password:
            return True, u

    return False, "Username atau Password Tidak Valid"