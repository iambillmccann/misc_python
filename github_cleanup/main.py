import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
org = os.getenv("GITHUB_ORG")


def main():
    headers = {"Authorization": f"token {token}"}
    response = requests.get(f"https://api.github.com/orgs/{org}/repos", headers=headers)
    repos = response.json()
    for repo in repos:
        print(repo["name"])


if __name__ == "__main__":
    main()
