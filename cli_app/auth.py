import csv
import re

USER_DATA  = "cli_app/data/user.csv"
ATTRIBUTE_DATA = "cli_app/data/data_attribute.csv"

def email_validator(email):
    return "@" in email and "." in email

def username_validator(username):
    if not username:
        return False, "Username tidak boleh kosong"
    
    username = username.strip()

    if len(username) < 4:
        return False, "Username harus terdiri dari minimal 4 karakter"
    
    if len(username) > 16:
        return False, "Username tidak boleh lebih dari 16 karakter"

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return False, "Username hanya boleh berisi huruf, angka, dan underscore (_)"

    return True, username

def password_validator(password):
    if not password:
        return False, "Password tidak boleh kosong"
    
    if not re.match(r"^[a-zA-Z0-9_]+$", password):
        return False, "Password hanya boleh berisi huruf, angka, dan underscore (_)"
    
    return True, password

def read_users():
    with open(USER_DATA, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_users(users):
    with open(USER_DATA, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["user_id", "nama_user", "password", "level", "total_xp", "email"]
        )
        writer.writeheader()
        writer.writerows(users)

def initialize_user_attributes(user_id):
    """Inisialisasi 6 attribute untuk user baru"""
    attributes = ['Intellect', 'Creativity', 'Vitality', 'Discipline', 'Social', 'Wealth']
    
    with open(ATTRIBUTE_DATA, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for attr in attributes:
            writer.writerow([user_id, attr, 1, 0])

def register(username, password, email):
    users = read_users()

    valid, result = username_validator(username)
    if not valid:
        return False, result
    
    username = result

    valid, result = password_validator(password)
    if not valid:
        return False, result

    if not email_validator(email):
        return False, "Tolong masukan email yang sesuai"

    # Cek username dengan case-insensitive
    for u in users:
        if u["nama_user"].lower() == username.lower():
            return False, "Username tersebut sudah digunakan"
        if u["email"].lower() == email.lower():
            return False, "Email sudah terdaftar"
        
    new_id = max(int(u["user_id"]) for u in users) + 1 if users else 1

    new_user = {
        "user_id": new_id,
        "nama_user": username,  # Simpan sesuai input user
        "password": password,
        "level": 1,
        "total_xp": 0,
        "email": email
    }

    users.append(new_user)
    write_users(users)
    
    # Inisialisasi attributes untuk user baru
    initialize_user_attributes(new_id)

    return True, "Registrasi berhasil"

def check_and_create_attributes(user_id):
    """Cek apakah user sudah punya attributes, jika belum maka buat"""
    try:
        with open(ATTRIBUTE_DATA, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row["user_id"]) == user_id:
                    # User sudah punya attribute
                    return False
        
        # User belum punya attribute, buat sekarang
        initialize_user_attributes(user_id)
        return True
    except FileNotFoundError:
        # File tidak ada, buat file dan attributes
        with open(ATTRIBUTE_DATA, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "attribute", "level", "xp"])
        
        initialize_user_attributes(user_id)
        return True

def login(username, password):
    users = read_users()

    # Login dengan case-insensitive untuk username
    for u in users:
        if u["nama_user"].lower() == username.lower() and u["password"] == password:
            user_id = int(u["user_id"])
            
            # Cek dan buat attributes jika belum ada (untuk user lama)
            created = check_and_create_attributes(user_id)
            if created:
                print("⚠️  Attributes diinisialisasi untuk akun Anda.")
            
            return True, u

    return False, "Username atau password salah"

print('')