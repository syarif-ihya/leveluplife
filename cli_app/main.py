# main.py
# print("ngerjainnya alis ngebuat appnya disini aja ges!")

from gamification import add_achievement, process_achievement, view_profile, view_achievement
from auth import register, login
from gamification import add_achievement, view_profile

# status, msg = register("Shirin", "12345678")
# print(msg)

status, user = login("Shirin", "1234")
if status:
    print('Login Berhasil')
    user_id = int(user["user_id"])
    add_achievement(user_id, "Belajar Python", 2, 1)
    print(view_profile(user_id))


    u = 1
    text = str(input("text:"))
    diff = int(input("diff:"))
    kat = int(input("kat:"))

    print(add_achievement(u, text, diff, kat))
    print(process_achievement(u, diff))
    print(view_profile(u))
    print(view_achievement(u))
else :
    print('Login Gagal')
