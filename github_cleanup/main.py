import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
org = os.getenv("GITHUB_ORG")
# List of repositories to keep
repos_to_keep = [
    "crush-it-backup",
    "js-samples",
    "serverless_compute_platform",
    "student-info-api",
    "source-code-management-exercise",
    "longest-substring-k-unique-template",
    "microservice-api-js-template",
    "osiris-core",
    "osiris-infrastructure",
    "osiris-function-library",
    "osiris-index-ledger",
    "osiris-admin-portal",
    "osiris-code-generation",
    "docker-introduction-assignment",
    "resume_analyzer_documentation",
]


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


def delete_repo(org, repo, token):
    headers = {"Authorization": f"token {token}"}
    response = requests.delete(
        f"https://api.github.com/repos/{org}/{repo}", headers=headers
    )
    if response.status_code == 204:
        print(f"Deleted {repo}")
    else:
        print(f"Failed to delete {repo}: {response.status_code}")


def main():
    repos = get_all_repos(org, token)
    for repo in repos:
        if repo["name"] not in repos_to_keep:
            delete_repo(org, repo["name"], token)
        else:
            print(f"Skipping {repo['name']}")


if __name__ == "__main__":
    main()
