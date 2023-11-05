import json
import os

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(expenses, file, ensure_ascii=False, indent=2)


def add_expense(expenses):
    name = input("Название траты: ")
    try:
        amount = float(input("Сумма: "))
    except ValueError:
        print("Нужно ввести число.")
        return
    expenses.append({"name": name, "amount": amount})
    save_expenses(expenses)
    print("Трата добавлена.")


def show_expenses(expenses):
    if len(expenses) == 0:
        print("Трат пока нет.")
        return
    for number, expense in enumerate(expenses, start=1):
        print(f"{number}. {expense['name']} — {expense['amount']}")


def show_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    print(f"Всего потрачено: {total}")


def main():
    expenses = load_expenses()
    while True:
        print("\n1 - Добавить трату")
        print("2 - Показать все траты")
        print("3 - Показать общую сумму")
        print("0 - Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_total(expenses)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта, попробуйте ещё раз.")


main()
