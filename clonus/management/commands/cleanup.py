from django.core import management
from django.core.management.base import BaseCommand

from clonus.models import Package


class Command(BaseCommand):
    help = 'Clear db, remove packages'

    # pylint: broad-exception-caught
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('Removing packages...'))
            for p in Package.objects.all():
                self.stdout.write(p.path)
                p.rmdir()

            self.stdout.write(self.style.WARNING('Removing database entries...'))
            management.call_command('migrate', 'clonus', 'zero')

            self.stdout.write(self.style.WARNING('Migrating database...'))
            management.call_command('migrate', 'clonus')

            self.stdout.write(self.style.SUCCESS('Done'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(exc))