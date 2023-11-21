import random
import subprocess
from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Context
from os import getenv

load_dotenv('/Users/mimi/coding/obey_testing_goat/.env')
REPO_URL = getenv('REPOSITORY')
USERNAME = getenv('USERNAME')
HOST = getenv('HOST')
SITENAME = getenv('SITENAME')
GIT_PATH = "/usr/bin/git"


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
        # _create_or_update_dotenv(c)
        # _update_static_files(c)
        # _update_database(c)


def _get_latest_source(c):
    """Change to the directory where the source code is located and pull the latest code from the repository."""
    if c.run(f"test -d /home/{USERNAME}/sites/{SITENAME}/.git", warn=True).failed:
        c.run(f"{GIT_PATH} clone {REPO_URL} /home/{USERNAME}/sites/{SITENAME}")
    current_commit = subprocess.check_output([GIT_PATH, "log", "-n 1", "--format=%H"]).decode("utf-8").strip("\n")
    c.run(f"cd /home/{USERNAME}/sites/{SITENAME} && {GIT_PATH} fetch")
    # TODO: Fabric doesn't like the reset command. It runs but receives this error:
    # fatal: not a git repository (or any of the parent directories): .git
    c.run(f'{GIT_PATH} reset --hard {current_commit}')
    c.run(f'{GIT_PATH} log -n 1 --format=%H')


def _update_virtualenv(c):
    """Change to the directory where the source code is located and update the virtual environment."""
    c.run(f"cd /home/{USERNAME}/sites/{SITENAME}"
          f"&& /home/{USERNAME}/sites/{SITENAME}.venv/bin/pip install -r requirements.txt")


def _create_or_update_dotenv(c):
    """Create or update the .env file in the source code directory."""
    current_contents = c.run(f"cat /home/{USERNAME}/sites/{SITENAME}/.env", hide=True).stdout
    if "DJANGO_DEBUG_FALSE=y" not in current_contents:
        current_contents = current_contents.append("DJANGO_DEBUG_FALSE=y")
    if f"SITENAME={SITENAME}" not in current_contents:
        current_contents = current_contents.append(f"SITENAME={SITENAME}")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret = "".join(random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=50))
        current_contents = current_contents.append(f"DJANGO_SECRET_KEY={new_secret}")
    # TODO: Change to .env if all works well and the .env test file looks correct
    c.run(f"echo \"{current_contents}\" > /home/{USERNAME}/sites/{SITENAME}/TEST_RUN_DELETE")
    c.run(f"cat /home/{USERNAME}/sites/{SITENAME}/TEST_RUN_DELETE")


context = Context()

deploy(context)
