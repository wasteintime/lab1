import os
import shutil
from pathlib import Path
# --- 2.2 Practical Exercises: Directory Management ---

# 1. Создание вложенных папок
# os.makedirs создаст всю цепочку, если ее нет
os.makedirs("project/logs/daily", exist_ok=True)

# 2. Узнать, где мы сейчас, и сменить папку
print(f"Current Dir: {os.getcwd()}")
# os.chdir("project") # Пример смены директории

# 3. Список файлов и поиск по расширению
print("Files in current directory:", os.listdir("."))
txt_files = list(Path(".").glob("*.txt"))
print("Found .txt files via pathlib:", txt_files)

# 4. Перемещение файла (используем shutil)
if os.path.exists("data.txt"):
    shutil.move("data.txt", "project/logs/daily/data_moved.txt")
    print("File moved to nested directory.")