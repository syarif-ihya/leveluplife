# gamification.py
import pandas as pd
import csv
from datetime import datetime 

DIFFICULTY_LEVELS = ('Mudah', 'Sedang', 'Sulit', 'Sangat Sulit')  
ATTRIBUTE_TYPES = ('Intellect', 'Creativity', 'Vitality', 'Discipline', 'Social', 'Wealth')


# utility function
def xp_required(level):
    """Hitung XP yang dibutuhkan untuk naik ke level berikutnya"""
    return 50 + (level * 25)

def update_attribute(user_id, category, xp_gain):
    rows = []

    with open("cli_app/data/data_attribute.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["user_id"]) == user_id and row["attribute"] == category:
                current_xp = int(row["xp"])
                current_level = int(row["level"])
                
                # Tambahkan XP
                current_xp += xp_gain
                
                # Level up jika XP mencukupi (dinamis)
                while current_xp >= xp_required(current_level):
                    current_xp -= xp_required(current_level)
                    current_level += 1
                
                row["xp"] = str(current_xp)
                row["level"] = str(current_level)
            
            rows.append(row)

    with open("cli_app/data/data_attribute.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "attribute", "level", "xp"])
        writer.writeheader()
        writer.writerows(rows)


# ambil id achievement
def id_achievement():
    with open("cli_app/data/data_achievement.csv", "r", encoding="utf-8") as file:
        reader = list(csv.reader(file))
        
        if len(reader) <= 1:
            return 1
        
        id = int(reader[-1][0])
        return id + 1


# add achievement
def add_achievement(user_id, text, difficulty, category):
    id = id_achievement()

    difficulty_type = {
        DIFFICULTY_LEVELS[0]: 10,   # Mudah
        DIFFICULTY_LEVELS[1]: 25,   # Sedang
        DIFFICULTY_LEVELS[2]: 50,   # Sulit
        DIFFICULTY_LEVELS[3]: 100   # Sangat Sulit
    }
    
    if not text or str(text).strip() == "":
        return {"status": False, "message": "Teks achievement tidak boleh kosong!", "attribute": "", "xp_gained": 0}
    
    if not str(difficulty).strip():
        return {"status": False, "message": "Tingkat kesulitan tidak boleh kosong!", "attribute": "", "xp_gained": 0}

    if not str(difficulty).isdigit():
        return {"status": False, "message": "Input harus berupa angka!", "attribute": "", "xp_gained": 0}
    
    difficulty = int(difficulty)
    d_index = difficulty - 1

    if d_index < 0 or d_index >= len(DIFFICULTY_LEVELS):
        return {"status": False, "message": "Tingkat kesulitan tidak valid!", "attribute": "", "xp_gained": 0}
    
    d_selected = DIFFICULTY_LEVELS[d_index]
    
    if not str(category).isdigit():
        return {"status": False, "message": "Input harus berupa angka!", "attribute": "", "xp_gained": 0}
    
    category = int(category)
    c_index = category - 1
    if c_index < 0 or c_index >= len(ATTRIBUTE_TYPES):
        return {"status": False, "message": "Kategori tidak valid!", "attribute": "", "xp_gained": 0}
    
    category_selected = ATTRIBUTE_TYPES[c_index]
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("cli_app/data/data_achievement.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([id, user_id, text, d_selected, category_selected, date])

    # Update attribute XP
    update_attribute(user_id, category_selected, difficulty_type[d_selected])
    
    # Update total XP user (DINAMIS)
    result = process_achievement(user_id, difficulty)

    return {
        "status": True,
        "message": f"Achievement tersimpan! Level: {result['level']}, Total XP: {result['xp']}",
        "attribute": category_selected,
        "xp_gained": difficulty_type[d_selected]
    }


# proses XP achievement
def process_achievement(user_id, difficulty):
    difficulty_type = {
        1: 10,   # Mudah
        2: 25,   # Sedang
        3: 50,   # Sulit
        4: 100   # Sangat Sulit
    }

    if difficulty not in difficulty_type:
        return {"xp": 0, "level": 0}

    xp_gain = difficulty_type[difficulty]
    
    # Baca user data
    users = []
    with open("cli_app/data/user.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["user_id"]) == user_id:
                current_xp = int(row["total_xp"])
                current_level = int(row["level"])
                
                # Tambahkan XP
                current_xp += xp_gain
                
                # Level up dengan threshold DINAMIS
                while current_xp >= xp_required(current_level):
                    current_xp -= xp_required(current_level)
                    current_level += 1
                
                row["total_xp"] = str(current_xp)
                row["level"] = str(current_level)
            
            users.append(row)
    
    # Tulis kembali
    with open("cli_app/data/user.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "nama_user", "password", "level", "total_xp", "email"])
        writer.writeheader()
        writer.writerows(users)
    
    return {"xp": current_xp, "level": current_level}


# data user-achievement
def data_user_achievement(user_id):
    csvUser = pd.read_csv("cli_app/data/user.csv")
    csvAchi = pd.read_csv("cli_app/data/data_achievement.csv")

    user = csvUser[csvUser['user_id'] == user_id].iloc[0]
    achievement = csvAchi[csvAchi['user_id'] == user_id]

    return user, achievement


# view profile
def view_profile(user_id):
    user, achievement = data_user_achievement(user_id)
    
    name = user['nama_user']
    level = int(user['level'])
    xp = int(user['total_xp'])

    total_achi = len(achievement)
    
    # Hitung XP yang dibutuhkan untuk level selanjutnya (DINAMIS)
    xp_needed = xp_required(level)
    progress_pct = (xp / xp_needed) * 100 
    
    # Baca data attribute
    attributes = {}
    with open("cli_app/data/data_attribute.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["user_id"]) == user_id:
                attr_name = row["attribute"]
                attr_level = int(row["level"])
                attr_xp = int(row["xp"])
                attr_xp_needed = xp_required(attr_level)
                attr_progress_pct = (attr_xp / attr_xp_needed) * 100
                
                # Simpan info lengkap untuk progress bar
                attributes[attr_name] = {
                    "level": attr_level,
                    "xp": attr_xp,
                    "xp_needed": attr_xp_needed,
                    "progress_pct": attr_progress_pct
                }

    return {
        "nama": name,
        "level": level,
        "total_xp": xp,
        "progress_to_next": f"{xp}/{xp_needed} XP ({progress_pct:.1f}%)",
        "total_achievements": total_achi,
        "attributes": attributes,
    }


# view achievement (default)
def view_achievement(user_id):
    user, achievement = data_user_achievement(user_id)

    name = user['nama_user']
    
    if len(achievement) > 0:
        ach_display = achievement[['achievement_id','text', 'difficulty', 'category', 'datetime']].reset_index(drop=True)
        ach_display.index = ach_display.index + 1  # Mulai dari 1

        ach_display.columns = ['ID', 'Text', 'Difficulty', 'Category', 'Datetime']
        return name, ach_display
    else:
        return name, pd.DataFrame()


# sort achievement
def view_achievement_sorted(user_id, sort_by='datetime', reverse=False):
    user, achievement = data_user_achievement(user_id)
    name = user['nama_user']
    
    if len(achievement) > 0:
        # Sorting menggunakan pandas sort_values
        if sort_by == 'difficulty':
            # Buat mapping untuk sorting difficulty
            difficulty_order = {
                'Mudah': 1, 
                'Sedang': 2, 
                'Sulit': 3, 
                'Sangat Sulit': 4
            }
            achievement = achievement.sort_values(
                by='difficulty', 
                key=lambda x: x.map(difficulty_order),
                ascending=not reverse
            )
        elif sort_by == 'category':
            achievement = achievement.sort_values(by='category', ascending=not reverse)
        else:  # datetime
            achievement = achievement.sort_values(by='datetime', ascending=not reverse)
        
        ach_display = achievement[['text', 'difficulty', 'category', 'datetime']].reset_index(drop=True)
        ach_display.index = ach_display.index + 1
        return name, ach_display
    else:
        return name, pd.DataFrame()


# search achievement
def search_achievement(user_id, keyword):
    user, achievement = data_user_achievement(user_id)
    name = user['nama_user']
    
    if len(achievement) > 0:
        # Linear search: filter berdasarkan keyword (case-insensitive)
        keyword_lower = keyword.lower()
        filtered = achievement[
            achievement['text'].str.lower().str.contains(keyword_lower, na=False) |
            achievement['category'].str.lower().str.contains(keyword_lower, na=False)
        ]
        
        if len(filtered) > 0:
            ach_display = filtered[['text', 'difficulty', 'category', 'datetime']].reset_index(drop=True)
            ach_display.index = ach_display.index + 1
            return name, ach_display, True
        else:
            return name, pd.DataFrame(), False
    else:
        return name, pd.DataFrame(), False
    

# get data untuk edit
def get_edit_achievement(user_id, achievement_id):
    user, achievement = data_user_achievement(user_id)
    name = user['nama_user']

    if len(achievement) == 0:
        return None
    
    target = achievement[achievement['achievement_id'] == achievement_id]

    if target.empty:
        return None
    
    row = target.iloc[0]

    text = row['text']
    difficulty = row['difficulty']
    category = row['category']

    return text, difficulty, category


# edit achievement
def edit_achievement(user_id, achievement_id, new_text, new_diff, new_cate):
    df = pd.read_csv("cli_app/data/data_achievement.csv")

    achievement_id = int(achievement_id)

    line = (df['achievement_id'] == achievement_id) & (df['user_id'] == user_id)

    if new_text is not None:
        df.loc[line, 'text'] = new_text

    if new_diff is not None:
        df.loc[line, 'difficulty'] = DIFFICULTY_LEVELS[new_diff - 1]

    if new_cate is not None:
        df.loc[line, 'category'] = ATTRIBUTE_TYPES[new_cate - 1]

    df.to_csv("cli_app/data/data_achievement.csv", index=False)

    return True


# form input difficult dan category untuk edit
def input_difficulty(allow_empty=False):
    while True:
        print("\nDifficulty:")
        for i, level in enumerate(DIFFICULTY_LEVELS, 1):
            print(f"  {i}. {level}")

        diff = input("Pilih (1-4): ")

        if allow_empty and not diff.strip():
            return None

        if not diff.strip():
            print("Tingkat kesulitan tidak boleh kosong!")
            continue
        if not diff.isdigit():
            print("Input harus berupa angka!")
            continue

        diff = int(diff)
        if diff not in range(1, len(DIFFICULTY_LEVELS) + 1):
            print("Tingkat kesulitan tidak valid!")
            continue

        return diff

def input_category(allow_empty=False):
    while True:
        print("\nCategory:")
        for i, attr in enumerate(ATTRIBUTE_TYPES, 1):
            print(f"  {i}. {attr}")

        kat = input("Pilih Kategori (1-6): ")

        if allow_empty and not kat.strip():
            return None

        if not kat.strip():
            print("Kategori tidak boleh kosong!")
            continue

        if not kat.isdigit():
            print("Input harus berupa angka!")
            continue

        kat = int(kat)
        if kat not in range(1, len(ATTRIBUTE_TYPES) + 1):
            print("Kategori tidak valid!")
            continue

        return kat
