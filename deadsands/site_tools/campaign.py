from collections import defaultdict
from pathlib import Path

import shutil
import yaml

from reckoning import telisaran


def string_to_date(date):
    return telisaran.datetime.from_expression(f"on {date}", timeline={})


def date_to_string(date):
    return date.numeric


def _rotate_backups(path, max_backups=10):

    oldest = None
    if not path.exists():
        return oldest

    # move file.000 to file.001, file.001 to file.002, etc...
    for i in range(max_backups - 2, -1, -1):
        source = Path(f"{path}.{i:03d}")
        target = Path(f"{path}.{i+1:03d}")
        if not source.exists():
            continue
        if oldest is None:
            oldest = i
        if i == max_backups:
            source.unlink()
        shutil.move(source, target)

    return oldest


def save(campaign, path='.', name='dnd_campaign'):
    savedir = Path(path).expanduser()
    savepath = savedir / f"{name}.yaml"

    savedir.mkdir(exist_ok=True)
    backup_count = _rotate_backups(savepath)

    if savepath.exists():
        target = Path(f"{savepath}.000")
        shutil.move(savepath, target)

    campaign['date'] = date_to_string(campaign['date'])
    campaign['start_date'] = date_to_string(campaign['start_date'])
    savepath.write_text(yaml.safe_dump(dict(campaign)))
    return savepath, (backup_count or 0) + 2


def load(path=".", name='dnd_campaign', start_date='', backup=None, console=None):
    ext = "" if backup is None else f".{backup:03d}"

    default_date = string_to_date(start_date)
    campaign = defaultdict(str)
    campaign['start_date'] = default_date
    campaign['date'] = default_date
    campaign['level'] = 1

    if console:
        console.print(f"Loading campaign {name} from {path}...")
    try:
        target = Path(path).expanduser() / f"{name}.yaml{ext}"
        with open(target, 'rb') as f:
            loaded = yaml.safe_load(f)
            loaded['start_date'] = string_to_date(loaded['start_date'])
            loaded['date'] = string_to_date(loaded['date'])
            campaign.update(loaded)
            if console:
                console.print(f"Successfully loaded Campaign {name} from {target}!")
            return campaign
    except FileNotFoundError:
        console.print(f"No existing campaigns found in {path}.")
        return campaign
    except yaml.parser.ParserError as e:
        if console:
            console.print(f"{e}\nWill try an older backup.")
        return load(path, 0 if backup is None else backup+1)
