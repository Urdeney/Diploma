from django.core import management
from django.core.management.base import BaseCommand

from shutil import rmtree
from pathlib import Path


class Command(BaseCommand):
    help = 'Clear db, remove packages'

    # pylint: broad-exception-caught
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('Removing packages...'))
            for p in Path('packages').iterdir():
                self.stdout.write(f'Deleting {p}...')
                rmtree(p)

            self.stdout.write(self.style.WARNING('Removing database entries...'))
            management.call_command('migrate', 'clonus', 'zero')

            self.stdout.write(self.style.WARNING('Migrating database...'))
            management.call_command('migrate', 'clonus')

            self.stdout.write(self.style.SUCCESS('Done'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(exc))