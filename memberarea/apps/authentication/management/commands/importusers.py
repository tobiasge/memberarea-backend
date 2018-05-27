import argparse
import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from memberarea.apps.authentication.models import User


class Command(BaseCommand):
    help = 'Import users from S-Verein export. File musst be UTF8.'

    date_format: str = '%d.%m.%Y'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=argparse.FileType())

    def handle(self, *args, **options):
        for userfile in options['file']:
            reader = csv.DictReader(userfile, delimiter=';', quotechar='"')
            for row in reader:
                member_id = row['Mitglieds-Nr']
                if not member_id:
                    self.stderr.write('No member ID found for: ' + row['Nachname'] + ', ' + row['Vorname'])
                    continue
                self.stdout.write('Importing user for: ' + row['Nachname'] + ', ' + row['Vorname'])

                # Building fields from CSV file
                user, created = User.objects.get_or_create(member_id=member_id)

                # Setting all fields
                user.salutation = row['Anrede']
                user.first_name = row['Vorname']
                user.last_name = row['Nachname']
                user.sex = 'M' if row['Geschlecht'] == 'männlich' else ('F' if row['Geschlecht'] == 'weiblich' else ' ')
                user.birthday = None if not row['Geburtsdatum'] else datetime.strptime(row['Geburtsdatum'], self.date_format)
                user.email = row['KommE-Mail_G1']
                user.username = row['Vorname'].lower() + '.' + row['Nachname'].lower()

                user.member_id = int(member_id)
                user.entry_date = None if not row['Eintrittsdatum'] else datetime.strptime(row['Eintrittsdatum'], self.date_format)
                user.exit_date = None if not row['Austrittsdatum'] else datetime.strptime(row['Austrittsdatum'], self.date_format)
                user.state = 'P' if row['Status'] == 'Passiv' else 'A'

                if created:
                    user.set_password(row['Geburtsdatum'])
                    # Force user to change his password
                    user.password_expired = True
                else:
                    self.stdout.write('  User in database with user.id = ' + str(user.id))

                try:
                    user.save()
                    self.stdout.write('  User saved with user.id = ' + str(user.id))
                except:
                    if created:
                        user.delete()
                    self.stderr.write('User saving failed')
