from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Session
from offering.models import Timeslot
from django.utils import timezone
import decimal, pytz, datetime


class TutorForm(forms.Form):
    SCHOOL_CHOICES = (('0', 'All Universities'), ('1', 'University of Hong Kong'),('2', 'Hong Kong University of Science and Technology'),
        ('3', 'Chinese University of Hong Kong'), ('4', 'City University of Hong Kong'), 
        ('5', 'The Hong Kong Polytechnic University'), ('6', 'Hong Kong Baptist University'))
    univserity = forms.ChoiceField(label=("Univserity"), required=False, choices=SCHOOL_CHOICES, widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    course = forms.CharField(label=("Course"), required=False, max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course code..'}))
    name = forms.CharField(label=("Name"), required=False, max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tutor name..'}))
    subject = forms.CharField(label=("Subject"), required=False, max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject tags, separate by ";"..'}))
    TUTORTYPE_CHOICES = (('A', 'All'),('P', 'Private Tutor'),('C', 'Contracted Tutor'))
    tutortype = forms.ChoiceField(label=("Tutortype"), required=False, choices=TUTORTYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    price_min = forms.DecimalField(label=("Price_min"), required=False, max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Minimum rate'}))
    price_max = forms.DecimalField(label=("Price_max"), required=False, max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maximum rate'}))
    available_only = forms.BooleanField(label=("Available_only"), required=False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

class BookingForm(forms.Form):
    # slots = forms.ModelChoiceField(queryset=Timeslot.objects.all(), widget=forms.RadioSelect, empty_label=None)
    fields = {}
    def __init__(self, TutorID, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

        self.allSlots = Timeslot.objects.filter(tutor__id=TutorID).order_by('start')
        for i in range(len(self.allSlots)):
            startlocal = self.allSlots[i].start.astimezone(TIMEZONELOCAL)
            endlocal = self.allSlots[i].end.astimezone(TIMEZONELOCAL)
            date = startlocal.strftime('%Y-%m-%d')
            startTime = startlocal.strftime('%H:%M')
            endTime = endlocal.strftime('%H:%M')
            status = self.allSlots[i].status
            if status == 'Available':
                self.fields["slot{0}".format(i)] = forms.BooleanField(required=False, 
                    widget=forms.CheckboxInput(attrs={'status': status, 'date':date, 'startTime':startTime, 'endTime':endTime}))
            else:
                self.fields["slot{0}".format(i)] = forms.BooleanField(required=False, 
                    widget=forms.CheckboxInput(attrs={'disabled': '' ,'status': status, 'date':date, 'startTime':startTime, 'endTime':endTime}))

        # utcCurrentTime = timezone.now()
        # timezonelocal = pytz.timezone('Asia/Hong_Kong')
        # currentTime = timezone.localtime(utcCurrentTime, timezonelocal)

        # endTime = currentTime + datetime.timedelta(days=7)
        # if currentTime.minute < 30:
        #     mintime = datetime.datetime(currentTime.year, currentTime.month, currentTime.day+1, currentTime.hour, 30, 0, 0)
        # else:
        #     mintime = datetime.datetime(currentTime.year, currentTime.month, currentTime.day+1, currentTime.hour+1, 0, 0, 0)
        # maxtime = datetime.datetime(endTime.year, endTime.month, endTime.day, 22, 0, 0, 0)
        # self.fields['slots'].queryset = Timeslot.objects.filter(tutor__id=TutorID, status='Available', start__lte=maxtime, start__gte=mintime)
    def save(self, Student):

        for i in range(len(self.allSlots)):
            if self.cleaned_data["slot{0}".format(i)] == True:
                timeslot = self.allSlots[i]
                timeslot.status = 'Booked'
                timeslot.save()
                session = Session(student=Student, timeslot=timeslot, status='Pending')
                session.save()
                return session.id

        # timeslot = self.cleaned_data['slots']
        # timeslot.status = 'Booked'
        # timeslot.save()
        # session = Session(student=Student, tutor=timeslot.tutor, start=timeslot.start, end=timeslot.end, status='Pending')
        # session.save()
        # return session.id
        # 

class ReviewForm(forms.Form):
    SCORE_CHOICE = ((0, '-----'),(1, '*----'),(2, '**---'),(3, '***--'),(4, '****-'),(5, '*****'))

    score = forms.ChoiceField(label=("Score"), required=True, choices=SCORE_CHOICE, widget=forms.Select(attrs={'class': 'form-control custom-select'}))
    comment = forms.CharField(label=("Comment"), required=False, max_length=1000, widget=forms.Textarea(attrs={'rows':3, 'class': 'form-control', 'placeholder': 'Comment ..'}))
    isAnonymous = forms.BooleanField(label=("IsAnonymous"), required=True, widget=forms.CheckboxInput(attrs={'class': 'form-control-input'}))
