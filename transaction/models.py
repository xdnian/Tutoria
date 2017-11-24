from django.db import models
from django.contrib.auth.models import User
import decimal, pytz, datetime
from django.utils import timezone

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet_owner')
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=30, blank = True)

    def addBalance(self, amount):
        self.balance = self.balance + amount
        self.save()

    def withdraw(self, amount):
        self.balance = self.balance - amount
        self.save()

    def checkBalance(self, amount):
        if (self.balance < amount):
            return False
        else:
            return True

    def __str__(self):
        return self.user.username + ' $' + str(self.balance)

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
        if self.from_wallet != None and self.to_wallet != None:
            return self.from_wallet.user.username + ' to ' + self.to_wallet.user.username + ' $' + str(self.amount) + ' ' + date + ' ' + time
        elif self.from_wallet == None:
            return 'bank account' + ' to ' + self.to_wallet.user.username + ' $' + str(self.amount) + ' ' + date + ' ' + time
        else:
            return self.from_wallet.user.username + ' to ' + 'bank account' + ' $' + str(self.amount) + ' ' + date + ' ' + time
    
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    expire_date = models.DateTimeField()

    def __str__(self):
        return self.code

    def isValid(self, code):
        utcCurrentTime = timezone.now()
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
        allCodes = Coupon.objects.filter(expire_date__gte=currentTime)
        for each in allCodes:
            if each.code == code:
                return True
        return False
