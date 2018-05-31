from django.db import models

from memberarea.apps.core.models import TimestampedModel


class Clubhouse(TimestampedModel):
    name = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name', )


class Room(TimestampedModel):
    name = models.CharField(max_length=80)
    clubhouse = models.ForeignKey(Clubhouse, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self) -> str:
        return "{} \ {}".format(self.clubhouse.name, self.name)

    class Meta:
        ordering = ('name', )
