import requests
import json

def get_github_token():
    """Gets the GitHub token from the environment variable."""
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise Exception('Please set the GITHUB_TOKEN environment variable.')
    return github_token

def recognize_new_commit(owner, repo):
    """Recognizes the new git commit happened in the repo using git rest api in python."""
    session = requests.Session()
    session.headers['Authorization'] = f'token {get_github_token()}'
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f'Failed to get commits: {response.status_code}')
    commits = json.loads(response.content)
    latest_commit = commits[0]
    current_commit = get_latest_commit(owner, repo)
    if latest_commit['sha'] != current_commit:
        print('New commit has been happened!')
        print(latest_commit['message'])
        print(latest_commit['author']['name'])
        print(latest_commit['author']['email'])
    else:
        print('No new commit has been happened.')

def get_latest_commit(owner, repo):
    """Gets the latest commit sha from the repo."""
    session = requests.Session()
    session.headers['Authorization'] = f'token {get_github_token()}'
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/master'
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f'Failed to get latest commit: {response.status_code}')
    commit = json.loads(response.content)
    return commit['sha']

if __name__ == '__main__':
    owner = 'bard'
    repo = 'bard'
    recognize_new_commit(owner, repo)