import datetime
import sys

from django.db import models

from memberarea.apps.core.models import TimestampedModel


class RequiredHours(TimestampedModel):
    year = models.IntegerField(default=datetime.datetime.now().year)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    missingHoursPrice = models.DecimalField(max_digits=5, decimal_places=2)
    fromYearOfBirth = models.IntegerField(null=True, blank=True)
    toYearOfBirth = models.IntegerField(null=True, blank=True)

    def is_valid_for_year_of_birth(self, year_of_birth):
        if self.fromYearOfBirth is None and self.toYearOfBirth is None:
            return True

        if self.fromYearOfBirth is None:
            return year_of_birth < self.toYearOfBirth

        if self.toYearOfBirth is None:
            return self.fromYearOfBirth <= year_of_birth

        return self.fromYearOfBirth <= year_of_birth <= self.toYearOfBirth

    def overlaps_with(self, rhs) ->bool:
        lhs = self
        if lhs.year != rhs.year:
            return False

        # Sanitize ranges for comparision
        max_year = sys.maxsize
        min_year = -sys.maxsize - 1
        x1 = min_year if lhs.fromYearOfBirth is None else lhs.fromYearOfBirth
        y1 = min_year if rhs.fromYearOfBirth is None else rhs.fromYearOfBirth
        x2 = max_year if lhs.toYearOfBirth is None else lhs.toYearOfBirth
        y2 = max_year if rhs.toYearOfBirth is None else rhs.toYearOfBirth
        
        return (x1 <= y2) and (y1 <= x2)

    @property
    def __str__(self):
        return "year: {}, fromYearOfBirth: {}, toYearOfBirth: {}".format(self.year, self.fromYearOfBirth,
                                                                         self.toYearOfBirth)

    class Meta:
        ordering = ('-year', '-fromYearOfBirth', '-toYearOfBirth')
