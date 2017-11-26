from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Timeslot
import pytz, datetime

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
        today = datetime.date.today()
        start_time = datetime.datetime(today.year, today.month, today.day, 0, 0, 0, 0)
        self.allSlots = Timeslot.objects.filter(tutor__id=Tutor.id, start__gte=start_time).order_by('start')
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
        warning = False
        for i in range(len(self.allSlots)):
            if self.cleaned_data["slot{0}".format(i)]:
                if self.allSlots[i].status == 'Available':
                    self.allSlots[i].status = 'Blocked'
                    self.allSlots[i].save()
                elif self.allSlots[i].status == 'Booked':
                    warning = True
            elif self.allSlots[i].status == 'Blocked':
                self.allSlots[i].status = 'Available'
                self.allSlots[i].save()
        if warning:
            return 'Some of the timeslots you want to black-out have been booked.'
        else:
            return ''

