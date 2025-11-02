#!/usr/bin/env python3.7

import requests
import json
import os
import time, datetime
from pathlib import Path


def validity_checker(syntax_ok: str) -> bool:

    if not syntax_ok.isalpha():
        print("Not supported type, must be string!")
        return False
    elif len(syntax_ok) != 3:
        print("3 characters allowed!")
        return False
    return True


def fetch_exchange_data(base: str) -> dict:

    url = f"https://api.exchangerate.host/live?source={base}"
    api_key = os.getenv("EXCH_API")
    query_params = {
            "access_key": api_key
            }
    try:
        res = requests.get(url, query_params, timeout=3)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.HTTPError as err:
        print(f"Error occurred: {err}")
    except requests.exceptions.ConnectionError:
        print(f"Connection error!")


def get_rates(data: dict, targets: list) -> list:

    while True:
        user_input = input("Enter the target currency (EUR, GBP etc.): ").upper()
        if validity_checker(user_input):
            break

    for currency, rate in data['quotes'].items():
        if currency.endswith(user_input):
            result = f"{user_input}: {rate}"
            print(result)
            targets.append(result)

    return targets


def view_currencies(data: dict) -> bool:
    user_input = input("Would you like to see all currencies? (Y/N): ").upper()

    if user_input == "Y":
        for currency, rate in data['quotes'].items():
            print(f"{currency}: {rate}")
        return True
    elif user_input == "N":
        return False
    else:
        print("Invalid Input!")
        return False


def save_to_file(base: str, targets: list, json_file):
    payload = {"timestamp": time.ctime(), "base": base, "rates": targets}
    with open(json_file, "w") as f:
        json.dump(payload, f, indent=4)
    print(f"Data saved to {json_file}.")


def main():
    json_file = Path("exchange_rates.json")
    targets: List[str] = []

    while True:
        base = input("Choose a base currency (e.g. 'USD'): ").upper()
        if validity_checker(base):
            break

    data = fetch_exchange_data(base)
    if not data:
        return

    print("\n==== EXCHANGE RATES ====")
    print(f"Base: {base}")
    print("-" * 25)

    while True:
        get_rates(data, targets)
        again = input("Would you like another exchange? (Y/N): ").upper()
        if again != "Y":
            view_currencies(data)
            save_to_file(base, targets, json_file)
            print("Good bye!")
            break

if __name__ == "__main__":
    main()
