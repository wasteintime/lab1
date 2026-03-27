import csv
import psycopg2
from connect import connect  # Импортируем твою функцию подключения

def add_contact(name, phone):
    """1. Добавить новый контакт (Insert)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            # ON CONFLICT предотвратит ошибку, если такой номер уже есть
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", (name, phone))
            conn.commit()
            print(f"Успех: Контакт {name} добавлен.")
            cur.close()
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
        finally:
            conn.close()

def update_contact(name, new_phone):
    """2. Обновить номер телефона (Update)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (new_phone, name))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Успех: Номер для {name} обновлен.")
            else:
                print("Контакт не найден.")
            cur.close()
        finally:
            conn.close()

def query_contacts(pattern):
    """3. Поиск контактов по фильтру (Select)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            # Ищем совпадение в имени (через ILIKE - без учета регистра)
            cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f'%{pattern}%',))
            rows = cur.fetchall()
            print("\n--- Результаты поиска ---")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[3]}")
            cur.close()
        finally:
            conn.close()

def delete_contact(name_or_phone):
    """4. Удалить контакт по имени или телефону (Delete)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone = %s", (name_or_phone, name_or_phone))
            conn.commit()
            print(f"Записей удалено: {cur.rowcount}")
            cur.close()
        finally:
            conn.close()

def upload_from_csv(filename):
    """5. Загрузка данных из CSV файла (Batch Insert)"""
    conn = connect()
    if conn:
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # пропускаем заголовок
                cur = conn.cursor()
                for row in reader:
                    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING", (row[0], row[1]))
                conn.commit()
                print("Данные из CSV успешно импортированы.")
                cur.close()
        except Exception as e:
            print(f"Ошибка при работе с CSV: {e}")
        finally:
            conn.close()

# --- ГЛАВНОЕ МЕНЮ ---
def main():
    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Добавить контакт")
        print("2. Обновить номер")
        print("3. Поиск (фильтр)")
        print("4. Удалить контакт")
        print("5. Загрузить из CSV (contacts.csv)")
        print("0. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            add_contact(name, phone)
        elif choice == '2':
            name = input("Имя контакта: ")
            phone = input("Новый номер: ")
            update_contact(name, phone)
        elif choice == '3':
            p = input("Введите имя для поиска: ")
            query_contacts(p)
        elif choice == '4':
            target = input("Введите имя или телефон для удаления: ")
            delete_contact(target)
        elif choice == '5':
            upload_from_csv('contacts.csv')
        elif choice == '0':
            break
        else:
            print("Неверный ввод!")

if __name__ == "__main__":
    main()