import csv

USER_DATA  = "cli_app/data/user.csv"
ATTRIBUTE_DATA = "cli_app/data/data_attribute.csv"

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

def initialize_user_attributes(user_id):
    """Inisialisasi 6 attribute untuk user baru"""
    attributes = ['Intellect', 'Creativity', 'Vitality', 'Discipline', 'Social', 'Wealth']
    
    with open(ATTRIBUTE_DATA, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for attr in attributes:
            writer.writerow([user_id, attr, 1, 0])

def register(username, password):
    users = read_users()

    # Cek username dengan case-insensitive
    for u in users:
        if u["nama_user"].lower() == username.lower():
            return False, "Username sudah ada"

    new_id = max(int(u["user_id"]) for u in users) + 1 if users else 1

    new_user = {
        "user_id": new_id,
        "nama_user": username,  # Simpan sesuai input user
        "password": password,
        "level": 1,
        "total_xp": 0
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