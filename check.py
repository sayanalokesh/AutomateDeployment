import requests
import os
import shutil
from git import Repo
import git
import subprocess



# def git_pull(repo_path):
#     try:
       
#         subprocess.run(['git', 'pull'],  check=True)
#         print("Git pull successful")
#     except subprocess.CalledProcessError as e:
#         print("Git pull failed:", e)

# # Call the function with the repository path
# repository_path = '/devops/herovired/'
# git_pull(repository_path)




headers = {
    'Authorization': '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'
}

owner = 'AdarshIITDH'
repo='CICD-project-with-bash'
repo_path = '/devops/herovired/CI_CD/CICD-project-with-bash'
branch = 'dev'
nginx_folder = '/devops/herovired/CI_CD/'
file='index.html'

url = f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    latest_commit_hash = response.json()['commit']['sha']
else:
    print("Error fetching commit hash:", response.text)
    latest_commit_hash = None

previously_recorded_commit_hash = 'cd7db144b16fc92c8e5359922c4a0009c58f4a5b'  # Retrieve from your storage or set to None initially

if latest_commit_hash and latest_commit_hash != previously_recorded_commit_hash:
    print("New commit detected:", latest_commit_hash)

    src_file_path = os.path.join(repo_path, file)
    dest_file_path = os.path.join(nginx_folder, file)

    try:
        shutil.copy(src_file_path, dest_file_path)
        print("Copied index.html to Nginx folder.")
    except Exception as e:
        print("Error copying file:", e)



else:
    print("No new commits.")
