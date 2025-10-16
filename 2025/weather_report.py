#!/usr/bin/env python3.7

import requests
import json
import time, datetime
from pathlib import Path
from typing import Dict, Tuple, List

'''
    Goal: Fetch current weather data for a list of european_capitals using the Open-Meteo API, store it in a JSON file, and print a summary report.

    Return: Name of the european_capitals with current temperature.

'''

def get_data(european_capitals: Dict[str, Tuple[float, float]]) -> List[Dict]:

    try:
        url = "https://api.open-meteo.com/v1/forecast"

        print("-" * 34)
        print("City         Temp (°C)  Wind (km/h)")
        print("-" * 34)

        data_list = []
        for k, v in sorted(european_capitals.items()):
            query_params = {
                    "latitude": v[0],
                    "longitude": v[1],
                    "current_weather": True,
                    }
            res = requests.get(url, params=query_params, timeout=5)
            res.raise_for_status()
            current = res.json()["current_weather"]
            result = {
                    k: {"temperature": current["temperature"], "windspeed": current["windspeed"]}
                    }

            data_list.append(result)
            
            print(f"{k:<12} {current['temperature']:<10} {current['windspeed']:<10}")

    except requests.exceptions.HTTPError as err:
        print(f"Error occurred: {err}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"Connection error!")
        return False

    return data_list


def process_data(imported_list):
    payload = {"timestamp": current_time, "european_capitals": imported_list}

    if not filename.is_file():
        with open(filename, 'w') as f:
            json.dump(payload, f, indent=4)
        print(f"Data wrote successfully into the {filename} JSON file.")
    else:
        user_input = input(f"\nfile {filename} is already exists, do you want to overwrite (Y/N)? ").lower()
        if user_input == 'y':
            with open(filename, 'w') as f:
                json.dump(payload, f, indent=4)
            print(f"Data wrote successfully into the {filename} JSON file.")


if __name__ == "__main__":
    filename = Path("weather_report.json")
    european_capitals = {
            "London": (51.5074, -0.1278),
            "Paris": (48.8566, 2.3522),
            "Berlin": (52.5200, 13.4050),
            "Rome": (41.9028, 12.4964),
            "Madrid": (40.4168, -3.7038),
            "Lisbon": (38.7169, -9.1399),
            "Vienna": (48.2082, 16.3738),
            "Prague": (50.0755, 14.4378),
            "Warsaw": (52.2297, 21.0122),
            "Budapest": (47.4979, 19.0402),
            "Athens": (37.9838, 23.7275),
            "Dublin": (53.3498, -6.2603),
            "Copenhagen": (55.6761, 12.5683),
            "Stockholm": (59.3293, 18.0686),
            "Oslo": (59.9139, 10.7522),
            "Helsinki": (60.1699, 24.9384),
            "Brussels": (50.8503, 4.3517),
            "Amsterdam": (52.3676, 4.9041),
            "Luxembourg": (49.6117, 6.1319),
            "Bern": (46.9480, 7.4474),
            "Reykjavik": (64.1355, -21.8954),
            "Tallinn": (59.4370, 24.7536),
            "Riga": (56.9496, 24.1052),
            "Vilnius": (54.6872, 25.2797),
            "Bratislava": (48.1486, 17.1077),
            "Ljubljana": (46.0569, 14.5058),
            "Zagreb": (45.8150, 15.9819),
            "Sarajevo": (43.8563, 18.4131),
            "Belgrade": (44.7866, 20.4489),
            "Sofia": (42.6977, 23.3219),
            "Bucharest": (44.4268, 26.1025),
            "Tirana": (41.3275, 19.8189),
            "Skopje": (41.9981, 21.4254),
            "Kiev": (50.4501, 30.5234),
            }

    current_time = time.ctime()
    output = get_data(european_capitals)
    process_data(output)
