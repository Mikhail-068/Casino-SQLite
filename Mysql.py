import sqlite3

db = sqlite3.connect('Casino.db')
sql = db.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users("
            "login TEXT,"
            "password TEXT,"
            "cash INT)")
db.commit()

user_login = input('Введите логин: ')
user_password = input('Введите пароль: ')

sql.execute("SELECT login FROM users")
if sql.fetchone() is None:
    sql.execute("INSERT INTO users (login, password, cash) VALUES (?, ?, ?)",
            (user_login, user_password, 0))
    db.commit()
else:
    print(f'{user_login} у нас уже есть!')

