from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

OPEN_BROWSER_ON_SERVE = True

DEV_SETTINGS_FILE_BASE = "pelicanconf.py"
PUB_SETTINGS_FILE_BASE = "publishconf.py"

SETTINGS = {}

SETTINGS.update(DEFAULT_CONFIG)

LOCAL_SETTINGS = get_settings_from_file(DEV_SETTINGS_FILE_BASE)

SETTINGS.update(LOCAL_SETTINGS)
