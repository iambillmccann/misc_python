import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
org = os.getenv("GITHUB_ORG")


def get_all_repos(org, token):
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1

    while True:
        response = requests.get(
            f"https://api.github.com/orgs/{org}/repos",
            headers=headers,
            params={"page": page, "per_page": 100},
        )
        if response.status_code != 200:
            break
        repos.extend(response.json())
        if len(response.json()) == 0:
            break
        page += 1

    return repos


def main():
    repos = get_all_repos(org, token)
    for repo in repos:
        print(repo["name"])


if __name__ == "__main__":
    main()
