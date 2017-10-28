from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Session
from offering.models import Timeslot


class TutorForm(forms.Form):
    allTutors = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.RadioSelect, empty_label=None)
    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        self.fields['allTutors'].queryset = User.objects.filter(profile__identity='T')


class BookingForm(forms.Form):
    slots = forms.ModelChoiceField(queryset=Timeslot.objects.all(), widget=forms.RadioSelect, empty_label=None)
    def __init__(self, TutorID, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['slots'].queryset = Timeslot.objects.filter(tutor__id=TutorID)
    def save(self, Student):
        timeslot = self.cleaned_data['slots']
        session = Session(student=Student, tutor=timeslot.tutor, start=timeslot.start, end=timeslot.end, price=timeslot.price)
        session.save()
        Student.profile.wallet = Student.profile.wallet - timeslot.price
        Student.save()
        timeslot.delete()


class CancelingForm(forms.Form):
    sessions = forms.ModelMultipleChoiceField(queryset=Session.objects.none(), widget=forms.CheckboxSelectMultiple)
    def __init__(self, Student, *args, **kwargs):
        super(CancelingForm, self).__init__(*args, **kwargs)
        self.fields['sessions'].queryset = Session.objects.filter(student__id=Student.id)
    def save(self):
        for session in self.cleaned_data['sessions']:
            timeslot = Timeslot(tutor=session.tutor, start=session.start, end=session.end, price=session.price)
            timeslot.save()
            session.student.profile.wallet = session.student.profile.wallet + timeslot.price
            session.student.save()
            session.delete()