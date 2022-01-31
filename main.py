import fozzy
import db


# use this function to fill or update db
# fozzy.get_data()


def print_wines(lst, count=3):
    if len(lst) > count:
        lst = lst[:count]
    for row in lst:
        print("{} за {}грн (скидка {}) - {}".format(*row))


def look_at_this():
    print(f'Вина, на которые стоит обратить внимание:')
    data = db.good_price()
    print_wines(data)

    
def best_discount_absolute():
    print("Наибольшая абсолютная скидка сейчас на эти позиции:")
    data = db.best_choise()
    print_wines(data)


def best_discount_relative():
    print("Наибольшая относительныая скидка сейчас на эти позиции:")
    data = db.best_choise_relative()
    print_wines(data)


def main():
    look_at_this()
    print("--------------------------------------------------------")
    best_discount_absolute()
    print("--------------------------------------------------------")
    best_discount_relative()



if __name__ == "__main__":
    main()