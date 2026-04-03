import csv
import psycopg2
from connect import connect

def add_or_update_contact(name, phone):
    """1 & 2. Добавить или обновить (Upsert через процедуру)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            # Явно указываем типы ::varchar, чтобы избежать ошибки unknown
            cur.execute("CALL upsert_contact(%s::varchar, %s::varchar)", (name, phone))
            conn.commit()
            print(f"✅ Контакт {name} успешно обработан (добавлен/обновлен).")
            cur.close()
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        finally:
            conn.close()
def show_all_contacts():
    """Пункт 3: Показать все контакты (используем поиск с пустым паттерном)"""
    # Если передать пустую строку в ILIKE '%||%', он вернет всё
    query_contacts("") 

def import_csv_with_upsert(filename):
    """Пункт 1: Импорт из CSV с использованием нашей процедуры"""
    conn = connect()
    if conn:
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Пропускаем заголовок
                cur = conn.cursor()
                for row in reader:
                    # Вызываем нашу процедуру для каждой строки из CSV
                    cur.execute("CALL upsert_contact(%s::varchar, %s::varchar)", (row[0], row[1]))
                conn.commit()
                print(f"✅ Данные из {filename} успешно импортированы.")
            cur.close()
        except Exception as e:
            print(f"❌ Ошибка CSV: {e}")
        finally:
            conn.close()

def query_contacts(pattern):
    """3. Поиск по паттерну через функцию"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s::text)", (pattern,))
            rows = cur.fetchall()
            print("\n--- Результаты поиска ---")
            if not rows:
                print("Ничего не найдено.")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
            cur.close()
        finally:
            conn.close()

def delete_contact(identifier):
    """4. Удаление через процедуру"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("CALL delete_contact(%s::varchar)", (identifier,))
            conn.commit()
            print(f"🗑️ Запрос на удаление выполнен для: {identifier}")
            cur.close()
        finally:
            conn.close()

def get_paginated_contacts(limit, offset):
    """5. Пагинация через функцию"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_paged(%s::int, %s::int)", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Список контактов (Limit: {limit}, Offset: {offset}) ---")
            for row in rows:
                print(f"ID: {row[0]} | {row[1]}: {row[2]}")
            cur.close()
        finally:
            conn.close()

def bulk_insert_from_list():
    """Пункт 7: Массовая вставка через ввод в консоли"""
    names = []
    phones = []
    
    print("\n--- Режим массового ввода ---")
    print("Введите 'stop' в поле имени, чтобы завершить ввод.")
    
    while True:
        name = input("Введите имя: ").strip()
        if name.lower() == 'stop':
            break
        phone = input(f"Введите телефон для {name}: ").strip()
        
        names.append(name)
        phones.append(phone)

    if not names:
        print("Данные не введены.")
        return

    # Отправляем собранные списки в базу данных одним запросом
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            # Передаем накопленные списки как массивы PostgreSQL
            cur.execute("SELECT * FROM insert_many_contacts(%s::varchar[], %s::varchar[])", (names, phones))
            errors = cur.fetchall()
            
            if not errors:
                print(f"🚀 Успех! Все {len(names)} контактов добавлены/обновлены.")
            else:
                print("\n⚠️ Результаты проверки в БД:")
                # Вычисляем сколько добавлено успешно
                success_count = len(names) - len(errors)
                print(f"Успешно: {success_count}")
                print(f"Ошибки: {len(errors)}")
                
                for err in errors:
                    print(f"❌ Контакт '{err[0]}' (тел: {err[1]}) отклонен. Причина: {err[2]}")
            
            conn.commit()
            cur.close()
        except Exception as e:
            print(f"Ошибка массовой вставки: {e}")
        finally:
            conn.close()

# --- ГЛАВНОЕ МЕНЮ ---
def main():
    while True:
        print("\n=== PhoneBook Menu (Practice 8) ===")
        print("1. Import from CSV")
        print("2. Add or update contact")
        print("3. Show all contacts")
        print("4. Search by pattern")
        print("5. Pagination")
        print("6. Delete contact")
        print("7. Bulk insert")
        print("0. Exit")
        
        choice = input("\nSelect action: ")
        
        if choice == '1':
            import_csv_with_upsert('contacts.csv')
        elif choice == '2':
            name = input("Name: ")
            phone = input("Phone: ")
            add_or_update_contact(name, phone)
        elif choice == '3':
            show_all_contacts()
        elif choice == '4':
            p = input("Search pattern: ")
            query_contacts(p)
        elif choice == '5':
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated_contacts(limit, offset)
        elif choice == '6':
            target = input("Name or Phone to delete: ")
            delete_contact(target)
        elif choice == '7':
            bulk_insert_from_list()
        elif choice == '0':
            break
        else:
            print("Неверный ввод!")

if __name__ == "__main__":
    main()