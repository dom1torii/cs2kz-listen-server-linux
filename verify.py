import os
import sys
import time
import urllib.error
import urllib.request

import common


BASE_URL = (
  "https://raw.githubusercontent.com/SteamDatabase/GameTracking-CS2/refs/heads/master/"
)
FILE_PATHS = ["game/csgo/gameinfo.gi"]


print("Attempting to restore gameinfo files...")
path = common.get_cs2_path()
if path is None:
  print("Failed to get CS2 path.")
  sys.exit()

# Download the stock gameinfo files and overwrite the local ones
for file_path in FILE_PATHS:
  url = BASE_URL + file_path
  print(f"Downloading {url}...")
  try:
    with urllib.request.urlopen(url) as response:
      content = response.read().decode("utf-8").replace("\n", "\r\n")
  except urllib.error.HTTPError as e:
    print(f"Failed to download {url}. ({e.code})")
    continue

  out_path = os.path.join(path, file_path)
  os.makedirs(os.path.dirname(out_path), exist_ok=True)
  with open(out_path, "wb") as f:
    _ = f.write(content.encode("utf-8"))

print("Done! Closing in 3 seconds...")
time.sleep(3)
