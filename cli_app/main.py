# print("ngerjainnya alis ngebuat appnya disini aja ges!")

from gamification import add_achievement, process_achievement

u = 1
text = str(input("text:"))
diff = int(input("diff:"))
kat = int(input("kat:"))

print(add_achievement(u, text, diff, kat))
print(process_achievement(u, diff))