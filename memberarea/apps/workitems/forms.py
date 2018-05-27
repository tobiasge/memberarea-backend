import sys

from django import forms

from .models import RequiredHours


class RequiredHoursAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        # Check if range is correct
        max_year = sys.maxsize
        min_year = -sys.maxsize - 1
        from_year_of_birth = min_year if cleaned_data['fromYearOfBirth'] is None else cleaned_data['fromYearOfBirth']
        to_year_of_birth = max_year if cleaned_data['toYearOfBirth'] is None else cleaned_data['toYearOfBirth']
        if not (from_year_of_birth < to_year_of_birth):
            raise forms.ValidationError('FromYearOfBirth must be less to ToYearOfBirth')

        # Check for overlapping
        new_rh = RequiredHours(year=cleaned_data['year'], fromYearOfBirth=cleaned_data['fromYearOfBirth'],
                               toYearOfBirth=cleaned_data['toYearOfBirth'])
        qs = RequiredHours.objects.filter(year=cleaned_data['year'])

        for rh in qs:
            if rh.overlaps_with(new_rh) and not (self.instance.pk == rh.pk):
                raise forms.ValidationError(
                    'Overlaps with entry for the year {} and the year of birth range from {} to {}'
                    .format(rh.year, rh.fromYearOfBirth, rh.toYearOfBirth))
        return None


class WorkitemAdminForm(forms.ModelForm):
    pass
