import psycopg2
from config import load_config

def connect():
    """ Функция для подключения к серверу PostgreSQL """
    conn = None
    try:
        # Читаем параметры подключения
        params = load_config()

        # Подключаемся к серверу
        print('Подключение к базе данных PostgreSQL...')
        conn = psycopg2.connect(**params)
        
        # Создаем курсор (это как "курсор" мышки в базе)
        cur = conn.cursor()
        
        # Выполняем запрос, чтобы узнать версию базы (проверка связи)
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f'Версия базы данных: {db_version}')
        
        # Закрываем курсор
        cur.close()
        return conn # Возвращаем объект соединения для работы в других файлах

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при подключении: {error}")
        return None

if __name__ == '__main__':
    # Если запустить этот файл напрямую, он просто проверит связь
    connection = connect()
    if connection:
        connection.close()
        print('Соединение проверено и закрыто.')