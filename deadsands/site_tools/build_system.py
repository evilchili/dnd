from collections import defaultdict
from pathlib import Path
from time import sleep

import os
import subprocess
import shlex
import shutil
import webbrowser

from pelican import main as pelican_main
from livereload import Server
from livereload.watcher import INotifyWatcher

import site_tools as st

CONFIG = defaultdict(dict)
CONFIG.update(
    {
        "settings_base": st.DEV_SETTINGS_FILE_BASE,
        "settings_publish": st.PUB_SETTINGS_FILE_BASE,
        # Output path. Can be absolute or relative to tasks.py. Default: 'output'
        "deploy_path": st.SETTINGS["OUTPUT_PATH"],
        # Remote server configuration
        "ssh_user": "greg",
        "ssh_host": "froghat.club",
        "ssh_port": "22",
        "ssh_path": "/usr/local/deploy/deadsands/",
        # Host and port for `serve`
        "host": "localhost",
        "port": 8000,
        # content manager config
        "templates_path": "markdown-templates",
        # directory to watch for new assets
        "import_path": "imports",
        # where new asseets will be made available
        "production_host": "deadsands.froghat.club",
        # where to find roll table sources
        "table_sources_path": "sources",
        # where to store campaign state
        "campaign_save_path": '~/.dnd',
        "campaign_name": "deadsands",
        # campaign start date
        "campaign_start_date": "2.1125.5.25",
    }
)


def pelican_run(cmd: list = [], publish=False) -> None:
    settings = CONFIG["settings_publish" if publish else "settings_base"]
    pelican_main(["-s", settings] + cmd)


def clean():
    if os.path.isdir(CONFIG["deploy_path"]):
        shutil.rmtree(CONFIG["deploy_path"])
        os.makedirs(CONFIG["deploy_path"])


def build():
    subprocess.run(shlex.split("git submodule update --remote --merge"))
    pelican_run()


def watch():
    import_path = Path(CONFIG["import_path"])
    content_path = Path(st.SETTINGS["PATH"])

    def do_import():
        assets = []
        for src in import_path.rglob("*"):
            relpath = src.relative_to(import_path)
            target = content_path / relpath
            if src.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if target.exists():
                print(f"{target}: exists; skipping.")
                continue
            print(f"{target}: importing...")
            src.link_to(target)
            subprocess.run(shlex.split(f"git add {target}"))
            uri = target.relative_to("content")
            assets.append(f"https://{CONFIG['production_host']}/{uri}")
            src.unlink()
        if assets:
            publish()
            print("\n\t".join(["\nImported Asset URLS:"] + assets))
            print("\n")
    watcher = INotifyWatcher()
    watcher.watch(import_path, do_import)
    watcher.start(do_import)
    print(f"Watching {import_path}. CTRL+C to exit.")
    while True:
        watcher.examine()
        sleep(5)


def serve():
    url = "http://{host}:{port}/".format(**CONFIG)

    def cached_build():
        pelican_run(["-ve", "CACHE_CONTENT=true", "LOAD_CONTENT_CACHE=true", "SHOW_DRAFTS=true", f'SITEURL="{url}"'])
    clean()
    cached_build()
    server = Server()
    theme_path = st.SETTINGS["THEME"]
    watched_globs = [
        CONFIG["settings_base"],
        "{}/templates/**/*.html".format(theme_path),
    ]

    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_glob = "{0}/**/*{1}".format(st.SETTINGS["PATH"], extension)
        watched_globs.append(content_glob)

    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file_glob = "{0}/static/**/*{1}".format(theme_path, extension)
        watched_globs.append(static_file_glob)

    for glob in watched_globs:
        server.watch(glob, cached_build)

    if st.OPEN_BROWSER_ON_SERVE:
        webbrowser.open(url)

    server.serve(host=CONFIG["host"], port=CONFIG["port"], root=CONFIG["deploy_path"])


def publish():
    clean()
    pelican_run(publish=True)
    subprocess.run(
        shlex.split(
            'rsync --delete --exclude ".DS_Store" -pthrvz -c '
            '-e "ssh -p {ssh_port}" '
            "{} {ssh_user}@{ssh_host}:{ssh_path}".format(CONFIG["deploy_path"].rstrip("/") + "/", **CONFIG)
        )
    )
