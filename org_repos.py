# A basic script to grab all repos for an organization and tell me if they are archived or private
# > python3 org_repos.py --org buzzfeed --token secret

import argparse
import csv
import requests
import sys


def get_repos(org, token):
    repos = []
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100"

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


def main(org, token):
    repos = get_repos(org, token)
    print(f"Found {len(repos)} repositories for {org}.")

    with open('org_repos.csv', mode='w') as repos_csv:
        repos_writer = csv.writer(repos_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        repos_writer.writerow(['name', 'archived', 'private'])
        for repo in repos:
            repos_writer.writerow([repo['name'], repo['archived'], repo['private']])


if __name__ == '__main__':
    cl = argparse.ArgumentParser(description="This script fetches repositories for a Github organization.")
    cl.add_argument("--org", help="the name of the organization")
    cl.add_argument("--token", help="a session token for accessing private repos")
    args = cl.parse_args()

    print(f"Finding all repositories for {args.org}...\n")
    sys.exit(main(args.org, args.token))
