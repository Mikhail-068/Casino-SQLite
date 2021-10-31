import sqlite3

db = sqlite3.connect('Casino.db')
sql = db.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users("
            "login TEXT,"
            "password TEXT,"
            "cash INT)")

db.commit()