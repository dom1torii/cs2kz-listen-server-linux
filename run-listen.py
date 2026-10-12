import argparse
import subprocess
import time
from common import *

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="cs2kz listen server")
  _ = parser.add_argument("map_id", nargs="?", help="workshop map id")
  _ = parser.add_argument("map_name", nargs="?", help="map name")
  args = parser.parse_args()

  if (args.map_id is None) != (args.map_name is None):
    parser.error("give both map_id and map_name, or none")

  map_id = args.map_id or "3121168339"
  map_name = args.map_name or "kz_grotto"

  path = get_cs2_path()
  if path is None:
    print("Failed to get CS2 path. Closing in 3 seconds...")
    time.sleep(3)
    exit()

  gameinfo_path, backup_path = backup_files(path)

  modify_gameinfo(gameinfo_path)
  modify_gameinfo_p2p(gameinfo_path)

  _ = subprocess.Popen(
    ["steam", "-applaunch", "730", "-insecure", f"+map_workshop {map_id} {map_name}"]
  )

  # next launch is clean game
  time.sleep(15)
  restore_files(backup_path, gameinfo_path)
