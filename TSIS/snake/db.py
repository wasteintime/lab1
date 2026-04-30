import psycopg2
from datetime import datetime

# Настройки подключения (измени под свой пароль)
DB_CONFIG = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": "1206",
    "host": "localhost"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def save_score(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    # 1. Добавляем или получаем игрока
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING RETURNING id;", (username,))
    res = cur.fetchone()
    if res:
        player_id = res[0]
    else:
        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        player_id = cur.fetchone()[0]
    
    # 2. Сохраняем сессию
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);", 
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top_scores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached, s.played_at 
        FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(score) FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        WHERE p.username = %s;
    """, (username,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0