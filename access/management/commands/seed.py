import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the database with initial data from JSON fixtures'

    def handle(self, *args, **options):
        fixture_path = os.path.join(settings.BASE_DIR, 'access', 'fixtures', 'initial_data.json')

        if os.path.exists(fixture_path):
            # Load the fixture data
            self.stdout.write(self.style.NOTICE(f'Loading fixture data from {fixture_path}'))
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS('Database seeded successfully from initial_data.json'))
        else:
            self.stdout.write(self.style.ERROR(f'Fixture file not found at {fixture_path}'))
