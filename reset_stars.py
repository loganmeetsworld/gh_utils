# A script that removes all your stared repos.
# > python3 reset_stars.py --token <token>

import argparse
import csv
import requests
import sys


def get_stars(token):
    repos = []
    url = "https://api.github.com/user/starred?per_page=100"
    while True:
        if token:
            url += f"&access_token={token}"
        resp = requests.get(url)
        resp.raise_for_status()
        repos.extend(resp.json())
        url = resp.links.get('next', {}).get('url')
        if not url:
            break
    return repos


def main(token):
    stars = get_stars(token)
    print(f"Found {len(stars)} stars.")
    for star in stars:
        owner = star['owner']['login']
        repo = star['name']
        url = f"https://api.github.com/user/starred/{owner}/{repo}"
        requests.delete(url)


if __name__ == '__main__':
    cl = argparse.ArgumentParser(description="This script removes all your stars.")
    cl.add_argument("--token", help="a session token for accessing stars")
    args = cl.parse_args()

    print("Removing stars from your account")
    sys.exit(main(args.token))
