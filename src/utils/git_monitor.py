import json
import requests

def check_new_stars(repo_owner, repo_name, token):
    # Use the GitHub API to fetch the repository's stars
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    repo_owner = 'your_repo_owner'
    repo_name = 'your_repo_name'
    token = 'your_token'
    new_stars = check_new_stars(repo_owner, repo_name, token)
    print(new_stars)
if __name__ == '__main__':
    main()