from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import BookingForm, TutorForm, CancelingForm
from .models import Session
from offering.models import Timeslot
import decimal

@login_required
def search(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            univserity = form.cleaned_data.get('univserity')
            course = form.cleaned_data.get('course')
            name = form.cleaned_data.get('name')
            subject = form.cleaned_data.get('subject')
            identity = form.cleaned_data.get('identity')
            available_only = form.cleaned_data.get('available_only')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            '''start query'''
            allTutors = User.objects.filter(Q(profile__identity='T') | Q(profile__identity='C'))

            if identity == 'T':
                allTutors = allTutors.filter(profile__identity='T')
            elif identity == 'C':
                allTutors = allTutors.filter(profile__identity='C')

            if univserity != '0':
                allTutors = allTutors.filter(profile__school=univserity)
            if course != '':
                for tutor in allTutors:
                    tutor.profile.courses = tutor.profile.courses.split(';')
                    if course not in tutor.profile.courses:
                        allTutors = allTutors.exclude(id=tutor.id)
            if subject != '':
                for tutor in allTutors:
                    tutor.profile.subjects = tutor.profile.subjects.split(';')
                    if subject not in tutor.profile.subjects:
                        allTutors = allTutors.exclude(id=tutor.id)
            if name != '':
                name = name.split(' ')
                if len(name) == 1:
                    allTutors = allTutors.filter(Q(first_name=name[0]) | Q(last_name=name[0]))
                else:
                    allTutors = allTutors.filter((Q(first_name=name[0])&Q(last_name=name[1]))
                     | (Q(first_name=name[1])&Q(last_name=name[0])))
            if price_min != None:
                price_min = decimal.Decimal(price_min)
                allTutors = allTutors.filter(profile__price__gte=price_min)
            if price_max != None:
                price_max = decimal.Decimal(price_max)
                allTutors = allTutors.filter(profile__price__lte=price_max)
            if available_only == True:
                for tutor in allTutors:
                    available_timeslot = Timeslot.objects.filter(tutor__id=tutor.id, status='Available')
                    if len(available_timeslot) == 0:
                        allTutors = allTutors.exclude(id=tutor.id)
            for tutor in allTutors:
                    tutor.profile.subjects = tutor.profile.subjects.split(';')
            for tutor in allTutors:
                    tutor.profile.courses = tutor.profile.courses.split(';')
            return render(request, 'search.html', {'form': form, 'allTutors': allTutors})
    else:
        form = TutorForm()
    return render(request, 'search.html', {'form': form})

    # allTutors = User.objects.filter(Q(profile__identity='T') | Q(profile__identity='C'))
    # for tutor in allTutors:
    #     tutor.profile.subjects = tutor.profile.subjects.split(';')
    # return render(request, 'catalogue.html', {'allTutors': allTutors})


def booking(request, pk):
    if request.method == 'POST':
        form = BookingForm(pk, request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('home')
    else:
        form = BookingForm(pk)
    return render(request, 'tutor-info.html', {'form': form})

def session(request):
    allSessions = Session.objects.filter(student__id=request.user.id)
    return render(request, 'records.html', {'allSessions': allSessions})

def canceling(request, pk):
    # if request.method == 'POST':
    #     form = CancelingForm(request.user, request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    # else:
    #     form = CancelingForm(request.user)
    # return render(request, 'canceling.html', {'form': form})
    session = Session.objects.filter(pk=pk)[0]
    timeslot = Timeslot.objects.filter(tutor=session.tutor, start=session.start, end=session.end, status='Booked')[0]
    timeslot.status = 'Available'
    timeslot.save()
    session.student.profile.wallet = session.student.profile.wallet + timeslot.tutor.profile.price*decimal.Decimal(1.05)
    session.student.save()
    session.delete()
    return redirect('session')


def schedule(request):
    sessions = Session.objects.filter(Q(tutor=request.user) | Q(student=request.user))
    return render(request, 'schedule.html', {'context': sessions})