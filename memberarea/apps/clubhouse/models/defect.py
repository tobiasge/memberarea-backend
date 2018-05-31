from django.conf import settings
from django.db import models

from memberarea.apps.core.models import TimestampedModel
from .clubhouse import Clubhouse, Room


class Defect(TimestampedModel):
    title = models.CharField(max_length=80)
    description = models.TextField()
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reported_defects')
    repaired = models.BooleanField(db_index=True, default=False)

    # Link to ClubHouse and/or Room
    clubhouse = models.ForeignKey(Clubhouse, on_delete=models.PROTECT, null=True, blank=True, related_name='defects')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, null=True, blank=True, related_name='defects')

    class Meta:
        ordering = ('title', )
