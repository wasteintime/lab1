import csv
import json
import psycopg2
from connect import connect

# ==========================================
# === ТВОЙ ОРИГИНАЛЬНЫЙ КОД (БЕЗ ИЗМЕНЕНИЙ) ===
# ==========================================

def add_or_update_contact(name, phone):
    """1 & 2. Добавить или обновить (Upsert через процедуру)"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
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

    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM insert_many_contacts(%s::varchar[], %s::varchar[])", (names, phones))
            errors = cur.fetchall()
            
            if not errors:
                print(f"🚀 Успех! Все {len(names)} контактов добавлены/обновлены.")
            else:
                print("\n⚠️ Результаты проверки в БД:")
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


# ==========================================
# === НОВЫЙ КОД ДЛЯ TSIS 1 (ДОПОЛНЕНИЕ) ====
# ==========================================

def interactive_pagination_loop(limit=3):
    """Консольный цикл для навигации по страницам"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            offset = 0
            while True:
                cur.execute("SELECT * FROM get_contacts_paged(%s::int, %s::int)", (limit, offset))
                rows = cur.fetchall()
                
                print(f"\n--- Страница {(offset // limit) + 1} ---")
                if not rows:
                    print("Пусто.")
                else:
                    for row in rows:
                        print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
                
                print("\n[n] Следующая | [p] Предыдущая | [q] Выход")
                choice = input("Выбор: ").strip().lower()
                
                if choice == 'n':
                    if len(rows) == limit: offset += limit
                    else: print("Вы на последней странице.")
                elif choice == 'p':
                    if offset >= limit: offset -= limit
                    else: print("Вы на первой странице.")
                elif choice == 'q':
                    break
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            conn.close()

def filter_and_sort_contacts():
    """Фильтрация по группе и сортировка"""
    group_filter = input("Введите название группы для фильтра (Enter - показать всех): ").strip()
    sort_choice = input("Сортировка: 1 - Имя, 2 - День рождения, 3 - Дата добавления (по умолчанию 1): ").strip()
    
    order_by = "c.first_name"
    if sort_choice == '2': order_by = "c.birthday"
    elif sort_choice == '3': order_by = "c.created_at"
    
    query = """
        SELECT c.first_name, g.name, c.email, c.birthday 
        FROM phonebook c
        LEFT JOIN groups g ON c.group_id = g.id
    """
    params = []
    if group_filter:
        query += " WHERE g.name ILIKE %s"
        params.append(f"%{group_filter}%")
        
    query += f" ORDER BY {order_by} NULLS LAST;"
    
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            for r in cur.fetchall():
                print(f"Имя: {r[0]} | Группа: {r[1]} | Email: {r[2]} | ДР: {r[3]}")
        finally:
            conn.close()

def advanced_search():
    """Продвинутый поиск (по email, всем телефонам)"""
    query = input("Введите запрос (имя, email или телефон): ")
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM search_contacts(%s::text)", (query,))
            rows = cur.fetchall()
            print("\n--- Результаты поиска ---")
            if not rows: print("Ничего не найдено.")
            for r in rows:
                print(f"ID: {r[0]} | Имя: {r[1]} | Email: {r[2]} | Доп.Тел: {r[3]} ({r[4]})")
        finally:
            conn.close()

