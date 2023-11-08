import csv
import datetime
import json
import os

FILE_NAME = "expenses.json"
CSV_NAME = "expenses.csv"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)


def show_expenses(expenses):
    if len(expenses) == 0:
        print("Трат пока нет.")
        return
    for number, expense in enumerate(expenses, start=1):
        date = expense.get("date", "-")
        print(f"{number}. {date} {expense['name']} — {expense['amount']}")


def ask_number(expenses):
    if len(expenses) == 0:
        print("Трат пока нет.")
        return None
    show_expenses(expenses)
    try:
        number = int(input("Номер траты: "))
    except ValueError:
        print("Нужно ввести число.")
        return None
    if number < 1 or number > len(expenses):
        print("Такого номера нет.")
        return None
    return number - 1


def add_expense(expenses):
    name = input("Название траты: ")
    try:
        amount = float(input("Сумма: "))
    except ValueError:
        print("Нужно ввести число.")
        return
    today = datetime.date.today().isoformat()
    expenses.append({"name": name, "amount": amount, "date": today})
    save_expenses(expenses)
    print("Трата добавлена.")


def edit_expense(expenses):
    index = ask_number(expenses)
    if index is None:
        return
    expense = expenses[index]
    new_name = input(f"Новое название (Enter - оставить «{expense['name']}»): ")
    new_amount = input(f"Новая сумма (Enter - оставить {expense['amount']}): ")
    if new_name != "":
        expense["name"] = new_name
    if new_amount != "":
        try:
            expense["amount"] = float(new_amount)
        except ValueError:
            print("Сумма не изменена: нужно ввести число.")
    save_expenses(expenses)
    print("Трата изменена.")


def delete_expense(expenses):
    index = ask_number(expenses)
    if index is None:
        return
    answer = input("Точно удалить? (да/нет): ")
    if answer == "да":
        del expenses[index]
        save_expenses(expenses)
        print("Трата удалена.")
    else:
        print("Удаление отменено.")


def show_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    print(f"Всего потрачено: {total}")


def filter_by_date(expenses):
    start = input("С какой даты (ГГГГ-ММ-ДД): ")
    end = input("По какую дату (ГГГГ-ММ-ДД): ")
    found = []
    for expense in expenses:
        date = expense.get("date", "")
        if start <= date <= end:
            found.append(expense)
    if len(found) == 0:
        print("За этот период трат нет.")
        return
    total = 0
    for expense in found:
        date = expense.get("date", "-")
        print(f"{date} {expense['name']} — {expense['amount']}")
        total += expense["amount"]
    print(f"Итого за период: {total}")


def export_csv(expenses):
    with open(CSV_NAME, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "name", "amount"])
        for expense in expenses:
            writer.writerow([expense.get("date", ""), expense["name"], expense["amount"]])
    print(f"Сохранено в файл {CSV_NAME}.")


def main():
    expenses = load_expenses()
    while True:
        print("\n1 - Добавить трату")
        print("2 - Показать все траты")
        print("3 - Показать общую сумму")
        print("4 - Изменить трату")
        print("5 - Удалить трату")
        print("6 - Траты за период")
        print("7 - Экспорт в CSV")
        print("0 - Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "4":
            edit_expense(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            filter_by_date(expenses)
        elif choice == "7":
            export_csv(expenses)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта, попробуйте ещё раз.")


main()
