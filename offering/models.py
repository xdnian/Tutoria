from django.db import models
from django.contrib.auth.models import User
import pytz

TIMEZONELOCAL = pytz.timezone('Asia/Hong_Kong')

# Create your models here.
class Timeslot(models.Model):
    global TIMEZONELOCAL
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20, default='Available')
    # time = None
    
    def __init__(self, *args, **kwargs):
        super(Timeslot, self).__init__(*args, **kwargs)
        self.time = self.start.astimezone(TIMEZONELOCAL).strftime('%Y-%m-%d %H:%M')

    def __str__(self):
        startlocal = self.start.astimezone(TIMEZONELOCAL)
        endlocal = self.end.astimezone(TIMEZONELOCAL)
        date = startlocal.strftime('%Y-%m-%d')
        time = startlocal.strftime('%H:%M')  + ' ~ ' + endlocal.strftime('%H:%M')
        return self.tutor.username + ' ' + date + ' ' + time + ' price: $' + str(self.tutor.profile.price)
