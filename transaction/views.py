from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ChangeBalanceForm
from .models import Wallet, Transaction
import decimal
import pytz
import datetime

@login_required
def wallet(request):
    userWallet = Wallet.objects.get(user = request.user)
    return render(request, 'wallet.html', {'balance': userWallet.checkBalance(), 'bank_account': userWallet.bank_account})

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
