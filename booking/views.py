from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import BookingForm, TutorForm, CancelingForm
from .models import Session

@login_required
def viewAll(request):
    # if request.method == 'POST':
    #     form = TutorForm(request.POST)
    #     if form.is_valid():
    #         tutor = form.cleaned_data.get('allTutors')
    #         return redirect('booking', pk=tutor.id)
    # else:
    #     form = TutorForm()
    # return render(request, 'viewAll.html', {'form': form})
    allTutors = User.objects.filter(profile__identity='T')
    for tutor in allTutors:
        tutor.profile.subjects = tutor.profile.subjects.split(';')
    return render(request, 'test.html', {'allTutors': allTutors})


def booking(request, pk):
    if request.method == 'POST':
        form = BookingForm(pk, request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('home')
    else:
        form = BookingForm(pk)
    return render(request, 'booking.html', {'form': form})

def canceling(request):
    if request.method == 'POST':
        form = CancelingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CancelingForm(request.user)
    return render(request, 'canceling.html', {'form': form})


def schedule(request):
    sessions = Session.objects.filter(Q(tutor=request.user) | Q(student=request.user))
    return render(request, 'schedule.html', {'context': sessions})