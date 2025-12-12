# import pandas as pd

# add achievement
def add_achievement(user_id, title, text, difficulty, category):
    difficulty_type = {
        "Mudah": 10,
        "Sedang": 25,
        "Sulit": 50,
        "Sangat Sulit": 100
    }

    category_type = ['Intellect', 'Creativity', 'Vitality', 'Dicipline', 'Social', 'Wealth']
    
    if not (title and text and category):
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
        return {"status": False, "notification": "Kategori tidak valid!"}
    
    with open("cli_app/data/data_achievement.csv", "a") as file:
        file.write(f"{user_id}, {title}, {text}, {d_selected}, {category}\n")
        return {"status": True, "notification": "Data telah tersimpan!"}


