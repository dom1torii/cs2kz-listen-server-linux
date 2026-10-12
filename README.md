Ai slopped python script based on [cs2kz-mapping by zer0k](https://github.com/zer0k-z/cs2kz-mapping) to run cs2kz listen server on linux.  
Usage:
```bash
# create venv (obviously get python first)
python -m venv .venv
source .venv/bin/activate
# or in nushell (get virtualenv package for ur distro)
python -m virtualenv .venv
overlay use .venv/bin/activate.nu

python verify.py # (Optional, if gameinfo.gi is corrupt)
python setup.py
python run-listen.py # defaults to kz_grotto, set ur map by adding map id and name as 1st and 2nd argument
```

Stuff to consider:
- before running the script or changing maps you need to subscribe the map on workshop ([kz_grotto](https://steamcommunity.com/sharedfiles/filedetails/?id=3121168339) by default)
- `run-listen.py` starts the game via steam. your game has 15 seconds to launch, adjust if needed. you can safely skip shader processing if needed.
- exiting to main menu will cause the game to deadlock, change maps with `map_workshop <map_id> <map_name>`
- multiaddonmanager is not supposed to run on a listen server so expect bugs and stuff. it doesn't work at all on first launch and requires a map change to work.
