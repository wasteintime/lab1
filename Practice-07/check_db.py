import psycopg2
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    return config

def connect():
    """ Подключение к серверу и создание таблицы """
    params = load_config()
    try:
        # Подключаемся
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Создаем таблицу, если её нет
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS phonebook (
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        phone VARCHAR(20) UNIQUE
                    )
                """)
                print("--- Успех! База данных подключена, таблица 'phonebook' создана. ---")
    except Exception as error:
        print(f"Ошибка при подключении: {error}")

if __name__ == '__main__':
    connect()