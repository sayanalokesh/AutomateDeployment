import shutil

source_path = r"L:\Udemy\AutomateDeployment\index.html"
destination_path = r"C:\nginx-1.24.0\AutoDeploy"

try:
    shutil.copy(source_path, destination_path)
    print("File copied successfully.")
except Exception as e:
    print("An error occurred:", str(e))

