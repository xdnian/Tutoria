from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ChangeBalanceForm
from .models import Wallet, Transaction, Coupon
import decimal, pytz, datetime

from django.http import HttpResponse

PRIVATE_TUTOR_TIMESLOTS = [(str(i) + ':00') for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [[str(i) + ':00', str(i) + ':30'] for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [item for sublist in CONTRACTED_TUTOR_TIMESLOTS for item in sublist]

@login_required
def wallet(request):
    userWallet = Wallet.objects.get(user = request.user)
    return render(request, 'wallet.html', {'balance': str(userWallet.balance).split('.'), 'bank_account': userWallet.bank_account})

def transactionHistory(request):
    userWallet = Wallet.objects.get(user = request.user)

    utcCurrentTime = timezone.now()
    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    minimumTime = timezone.localtime(utcCurrentTime - datetime.timedelta(days = 30), timezonelocal)
        
    allTransactions = Transaction.objects.filter( Q(from_wallet=userWallet, time__gte = minimumTime) | Q(to_wallet=userWallet, time__gte = minimumTime) ).order_by('-time')
    return render(request, 'transactionHistory.html', {'allTransactions': allTransactions})

def addBalanceRequest(request):
    if request.method == 'POST':
        form = ChangeBalanceForm(request.POST)
        if form.is_valid():
            form.save(request.user, 'add')
            return redirect('wallet')
    else:
        form = ChangeBalanceForm()
    return render(request, 'changeBalanceRequest.html', {'form': form, 'action': 'add'})

def withdrawBalanceRequest(request):
    if request.method == 'POST':
        form = ChangeBalanceForm(request.POST)
        if form.is_valid():

            if( form.save(request.user, 'withdraw') ):
                return redirect('wallet')
            else:
                return render(request, 'changeBalanceRequest.html', {'form': form, 'action': 'withdraw'})
    else:
        form = ChangeBalanceForm()
    return render(request, 'changeBalanceRequest.html', {'form': form, 'action': 'withdraw'})

def isValidCoupon(request, code):
    utcCurrentTime = timezone.now()
    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
    allCodes = Coupon.objects.filter(expire_date__gte=currentTime)
    print(code)
    for each in allCodes:
        if each.code == code:
            return HttpResponse('1')
    return HttpResponse('0')

