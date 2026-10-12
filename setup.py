import io
import os
import sys
import tarfile
import time

import requests

from common import get_cs2_path


def download_and_extract(url: str, dest: str, name: str):
  print(f"Downloading {name} from {url}...")

  response = requests.get(url)

  if response.status_code != 200:
    raise Exception(
      f"Failed to download {name}: {response.status_code} - {response.text}"
    )

  with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar:
    tar.extractall(dest)

  print(f"Extracted {name} into {dest}")


def get_latest(repo: str):
  response = requests.get(f"https://api.github.com/repos/{repo}/releases/latest")

  if response.status_code != 200:
    raise Exception(
      f"Failed to fetch latest release for repository {repo}: {response.status_code} - {response.text}"
    )

  release = response.json()
  if not release.get("assets"):
    raise Exception(f"No assets found for {repo}")
  return release


def install_metamod(cs2_dir: str):
  releases = requests.get(
    "https://api.github.com/repos/alliedmodders/metamod-source/releases"
  ).json()
  prerelease = next(r for r in releases if r["prerelease"] and not r["draft"])
  asset = next(
    a
    for a in prerelease["assets"]
    if a["name"].endswith(".tar.gz") and "linux" in a["name"].lower()
  )
  download_and_extract(asset["browser_download_url"], cs2_dir, "Metamod")


def install_cs2kz(cs2_dir: str):
  release = get_latest("KZGlobalTeam/cs2kz-metamod")
  asset = next(a for a in release["assets"] if a["name"] == "cs2kz-linux-master.tar.gz")
  download_and_extract(asset["browser_download_url"], cs2_dir, "CS2KZ")


def install_multiaddonmanager(cs2_dir: str):
  release = get_latest("Source2ZE/MultiAddonManager")
  asset = next(a for a in release["assets"] if a["name"].endswith("-steamrt4.tar.gz"))
  download_and_extract(asset["browser_download_url"], cs2_dir, "MultiAddonManager")


path = get_cs2_path()
if path is None:
  print("Failed to get CS2 path.")
  exit(1)

cs2_dir = os.path.join(path, "game", "csgo")

print(f"Setting up CS2KZ in {path}...")
install_metamod(cs2_dir)
install_cs2kz(cs2_dir)
install_multiaddonmanager(cs2_dir)

print("Setup complete, closing in 3 seconds...")
time.sleep(3)
