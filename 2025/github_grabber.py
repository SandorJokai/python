#!/usr/bin/env python3.7

import requests
import json
import sys
from pathlib import Path

def get_username() -> str:
    while True:
        username = input("Enter a GitHub username: ").lower()
    
        if not username.isalpha():
            print(f"Wrong type!")
            continue
    
        return username

def get_github(username: str) -> str:

    filename = Path(f"github_summary_{username}.json")

    try:
        url = f"https://api.github.com/users/{username}/repos"
        res = requests.get(url, timeout=5)
        print(f"Requested url: {res.url}")
        res.raise_for_status()
        repolist = res.json()

        repos_summary = list()
        count = 0
        for repo in repolist:
            repo_info = {
                    "name": repo["name"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo["language"]
                    }
            repos_summary.append(repo_info)
            count += 1

        print(f"Total repositories found: {count}\n")

        if not filename.is_file():
            with open(filename, 'w') as f:
                json.dump(repos_summary, f, indent=4)
                print(f"Data saved to: {filename}")
        else:
            file_exists = input(f"JSON file \"{filename}\" is exists, would you like to overwrite (Y/N)? ").lower()
            if file_exists == "y":
                with open(filename, 'w') as f:
                    json.dump(repos_summary, f, indent=4)
                    print(f"Data saved to: {filename}")

        print("-" * 60)
        print(f"{'Repository Name':<30} {'Stars':<7} {'Forks':<7} {'Language':<15}")
        print("-" * 60)

        for idx in repos_summary:
            print(f"{idx['name']:<30} {idx['stars']:<7} {idx['forks']:<7} {str(idx['language']):<15}")
    
    except requests.exceptions.HTTPError as err:
        print(f"Error occurred! {err}")
    

if __name__ == "__main__":
    user = get_username()
    get_github(user)
