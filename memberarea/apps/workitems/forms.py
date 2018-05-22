import sys

from django import forms

from .models import RequiredHours


class RequiredHoursAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        # Check if range is correct
        maxYear = sys.maxsize
        minYear = -sys.maxsize - 1
        fromYearOfBirth = minYear if cleaned_data['fromYearOfBirth'] is None else cleaned_data['fromYearOfBirth']
        toYearOfBirth = maxYear if cleaned_data['toYearOfBirth'] is None else cleaned_data['toYearOfBirth']
        if not (fromYearOfBirth < toYearOfBirth):
            raise forms.ValidationError('FromYearOfBirth must be less to ToYearOfBirth')

        # Check for overlapping
        newRh = RequiredHours(year=cleaned_data['year'], fromYearOfBirth=cleaned_data['fromYearOfBirth'],
                              toYearOfBirth=cleaned_data['toYearOfBirth'])
        qs = RequiredHours.objects.filter(year=cleaned_data['year'])

        for rh in qs:
            if(rh.overlapsWith(newRh) and not (self.instance.pk == rh.pk)):
                raise forms.ValidationError('Overlaps with entry for the year {} and the year of birth range from {} to {}'
                    .format(rh.year, rh.fromYearOfBirth, rh.toYearOfBirth))
        return None

class WorkitemAdminForm(forms.ModelForm):
    pass
