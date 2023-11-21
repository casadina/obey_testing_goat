import random
import subprocess
from os.path import exists

from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Context
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
REPO_URL = getenv('REPOSITORY')
USERNAME = getenv('USERNAME')
HOST = getenv('HOST')
SITENAME = getenv('SITENAME')
GIT_PATH = "/usr/bin/git"
CD_PATH = f"/home/{USERNAME}/sites/{SITENAME}"


@task
def deploy(ctx):
    with Connection(
        host=HOST,
        user=USERNAME,
        port=2222,
        connect_kwargs={"key_filename": getenv('SSH_PKEY')}
    ) as c:
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_static_files(c)
        _update_database(c)


def _get_latest_source(c):
    """Change to the directory where the source code is located and pull the latest code from the repository."""
    if c.run(f"test -d {CD_PATH}/.git", warn=True).failed:
        c.run(f"{GIT_PATH} clone {REPO_URL} {CD_PATH}")
    current_commit = subprocess.check_output([GIT_PATH, "log", "-n 1", "--format=%H"]).decode("utf-8").strip("\n")
    c.run(f"cd {CD_PATH} && {GIT_PATH} fetch")
    c.run(f'cd {CD_PATH} && {GIT_PATH} reset --hard {current_commit}')
    c.run(f'cd {CD_PATH} && {GIT_PATH} log -n 1 --format=%H')


def _update_virtualenv(c):
    """Change to the directory where the source code is located and update the virtual environment."""
    if not exists(f"{CD_PATH}/.venv/bin/pip"):
        c.run(f"python3 -m venv {CD_PATH}/.venv")
    c.run(f"{CD_PATH}/.venv/bin/pip install -r {CD_PATH}/requirements.txt")


def _create_or_update_dotenv(c):
    """Create or update the .env file in the source code directory."""
    current_contents = c.run(f"cat {CD_PATH}/.env", hide=True).stdout
    if "DJANGO_DEBUG_FALSE=y" not in current_contents:
        current_contents = current_contents.append("DJANGO_DEBUG_FALSE=y")
    if f"SITENAME={SITENAME}" not in current_contents:
        current_contents = current_contents.append(f"SITENAME={SITENAME}")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50))
        current_contents = current_contents.append(f"DJANGO_SECRET_KEY={new_secret}")
    c.run(f"echo \"{current_contents}\" > {CD_PATH}/.env")
    c.run(f"cat {CD_PATH}/.env")


def _update_static_files(c):
    """Change to the directory where the source code is located and update the static files."""
    c.run(f"cd {CD_PATH} && {CD_PATH}/.venv/bin/python manage.py collectstatic --noinput")


def _update_database(c):
    """Change to the directory where the source code is located and update the database."""
    c.run(f"cd {CD_PATH} && {CD_PATH}/.venv/bin/python manage.py migrate --noinput")


context = Context()

deploy(context)
