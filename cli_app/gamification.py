import pandas as pd
from datetime import datetime 

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
    
    with open("cli_app/data/data_achievement.csv", "a") as file:
        file.write(f"{user_id}, {text}, {d_selected}, {category}, {date}\n")
        return "Data telah tersimpan!"


# proses XP achievement
def process_achievement(user_id, difficulty):
    difficulty_type = {
        "Mudah": 10,
        "Sedang": 25,
        "Sulit": 50,
        "Sangat Sulit": 100
    }

    max_xp = 1000

    d_index = difficulty - 1
    keys = list(difficulty_type.values())

    if (d_index == len(keys)) or (d_index > len(keys)):
        return "Tingkat kesulitan tidak valid!"

    csvUser = pd.read_csv("cli_app/data/user.csv")
    csvFilterID = csvUser[csvUser['user_id'] == user_id]

    csvFilter = csvFilterID.filter(items=['level','total_xp'])

    achievement_values = keys[d_index]
    current_xp = int(csvFilter['total_xp'].iloc[0])

    xp = current_xp + achievement_values
    csvUser.loc[csvUser['user_id'] == user_id, "total_xp"] = xp

    level = xp // max_xp 
    csvUser.loc[csvUser['user_id'] == user_id, "level"] = level

    with open("cli_app/data/user.csv", "r") as file:
        line = file.readlines()

    i = 1
    while i < len(line) :
        data = line[i].strip().split(",")

        if int(data[0]) == user_id:
            line[i] = (data[0] + "," + data[1] + "," + str(level) + "," + str(xp)+ "\n")
            break
        i += 1

    with open("cli_app/data/user.csv", "w") as file:
        file.writelines(line)
    
    return xp, level


# view profile
def view_profile(user_id):
    csvUser = pd.read_csv("cli_app/data/user.csv")
    csvAchi = pd.read_csv("cli_app/data/data_achievement.csv")

    csvFilterUser = csvUser[csvUser['user_id'] == user_id]
    csvFilterAchi = csvAchi[csvAchi['user_id'] == user_id]

    name = csvFilterUser['nama_user']
    level = csvFilterUser['level']
    xp = csvFilterUser['xp']

    text = csvFilterAchi['text']
    difficulty = csvFilterAchi['difficulty']
    category = csvFilterAchi['kategori']
    date = csvFilterAchi['datetime']

    return name, level, xp, text, difficulty, category, date