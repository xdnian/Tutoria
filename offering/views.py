from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import TimeForm
import pytz, datetime, sys
from .models import Timeslot

@login_required
def offerslot(request):
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=1)
    timeslots = Timeslot.objects.filter(tutor__id=request.user.id).order_by('-start')
    if len(timeslots)==0:
        for i in range(2):
            for j in range(24):
                this_date = start_date + datetime.timedelta(days=i)
                start = datetime.datetime(this_date.year, this_date.month, this_date.day, j, 0, 0, 0)
                if j == 23:
                    this_date = this_date + datetime.timedelta(days=1)
                    j = -1
                end = datetime.datetime(this_date.year, this_date.month, this_date.day, j+1, 0, 0, 0)
                add_slot = Timeslot(tutor=request.user, start=start, end=end, status='Available')
                add_slot.save()
    elif timeslots[0].start.date() != end_date:
        for j in range(24):
            this_date = end_date
            start = datetime.datetime(this_date.year, this_date.month, this_date.day, j, 0, 0, 0)
            if j == 23:
                this_date = this_date + datetime.timedelta(days=1)
                j = -1
            end = datetime.datetime(this_date.year, this_date.month, this_date.day, j+1, 0, 0, 0)
            add_slot = Timeslot(tutor=request.user, start=start, end=end, status='Available')
            add_slot.save()

    if request.method == 'POST':
        form = TimeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TimeForm(request.user)
    return render(request, 'offerslot.html', {'form': form})
