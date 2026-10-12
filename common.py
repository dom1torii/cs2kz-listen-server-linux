import os
import vdf
import shutil
from typing import Any, cast


def get_steam_directory():
  return os.path.expandvars("$HOME/.steam/steam")


def find_cs2_library_path(libraryfolders_path: str) -> str | None:
  """Parse libraryfolders.vdf and return the library path that holds CS2 (app 730)."""
  if not os.path.exists(libraryfolders_path):
    print(f"libraryfolders.vdf not found at {libraryfolders_path}")
    return None

  with open(libraryfolders_path, "r", encoding="utf-8") as file:
    library_data = cast(dict[str, Any], vdf.load(file))  # pyright: ignore[reportUnknownMemberType]

  folders = cast(dict[str, dict[str, Any]], library_data.get("libraryfolders", {}))
  for folder in folders.values():
    if "730" in folder.get("apps", {}):
      return cast(str, folder["path"])
  print("Failed to find CS2 library path.")
  return None


def get_cs2_path() -> str | None:
  library_path = find_cs2_library_path(
    os.path.join(get_steam_directory(), "steamapps", "libraryfolders.vdf")
  )
  if library_path is None:
    return None
  manifest = os.path.join(library_path, "steamapps", "appmanifest_730.acf")
  with open(manifest, "r", encoding="utf-8") as file:
    manifest_data = cast(dict[str, Any], vdf.load(file))
  installdir = cast(str, manifest_data["AppState"]["installdir"])
  return os.path.join(library_path, "steamapps", "common", installdir)


def modify_gameinfo(gameinfo_path: str) -> None:
  with open(gameinfo_path, "r") as f:
    lines = f.readlines()

  # Insert metamod into the search paths, right before the csgo entry
  target_line = "\t\t\tGame\tcsgo\n"
  new_line = "\t\t\tGame\tcsgo/addons/metamod\n"
  modified_lines: list[str] = []
  skip = 0

  for line in lines:
    # Remove the CustomNavBuild block (this line and the next 4)
    if "CustomNavBuild" in line:
      skip = 5
    if skip > 0:
      skip -= 1
      continue
    if line == target_line:
      modified_lines.append(new_line)
    modified_lines.append(line)

  with open(gameinfo_path, "w") as f:
    f.writelines(modified_lines)


def modify_gameinfo_p2p(gameinfo_path: str) -> None:
  modified_lines: list[str] = []

  with open(gameinfo_path, "r") as f:
    lines = f.readlines()

  for line in lines:
    if line == "\t\t// Bandwidth control default: 300,000 Bps\n":
      modified_lines.append('\t\t"net_p2p_listen_dedicated" "1"\n')
    elif line == "\tGameInstructor\n":
      modified_lines.append("\tNetworkSystem\n")
      modified_lines.append("\t{\n")
      modified_lines.append('\t\t"CreateListenSocketP2P" "2"\n')
      modified_lines.append("\t}\n")
    modified_lines.append(line)

  with open(gameinfo_path, "w") as f:
    f.writelines(modified_lines)


def backup_files(path: str) -> tuple[str, str]:
  gameinfo_path = os.path.join(path, "game", "csgo", "gameinfo.gi")
  backup_path = gameinfo_path + ".bak"

  _ = shutil.copyfile(gameinfo_path, backup_path)

  return gameinfo_path, backup_path


def restore_files(backup_path: str, gameinfo_path: str) -> None:
  _ = shutil.move(backup_path, gameinfo_path)
