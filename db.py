import sqlite3

db = sqlite3.connect('wine-cellar.db')
cursor = db.cursor()


def add_new_wine(name, price_now, regular_price, discont, url):
    cursor.execute("SELECT name FROM wines WHERE name=?", (name, ))
    if cursor.fetchone() is None:
        print(f"Add {name} to DB")
        cursor.execute("INSERT INTO wines VALUES (?, ?, ?, ?, ?)", (name, price_now, regular_price, discont, url))
        db.commit()
    else:
        print(f"{name} is already in DB")


def clear_db():
    cursor.execute("DELETE FROM wines")
    db.commit()


def best_choise(discont:int=100, price:int=1000):
    cursor.execute("SELECT name, price_now, discont, url FROM wines WHERE discont > ? AND price_now < ?", (discont, price))
    wine_choise = sorted(cursor.fetchall(), key=lambda row: row[2], reverse=True)
    return wine_choise


def best_choise_relative(discont:int=100, price:int=1000):
    cursor.execute("SELECT name, price_now, regular_price, url FROM wines WHERE discont > ? AND price_now < ?", (discont, price))
    data = [count_discount(row) for row in cursor.fetchall()]
    return sorted(data, key=lambda row: row[2], reverse=True)


def count_discount(row):
    discount = str(int((row[2] - row[1]) / row[2] * 100)) + '%'
    return row[0], row[1], discount, row[3]


def good_price(price_min=150, price_max=350):
    cursor.execute("SELECT name, price_now, discont, url FROM wines WHERE price_now > ? AND price_now < ?", (price_min, price_max))
    return sorted(cursor.fetchall(), key=lambda row: row[2], reverse=True)


