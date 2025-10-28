#!/usr/bin/env python3.7

import sys
import json
import time, datetime
from pathlib import Path
from typing import Dict, List

print("==== EXPENSE TRACKER ====")
print("1. Add expense\n2. View all\n3. Show summary\n4. Write to JSON\n5. Exit")

out_json = Path('expenses.json')

def add_exp(expenses: List) -> List:
    cat = input("Enter category: ").lower()
    desc = input("Enter description: ").lower()
    price = float(input("Enter amount: "))
    print()

    exp_dict = {
        "datetime": time.ctime(),
        "category": cat,
        "description": desc,
        "amount": price
    }

    expenses.append(exp_dict)

    print("Expense added successfully!")
    print("-" * 20)
    
    return expenses


def view_all(expenses: List) -> None:
    for i in expenses: 
        print(f"{i.get('description')}: ${i.get('amount')}")
    print("-" * 20)


def summary(expenses: List) -> None:
    print("----- SUMMARY -----")
    total = 0
    cat_total = {}
    for i in expenses:
        category = i.get('category', 'Unknown')
        amount = float(i.get('amount', 0))

        total += amount
        cat_total[category] = cat_total.get(category, 0) + amount

    for cat, amt in cat_total.items():
        print(f"{cat}: ${amt:.2f}")

    print()
    print(f"Total: ${total}")
    print("-" * 20)


def write_to_file(expenses: List) -> None:

    if out_json.is_file():
        if input(f"The json file {out_json} is already exists. Overwrite (Y/N)? ").lower() != "y":
            return
    
    with open(out_json, 'w') as file:
        json.dump(expenses, file, indent=4)
    print(f"Expenses written to {out_json}")


def main():
    is_running = True
    expenses = list()

    while is_running:
        try:
            user_input = int(input("Select an option: "))
            print("-" * 20)
        except ValueError:
            print("Please enter a valid number!")
            continue

        if user_input == 1:
            add_exp(expenses)
        elif user_input == 2:
            view_all(expenses)
        elif user_input == 3:
            summary(expenses)
        elif user_input == 4:
            write_to_file(expenses)
        elif user_input == 5:
            exit_me()
        else:
            print("Invalid choice, try again!")


def exit_me():
    is_running = False
    print("Good bye!")
    sys.exit(0)


if __name__ == "__main__":
    main()
