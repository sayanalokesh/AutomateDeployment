import requests
import json
import os

def get_github_token():
    """Gets the GitHub token from the environment variable."""
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise Exception('Please set the GITHUB_TOKEN environment variable.')
    return github_token

def pull_from_repo(repo_url, repo_path):
    """Pulls from the git repository at the given URL and saves the changes to the given path."""
    session = requests.Session()
    session.headers['Authorization'] = f'token {get_github_token()}'
    url = f'https://api.github.com/repos/{repo_url}/git/fetches'
    data = {
        'ref': 'refs/heads/master',
        'update_shallow': True,
    }
    response = session.post(url, json=data)
    if response.status_code != 202:
        raise Exception(f'Failed to fetch from remote: {response.status_code}')
    repo = git.Repo(repo_path, search_parent_directories=True)
    repo.git.pull('origin', 'master')

def commit_changes(repo_path):
    """Commits the changes in the given repository."""
    repo = git.Repo(repo_path, search_parent_directories=True)
    repo.git.add('*')
    repo.git.commit('-m', 'Automated commit')

def copy_files_to_nginx(repo_path, nginx_path):
    """Copies the files from the given repository to the Nginx folder."""
    files = repo.git.ls_files('--exclude-standard')
    for file in files:
        source = os.path.join(repo_path, file)
        destination = os.path.join(nginx_path, file)
        shutil.copy(source, destination)

if __name__ == "__main__":
    repo_url = "https://github.com/bard/bard"
    repo_path = "/tmp/bard"
    nginx_path = "/etc/nginx/sites-available"
    pull_from_repo(repo_url, repo_path)
    commit_changes(repo_path)
    copy_files_to_nginx(repo_path, nginx_path)
