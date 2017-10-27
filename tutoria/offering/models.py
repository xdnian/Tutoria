from django.db import models
from django.contrib.auth.models import User
import pytz

# Create your models here.
class Timeslot(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    def __str__(self):
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        startlocal = self.start.astimezone(timezonelocal)
        endlocal = self.end.astimezone(timezonelocal)
        date = startlocal.strftime('%Y-%m-%d')
        time = startlocal.strftime('%H:%M')  + ' ~ ' + endlocal.strftime('%H:%M')
        return self.tutor.username + ' ' + date + ' ' + time + ' price: $' + str(self.price)
