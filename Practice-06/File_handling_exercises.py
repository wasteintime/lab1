import os
import shutil
from pathlib import Path

# --- 2.2 Practical Exercises: File Handling ---

# 1. Создание и запись (режим 'w')
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("First line\nSecond line\nThird line\n")

# 2. Разные способы чтения
print("--- Reading Methods ---")
with open("data.txt", "r") as f:
    # print(f.read())      # Читает весь файл сразу
    # print(f.readline())  # Читает только одну строку
    lines = f.readlines()  # Читает всё и превращает в список строк
    print(f"List of lines: {lines}")

# 3. Добавление данных (режим 'a') и создание нового ('x')
with open("data.txt", "a") as f:
    f.write("Fourth line (appended)\n")

# 4. Копирование и Бэкап (используем shutil)
shutil.copy("data.txt", "data_backup.txt")
print("Backup created using shutil.")

# 5. Удаление (безопасно через os)
if os.path.exists("data_backup.txt"):
    os.remove("data_backup.txt")
    print("Backup deleted.")