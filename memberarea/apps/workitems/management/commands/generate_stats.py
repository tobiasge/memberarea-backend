from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from memberarea.apps.workitems.models import WorkedHoursStats


class Command(BaseCommand):
    help = "Calculates the worked hour statistics for each active club member"

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            help='Calculate stats for the given year. Current year if emtpy',
            type=int,
        )


    def handle(self, *args, **options):
        year = datetime.now().year if not options['year'] else options['year']
        print("Calculation statistics for the year {}".format(year))

        users = get_user_model().objects.filter(state='A')
        for user in users:
            print("Calculation statistics for {}".format(user.display_name))
            hoursConfirmed = 0
            hoursNotConfirmed = 0
            hasWorkitems = False
            for wia in user.assigned_workitems.filter(done_at__year=year):
                hasWorkitems = True
                if wia.duration_real:
                    duration = wia.duration_real
                else:
                    duration = wia.workitem.duration_expected

                if wia.verified:
                    hoursConfirmed += duration
                else:
                    hoursNotConfirmed += duration

            if hasWorkitems:
                if WorkedHoursStats.objects.filter(user=user).filter(year=year).exists():
                    stats = WorkedHoursStats.objects.filter(user=user).filter(year=year).get()
                    stats.hoursConfirmed=hoursConfirmed / 60
                    stats.hoursNotConfirmed=hoursNotConfirmed / 60
                else:
                    stats = WorkedHoursStats(user=user, year=year, hoursConfirmed=hoursConfirmed / 60, hoursNotConfirmed=hoursNotConfirmed / 60)
                stats.save()

