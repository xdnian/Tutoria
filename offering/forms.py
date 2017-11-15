from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Timeslot
import pytz

TIMEZONELOCAL = pytz.timezone('Asia/Hong_Kong')

# class TimeForm(forms.Form):
#     slots = forms.ModelMultipleChoiceField(queryset=Timeslot.objects.none(), widget=forms.CheckboxSelectMultiple, to_field_name="time")
#     def __init__(self, Tutor, *args, **kwargs):
#         super(TimeForm, self).__init__(*args, **kwargs)
#         self.fields['slots'].queryset = Timeslot.objects.filter(tutor__id=Tutor.id).order_by('start')
#     def save(self):
#         for timeslot in self.cleaned_data['slots']:
#             timeslot.status = 'Blocked'
#             timeslot.save()

class TimeForm(forms.Form):
    fields = {}
    def __init__(self, Tutor, *args, **kwargs):
        super(TimeForm, self).__init__(*args, **kwargs)
        self.allSlots = Timeslot.objects.filter(tutor__id=Tutor.id).order_by('start')
        for i in range(len(self.allSlots)):
            startlocal = self.allSlots[i].start.astimezone(TIMEZONELOCAL)
            endlocal = self.allSlots[i].end.astimezone(TIMEZONELOCAL)
            date = startlocal.strftime('%b %d')
            startTime = startlocal.strftime('%H:%M')
            endTime = endlocal.strftime('%H:%M')
            status = self.allSlots[i].status

            attrs = {'status': status, 'date':date, 'startTime':startTime, 'endTime':endTime}
            if status != 'Available':
                if status == 'Blocked':
                    attrs['checked'] = ''
                else:
                    attrs['disabled'] = ''

            self.fields["slot{0}".format(i)] = forms.BooleanField(required=False, 
                    widget=forms.CheckboxInput(attrs = attrs))
    def save(self):
        for i in range(len(self.allSlots)):
            if self.cleaned_data["slot{0}".format(i)] == True:
                if self.allSlots[i].status == 'Available':
                    self.allSlots[i].status = 'Blocked'
                    self.allSlots[i].save()
                else:
                    # TODO: error msg
                    pass
            elif self.allSlots[i].status == 'Blocked':
                self.allSlots[i].status = 'Available'
                self.allSlots[i].save()
