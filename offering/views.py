from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import TimeForm
import pytz, datetime, sys
from .models import Timeslot

PRIVATE_TUTOR_TIMESLOTS = [(str(i) + ':00') for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [[str(i) + ':00', str(i) + ':30'] for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [item for sublist in CONTRACTED_TUTOR_TIMESLOTS for item in sublist]

@login_required
def offerslot(request):
    start_date = datetime.date.today()
    # TODO: end_date why 13?
    end_date = start_date + datetime.timedelta(days=13)
    timeslots = Timeslot.objects.filter(tutor__id=request.user.id).order_by('-start')
    if len(timeslots)==0:
        for i in range(14):
            this_date = start_date + datetime.timedelta(days=i)
            addOneDaySlots(user=request.user, date=this_date)

    elif timeslots[0].start.date() != end_date:
        this_date = end_date
        addOneDaySlots(user=request.user, date=this_date)
    # TODO: else?
    
    if request.method == 'POST':
        form = TimeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('offerslot')
    else:
        form = TimeForm(request.user)
    timeslots = PRIVATE_TUTOR_TIMESLOTS if request.user.profile.identity == 'T' else CONTRACTED_TUTOR_TIMESLOTS
    return render(request, 'offerslot.html', {'form': form, 'timeslots': timeslots})

def addOneDaySlots(user, date):
    for j in range(8,22):
        start = datetime.datetime(date.year, date.month, date.day, j, 0, 0, 0)
        end = datetime.datetime(date.year, date.month, date.day, j+1, 0, 0, 0)

        # private tutor
        if user.profile.identity == 'T': 
            Timeslot(tutor=user, start=start, end=end, status='Available').save()
        # contracted tutor
        else: 
            mid = datetime.datetime(date.year, date.month, date.day, j, 30, 0, 0)
            Timeslot(tutor=user, start=start, end=mid, status='Available').save()
            Timeslot(tutor=user, start=mid, end=end, status='Available').save()
