import json
import os
from datetime import datetime

# File untuk menyimpan data
DATA_FILE = "levelup_data.json"

# Konstanta
XP_PER_LEVEL = 100
CATEGORIES = ["Intellect", "Creativity", "Vitality", "Discipline", "Social", "Wealth"]
DIFFICULTIES = {
    "mudah": 10,
    "sedang": 25,
    "sulit": 50,
    "sangat sulit": 100
}

class LevelUpLife:
    def __init__(self):
        self.current_user = None
        self.data = self.load_data()
    
    def load_data(self):
        """Memuat data dari file JSON"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {"users": {}}
    
    def save_data(self):
        """Menyimpan data ke file JSON"""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def register(self):
        """Registrasi user baru"""
        print("\n=== REGISTRASI ===")
        username = input("Username: ").strip()
        
        if username in self.data["users"]:
            print("❌ Username sudah digunakan!")
            return False
        
        password = input("Password: ").strip()
        
        # Inisialisasi data user
        self.data["users"][username] = {
            "password": password,
            "level": 1,
            "xp": 0,
            "total_xp": 0,
            "achievements": [],
            "attributes": {cat: 0 for cat in CATEGORIES}
        }
        
        self.save_data()
        print(f"✅ Registrasi berhasil! Selamat datang, {username}!")
        return True
    
    def login(self):
        """Login user"""
        print("\n=== LOGIN ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if username not in self.data["users"]:
            print("❌ Username tidak ditemukan!")
            return False
        
        if self.data["users"][username]["password"] != password:
            print("❌ Password salah!")
            return False
        
        self.current_user = username
        print(f"✅ Login berhasil! Selamat datang kembali, {username}!")
        return True
    
    def add_achievement(self):
        """Menambah pencapaian baru"""
        if not self.current_user:
            print("❌ Silakan login terlebih dahulu!")
            return
        
        print("\n=== TAMBAH PENCAPAIAN ===")
        title = input("Judul pencapaian: ").strip()
        
        print("\nKategori:")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"{i}. {cat}")
        
        cat_choice = int(input("Pilih kategori (1-6): ")) - 1
        if cat_choice < 0 or cat_choice >= len(CATEGORIES):
            print("❌ Pilihan tidak valid!")
            return
        
        category = CATEGORIES[cat_choice]
        
        print("\nTingkat Kesulitan:")
        for i, (diff, xp) in enumerate(DIFFICULTIES.items(), 1):
            print(f"{i}. {diff.title()} (+{xp} XP)")
        
        diff_choice = int(input("Pilih kesulitan (1-4): "))
        difficulty = list(DIFFICULTIES.keys())[diff_choice - 1]
        xp_gained = DIFFICULTIES[difficulty]
        
        # Simpan achievement
        achievement = {
            "title": title,
            "category": category,
            "difficulty": difficulty,
            "xp": xp_gained,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        user = self.data["users"][self.current_user]
        user["achievements"].append(achievement)
        user["xp"] += xp_gained
        user["total_xp"] += xp_gained
        user["attributes"][category] += xp_gained
        
        # Cek level up
        while user["xp"] >= XP_PER_LEVEL:
            user["xp"] -= XP_PER_LEVEL
            user["level"] += 1
            print(f"\n🎉 LEVEL UP! Sekarang kamu Level {user['level']}!")
        
        self.save_data()
        print(f"\n✅ Pencapaian '{title}' berhasil ditambahkan!")
        print(f"💎 +{xp_gained} XP | Level {user['level']} ({user['xp']}/{XP_PER_LEVEL} XP)")
    
    def view_profile(self):
        """Melihat profil dan statistik"""
        if not self.current_user:
            print("❌ Silakan login terlebih dahulu!")
            return
        
        user = self.data["users"][self.current_user]
        
        print(f"\n{'='*50}")
        print(f"PROFIL: {self.current_user}")
        print(f"{'='*50}")
        print(f"Level: {user['level']}")
        print(f"XP: {user['xp']}/{XP_PER_LEVEL}")
        print(f"Total XP: {user['total_xp']}")
        print(f"Total Pencapaian: {len(user['achievements'])}")
        
        # Progress bar
        progress = int((user['xp'] / XP_PER_LEVEL) * 20)
        bar = "█" * progress + "░" * (20 - progress)
        print(f"\nProgress: [{bar}] {int((user['xp'] / XP_PER_LEVEL) * 100)}%")
        
        # Atribut
        print(f"\n{'ATRIBUT':-^50}")
        max_attr = max(user['attributes'].values()) if max(user['attributes'].values()) > 0 else 1
        
        for attr, value in user['attributes'].items():
            bar_length = int((value / max_attr) * 30) if max_attr > 0 else 0
            bar = "█" * bar_length
            print(f"{attr:12} [{bar:30}] {value}")
        
        # 5 Pencapaian terakhir
        if user['achievements']:
            print(f"\n{'PENCAPAIAN TERAKHIR':-^50}")
            for ach in user['achievements'][-5:]:
                print(f"• {ach['title']} ({ach['category']}) +{ach['xp']} XP")
                print(f"  {ach['date']}")
        
        print(f"{'='*50}\n")
    
    def view_achievements(self):
        """Melihat semua pencapaian"""
        if not self.current_user:
            print("❌ Silakan login terlebih dahulu!")
            return
        
        user = self.data["users"][self.current_user]
        
        if not user['achievements']:
            print("\n📝 Belum ada pencapaian. Yuk mulai catat pencapaianmu!")
            return
        
        print(f"\n{'DAFTAR PENCAPAIAN':-^60}")
        for i, ach in enumerate(user['achievements'], 1):
            print(f"\n{i}. {ach['title']}")
            print(f"   Kategori: {ach['category']} | Kesulitan: {ach['difficulty']}")
            print(f"   XP: +{ach['xp']} | Tanggal: {ach['date']}")
        print(f"{'-'*60}\n")
    
    def run(self):
        """Menjalankan aplikasi"""
        print("\n" + "="*50)
        print("SELAMAT DATANG DI LEVEL UP LIFE".center(50))
        print("="*50)
        
        while True:
            if not self.current_user:
                print("\n1. Login")
                print("2. Registrasi")
                print("0. Keluar")
                choice = input("\nPilih menu: ").strip()
                
                if choice == "1":
                    self.login()
                elif choice == "2":
                    self.register()
                elif choice == "0":
                    print("\n👋 Terima kasih! Sampai jumpa lagi!")
                    break
                else:
                    print("❌ Pilihan tidak valid!")
            
            else:
                print(f"\n{'='*50}")
                print(f"User: {self.current_user}".center(50))
                print(f"{'='*50}")
                print("1. Tambah Pencapaian")
                print("2. Lihat Profil")
                print("3. Lihat Semua Pencapaian")
                print("4. Logout")
                print("0. Keluar")
                choice = input("\nPilih menu: ").strip()
                
                if choice == "1":
                    self.add_achievement()
                elif choice == "2":
                    self.view_profile()
                elif choice == "3":
                    self.view_achievements()
                elif choice == "4":
                    print(f"\n👋 Sampai jumpa, {self.current_user}!")
                    self.current_user = None
                elif choice == "0":
                    print("\n👋 Terima kasih! Sampai jumpa lagi!")
                    break
                else:
                    print("❌ Pilihan tidak valid!")

# Jalankan aplikasi
if __name__ == "__main__":
    app = LevelUpLife()
    app.run()