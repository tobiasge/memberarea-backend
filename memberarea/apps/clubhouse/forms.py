from django import forms

# from .models import ClubHouse, Room, Defect


class DefectAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['room'] is not None:
            cleaned_data['clubhouse'] = cleaned_data['room'].clubhouse

        return None
