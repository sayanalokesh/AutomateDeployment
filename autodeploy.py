import os
import requests
import shutil
from git import Repo
from subprocess import run
import logging
from config import access_token, owner, repo_name, local_repo_path, nginx_path, file_to_copy, branch


# # GitHub repository details
# owner = 'sayanalokesh'
# repo_name = 'AutomateDeployment'
# branch = 'dev'

# # Paths
# local_repo_path = r"C:\Users\Lokesh\OneDrive\Desktop\Hero Vired\Sessions\AutomateDeployment"
# nginx_path = r"C:\nginx-1.24.0\autodeploy"
# file_to_copy = "index.html"

# # GitHub Personal Access Token
# access_token = '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'

# API request headers
headers = {
    'Authorization': f'Bearer {access_token}'
}

# API URL to get latest commit
url = f'https://api.github.com/repos/{owner}/{repo_name}/branches/{branch}'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    latest_commit_hash = response.json()['commit']['sha']
else:
    print("Error fetching commit hash:", response.text)
    latest_commit_hash = None

# Check if there's a new commit
previous_commit_hash_file = 'previous_commit_hash.txt'
if os.path.exists(previous_commit_hash_file):
    with open(previous_commit_hash_file, 'r') as file:
        previous_commit_hash = file.read().strip()
else:
    previous_commit_hash = None

if latest_commit_hash and latest_commit_hash != previous_commit_hash:
    print("New commit detected:", latest_commit_hash)

    # Clone or pull the repository
    if os.path.exists(local_repo_path):
        repo = Repo(local_repo_path)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(f'https://github.com/{owner}/{repo_name}.git', local_repo_path)

    # Check if index.html has changed
    if repo.git.diff(previous_commit_hash, latest_commit_hash, '--', file_to_copy):
        src_path = os.path.join(local_repo_path, file_to_copy)
        dest_path = os.path.join(nginx_path, file_to_copy)
        if os.path.exists(src_path):
            shutil.copy(src_path, dest_path)
            print("Copied index.html to Nginx folder.")

    # Create a merge request
    if branch == 'dev':
        url = f'https://api.github.com/repos/{owner}/{repo_name}/pulls'
        data = {
            "title": "Merge dev to main",
            "head": "dev",
            "base": "main"
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("Merge request created successfully.")
        else:
            print("Error creating merge request:", response.text)

    # Update the previous commit hash
    with open(previous_commit_hash_file, 'w') as file:
        file.write(latest_commit_hash)