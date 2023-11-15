import random
from dotenv import load_dotenv
from fabric import Connection, task
from invoke import Context
from os import getenv

load_dotenv('/Users/mimi/coding/obey_testing_goat/.env')
REPO_URL = getenv('REPOSITORY')
USERNAME = getenv('USERNAME')
HOST = getenv('HOST')
SITENAME = getenv('SITENAME')


@task
def deploy(ctx):
    with Connection(
        host=HOST,
        user=USERNAME,
        port=2222,
        connect_kwargs={"key_filename": getenv('SSH_PKEY')}
    ) as c:
        c.run(f"mkdir -p /home/{USERNAME}/test_getenv")
        c.run(f"ls -al /home/goat")
        print("Created test directory?")
        """
        c.run(f"cd /home/USERNAME/sites/{SITENAME} && git pull")
        c.run(f"cd /home/USERNAME/sites/your_site && /home/USERNAME/.virtualenvs/your_virtualenv/bin/pip install -r requirements.txt")
        c.run(f"cd /home/USERNAME/sites/your_site && /home/USERNAME/.virtualenvs/your_virtualenv/bin/python manage.py migrate --noinput")
        c.run(f"cd /home/USERNAME/sites/your_site && /home/USERNAME/.virtualenvs/your_virtualenv/bin/python manage.py collectstatic --noinput")
        """


ctx = Context()

deploy(ctx)
