from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Timeslot



class TimeForm(forms.Form):
    slots = forms.ModelMultipleChoiceField(queryset=Timeslot.objects.none(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, Tutor, *args, **kwargs):
        super(TimeForm, self).__init__(*args, **kwargs)
        self.fields['slots'].queryset = Timeslot.objects.filter(tutor__id=Tutor.id, status='Available').order_by('start')
    def save(self):
        for timeslot in self.cleaned_data['slots']:
            timeslot.status = 'Blocked'
            timeslot.save()