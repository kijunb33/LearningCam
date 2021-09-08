from django import forms

from log.models import Log


class LogCreateForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['user', 'motion']