def export_to_json(filename='contacts.json'):
    """Экспорт в JSON"""
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.first_name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name, c.phone,
                       COALESCE(json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL), '[]')
                FROM phonebook c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, c.first_name, c.email, c.birthday, g.name, c.phone;
            """)
            data = []
            for r in cur.fetchall():
                phones_list = r[5]
                if r[4]: # Добавляем основной телефон из старой колонки в список
                    phones_list.insert(0, {'phone': r[4], 'type': 'main'})
                data.append({"name": r[0], "email": r[1], "birthday": r[2], "group": r[3], "phones": phones_list})
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Экспортировано в {filename}")
        finally:
            conn.close()

def import_from_json(filename='contacts.json'):
    """Импорт из JSON с проверкой дубликатов"""
    conn = connect()
    if conn:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cur = conn.cursor()
            for item in data:
                name = item['name']
                cur.execute("SELECT id FROM phonebook WHERE first_name = %s", (name,))
                exists = cur.fetchone()
                
                if exists:
                    ans = input(f"Контакт '{name}' уже есть. Перезаписать? (y/n): ")
                    if ans.lower() != 'y': continue
                    cur.execute("DELETE FROM phonebook WHERE id = %s", (exists[0],))
                
                # Достаем первый телефон для основной колонки
                main_phone = item.get('phones')[0]['phone'] if item.get('phones') else '0000000000'
                
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone, email, birthday) VALUES (%s, %s, %s, %s) RETURNING id",
                    (name, main_phone, item.get('email'), item.get('birthday'))
                )
                c_id = cur.fetchone()[0]
                
                if item.get('group'):
                    cur.execute("CALL move_to_group(%s::varchar, %s::varchar)", (name, item['group']))
                    
                for i, ph in enumerate(item.get('phones', [])):
                    if i == 0: continue # Первый мы сохранили в основную колонку
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (c_id, ph.get('phone'), ph.get('type', 'mobile'))
                    )
            conn.commit()
            print("✅ Импорт завершен!")
        except FileNotFoundError:
            print(f"❌ Файл {filename} не найден.")
        finally:
            conn.close()


# ==========================================
# === ОБНОВЛЕННОЕ ГЛАВНОЕ МЕНЮ =============
# ==========================================

def main():
    while True:
        print("\n=== PhoneBook Menu (Practice 8 + TSIS 1) ===")
        print("1. Import from CSV (Original)")
        print("2. Add or update contact (Original)")
        print("3. Show all contacts (Original)")
        print("4. Search by pattern (Original)")
        print("5. Pagination (Original)")
        print("6. Delete contact (Original)")
        print("7. Bulk insert (Original)")
        print("-" * 30)
        print("8.  Interactive Pagination (Loop)")
        print("9.  Filter and Sort Contacts")
        print("10. Advanced Search (Email / All Phones)")
        print("11. Add Extra Phone (Procedure)")
        print("12. Move to Group (Procedure)")
        print("13. Export to JSON")
        print("14. Import from JSON")
        print("0. Exit")
        
        choice = input("\nSelect action: ")
        
        if choice == '1': import_csv_with_upsert('contacts.csv')
        elif choice == '2':
            name = input("Name: ")
            phone = input("Phone: ")
            add_or_update_contact(name, phone)
        elif choice == '3': show_all_contacts()
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
        elif choice == '7': bulk_insert_from_list()
        
        # НОВЫЕ ПУНКТЫ:
        elif choice == '8':
            limit = int(input("Limit: ") or 3)
            interactive_pagination_loop(limit)
        elif choice == '9': filter_and_sort_contacts()
        elif choice == '10': advanced_search()
        elif choice == '11':
            name = input("Contact Name: ")
            phone = input("New Phone: ")
            ptype = input("Type (home/work/mobile): ")
            conn = connect()
            cur = conn.cursor()
            try:
                cur.execute("CALL add_phone(%s::varchar, %s::varchar, %s::varchar)", (name, phone, ptype))
                conn.commit()
                print("Телефон добавлен.")
            except Exception as e: print("Ошибка:", e)
            finally: conn.close()
        elif choice == '12':
            name = input("Contact Name: ")
            group = input("Group Name: ")
            conn = connect()
            cur = conn.cursor()
            try:
                cur.execute("CALL move_to_group(%s::varchar, %s::varchar)", (name, group))
                conn.commit()
                print("Группа обновлена.")
            except Exception as e: print("Ошибка:", e)
            finally: conn.close()
        elif choice == '13': export_to_json()
        elif choice == '14': import_from_json()
        elif choice == '0': break
        else: print("Неверный ввод!")

if __name__ == "__main__":
    main()