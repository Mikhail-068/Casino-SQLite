import sqlite3
from random import randint
from time import sleep

db = sqlite3.connect('Casino.db')
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users("
            "login TEXT,"
            "password TEXT,"
            "cash INT)")
db.commit()

cur.execute("CREATE TABLE IF NOT EXISTS record("
            "id INT AUTO_INCREMENT NOT NULL,"
            "name TEXT,"
            "best INT,"
            "PRIMARY KEY(id))")
db.commit()

def add_best(name, best):
    cur.execute(f'UPDATE record SET name = "{name}", best = {best} WHERE id = 1;')
    db.commit()

def Maximalka(tabl):
    cur.execute(f"SELECT login, MAX(cash) FROM {tabl}")
    for name_, val_ in cur:
        pass
    cur.execute("INSERT INTO record (name, best) VALUES (?, ?)", (name_, val_))
    db.commit()


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
            for rec_name, rec_cash in cur.execute(f"SELECT name, MAX(best) FROM record"):
                print(f'Рекорд по сумме: {rec_cash} у игрока {rec_name}')
            pulse = rec_cash
            print(f'{user_login}! У вас {balance} евро')
            gain = int(input('Ваша ставка: '))
            if gain > balance:
                print('Ага, ставка больше чем у тебя есть, исправь: ')
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
                    if i[1] > pulse:
                        add_best(i[0], i[1])


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