from django.db import models
from django.contrib.auth.models import User
import pytz

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=30, blank = True)

    def addBalance(self, amount):
        self.balance = self.balance + amount
        self.save()

    def withdraw(self, amount):
        if (self.balance < amount):
            return False
        else:
            self.balance = self.balance - amount
            self.save()
            return True

    def checkBalance(self):
        return self.balance

    def __str__(self):
        return self.user.username + ' $' + str(self.balance) + ' ' + self.bank_account 

class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='from_wallet', null = True)
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='to_wallet', null = True)
    description = models.CharField(max_length=500, blank = True)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    time = models.DateTimeField()
    
    def __str__(self):

        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        timelocal = self.time.astimezone(timezonelocal)
        date = timelocal.strftime('%Y-%m-%d')
        time = timelocal.strftime('%H:%M')

        return self.from_wallet.user.username + ' ' + self.to_wallet.user.username + ' $' + str(self.amount) + ' ' + date + ' ' + time + ' ' + self.description
    