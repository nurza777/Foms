import json
import os

# пока что тут типа файл json для регистрации так как еще не имею доступа к бд или может просто
# сделаю вход как admin, admin
USERS_FILE = 'users.json'

def load_users():
    """Загрузка пользователей из файла"""
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    """Сохранение пользователей в файл"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def register_user(fullname, email, username, password):
    """Регистрация нового пользователя"""
    users = load_users()

    if username in users:
        return False, "Такой ник уже занят!"

    users[username] = {
        'fullname': fullname,
        'password': password  # (пока что без хеширования — позже можно добавить безопасность)
    }
    save_users(users)
    return True, "Регистрация прошла успешно!"

def verify_login(username, password):
    """Проверка входа пользователя"""
    users = load_users()

    if username not in users:
        return False

    return users[username]['password'] == password
