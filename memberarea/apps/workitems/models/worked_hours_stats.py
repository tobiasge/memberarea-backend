from django.conf import settings
from django.db import models

from memberarea.apps.core.models import TimestampedModel


class WorkedHoursStats(TimestampedModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    year = models.IntegerField()

    hoursConfirmed = models.DecimalField(max_digits=7, decimal_places=2)
    hoursNotConfirmed = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return "{} has {} confirmed and {} not confirmed hours".format(self.user.display_name, self.hoursConfirmed,
                                                                       self.hoursNotConfirmed)

    class Meta:
        ordering = ('user', '-year')

