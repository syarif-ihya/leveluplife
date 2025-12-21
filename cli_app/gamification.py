# gamification.py
import pandas as pd
import csv
from datetime import datetime 

# Utility Function
def xp_required(level):
    return 50 + (level * 25)

def update_attribute(user_id, category, xp_gain):
    rows = []

    with open("data/data_attribute.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["user_id"]) == user_id and row["attribute"] == category:
                row["xp"] = int(row["xp"]) + xp_gain

                while row["xp"] >= xp_required(int(row["level"])):
                    row["xp"] -= xp_required(int(row["level"]))
                    row["level"] = int(row["level"]) + 1

            rows.append(row)

    with open("data/data_attribute.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# add achievement
def add_achievement(user_id, text, difficulty, category):
    difficulty_type = {
        "Mudah": 10,
        "Sedang": 25,
        "Sulit": 50,
        "Sangat Sulit": 100
    }

    category_type = ['Intellect', 'Creativity', 'Vitality', 'Dicipline', 'Social', 'Wealth']
    
    if not (text and difficulty and category):
        return "Data tidak lengkap!"

    d_index = difficulty - 1
    keys = list(difficulty_type.keys())

    i = 0
    while i < len(keys):
        if i == d_index:
            d_selected = keys[i]
            break
        i+=1

    if (i == len(keys)) or (i > len(keys)):
        return "Tingkat kesulitan tidak valid!"
    
    c_index = category - 1
    j = 0
    while j < len(category_type):
        if j == c_index:
            category = category_type[j]
            break
        j+=1

    if (i == len(category_type)) or (i > len(category_type)):
        return "Kategori tidak valid!"
    
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("data/data_achievement.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_id, text, d_selected, category, date])

    # 2️⃣ update attribute (PROGRESS)
    update_attribute(user_id, category, difficulty_type[d_selected])

    return {
        "status": True,
        "message": "Achievement tersimpan & attribute bertambah",
        "attribute": category,
        "xp_gained": difficulty_type[d_selected]
    }


# proses XP achievement
def process_achievement(user_id, difficulty):
    difficulty_type = {
        "Mudah": 10,
        "Sedang": 25,
        "Sulit": 50,
        "Sangat Sulit": 100
    }

    max_xp = 100

    d_index = difficulty - 1
    keys = list(difficulty_type.values())

    if (d_index == len(keys)) or (d_index > len(keys)):
        return "Tingkat kesulitan tidak valid!"

    csvUser = pd.read_csv("data/user.csv")
    csvFilterID = csvUser[csvUser['user_id'] == user_id]

    csvFilter = csvFilterID.filter(items=['level','total_xp'])

    achievement_values = keys[d_index]
    current_xp = int(csvFilter['total_xp'].iloc[0])

    xp = current_xp + achievement_values
    csvUser.loc[csvUser['user_id'] == user_id, "total_xp"] = xp

    level = xp // max_xp 
    csvUser.loc[csvUser['user_id'] == user_id, "level"] = level

    with open("data/user.csv", "r") as file:
        line = file.readlines()

    i = 1
    while i < len(line) :
        data = line[i].strip().split(",")

        if int(data[0]) == user_id:
            line[i] = (data[0] + "," + data[1] + "," + str(level) + "," + str(xp)+ "\n")
            break
        i += 1

    with open("data/user.csv", "w") as file:
        file.writelines(line)
    
    return {
        "xp" : xp,
        "level" : level
    }


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
    
    name = user['nama_user']
    level = int(user['level'])
    xp = int(user['total_xp'])

    total_achi = len(achievement)
    
    max_xp = 100
    progress = xp % max_xp 
    progress = (progress / max_xp) * 100 

    return {
        "nama" : name,
        "level" : level,
        "xp" : xp,
        "total achievements" : total_achi
    }


# view achievement
def view_achievement(user_id):
    user, achievement = data_user_achievement(user_id)

    name = user['nama_user']

    return name, achievement[['text', 'difficulty', 'category', 'datetime']]