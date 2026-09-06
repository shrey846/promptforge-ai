import os
import sys
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"

def collect_files():
    files_payload = []
    for root, _, filenames in os.walk(DIST_DIR):
        for fname in filenames:
            fpath = Path(root) / fname
            rel_path = str(fpath.relative_to(DIST_DIR)).replace("\\", "/")
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                files_payload.append({
                    "file": rel_path,
                    "data": content
                })
            except Exception as e:
                # Binary fallback if any
                pass
    return files_payload

def deploy_to_vercel(token=None, project_name="promptforge-ai"):
    print("=" * 65)
    print("  PROMPTFORGE AI -> VERCEL DEPLOYMENT")
    print("=" * 65)

    auth_token = token or os.environ.get("VERCEL_TOKEN")

    if not auth_token:
        print("\n[!] No Vercel API Token detected.")
        print("\nChoose one of the two instant methods below to deploy to Vercel:\n")
        print("METHOD 1: Deploy with a Free Vercel Token (Instant, ~5 seconds)")
        print("1. Go to: https://vercel.com/account/tokens")
        print("2. Click 'Create Token', give it any name (e.g. 'promptforge'), and copy it.")
        print("3. Run this command:")
        print(f"   python deploy_vercel.py <YOUR_COPIED_TOKEN>\n")
        print("-" * 65)
        print("METHOD 2: Deploy via GitHub (Permanent CI/CD)")
        print("1. Create a new GitHub repo at https://github.com/new")
        print("2. Run these commands to push:")
        print(f"   cd \"{DIST_DIR}\"")
        print("   git init")
        print("   git add .")
        print("   git commit -m \"Initial PromptForge AI commit\"")
        print("   git remote add origin <YOUR_GITHUB_REPO_URL>")
        print("   git push -u origin main")
        print("3. In Vercel (https://vercel.com/new), select your repo and click 'Deploy'!")
        print("=" * 65)
        return

    print(f"[*] Deploying project '{project_name}' to Vercel...")
    files = collect_files()
    print(f"[*] Packed {len(files)} files ({', '.join(f['file'] for f in files)})")

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": project_name,
        "files": files,
        "projectSettings": {
          "framework": None
        }
    }

    try:
        url = "https://api.vercel.com/v13/deployments"
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            dep_url = data.get("url")
            aliases = data.get("alias", [])
            print("\n[SUCCESS] Deployed successfully to Vercel!")
            print(f"-> Deployment URL: https://{dep_url}")
            if aliases:
                print(f"-> Production Alias: https://{aliases[0]}")
        else:
            print(f"\n[-] Deployment failed ({resp.status_code}):")
            print(resp.text)
    except Exception as e:
        print(f"\n[-] Error connecting to Vercel API: {e}")

if __name__ == "__main__":
    token_arg = sys.argv[1] if len(sys.argv) > 1 else None
    name_arg = sys.argv[2] if len(sys.argv) > 2 else "promptforge-ai"
    deploy_to_vercel(token_arg, name_arg)
