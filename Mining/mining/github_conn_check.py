import subprocess
import requests


def run_cmd(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError:
        return None


print("---- Checking Git installation ----")
git_version = run_cmd("git --version")
if git_version:
    print(f"Git installed: {git_version}")
else:
    print("Git is NOT installed")
    exit()

print("\n---- Checking Git configuration ----")
username = run_cmd("git config --global user.name")
email = run_cmd("git config --global user.email")

print(f"Username: {username}")
print(f"Email: {email}")

if not username or not email:
    print("Git global configuration missing!")

print("\n---- Checking GitHub remote repository ----")
remote = run_cmd("git remote -v")
if remote:
    print(remote)
    if "github.com" in remote:
        print("GitHub repository detected")
else:
    print("No Git repository found in this folder yet")

print("\n---- Checking GitHub API connectivity ----")
try:
    r = requests.get("https://api.github.com")
    if r.status_code == 200:
        print("GitHub API reachable")
    else:
        print("GitHub API returned unexpected status:", r.status_code)
except Exception as e:
    print("Failed to connect to GitHub:", e)

print("\n---- Status Summary ----")
print("If Git is configured and GitHub remote exists, VS Code Git integration should work.")