import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"

def build():
    print("[*] Building PromptForge AI for Netlify...")
    
    # 1. Recreate clean dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    
    (DIST_DIR / "css").mkdir(parents=True, exist_ok=True)
    (DIST_DIR / "js").mkdir(parents=True, exist_ok=True)

    # 2. Process index.html with relative paths
    index_src = BASE_DIR / "templates" / "index.html"
    index_dest = DIST_DIR / "index.html"
    with open(index_src, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Convert /static/ paths to relative paths for Netlify
    html_content = html_content.replace('/static/css/styles.css', 'css/styles.css')
    html_content = html_content.replace('/static/js/app.js', 'js/app.js')

    with open(index_dest, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 3. Copy CSS and JS
    shutil.copy(BASE_DIR / "static" / "css" / "styles.css", DIST_DIR / "css" / "styles.css")
    shutil.copy(BASE_DIR / "static" / "js" / "app.js", DIST_DIR / "js" / "app.js")

    # 4. Copy Netlify and Vercel configs
    if (BASE_DIR / "netlify.toml").exists():
        shutil.copy(BASE_DIR / "netlify.toml", DIST_DIR / "netlify.toml")
    if (BASE_DIR / "vercel.json").exists():
        shutil.copy(BASE_DIR / "vercel.json", DIST_DIR / "vercel.json")

    with open(DIST_DIR / "_redirects", "w", encoding="utf-8") as f:
        f.write("/*    /index.html   200\n")

    # 5. Create ZIP package for Netlify Drop
    zip_path = BASE_DIR / "promptforge-netlify.zip"
    if zip_path.exists():
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                abs_file = Path(root) / file
                rel_file = abs_file.relative_to(DIST_DIR)
                zipf.write(abs_file, arcname=str(rel_file))

    print(f"[OK] Distribution built successfully in: {DIST_DIR}")
    print(f"[OK] Netlify deploy archive generated: {zip_path}")
    print(f"     File size: {zip_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    build()
