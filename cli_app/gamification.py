# gamification.py
import pandas as pd
import csv
from datetime import datetime 

# Utility Function
def xp_required(level):
    return 50 + (level * 25)

def update_attribute(user_id, category, xp_gain):
    rows = []

    try:
        with open("data/data_attribute.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["user_id"]) == user_id and row["attribute"] == category:
                    row["xp"] = int(row["xp"]) + xp_gain

                    while row["xp"] >= xp_required(int(row["level"])):
                        row["xp"] -= xp_required(int(row["level"]))
                        row["level"] = int(row["level"]) + 1

                rows.append(row)

        if rows:
            with open("data/data_attribute.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

    except FileNotFoundError:
        pass  # file belum ada → abaikan (aman untuk MVP)


# add achievement
def add_achievement(user_id, text, difficulty, category):
    difficulty_type = {
        "Mudah": 10,
        "Sedang": 25,
        "Sulit": 50,
        "Sangat Sulit": 100
    }

    category_type = ['Intellect', 'Creativity', 'Vitality', 'Dicipline', 'Social', 'Wealth']
    
    if not text:
        return {"status": False, "message": "Nama achievement tidak boleh kosong"}

    if difficulty not in [1,2,3,4]:
        return {"status": False, "message": "Tingkat kesulitan tidak valid"}

    if category not in [1,2,3,4,5,6]:
        return {"status": False, "message": "Kategori tidak valid"}

    d_selected = list(difficulty_type.keys())[difficulty - 1]
    category = category_type[category - 1]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open("data/data_achievement.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([user_id, text, d_selected, category, date])

        update_attribute(user_id, category, difficulty_type[d_selected])

        return {
            "status": True,
            "message": "Achievement tersimpan & attribute bertambah",
            "attribute": category,
            "xp_gained": difficulty_type[d_selected]
        }

    except Exception:
        return {"status": False, "message": "Gagal menyimpan achievement"}


# proses XP achievement
def process_achievement(user_id, difficulty):
    difficulty_type = [10, 25, 50, 100]

    if difficulty not in [1,2,3,4]:
        return

    csvUser = pd.read_csv("data/user.csv")
    user_row = csvUser[csvUser['user_id'] == user_id]

    if user_row.empty:
        return

    current_xp = user_row['total_xp'].iloc[0]
    if pd.isna(current_xp):
        current_xp = 0

    xp = int(current_xp) + difficulty_type[difficulty - 1]
    level = xp // 100

    csvUser.loc[csvUser['user_id'] == user_id, "total_xp"] = xp
    csvUser.loc[csvUser['user_id'] == user_id, "level"] = level
    csvUser.to_csv("data/user.csv", index=False)


# data user-achievement
def data_user_achievement(user_id):
    csvUser = pd.read_csv("data/user.csv")
    csvAchi = pd.read_csv("data/data_achievement.csv")

    user = csvUser[csvUser['user_id'] == user_id].iloc[0]
    achievement = csvAchi[csvAchi['user_id'] == user_id]

    return user, achievement


# view profile
def view_profile(user_id):
    user, achievement = data_user_achievement(user_id)

    xp = user['total_xp']
    xp = 0 if pd.isna(xp) else int(xp)

    return {
        "nama": user['nama_user'],
        "level": int(user['level']),
        "xp": xp,
        "total achievements": len(achievement)
    }


# view achievement
def view_achievement(user_id):
    user, achievement = data_user_achievement(user_id)
    name = user['nama_user']

    if achievement.empty:
        return name, None

    achievement_view = achievement[['text', 'difficulty', 'category', 'datetime']]
    achievement_view = achievement_view.reset_index(drop=True)
    achievement_view.index = achievement_view.index + 1

    return name, achievement_view
