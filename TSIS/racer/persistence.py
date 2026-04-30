import json
import os

# Автоматически находим абсолютный путь к папке TSIS 
# (на один уровень выше, чем папка racer, где лежит этот файл)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

SETTINGS_FILE = os.path.join(ROOT_DIR, "settings.json")
LEADERBOARD_FILE = os.path.join(ROOT_DIR, "leaderboard.json")

def load_settings():
    default = {"sound": True, "color": "Blue", "diff": "Medium"}
    if not os.path.exists(SETTINGS_FILE): return default
    with open(SETTINGS_FILE, "r") as f:
        try: return json.load(f)
        except: return default

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f: json.dump(data, f, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE): return []
    with open(LEADERBOARD_FILE, "r") as f:
        try: return json.load(f)
        except: return []

def save_score(name, score, distance):
    data = load_leaderboard()
    data.append({"name": name, "score": score, "distance": int(distance)})
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f: json.dump(data, f, indent=4)