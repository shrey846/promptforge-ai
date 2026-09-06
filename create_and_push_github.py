import os
import sys
import subprocess
import webbrowser
import requests
from pathlib import Path

REPO_NAME = "promptforge-ai"
USERNAME = "shrey846"
REMOTE_URL = f"https://github.com/{USERNAME}/{REPO_NAME}.git"

def main():
    token = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_TOKEN")

    print("=" * 60)
    print("  PROMPTFORGE AI -> GITHUB PUSH HELPER")
    print("=" * 60)

    if token:
        print(f"[*] Creating repository '{REPO_NAME}' on GitHub via API...")
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "name": REPO_NAME,
            "description": "PromptForge AI - AI-powered prompt engineering studio with 15+ metric evaluation and multi-model rewrites",
            "private": False
        }
        res = requests.post("https://api.github.com/user/repos", headers=headers, json=payload)
        if res.status_code in [201, 422]: # 422 if already exists
            print(f"[OK] GitHub repository ready at: https://github.com/{USERNAME}/{REPO_NAME}")
        else:
            print(f"[-] Could not create repository via API: {res.text}")

    # Push to GitHub
    print(f"[*] Pushing local commits to: {REMOTE_URL} ...")
    try:
        cmd = ["git", "push", "-u", "origin", "main"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print("\n[SUCCESS] Successfully pushed PromptForge AI to your GitHub!")
            print(f"-> View your repository at: https://github.com/{USERNAME}/{REPO_NAME}")
        else:
            print("\n[-] Push failed because the repository does not exist on GitHub yet.")
            print(f"-> Please open: https://github.com/new?name={REPO_NAME}")
            print("-> Click 'Create repository' (leave everything default).")
            print("-> Then re-run: python create_and_push_github.py")
            webbrowser.open(f"https://github.com/new?name={REPO_NAME}")
    except Exception as e:
        print(f"[-] Error executing git push: {e}")

if __name__ == "__main__":
    main()
