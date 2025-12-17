# main.py
# print("ngerjainnya alis ngebuat appnya disini aja ges!")

from gamification import add_achievement

u = 1
title = str(input("title:"))
text = str(input("text:"))
diff = int(input("diff:"))
kat = int(input("kat:"))

print(add_achievement(u, title, text, diff, kat))