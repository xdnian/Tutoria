from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Wallet, Transaction
from django.utils import timezone
import pytz
from home.models import Notification
class ChangeBalanceForm(forms.Form):
    amount = forms.DecimalField(label=("Amount"), max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    def save(self, user, action):

        if action == 'add':

            amount = self.cleaned_data.get('amount')
            userWallet = Wallet.objects.get(user = user)
            userWallet.addBalance(amount)

            utcCurrentTime = timezone.now()
            timezonelocal = pytz.timezone('Asia/Hong_Kong')
            currentTime = timezone.localtime(utcCurrentTime, timezonelocal)

            transaction = Transaction(to_wallet = userWallet, time = currentTime, amount = amount, description = 'Add balance from external source')
            transaction.save()
            Notification(user, 'Your have added HK$' + str(amount) + ' to your wallet.')
            return True

        elif action == 'withdraw':

            amount = self.cleaned_data.get('amount')
            userWallet = Wallet.objects.get(user = user)

            if userWallet.checkBalance(amount) == True:
                userWallet.withdraw(amount)
                utcCurrentTime = timezone.now()
                timezonelocal = pytz.timezone('Asia/Hong_Kong')
                currentTime = timezone.localtime(utcCurrentTime, timezonelocal)

                transaction = Transaction(from_wallet = userWallet, time = currentTime, amount = amount, description = 'Withdraw balance to external source')
                transaction.save()
                Notification(user, 'Your have withdrawn HK$' + str(amount) + ' from your wallet.')
                return True
            else:
                return False