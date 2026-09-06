import os
import sys
import requests
from pathlib import Path

ZIP_PATH = Path(__file__).resolve().parent / "promptforge-netlify.zip"

def deploy(token=None, site_name=None):
    print("=" * 65)
    print("  PROMPTFORGE AI -> NETLIFY DEPLOYMENT HELPER")
    print("=" * 65)

    if not ZIP_PATH.exists():
        print("[-] promptforge-netlify.zip not found. Please run 'python build_dist.py' first.")
        return

    # Check for token in environment or argument
    auth_token = token or os.environ.get("NETLIFY_AUTH_TOKEN")

    if not auth_token:
        print("\n[!] No Netlify Auth Token provided.")
        print("\n--- INSTANT 1-CLICK FREE DEPLOYMENT (NO LOGIN REQUIRED) ---")
        print("1. Open: https://app.netlify.com/drop")
        print("2. Drag and drop the following file into your browser:")
        print(f"   -> {ZIP_PATH}")
        print("3. Netlify will deploy your PromptForge dashboard in ~5 seconds with a live .netlify.app URL!")
        print("\n--- OR DEPLOY VIA CLI / API ---")
        print("If you have a Netlify Personal Access Token:")
        print("   python deploy_netlify.py <YOUR_NETLIFY_TOKEN>\n")
        return

    # Deploy via Netlify REST API
    print("[*] Connecting to Netlify REST API...")
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/zip"
    }

    url = "https://api.netlify.com/api/v1/sites"
    if site_name:
        url += f"?name={site_name}"

    with open(ZIP_PATH, "rb") as f:
        zip_data = f.read()

    try:
        response = requests.post(url, headers=headers, data=zip_data, timeout=60)
        if response.status_code in [200, 201]:
            data = response.json()
            site_url = data.get("ssl_url") or data.get("url")
            admin_url = data.get("admin_url")
            print("\n[SUCCESS] Deployed successfully to Netlify!")
            print(f"-> Live URL:      {site_url}")
            print(f"-> Admin Console: {admin_url}")
        else:
            print(f"[-] Deployment failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[-] Error connecting to Netlify API: {e}")

if __name__ == "__main__":
    cli_token = sys.argv[1] if len(sys.argv) > 1 else None
    cli_site_name = sys.argv[2] if len(sys.argv) > 2 else None
    deploy(cli_token, cli_site_name)
