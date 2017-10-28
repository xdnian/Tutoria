from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import TimeForm

@login_required
def offerslot(request):
    if request.method == 'POST':
        form = TimeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TimeForm(request.user)
    return render(request, 'offerslot.html', {'form': form})
