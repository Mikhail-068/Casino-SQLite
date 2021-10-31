import sqlite3
from random import randint
from time import sleep
from tqdm import tqdm as tq

db = sqlite3.connect('Casino.db')
cur = db.cursor()



cur.execute("CREATE TABLE IF NOT EXISTS users("
            "login TEXT,"
            "password TEXT,"
            "cash INT)")
db.commit()


def reg():
    global user_login
    global money

    user_login = input('Введите логин: ')

    cur.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (login) VALUES (?)",
                (user_login,))
        db.commit()
        print(f'{user_login} зарегистрирован!')
    else:
        print(f'{user_login} у нас уже есть!')

def show():
    for value in cur.execute('SELECT * FROM users'):
        print(value)

def MyCasino():
    user_login = input('Введите имя: ')
    cur.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if cur.fetchone() is None:
        print('Первый раз? Щас внесем в базу...')
        sleep(2)
        cur.execute("INSERT INTO users (login) VALUES (?)",
                    (user_login,))
        db.commit()
    else:
        cur.execute(f"UPDATE users SET cash = 1000 WHERE login = '{user_login}'")
        play = 'да'
        while play != 'нет':
            for i in cur.execute(f"SELECT cash FROM users WHERE login = '{user_login}'"):
                balance = i[0]
            print(f'{user_login}! У вас {balance} евро')
            gain = int(input('Ваша ставка: '))
            if gain > balance:
                print('Исправьте вашу ставку: ')
            else:
                coef = randint(1, 9)
                gain *= coef
                number = randint(0, 1)
                print(f'Играем! Коэфицент = {coef}...')
                sleep(2)
                if number == 1:
                    print('Вы выиграли!')
                    cur.execute(f"UPDATE users SET cash = {balance + gain} WHERE login = '{user_login}'")
                    db.commit()
                    cur.execute(f"SELECT login, cash FROM users WHERE login = '{user_login}'")
                    for i in cur:
                      print(i)
                    play = input('Ещё? ')
                else:
                    for i in cur.execute(f"SELECT cash FROM users WHERE login = '{user_login}'"):
                        balance = i[0]
                    print('Вы проиграли!')
                    cur.execute(f"UPDATE users SET cash = {balance - gain} WHERE login = '{user_login}'")
                    db.commit()
                    cur.execute(f"SELECT login, cash FROM users WHERE login = '{user_login}'")
                    for i in cur:
                        print(i)
                    for i in cur.execute(f"SELECT cash FROM users WHERE login = '{user_login}'"):
                        balance = i[0]
                    if balance < 0:
                        print('Пока неудачник!!!')
                        break
                    else:
                        play = input('Ещё? ')


MyCasino()