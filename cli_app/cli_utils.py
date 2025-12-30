import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(title):
    print("=" * 40)
    print(title.center(40))
    print("=" * 40)

def divider():
    print("-" * 40)

def pause():
    input("\nPress Enter to continue...")