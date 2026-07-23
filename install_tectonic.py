import urllib.request
import json
import zipfile
import os

url = "https://api.github.com/repos/tectonic-typesetting/tectonic/releases/latest"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print("Error fetching release info:", e)
    exit(1)

download_url = None
for asset in data.get("assets", []):
    if "x86_64-pc-windows-msvc.zip" in asset.get("name", ""):
        download_url = asset.get("browser_download_url")
        break

if download_url:
    print(f"Downloading from {download_url}")
    zip_path = "tectonic.zip"
    try:
        req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            out_file.write(response.read())
        print("Extracting...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("Done!")
    except Exception as e:
        print("Error downloading or extracting:", e)
else:
    print("Could not find Windows asset.")
