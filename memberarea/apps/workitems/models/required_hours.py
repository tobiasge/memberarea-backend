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

    def isValidForYearOfBirth(self, yearOfBirth):
        if self.fromYearOfBirth is None and self.toYearOfBirth is None:
            return True

        if self.fromYearOfBirth is None:
            return yearOfBirth < self.toYearOfBirth

        if self.toYearOfBirth is None:
            return self.fromYearOfBirth <= yearOfBirth

        return self.fromYearOfBirth <= yearOfBirth and yearOfBirth <= self.toYearOfBirth

    def overlapsWith(self, rhs):
        lhs = self
        if lhs.year != rhs.year:
            return False

        # Sanitize ranges for comparision
        maxYear = sys.maxsize
        minYear = -sys.maxsize - 1
        x1 = minYear if lhs.fromYearOfBirth is None else lhs.fromYearOfBirth
        y1 = minYear if rhs.fromYearOfBirth is None else rhs.fromYearOfBirth
        x2 = maxYear if lhs.toYearOfBirth is None else lhs.toYearOfBirth
        y2 = maxYear if rhs.toYearOfBirth is None else rhs.toYearOfBirth
        
        return (x1 <= y2) and (y1 <= x2)


    def __str__(self):
        return "year: {}, fromYearOfBirth: {}, toYearOfBirth: {}".format(self.year, self.fromYearOfBirth, self.toYearOfBirth)

    class Meta:
        ordering = ('-year', '-fromYearOfBirth', '-toYearOfBirth')
