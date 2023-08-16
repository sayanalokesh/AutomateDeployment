import os
import shutil
from git import Repo
import requests
import json

# repo_path = '/devops/herovired/CI_CD/CICD-project-with-bash'
# nginx_folder = '/devops/herovired/CI_CD/'
# dev_branch_name = 'dev'
# file_to_copy = 'index.html'


# repo = Repo(repo_path)
# dev_branch = repo.branches[dev_branch_name]
# current_commit_hash = dev_branch.commit.hexsha

# if current_commit_hash != dev_branch.tracking_branch().commit.hexsha:
#     # Checkout the dev branch
#     repo.git.checkout(dev_branch_name)

#     # Copy the index.html file to the Nginx folder
#     src_file_path = os.path.join(repo_path, file_to_copy)
#     dest_file_path = os.path.join(nginx_folder, file_to_copy)

#     try:
#         shutil.copy(src_file_path, dest_file_path)
#         print("Copied index.html to Nginx folder.")
#     except Exception as e:
#         print("Error copying file:", e)
# else:
#     print("No new commits in the dev branch.")



        
owner = 'AdarshIITDH'
repo='CICD-project-with-bash'

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

def get_github_token():
    github_token=os.environ.get('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')
    if not github_token:
        raise Exception('token error')
    return github_token

def recognize_new_git_commit(owner, repo):
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
    else:
        print('No new commit has been happened.')

if  __name__ =="__main__":
    owner = 'AdarshIITDH'
    repo='CICD-project-with-bash'
    recognize_new_git_commit(owner, repo)