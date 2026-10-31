# Source - https://stackoverflow.com/a/49166246
# Posted by Chillar Anand, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-31, License - CC BY-SA 4.0

import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = "pkill celery"
    subprocess.call(shlex.split(cmd))
    cmd = "celery -A norsk.project worker -l INFO"
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")

        # For Django>=2.2
        autoreload.run_with_reloader(restart_celery)

        # For django<2.1
        # autoreload.main(restart_celery)
